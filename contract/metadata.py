from utils.hex_math import *


def isolate_metadata_cbor(bytecode:list):
    ipfs = get_ipfs_hash(bytecode)
    #remove ipfs hash from bytecode or error 
    if ipfs != "":
        bytecode = bytecode[:-(len(ipfs)//2)]
    cbor_2bytes = get_CBOR_bytes(bytecode)
    metadata = get_metadata_hash(bytecode)
    return metadata, cbor_2bytes, ipfs

def get_ipfs_hash(bytecode: list):
    #within the 50 last bytes of the bytecode, check if 697066733a2f is present
    #if yes, the ipfs hash are the bytes from 697066733a2f to the end of the bytecode
    #else there is no ipfs hash
    ipfs_hash = ""
    index = 0
    for byte in bytecode:
        if index >= len(bytecode) - 80:
            ipfs_hash += byte
        index += 1
    if "697066733a2f" in ipfs_hash:
        ipfs_hash = ipfs_hash[ipfs_hash.index("697066733a2f"):]
        print("IPFS hash: " + ipfs_hash)
        return ipfs_hash
    else:
        print("No IPFS hash")
        return ""

def get_CBOR_bytes(bytecode):
    return "".join(bytecode[-2:])

def get_CBOR_length(bytecode):
    hex_length = "".join(bytecode[-2:])
    int_length = hex_str_to_int(hex_length)
    print(f"CBOR length: {int_length} bytes")
    return int_length

        
def get_metadata_hash(bytecode: list):
    #https://playground.sourcify.dev/
    index = 0
    metadata_hash = ""
    cbor_length = get_CBOR_length(bytecode)
    #get last cbor_length bytes of bytecode
    for byte in bytecode:
        if index >= len(bytecode) - cbor_length - 2  and not index > len(bytecode) - 3:
            metadata_hash += byte
        index += 1
    return metadata_hash

def remove_metadata_from_bytecode(bytecode: list):
    cbor_length = get_CBOR_length(bytecode)
    bytecode = bytecode[:-cbor_length-2]
    return bytecode

def hex_to_utf8(hex_string):
    try:
        bytes_object = bytes.fromhex(hex_string)
        utf8_string = bytes_object.decode('utf-8', errors='replace')
        return utf8_string
    except ValueError:
        return "Invalid hex string"
        
def utf8_to_hex(utf8_string):
    try:
        hex_string = utf8_string.encode('utf-8').hex()
        return hex_string
    except ValueError:
        return "Invalid utf8 string"

def get_last_INVALID_opcode(bytecode: list):
    index = len(bytecode) - 1
    last_fe_index = 0
    for byte in reversed(bytecode):
        if byte == "fe":
            last_fe_index = index
            print(f"Last fe PC: {int_to_hex_str(last_fe_index)}")
            break
        index -= 1
    return last_fe_index
