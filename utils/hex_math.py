def int_to_hex_str(integer: int) -> str:
    hex_string = hex(integer)[2:]
    if len(hex_string) % 2 != 0:
        hex_string = "0"+hex_string
    return hex_string

def hex_str_to_int(hex_string: str) -> int:
    return int(hex_string, 16)


def add_0_to_hex(hex_string: str) -> str: #if string uneven, add a 0 at the beginning
    if len(hex_string) % 2 != 0:
        hex_string = "0"+hex_string
    return hex_string


def hex_add_int(hex_number, integer): #add hex number with integer
    return hex(int(hex_number,16) + integer)

    
def eq_hex_str(hex_string_1: str, hex_string_2: str) -> bool:
    if len(hex_string_1) != len(hex_string_2):
        eq_hex_str(rem_lead_0s(hex_string_1), rem_lead_0s(hex_string_2))
    else:
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