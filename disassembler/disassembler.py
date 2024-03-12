
from opcodes.opcodes import PUSH, DUP, SWAP, LOG, INVALID
from opcodes.opcode_dict import opcodes_dict


def evmcode_string_to_list(bytecode):
    """
    Convert a given Ethereum Virtual Machine (EVM) bytecode string into a list of 2 characters bytecodes.
    """
    bytecode = bytecode.replace(' ', '')
    bytecode = bytecode.replace('0x', '')
    bytecode = bytecode.replace('\n', '')
    bytecode = bytecode.replace('\r', '')
    bytecode = bytecode.replace('\t', '')
    bytecode = bytecode.replace('\v', '')
    bytecode = bytecode.replace('\f', '')
    return [bytecode[i:i+2] for i in range(0, len(bytecode), 2)]


def bytecode_to_opcode(bytecode):
    """
    Convert a list of EVM bytecodes to a list of opcode objects.
    
    Parameters:
        bytecode (list): A list of EVM bytecodes ex. list("60","40","61","02","03").
        
    Returns:
        list: A list of opcode objects representing the EVM instructions.
      """
    opcodes_obj_list = list()
    i = 0
    while i < len(bytecode):
        opcode = bytecode[i]
        if opcodes_dict[opcode] == PUSH:
            byte_amount = int(bytecode[i], 16) - 0x60 + 1
            value = "".join(bytecode[i+1:i+byte_amount+1]) # merge the bytes next to PUSH instruction
            opcodes_obj_list.append(
                PUSH(byte_amount, value))  
            i += byte_amount

        elif opcodes_dict[opcode] == DUP:
            stack_position = int(bytecode[i], 16) - 0x80 + 1
            opcodes_obj_list.append(DUP(stack_position))  

        elif opcodes_dict[opcode] == SWAP:
            stack_position = int(bytecode[i], 16) - 0x90 + 1
            opcodes_obj_list.append(SWAP(stack_position))

        elif opcodes_dict[opcode] == LOG:
            log_number = int(bytecode[i], 16) - 0xa0
            opcodes_obj_list.append(LOG(log_number))

        elif opcodes_dict[opcode] == INVALID:
            opcodes_obj_list.append(opcodes_dict[opcode](opcode))

        else:
            opcodes_obj_list.append(opcodes_dict[opcode]())
        i += 1

    return opcodes_obj_list


# transform opcode list to bytecode string without "0x"
def opcode_to_bytecode(opcode_list):
    """
    Convert a list of opcode objects to a string of EVM bytecode.
    
    Parameters:
        opcode_list (list): A list of opcode objects representing the EVM instructions.
        
    Returns:
        str: A string representation of EVM bytecode.
        
    Note:
        This function handles various EVM instructions like PUSH and converts them into their corresponding bytecode.
    """
    bytecode = ""
    for opcode in opcode_list:
        if isinstance(opcode, PUSH):
            bytecode += opcode.opcode + opcode.value
        else:
            bytecode += opcode.opcode
    return bytecode
