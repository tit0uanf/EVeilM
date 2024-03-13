EVeilM 🦹‍♂️🔗
=======================


EVeilM is a PoC EVM Bytecode Obfuscator.

This tool helps you **analyze** and **obfuscate** EVM bytecode, enhancing the security of your contracts and protecting your intellectual property.

Table of Contents
-----------------

1. [Features](#features)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Obfuscation Techniques](#obfuscation-techniques)
5. [License](#license)

Features ⚡
----------

- Parse and disassemble EVM bytecode 🔍
- Obfuscate EVM bytecode 🦹‍♂️

Installation ⚙️
-------------

To install EVeilM, follow these steps:

1. Clone the repository:
```bash
git clone https://github.com/tit0uanf/eveilm.git
```
2. Navigate to the project directory:
```bash
cd eveilm
```
3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

Usage 🛠️
-------

To use the EVM Bytecode Obfuscator, follow these steps:

Choose an input method:
```bash
$ python eveilm.py
Choose input method:
❯ Paste Bytecode
  Select File
```


If you choose "Paste Bytecode", paste the bytecode and enter the contract name:
```bash
Please paste the bytecode (might get truncated): 6080604052...
What is the name of the contract ? MyContract
```
> [!IMPORTANT]
> Make sure that the bytecode input contains both Creation and Runtime Bytecode


If you choose "Select File", select the file containing the bytecode under `/resources/original`:
```bash
Choose a file to obfuscate:
  USDC.evm
❯ USDT.evm
  WETH.evm
```

> [!NOTE]
> The obfuscated bytecode are saved in `resources/obfuscated/MyContract.obf`

Obfuscation Techniques 🎭
-----------------------

These techniques are PoC obfuscation methods.


`ADD Opcode Stack Manipulation`: Obfuscates *ADD* opcodes by introducing additional manipulations.

`Function Signature Transformer`: Transforms function signatures to hide their name from decompilers.

`Control Flow Graph Spammer`: Insert random fake control flow paths.

`Jump Address Transformer`:  Obfuscate *JUMP* and *JUMPI* opcodes PC destination



Disclaimer ⚠️
-------
The author of the **EVeilM** is not responsible for any vulnerabilities or issues that may be introduced in the obfuscated smart contract bytecode. Users are advised to thoroughly test and audit their contracts before deploying them on the EVM compatible network. The tool is provided as-is, without any warranties or guarantees.
