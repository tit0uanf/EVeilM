import secrets
from opcodes.opcodes import PUSH
from utils.hex_math import *


def set_obf_attr_to_true(opcode_list):
    """
    Set the 'obfuscated' attribute of each opcode object in the list to True.
    
    Parameters:
        opcode_list (list): A list of opcode objects.
    """

    for opcode in opcode_list:
        opcode.obfuscated = True



def gen_random_func_sig():
    """
    Generate a random function signature 8 bytes long in hexadecimal format.
        
    Returns:
        str: The generated random function signature in hexadecimal format.
    """
    return secrets.token_hex(4)

def gen_random_func_sig_lower_than(func_sig):
    """
    Generate a random function signature 8 bytes lower than func_sig signature long in hexadecimal format.
    
    Parameters:
        func_sig (str): The function signature to be lower than.
        
    Returns:
        str: The generated random function signature in hexadecimal format.
    """
    random_func_sig = gen_random_func_sig()
    while int(random_func_sig, 16) > int(func_sig, 16):
        random_func_sig = gen_random_func_sig()
    return random_func_sig



def get_opcode_list_byte_length(opcode_list: list):
    """
    Compute the number of bytes in opcode_list
    """
    byte_length = 0
    for opcode in opcode_list:
        if isinstance(opcode, PUSH):
            byte_length += opcode.byte_amount + 1
        else:
            byte_length += 1
    return byte_length

def is_opcode_list_obfuscated(opcode_list: list):
    """
    Check if sequence is already obfuscated
    """
    for opcode in opcode_list:
        if not opcode.obfuscated:
            return False
    return True