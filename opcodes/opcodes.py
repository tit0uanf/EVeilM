import secrets

from opcodes.utils import *
from utils.hex_math import int_to_hex_str




class OPCODE(type):
    name = "OPCODE"

    def __init__(cls, name, bases, attrs):
        cls.obfuscated = False

    def __iter__(cls):
        return iter(cls.name)


class STOP(metaclass=OPCODE):
    opcode = "00"
    name = "STOP"
    ins = 0
    outs = 0
    gas = 0
    pc = ""


class ADD(metaclass=OPCODE):
    opcode = "01"
    name = "ADD"
    ins = 2
    outs = 1
    gas = 3
    pc = ""


class MUL(metaclass=OPCODE):
    opcode = "02"
    name = "MUL"
    ins = 2
    outs = 1
    gas = 5
    pc = ""


class SUB(metaclass=OPCODE):
    opcode = "03"
    name = "SUB"
    ins = 2
    outs = 1
    gas = 3
    pc = ""


class DIV(metaclass=OPCODE):
    opcode = "04"
    name = "DIV"
    ins = 2
    outs = 1
    gas = 5
    pc = ""


class SDIV(metaclass=OPCODE):
    opcode = "05"
    name = "SDIV"
    ins = 2
    outs = 1
    gas = 5
    pc = ""


class MOD(metaclass=OPCODE):
    opcode = "06"
    name = "MOD"
    ins = 2
    outs = 1
    gas = 5


class SMOD(metaclass=OPCODE):
    opcode = "07"
    name = "SMOD"
    ins = 2
    outs = 1
    gas = 5
    pc = ""


class ADDMOD(metaclass=OPCODE):
    opcode = "08"
    name = "ADDMOD"
    ins = 3
    outs = 1
    gas = 8
    pc = ""


class MULMOD(metaclass=OPCODE):
    opcode = "09"
    name = "MULMOD"
    ins = 3
    outs = 1
    gas = 8
    pc = ""


class EXP(metaclass=OPCODE):
    opcode = "0a"
    name = "EXP"
    ins = 2
    outs = 1
    gas = 10
    pc = ""


class SIGNEXTEND(metaclass=OPCODE):
    opcode = "0b"
    name = "SIGNEXTEND"
    ins = 2
    outs = 1
    gas = 5
    pc = ""


class LT(metaclass=OPCODE):
    opcode = "10"
    name = "LT"
    ins = 2
    outs = 1
    gas = 3
    pc = ""


class GT(metaclass=OPCODE):
    opcode = "11"
    name = "GT"
    ins = 2
    outs = 1
    gas = 3
    pc = ""


class SLT(metaclass=OPCODE):
    opcode = "12"
    name = "SLT"
    ins = 2
    outs = 1
    gas = 3
    pc = ""


class SGT(metaclass=OPCODE):
    opcode = "13"
    name = "SGT"
    ins = 2
    outs = 1
    gas = 3
    pc = ""


class EQ(metaclass=OPCODE):
    opcode = "14"
    name = "EQ"
    ins = 2
    outs = 1
    gas = 3
    pc = ""


class ISZERO(metaclass=OPCODE):
    opcode = "15"
    name = "ISZERO"
    ins = 1
    outs = 1
    gas = 3
    pc = ""


class AND(metaclass=OPCODE):
    opcode = "16"
    name = "AND"
    ins = 2
    outs = 1
    gas = 3
    pc = ""


class OR(metaclass=OPCODE):
    opcode = "17"
    name = "OR"
    ins = 2
    outs = 1
    gas = 3
    pc = ""


class XOR(metaclass=OPCODE):
    opcode = "18"
    name = "XOR"
    ins = 2
    outs = 1
    gas = 3
    pc = ""


class NOT(metaclass=OPCODE):
    opcode = "19"
    name = "NOT"
    ins = 1
    outs = 1
    gas = 3
    pc = ""


class BYTE(metaclass=OPCODE):
    opcode = "1a"
    name = "BYTE"
    ins = 2
    outs = 1
    gas = 3
    pc = ""


class SHL(metaclass=OPCODE):
    opcode = "1b"
    name = "SHL"
    ins = 2
    outs = 1
    gas = 3
    pc = ""


class SHR(metaclass=OPCODE):
    opcode = "1c"
    name = "SHR"
    ins = 2
    outs = 1
    gas = 3
    pc = ""


class SAR(metaclass=OPCODE):
    opcode = "1d"
    name = "SAR"
    ins = 2
    outs = 1
    gas = 3
    pc = ""


class KECCAK256(metaclass=OPCODE):
    opcode = "20"
    name = "KECCAK256"
    ins = 2
    outs = 1
    gas = 30
    pc = ""


class SHA3(metaclass=OPCODE):
    opcode = "20"
    name = "SHA3"
    ins = 2
    outs = 1
    gas = 30
    pc = ""


class ADDRESS(metaclass=OPCODE):
    opcode = "30"
    name = "ADDRESS"
    ins = 0
    outs = 1
    gas = 2
    pc = ""


class BALANCE(metaclass=OPCODE):
    opcode = "31"
    name = "BALANCE"
    ins = 1
    outs = 1
    gas = 20
    pc = ""


class ORIGIN(metaclass=OPCODE):
    opcode = "32"
    name = "ORIGIN"
    ins = 0
    outs = 1
    gas = 2
    pc = ""


class CALLER(metaclass=OPCODE):
    opcode = "33"
    name = "CALLER"
    ins = 0
    outs = 1
    gas = 2
    pc = ""


class CALLVALUE(metaclass=OPCODE):
    opcode = "34"
    name = "CALLVALUE"
    ins = 0
    outs = 1
    gas = 2
    pc = ""


class CALLDATALOAD(metaclass=OPCODE):
    opcode = "35"
    name = "CALLDATALOAD"
    ins = 1
    outs = 1
    gas = 3
    pc = ""


class CALLDATASIZE(metaclass=OPCODE):
    opcode = "36"
    name = "CALLDATASIZE"
    ins = 0
    outs = 1
    gas = 2
    pc = ""


class CALLDATACOPY(metaclass=OPCODE):
    opcode = "37"
    name = "CALLDATACOPY"
    ins = 3
    outs = 0
    gas = 3
    pc = ""


class CODESIZE(metaclass=OPCODE):
    opcode = "38"
    name = "CODESIZE"
    ins = 0
    outs = 1
    gas = 2
    pc = ""


class CODECOPY(metaclass=OPCODE):
    opcode = "39"
    name = "CODECOPY"
    ins = 3
    outs = 0
    gas = 3
    pc = ""


class GASPRICE(metaclass=OPCODE):
    opcode = "3a"
    name = "GASPRICE"
    ins = 0
    outs = 1
    gas = 2
    pc = ""


class EXTCODESIZE(metaclass=OPCODE):
    opcode = "3b"
    name = "EXTCODESIZE"
    ins = 1
    outs = 1
    gas = 20
    pc = ""


class EXTCODECOPY(metaclass=OPCODE):
    opcode = "3c"
    name = "EXTCODECOPY"
    ins = 4
    outs = 0
    gas = 20
    pc = ""


class RETURNDATASIZE(metaclass=OPCODE):
    opcode = "3d"
    name = "RETURNDATASIZE"
    ins = 0
    outs = 1
    gas = 2
    pc = ""


class RETURNDATACOPY(metaclass=OPCODE):
    opcode = "3e"
    name = "RETURNDATACOPY"
    ins = 3
    outs = 0
    gas = 3
    pc = ""


class EXTCODEHASH(metaclass=OPCODE):
    opcode = "3f"
    name = "EXTCODEHASH"
    ins = 1
    outs = 1
    gas = 400
    pc = ""


class BLOCKHASH(metaclass=OPCODE):
    opcode = "40"
    name = "BLOCKHASH"
    ins = 1
    outs = 1
    gas = 20
    pc = ""


class COINBASE(metaclass=OPCODE):
    opcode = "41"
    name = "COINBASE"
    ins = 0
    outs = 1
    gas = 2
    pc = ""


class TIMESTAMP(metaclass=OPCODE):
    opcode = "42"
    name = "TIMESTAMP"
    ins = 0
    outs = 1
    gas = 2
    pc = ""


class NUMBER(metaclass=OPCODE):
    opcode = "43"
    name = "NUMBER"
    ins = 0
    outs = 1
    gas = 2
    pc = ""


class DIFFICULTY(metaclass=OPCODE):
    opcode = "44"
    name = "DIFFICULTY"
    ins = 0
    outs = 1
    gas = 2
    pc = ""


class GASLIMIT(metaclass=OPCODE):
    opcode = "45"
    name = "GASLIMIT"
    ins = 0
    outs = 1
    gas = 2
    pc = ""


class CHAINID(metaclass=OPCODE):
    opcode = "46"
    name = "CHAINID"
    ins = 0
    outs = 1
    gas = 2
    pc = ""


class SELFBALANCE(metaclass=OPCODE):
    opcode = "47"
    name = "SELFBALANCE"
    ins = 0
    outs = 1
    gas = 5
    pc = ""


class BASEFEE(metaclass=OPCODE):
    opcode = "48"
    name = "BASEFEE"
    ins = 0
    outs = 1
    gas = 2
    pc = ""


class POP(metaclass=OPCODE):
    opcode = "50"
    name = "POP"
    ins = 1
    outs = 0
    gas = 2
    pc = ""


class MLOAD(metaclass=OPCODE):
    opcode = "51"
    name = "MLOAD"
    ins = 1
    outs = 1
    gas = 3
    pc = ""


class MSTORE(metaclass=OPCODE):
    opcode = "52"
    name = "MSTORE"
    ins = 2
    outs = 0
    gas = 3
    pc = ""


class MSTORE8(metaclass=OPCODE):
    opcode = "53"
    name = "MSTORE8"
    ins = 2
    outs = 0
    gas = 3
    pc = ""


class SLOAD(metaclass=OPCODE):
    opcode = "54"
    name = "SLOAD"
    ins = 1
    outs = 1
    gas = 50
    pc = ""


class SSTORE(metaclass=OPCODE):
    opcode = "55"
    name = "SSTORE"
    ins = 2
    outs = 0
    gas = 0
    pc = ""


class JUMP(metaclass=OPCODE):
    def __init__(self, random=False):
        self.random = random
    opcode = "56"
    name = "JUMP"
    ins = 1
    outs = 0
    gas = 8
    pc = ""


class JUMPI(metaclass=OPCODE):
    def __init__(self, random=False):
        self.random = random
    opcode = "57"
    name = "JUMPI"
    ins = 2
    outs = 0
    gas = 10
    pc = ""


class PC(metaclass=OPCODE):
    opcode = "58"
    name = "PC"
    ins = 0
    outs = 1
    gas = 2
    pc = ""


class MSIZE(metaclass=OPCODE):
    opcode = "59"
    name = "MSIZE"
    ins = 0
    outs = 1
    gas = 2
    pc = ""


class GAS(metaclass=OPCODE):
    opcode = "5a"
    name = "GAS"
    ins = 0
    outs = 1
    gas = 2
    pc = ""


class JUMPDEST(metaclass=OPCODE):
    opcode = "5b"
    name = "JUMPDEST"
    ins = 0
    outs = 0
    gas = 1
    _pc = ""

    def __init__(self, random=False):
        self.linked = False
        self.random = random
        self.push_list = list()

    def __str__(self):
        return f"JUMPDEST linked={self.linked} random={self.random} pc={self.pc}"
    
    def link(self, push):
            self.linked = True
            self.push_list.append(push)
            return self._pc

    @property
    def pc(self):
        return self._pc

    @pc.setter
    def pc(self, value :str):
        self._pc = value
        for push in self.push_list:
            new_push_value = value
            if len(new_push_value) % 2 != 0:
                new_push_value = "0"+new_push_value
            push.value = new_push_value


class PUSH(metaclass=OPCODE):
    ins = 0
    outs = 1
    gas = 3
    byte_amount = None
    pc = ""

    # init PUSH obj, 1<byte_amount<32, value as a string ("6541")
    def __init__(self, byte_amount, value, random=False, linked_lower = None):
        self.linked_lower = linked_lower
        self.value = value
        self.updated = False
        self._jumpdest = None
        self.random = random
        
        self.contract = None
        self.creation_offset = False
        self.runtime_offset = False
        self.creation_runtime_offset = False


        if byte_amount > 32 or byte_amount < 1:
            raise Exception('Wrong amount of byte for PUSH')
        else:
            byte_amount = byte_amount

        if len(str(value)) != byte_amount*2:
            print(f"Invalid value ({value}) for PUSH{byte_amount}, needed PUSH{int(len(value)/2)}")
        else:
            value = value

    @property
    def opcode(self):
        return hex(0x60 + self.byte_amount - 1)[2:]

    @property
    def byte_amount(self):
        return round(len(str(self.value))/2)

    @property
    def value(self):
        if self.contract != None:
            if self.runtime_offset:
                lead_0 = "0"*abs((len(self._value) - len(int_to_hex_str(self.contract.runtime_length))))
                return lead_0 + add_0_to_hex(int_to_hex_str(self.contract.runtime_length))
            if self.creation_offset:
                lead_0 = "0"*abs((len(self._value) - len(int_to_hex_str(self.contract.creation_length))))
                return lead_0 + add_0_to_hex(int_to_hex_str(self.contract.creation_length))
            if self.creation_runtime_offset:
                lead_0 = "0"*abs((len(self._value) - len(int_to_hex_str(self.contract.creation_runtime_length))))
                return lead_0 + add_0_to_hex(int_to_hex_str(self.contract.creation_runtime_length))
        else:
            if (self._jumpdest is not None):
                if self.linked_lower != None:
                    lead_0 = "0"*abs((len(self._value) - len(self._jumpdest.pc)))
                    return  add_0_to_hex(self.value_substracted(self._jumpdest.pc))
                else:
                    lead_0 = "0"*abs((len(self._value) - len(self._jumpdest.pc)))
                    return  add_0_to_hex(self._jumpdest.pc)
            else:
                if self.linked_lower != None:
                    return add_0_to_hex(self.value_substracted(self._value))
                else:
                    return add_0_to_hex(self._value)

    @value.setter
    def value(self, new_value):
        if len(str(new_value)) != round(len(str(new_value))/2)*2:  #round(len(str(new_value))/2) = byte_amount
            print("Invalid value (%s) for PUSH with byte_amount = %s" % (new_value, round(len(str(new_value))/2)))
            self._value = add_0_to_hex(new_value)
        else:
            self._value = new_value

        if self.linked_lower != None:
            self._value = add_0_to_hex(self.value_substracted(self._value))
            
        self._byte_amount = round(len(str(new_value))/2)
        self._opcode = hex(0x60 + round(len(str(new_value))/2) - 1)
        self.updated = True 

    @property
    def name(self):
        if self._byte_amount != None:
            return "PUSH%s %s" % (self.byte_amount, self.value)
        else:
            return "PUSH"

    @property
    def jumpdest(self):
        return self._jumpdest

    @jumpdest.setter
    def jumpdest(self, jumpdest: JUMPDEST, ignore_exception=False):
        try:   
            jumpdest.link(self)
            self._jumpdest = jumpdest
            self.value = add_0_to_hex(jumpdest.pc)
        except:
                print(jumpdest)
                print("(push) Cannot link [%s] %s to [%s] JUMPDEST" % (self.pc, self.value, jumpdest.pc))


    def equals(self, other):
        return (isinstance(other, PUSH) and self.byte_amount == other.byte_amount and self.value == other.value)

    def value_substracted(self,value):
        a = int(value,16)
        b = int(self.linked_lower.value,16)
        return hex(a-b)[2:]

class DUP(metaclass=OPCODE):
    name = "DUP"
    gas = 3
    pc = ""

    def __init__(self, stack_position):
        self.opcode = hex(0x80 + stack_position - 1)[2:]  # (0x80 to 0x8f)
        self.name = f"DUP{stack_position}"
        self.ins = stack_position
        self.outs = stack_position + 1
        self.gas = 3

        if stack_position > 16 | stack_position < 1:
            raise Exception('Wrong stack position for DUP')
        else:
            stack_position = stack_position


class SWAP(metaclass=OPCODE):
    name = "SWAP"
    gas = 3
    pc = ""

    def __init__(self, stack_position):
        self.opcode = hex(0x90 + stack_position - 1)[2:]  # (0x90 to 0x9f)
        self.name = f"SWAP{stack_position}"
        self.ins = stack_position + 1
        self.outs = stack_position + 1

        if stack_position > 16 | stack_position < 1:
            raise Exception('Wrong stack position for SWAP')
        else:
            stack_position = stack_position


class LOG(metaclass=OPCODE):
    name = "LOG"
    outs = 0
    gas = 375
    pc = ""

    def __init__(self, log_number):
        self.opcode = hex(0xa0 + log_number)[2:]  # (0xa0 to 0xa4)
        self.name = f"LOG{log_number}"
        self.ins = log_number + 2

        if log_number > 4 | log_number < 1:
            raise Exception('Wrong log number for LOG')
        else:
            log_number = log_number


class CREATE(metaclass=OPCODE):
    opcode = "f0"
    name = "CREATE"
    ins = 3
    outs = 1
    gas = 32000
    pc = ""


class CALL(metaclass=OPCODE):
    opcode = "f1"
    name = "CALL"
    ins = 7
    outs = 1
    gas = 40
    pc = ""


class CALLCODE(metaclass=OPCODE):
    opcode = "f2"
    name = "CALLCODE"
    ins = 7
    outs = 1
    gas = 40
    pc = ""


class RETURN(metaclass=OPCODE):
    opcode = "f3"
    name = "RETURN"
    ins = 2
    outs = 0
    gas = 0
    pc = ""


class DELEGATECALL(metaclass=OPCODE):
    opcode = "f4"
    name = "DELEGATECALL"
    ins = 6
    outs = 1
    gas = 40
    pc = ""


class CREATE2(metaclass=OPCODE):
    opcode = "f5"
    name = "CREATE2"
    ins = 4
    outs = 1
    gas = 32000
    pc = ""


class STATICCALL(metaclass=OPCODE):
    opcode = "fa"
    name = "STATICCALL"
    ins = 6
    outs = 1
    gas = 40
    pc = ""


class REVERT(metaclass=OPCODE):
    opcode = "fd"
    name = "REVERT"
    ins = 2
    outs = 0
    gas = 0
    pc = ""


class INVALID(metaclass=OPCODE):
    name = "INVALID"
    ins = 0
    outs = 0
    gas = 0
    pc = ""

    def __init__(self, opcode):
        self.opcode = opcode

class SELFDESTRUCT(metaclass=OPCODE):
    opcode = "ff"
    name = "SELFDESTRUCT"
    ins = 1
    outs = 0
    gas = 0
    pc = ""


# if string uneven, add a 0 at the beginning
def add_0_to_hex(hex_string: str) -> str:
    if len(hex_string) % 2 != 0:
        hex_string = "0"+hex_string
    return hex_string

