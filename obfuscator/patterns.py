from dataclasses import dataclass
from typing import List, Tuple
from opcodes.opcodes import *

@dataclass
class Pattern:
    name: str
    original: List
    replaceable: bool
    obfuscated: List
    pattern_type: str


PATTERNS = [
    Pattern(
        name="ADD",
        original=[ADD],
        replaceable=True,
        obfuscated=[DUP(2), PUSH(1, "00"), SUB(), SUB(), SWAP(1), POP(), NOT(), PUSH(1, "01"), ADD()],
        pattern_type="runtime",
    ),
    Pattern(
        name="PUSH32",
        original=[PUSH],
        replaceable=True,
        obfuscated=[PUSH,PUSH,ADD],
        pattern_type="runtime",
    ),
    Pattern(
         name="FUNC_SELECTOR",
        original=[DUP, PUSH, EQ, PUSH, JUMPI],
        replaceable=True,
        obfuscated=[],
        pattern_type="runtime",
    ),
    Pattern(
         name="PAYABLE_CHECK",
        original=[CALLVALUE, DUP, ISZERO, PUSH, JUMPI, PUSH, DUP, REVERT],
        replaceable=False,
        obfuscated=[],
        pattern_type="runtime",
    ),
    Pattern(
         name="JUMPTRANSFO",
        original=[PUSH, JUMPI],
        replaceable=True,
        obfuscated=[],
        pattern_type="runtime",
    ),
    Pattern(
         name="LENGTH_OFFSET",
        original=[PUSH, DUP, PUSH, PUSH, CODECOPY, PUSH, RETURN],
        replaceable=True,
        obfuscated=[],
        pattern_type="creation",
    ),
    Pattern(
        name="CONSTRUCTOR",
        original=[PUSH, MLOAD, PUSH, CODESIZE, SUB, DUP, PUSH, DUP, CODECOPY],
        replaceable=True,
        obfuscated=[],
        pattern_type="creation",
    ),
]
