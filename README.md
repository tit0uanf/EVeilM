EVeilM 🦹‍♂️🔗
=======================

> Research software accompanying the KTH master's thesis *EVeilM: EVM Bytecode Obfuscation*.


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


Master Thesis Report 📝
-------
EVeilM is the outcome of a master's thesis project conducted at KTH Royal Institute of Technology. The project aimed to explore and develop techniques for obfuscating Ethereum smart contract bytecode. Throughout the research, various obfuscation methods were studied, analyzed, and implemented to create a comprehensive tool.
The report is available here : [EVeilM: EVM Bytecode Obfuscation](Master_Thesis_Report_KTH.pdf)


Citation 📚
-------

If EVeilM, its techniques, or results inform your research, please cite the thesis:

```bibtex
@mastersthesis{forissier2024eveilm,
  author = {Forissier, Titouan},
  title = {{EVeilM}: {EVM Bytecode Obfuscation}},
  school = {KTH Royal Institute of Technology},
  year = {2024},
  type = {Master's thesis},
  url = {https://urn.kb.se/resolve?urn=urn:nbn:se:kth:diva-359674}
}
```

The canonical thesis record is hosted by [KTH DiVA](https://urn.kb.se/resolve?urn=urn:nbn:se:kth:diva-359674). For a software-specific citation, use the GitHub **Cite this repository** control, which reads [CITATION.cff](CITATION.cff).

### Creating a citable release

This repository includes `.zenodo.json` metadata for archival releases. To obtain a DOI, connect the repository to [Zenodo's GitHub integration](https://zenodo.org/account/settings/github/), enable EVeilM, and publish a tagged GitHub release. Zenodo will archive that release and mint a version DOI; use its concept DOI in documentation when you want a DOI that always resolves to the latest archived release. Do not replace the thesis citation with the software DOI: cite both when your work uses both the thesis methods and a particular EVeilM release.


Disclaimer ⚠️
-------
The author of the **EVeilM** is not responsible for any vulnerabilities or issues that may be introduced in the obfuscated smart contract bytecode. Users are advised to thoroughly test and audit their contracts before deploying them on the EVM compatible network. The tool is provided as-is, without any warranties or guarantees.
