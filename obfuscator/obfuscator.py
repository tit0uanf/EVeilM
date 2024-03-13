from copy import deepcopy
import random
import secrets
from opcodes.opcodes import *
from contract.contract import Contract
from utils.eth_sig import *
from utils.utils import object_list_to_type_list
from obfuscator.utils import *
from obfuscator.patterns import PATTERNS
from utils.print_colors import colors as c

NB_JUMPDEST_SPAM = 18 #must be even number
JUMPDEST_CFG_SPAM = 10 #must be even number < NB_JUMPDEST_SPAM


class Obfuscator:
    def __init__(self, contract : Contract, obf_type: str):
        """
        Constructor for the Obfuscator class.
        
        Parameters:
            contract (Contract): An instance of the Contract class representing the Ethereum smart contract to be obfuscated.
        """
        self.contract = contract
        self.obf_type = obf_type #["full", "addmanip", "funcsigtransfo", "spamjumpdest", "jumptransfo"]


    def obfuscate_contract(self):
        """
        Perform the obfuscation process on the contract.
        """

        if NB_JUMPDEST_SPAM % 2 != 0:
            raise Exception("NB_JUMPDEST_SPAM must be even number")
        if JUMPDEST_CFG_SPAM > NB_JUMPDEST_SPAM: #Spam jumpdest before match_patterns because match_patterns deals with length offset
            raise Exception("JUMPDEST_CFG_SPAM must be smaller than NB_JUMPDEST_SPAM")
        
        if(self.obf_type in ("full","spamjumpdest", "jumptransfo")):
            self.spam_jumpdest(NB_JUMPDEST_SPAM)
        if(self.obf_type in ("full", "jumptransfo")):
            self.cfg_spammer(JUMPDEST_CFG_SPAM)
        self.contract.update_pc()

        self.match_patterns()
        self.contract.update_pc()
        return self.contract
    
    
    def match_patterns(self):
        """
        Identify and replace opcode patterns in both the creation and runtime bytecode of the contract with corresponding obfuscated patterns.
        """
        creation_opcode_type_list = object_list_to_type_list(self.contract.creation_opcode)
        runtime_type_list = object_list_to_type_list(self.contract.opcode)
        opcode_type_list = creation_opcode_type_list + runtime_type_list

        for pattern in PATTERNS:
            print(f"\n{c.BackgroundLightYellow}Searching for {pattern.name} in the bytecode{c.rst}")
            if set(pattern.original) <= set(opcode_type_list):
                if pattern.replaceable:
                    if pattern.pattern_type == "runtime":
                        self.obfuscate_runtime_pattern(
                            pattern.original,
                            pattern.obfuscated,
                            pattern.name
                        )
                    elif pattern.pattern_type == "creation":
                        self.obfuscate_creation_pattern(
                            creation_opcode_type_list,
                            pattern.original,
                            pattern.name
                        )
                else:
                    print(f"\"{pattern.name}\" is not replaceable\n")



    def obfuscate_runtime_pattern(self, pattern, instanciated_pattern, name):
        """
        Obfuscate a specific runtime pattern in the contract's opcode list.
        
        Parameters:
            pattern (list): The opcode pattern list to be obfuscated.
            instanciated_pattern (list): The obfuscated pattern that will replace the original pattern.
            opcode_type_list (list): A list of opcode types in the contract.
            name (str): The name of the pattern for documentation purposes.
            added_bytes (int): The number of additional bytes added during the obfuscation.
        """
        for i in range(len(self.contract.opcode)):
            if object_list_to_type_list(self.contract.opcode[i:i+len(pattern)]) == pattern:

                if name == "FUNC_SELECTOR" and self.obf_type in ("full","funcsigtransfo"):
                    print(f"\nApplying {c.Bold}Function Signature Transformer{c.rst}...")
                    added_bytes = self.func_sig_transformer(i, self.contract.opcode[i:i+len(pattern)])
                    i += added_bytes 
                    self.contract.update_pc() #need to update pc after each addings of bytecodes

                elif name == "JUMPTRANSFO" and not is_opcode_list_obfuscated(self.contract.opcode[i:i+len(pattern)]) and self.obf_type in ("full","jumptransfo"):
                    print(f"Applying {c.Bold}Jump Address Transformer{c.rst}...")
                    added_bytes = self.jump_address_transformer(i, self.contract.opcode[i:i+len(pattern)])
                    i += added_bytes
                    self.contract.update_pc() #need to update pc after each addings of bytecodes
                
                elif name == "PUSH32" and self.contract.opcode[i:i+len(pattern)][0].byte_amount == 32 and not is_opcode_list_obfuscated(self.contract.opcode[i:i+len(pattern)]) and self.obf_type in ("full","push32"):
                    print(f"Applying {c.Bold}PUSH32 Splitter{c.rst}...")
                    added_bytes = self.push32_splitter(i, self.contract.opcode[i:i+len(pattern)])
                    i += added_bytes
                    self.contract.update_pc() 
                #TODO: bug at ADD obfuscation
                elif name == "ADD" and not is_opcode_list_obfuscated(self.contract.opcode[i:i+len(pattern)]) and self.obf_type in ("full","add") and random.randint(1,3) == 1:                    
                    print(f"Applying ADD Opcode Stack Manipulation...")
                    set_obf_attr_to_true(instanciated_pattern)
                    original_bytes = get_opcode_list_byte_length(self.contract.opcode[i:i+len(pattern)])
                    self.contract.opcode[i:i+len(pattern)] = deepcopy(instanciated_pattern) #deepcopy to create new object and not just reference to have correct pc for each opcode
                    added_bytes = get_opcode_list_byte_length(self.contract.opcode[i:i+len(instanciated_pattern)]) - original_bytes
                    i += added_bytes
                    self.contract.update_pc() #need to update pc after each addings of bytecodes
                
                else:
                    i += 1
            else:
                i += 1

#TODO: identify end of function selector to insert random jumpdest starting from there
    def spam_jumpdest(self, nb_new_jumpdest: int):
        """
        Insert a specified number of random JUMPDEST opcodes into the contract's opcode sequence.
        
        Parameters:
            nb_new_jumpdest (int): The number of random JUMPDEST opcodes to be inserted.
        """
        print(f"\nSpamming {nb_new_jumpdest} new JUMPDEST...")

        current_opcode = self.contract.opcode
        for _ in range(nb_new_jumpdest):
            rd_pc = random.randint(500,len(current_opcode)-200) #-200 to avoid inserting JUMPDEST in metadata
            rd_jumpdest = JUMPDEST(random=True)
            self.contract.opcode[rd_pc:rd_pc] = [rd_jumpdest]
            self.contract.update_pc()
        print(f"Added {nb_new_jumpdest} random JUMPDEST")


    def cfg_spammer(self, nb_jumpdest_to_spam: int):
        """
        Insert control flow obfuscating sequences at random JUMPDEST positions in the contract's opcode list.
        
        Parameters:
            nb_jumpdest_to_spam (int): The number of random JUMPDEST opcodes to target for control flow obfuscation.
        """
        print(f"Applying {c.Bold}Control Flow Graph Spammer{c.rst} on {nb_jumpdest_to_spam} random JUMPDEST...")
        jumpdest_list =  self.contract.get_jumpdests(random_jumpdest=True)
        jumpdests_to_spam : list = random.sample(jumpdest_list, nb_jumpdest_to_spam) #shuffle list to avoid spamming same jumpdest
        
        while len(jumpdests_to_spam) > 0:
            dummy_value_1 = secrets.token_hex(1)
            dummy_value_2 = secrets.token_hex(1)
            dummy_push_top_1 = PUSH(1,dummy_value_1, True) #dummy value needed to avoid stack underflow with JUMPI
            dummy_push_top_2 = PUSH(1,dummy_value_2, True)

            linked_push_top = PUSH(1,"ff", True) #push value that will be linked to jumpdest and get its value updated
            jumpi_top = JUMPI(random=True)
            jumpdest_top = random.choice(jumpdests_to_spam)
            jumpdest_pc_top = self.contract.get_pc(jumpdest_top)
            jumpdests_to_spam.remove(jumpdest_top)              

            obf_sequence_top = [dummy_push_top_1,dummy_push_top_2,linked_push_top,jumpi_top]
            self.contract.opcode[jumpdest_pc_top:jumpdest_pc_top] = obf_sequence_top
            self.contract.update_pc() #need to update pc after each addings of bytecodes

            jumpdest_bot = random.choice(jumpdests_to_spam) #pick random jumpdest     
            jumpdests_to_spam.remove(jumpdest_bot) #remove random jumpdest to avoid spamming same jumpdest      
            linked_push_top.jumpdest = jumpdest_bot
            push_00 = PUSH(1,"00", random=True) #00 value to cancel jumpi
            push_pc_bot = PUSH(1,"ff", random=True) #push value that will be linked to jumpdest and get its value updated
            push_pc_bot.jumpdest = jumpdest_top
            jumpi_bot = JUMPI(random=True)

            jumpdest_pc_bot = self.contract.get_pc(jumpdest_bot) #get pc of jumpdest to insert at the right place
            self.contract.opcode[jumpdest_pc_bot:jumpdest_pc_bot] = [push_00] #insert fake_push_00 before jumpdest to cancel jumpi
            obf_sequence_bot = [push_pc_bot,jumpi_bot]
            self.contract.opcode[jumpdest_pc_bot+2:jumpdest_pc_bot+2] = obf_sequence_bot #insert after jumpdest
            self.contract.update_pc()


    def func_sig_transformer(self, i_contract: int, contract_func: list):
        """
        Transform Ethereum function selectors in the contract's opcode list by altering their corresponding PUSH opcodes.
        
        Parameters:
            i_contract (int): The starting index in the contract's opcode list where the function sequence begins.
            contract_func (list): A list of opcode objects representing a specific Ethereum function within the contract.
        """
        original_bytes = get_opcode_list_byte_length(contract_func)
        added_bytes = 0
        for i in range(len(contract_func)):
            if isinstance(contract_func[i], PUSH) and contract_func[i].byte_amount == 4:
                func_sig = contract_func[i].value
                self.contract.func_sig[func_sig] = get_function_name(contract_func[i].value)
                rd_func_sig = gen_random_func_sig_lower_than(func_sig)
                transformed_func_sig = compute_adjusted_push(contract_func[i],-int(rd_func_sig,16))
                contract_func[i].value = transformed_func_sig
                contract_func.insert(i+1, PUSH(4,rd_func_sig, random=True))
                contract_func.insert(i+2, ADD())
                set_obf_attr_to_true(contract_func)
                self.contract.opcode[i_contract:i_contract+5] = contract_func
                self.contract.opcode = self.contract.opcode
                added_bytes = get_opcode_list_byte_length(contract_func) - original_bytes
                return added_bytes
        return added_bytes
                
    def jump_address_transformer(self, i_contract: int, push_jump_sequence: list):
        original_bytes = get_opcode_list_byte_length(push_jump_sequence)
        if isinstance(push_jump_sequence[0], PUSH) and isinstance(push_jump_sequence[1], JUMPI):
            original_push = push_jump_sequence[0]
            rd_push_value = gen_push_value_lower_than(original_push.value)
            new_push = PUSH(len(original_push.value)//2 ,rd_push_value, random=True)

            original_push.linked_lower = new_push
            push_jump_sequence.insert(0, new_push)
            push_jump_sequence.insert(2, ADD())
            set_obf_attr_to_true(push_jump_sequence)
            
            original_push.linked_lower = new_push

            self.contract.opcode[i_contract:i_contract+2] = push_jump_sequence
            self.contract.opcode = self.contract.opcode
            added_bytes = get_opcode_list_byte_length(push_jump_sequence) - original_bytes
            return added_bytes
        else:
            return 0

    def push32_splitter(self, i_contract: int, push_single_opcode: list):
        original_bytes = get_opcode_list_byte_length(push_single_opcode)
        if isinstance(push_single_opcode[0], PUSH) and push_single_opcode[0].byte_amount == 32 and not all(char in {'0', 'f'} for char in push_single_opcode[0].value):
            push32_value = push_single_opcode[0].value
            if len(push32_value) == 64:
                half_length = len(push32_value) // 2
                first_half = push32_value[:half_length]
                second_half = push32_value[half_length:]

                leading_0_half = '0' * 32 + first_half
                trailing_0_half = second_half + '0' * 32

                lead_push = PUSH(32 ,leading_0_half)
                trail_push = PUSH(32 ,trailing_0_half)

                push_single_opcode.pop(0)
                push_single_opcode.insert(0,lead_push)
                push_single_opcode.insert(1,trail_push)
                push_single_opcode.insert(2,ADD())
                set_obf_attr_to_true(push_single_opcode)

                self.contract.opcode[i_contract:i_contract+1] = push_single_opcode
                self.contract.opcode = self.contract.opcode
                added_bytes = get_opcode_list_byte_length(push_single_opcode) - original_bytes
                return added_bytes
            else:
                return 0
        else:
            return 0

    def insert_random_func(self, i_contract: int):
        """
        Insert a sequence of opcodes representing a random Ethereum function selector into the contract's opcode list.
        
        Parameters:
            i_contract (int): The starting index in the contract's opcode list where the random function sequence will be inserted.
        """
        rd_func_sig = gen_random_func_sig()
        instanciated_rd_function = [DUP(1),PUSH(4,rd_func_sig),EQ(),PUSH(1,"00"),JUMPI()]
        self.contract.opcode[i_contract:i_contract] =  instanciated_rd_function


    def obfuscate_creation_pattern(self, opcode_type_list: list, pattern: list, name: str):
        """
        Obfuscate patterns in the creation bytecode of the contract.
        
        Parameters:
            opcode_type_list (list): A list representing the types of opcodes in the contract's creation bytecode.
            pattern (list): A list representing the opcode pattern to search for.
            name (str): The name of the pattern being obfuscated.

        """
        obf_i = 0  # obf_i is necessary to iterate over obfuscated bytecode (with more bytes than original bytecode)
        for i in range(len(opcode_type_list)):
            if opcode_type_list[i:i+len(pattern)] == pattern:
                if "LENGTH_OFFSET" in name:
                    print(f"Adjusting Runtime's bytecode length offset...")
                    length_offset_pattern = self.contract.creation_opcode[obf_i:obf_i+len(pattern)]
                    self.contract_length_offset_adjuster(obf_i, length_offset_pattern)

                if "CONSTRUCTOR" in name:
                    print(f"Adjusting Contract's bytecode length offset...")
                    constructor_args_length = self.contract.creation_opcode[obf_i:obf_i+len(pattern)]
                    self.constructor_args_length_adjuster(obf_i, constructor_args_length)

            else:
                obf_i += 1


    def contract_length_offset_adjuster(self, contract_i: int, length_offset_pattern: list):
        """
        Adjust the offset related to the runtime bytecode length in the contract's creation bytecode.
        
        Parameters:
            contract_i (int): The index in the contract's creation opcode list where the length offset pattern begins.
            length_offset_pattern (list): A list of opcode objects representing the pattern in the creation bytecode that includes the length offset.
    
        """
        old_length_offset = length_offset_pattern[0].value
        print("Old contract length offset: %s" % old_length_offset)
        print(f"Old contract length: {self.contract.original_contract_length}")
        length_offset_pattern[0].contract = self.contract
        length_offset_pattern[0].runtime_offset = True
        print("New contract length offset: %s" % length_offset_pattern[0].value)
        print(f"New contract length: {self.contract.runtime_length}")

        length_offset_pattern[2].contract = self.contract
        length_offset_pattern[2].creation_offset = True

        new_creation_opcode = deepcopy(self.contract.creation_opcode) #need deepcopy to trigger property setter instaed of list[i:i+1]
        new_creation_opcode[contract_i:contract_i+7] = length_offset_pattern
        self.contract.creation_opcode = new_creation_opcode

    def constructor_args_length_adjuster(self, contract_i: int, constructor_offset_pattern: list):
        """
        Adjust the offset related to the creation+runtime bytecode length in the contract's creation bytecode.
        
        Parameters:
            contract_i (int): The index in the contract's creation opcode list where the length offset pattern begins.
            constructor_offset_pattern (list): A list of opcode objects representing the pattern in the creation bytecode that includes the length offset.
        """
        print(f"Old Constructor offset: {constructor_offset_pattern[2].value}")

        constructor_offset_pattern[2].contract = self.contract
        constructor_offset_pattern[2].creation_runtime_offset = True

        constructor_offset_pattern[6].contract = self.contract
        constructor_offset_pattern[6].creation_runtime_offset = True
 
        print(f"New Constructor offset: {constructor_offset_pattern[2].value}")
        print(f"New Creation bytecode length: {self.contract.creation_length}")
        print(f"New Runtime bytecode length: {self.contract.runtime_length}")
        print(f"New Creation+Runtime offset: {self.contract.creation_runtime_length}")

        new_creation_opcode = deepcopy(self.contract.creation_opcode) #need deepcopy to trigger property setter instaed of list[i:i+1]
        new_creation_opcode[contract_i:contract_i+9] = constructor_offset_pattern
        self.contract.creation_opcode = new_creation_opcode


            