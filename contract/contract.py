import copy
from contract.metadata import isolate_metadata_cbor
from opcodes.opcode_dict import *
from opcodes.opcodes import *
from disassembler.disassembler import opcode_to_bytecode, bytecode_to_opcode
from utils.hex_math import *
from utils.print_colors import colors as c

class Contract:
    def __init__(self, filename, bytecode: list):
        """
        Initialize the Contract class.

        Parameters:
            filename (str): The name of the file containing the contract's bytecode.
            bytecode (list): The EVM bytecode of the contract.
        """
        self.name = filename.split("/")[-1].split(".evm")[0]  # Extract contract name from filename
        self.creation_bytecode, self.bytecode = isolate_creation_runtime_bytecode(bytecode)  # Separate creation and runtime bytecode
        self.metadata, self.cbor_2bytes, self.ipfs = isolate_metadata_cbor(self.bytecode)  # Isolate metadata, CBOR data, and unknown data
        self.opcode = bytecode_to_opcode(self.bytecode)  # Convert runtime bytecode to opcode list
        self.creation_opcode = bytecode_to_opcode(self.creation_bytecode)  # Convert creation bytecode to opcode list
        self.creation_length = len("".join(self.creation_bytecode)) // 2  
        self.runtime_length = len(self.bytecode) // 2  
        self.creation_runtime_length = len(self.creation_bytecode + self.bytecode) // 2  # Calculate total bytecode length

        self.original_contract_length = copy.deepcopy(self.runtime_length)  # Store original contract length

        self.func_sig = {}  # Initialize function signatures dictionary

    # Getters and setters for bytecode and opcode
    @property
    def bytecode(self):
        return self._bytecode

    @bytecode.setter
    def bytecode(self, new_bytecode):
        self._bytecode = new_bytecode
        self._opcode = bytecode_to_opcode(new_bytecode)
        self.runtime_length = len(new_bytecode) // 2
        self.creation_runtime_length = len(self.creation_bytecode + new_bytecode) // 2

    @property
    def opcode(self):
        return self._opcode

    @opcode.setter
    def opcode(self, new_opcode_list):
        self._opcode = new_opcode_list
        new_bytecode = opcode_to_bytecode(new_opcode_list)
        self._bytecode = new_bytecode
        self.runtime_length = len(new_bytecode) // 2
        self.creation_runtime_length = len("".join(self.creation_bytecode) + new_bytecode) // 2

    @property
    def creation_opcode(self):
        return self._creation_opcode

    @creation_opcode.setter
    def creation_opcode(self, new_creation_opcode):
        self._creation_opcode = new_creation_opcode
        new_creation_bytecode = opcode_to_bytecode(new_creation_opcode)
        self.creation_bytecode = new_creation_bytecode
        self.creation_length = len(new_creation_bytecode) // 2
        self.creation_runtime_length = len(new_creation_bytecode + self.bytecode) // 2

    def __str__(self) -> str:
        pc_opcode = pc_opcode_dict(self.opcode)
        opcode_full_print = ""
        
        for pc, opcode in pc_opcode.items():
            if opcode.pc != hex(pc)[2:]:
                print(f"Error at {pc} : {opcode.pc} != {hex(pc)[2:]} A pc update is required somewhere")
            
            opcode_infos = f"({opcode.pc}) {opcode.opcode[2:]} {opcode.name} {c.rst}\n"
            if((isinstance(opcode, (JUMPDEST, JUMPI, PUSH)) and opcode.random)):
                opcode_full_print += f"{c.Yellow}{opcode_infos}"
            elif(isinstance(opcode, PUSH) and opcode.updated):
                opcode_full_print += f"{c.Blue}{opcode_infos}"
            elif(isinstance(opcode, JUMPDEST) and opcode.linked):
                opcode_full_print += f"{c.Cyan}{opcode_infos}"
            elif(opcode.obfuscated):
                opcode_full_print += f"{c.Green}{opcode_infos}"
            else:
                opcode_full_print += f"{opcode_infos}"
                
        return opcode_full_print

    def get_jumpdests(self, random_jumpdest=False):
        """
        Retrieve all JUMPDEST opcodes in the contract.
        """
        pc_opcode = pc_opcode_dict(self.opcode)
        jumpdest_list = []
        for opcode in pc_opcode.values():
            if isinstance(opcode, JUMPDEST):
                if not random_jumpdest and not opcode.linked:
                    jumpdest_list.append(opcode)
                elif random_jumpdest and opcode.random:
                    jumpdest_list.append(opcode)

        return jumpdest_list

    def link_jumpdest_push(self):
        """
        Link JUMP and JUMPI opcodes in the contract to their corresponding JUMPDESTs.
        """
        print("Linking JUMPDESTs to PUSHs")

        jumpdest_list = self.get_jumpdests()
        pc_opcode = pc_opcode_dict(self.opcode)
        for i in range(len(pc_opcode)):
            jump_opcode = list(pc_opcode.items())[i][1]
            push_opcode = list(pc_opcode.items())[i - 1][1]

            if isinstance(jump_opcode, (JUMP, JUMPI)) and isinstance(push_opcode, PUSH):
                jumpdest_pc = push_opcode.value
                jumpdest_opcode = pc_opcode.get(hex_str_to_int(jumpdest_pc))

                if jumpdest_opcode is not None and isinstance(jumpdest_opcode, JUMPDEST):
                    push_opcode.jumpdest = jumpdest_opcode

            elif not isinstance(jump_opcode, (JUMP, JUMPI)) and isinstance(push_opcode, PUSH):
                for jumpdest in jumpdest_list:
                    if hex_str_to_int(jumpdest.pc) == hex_str_to_int(push_opcode.value):
                        push_opcode.jumpdest = jumpdest

    def update_pc(self):
        """
        Update the program counter (PC) for each opcode in the contract's opcode list.
        """
        pc_opcode = pc_opcode_dict(self.opcode)
        for pc, opcode in pc_opcode.items():
            opcode.pc = hex(pc)[2:]
        self.opcode = self.opcode

    def get_full_bytecode(self):
        """
        Return the full bytecode of the contract, concatenate creation and runtime bytecode.
        """
        full_bytecode = self.creation_bytecode + self.bytecode
        return full_bytecode
    
    def get_pc(self, unknown_opcode: OPCODE):
        """
        Conpute PC of unknown_opcode present in contract
        """
        pc_opcode = pc_opcode_dict(self.opcode)
        pc_b10 = 0
        for pc, opcode in pc_opcode.items():
            if opcode is unknown_opcode:
                return pc_b10
            pc_b10 += 1
 
def pc_opcode_dict(opcode_list):
    """
    Create a dictionnary of OPCODE objects with their corrresponding PC as their key

    Parameters: opcode_list (list): Opcode list
    """
    pc = int("0", base=16)
    pc_bytecode_dict = {}
    iter_opcode = iter(opcode_list)
    for opcode in iter_opcode:
        if isinstance(opcode, PUSH):
            pc_bytecode_dict[pc] = opcode
            pc += opcode.byte_amount + 1
        else:
            pc_bytecode_dict[pc] = opcode
            pc += 1

    return pc_bytecode_dict


def isolate_creation_runtime_bytecode(bytecode: str):
    """
    Isolate the creation and runtime bytecode from a given full bytecode sequence.
    
    Parameters:
        bytecode (str): The full bytecode sequence as a hexadecimal string.
    """
    index = 0
    runtime_bytecode = bytecode
    creation_bytecode = []
    for byte in bytecode:
        if ((byte == "f3" or byte == "fe") and (bytecode[index+1] == "00" or bytecode[index+1] == "fe")):
            runtime_bytecode = bytecode[index+2:]   #+2 to include/exclude 0xf3 & 0xfe
            creation_bytecode = bytecode[:index+2]
            return creation_bytecode, runtime_bytecode
        elif (byte == "fe" and (bytecode[index+1] == "60" and bytecode[index+2] == "80")): #for Seaport
            print("End of Creation code ending with 'fe' only")
            runtime_bytecode = bytecode[index+1:]   #+2 to include/exclude 0xf3 & 0xfe
            creation_bytecode = bytecode[:index+1]
            return creation_bytecode, runtime_bytecode
        index += 1
    throw = Exception("No end of creation code found")
    

