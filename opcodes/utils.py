import secrets
from utils.hex_math import add_0_to_hex, hex_add_int


def compute_adjusted_push(push_to_adjust, nb_bytes_to_add):
    """
    Compute the adjusted value of a PUSH opcode after adding nb_bytes_to_add of bytes.
    
    Parameters:
        push_to_adjust (Opcode): The PUSH opcode object to be adjusted.
        bytes_to_add (int): The number of bytes to add.
        
    Returns:
        str: The new hexadecimal value of the PUSH opcode.
    """
    new_push_value =  add_0_to_hex(hex_add_int(push_to_adjust.value, nb_bytes_to_add)[2:])
    return new_push_value

def gen_push_value_lower_than(push_value):
    """
    Generate a random push value lower than push_value in hexadecimal format.
    
    Parameters:
        push_value (str): The push value to be lower than.
        
    Returns:
        str: The generated random push value in hexadecimal format.
    """
    random_push_value = secrets.token_hex(len(push_value)//2)
    while int(random_push_value, 16) > int(push_value, 16):
        random_push_value = secrets.token_hex(len(push_value)//2)
    return random_push_value

def eq_hex_(hex_string_1: str, hex_string_2: str) -> bool:
    hex_string_1 = rem_lead_0s(hex_string_1)
    hex_string_2 = rem_lead_0s(hex_string_2)
    if len(hex_string_1 ) != len(hex_string_2):
        raise Exception(f"Hex strings are not the same length : {hex_string_1} and {hex_string_2}")
    for i in range(len(hex_string_1)):
        if hex_string_1[i] != hex_string_2[i]:
            return False
    return True


def rem_lead_0s(hex_string: str) -> str:
    if len(hex_string) == 0:
        return hex_string
    else:
        if hex_string[0] == "0":
            return rem_lead_0s(hex_string[1:])
        else:
            return hex_string