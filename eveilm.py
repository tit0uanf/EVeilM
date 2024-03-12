import click
import inquirer
import os
from obfuscator.obfuscator import Obfuscator
from utils.utils import read_file
from disassembler.disassembler import evmcode_string_to_list
from contract.contract import Contract
from utils.print_colors import colors as c

def analyze_evmcode_file(filepath):
    filename = os.path.basename(filepath)
    evmcode = read_file("./resources/original/" + filepath)
    bytecode = evmcode_string_to_list(evmcode)
    contract = Contract(filename, bytecode)
    print(f"{c.Bold}Successfully decompiled %s" % filename)
    contract.update_pc()
    print("Attributing PC to opcodes")
    contract.link_jumpdest_push()
    return contract

def write_to_file(contract, obf_type):
    obfuscated_dir = os.path.join('resources', 'obfuscated', obf_type)
    if not os.path.exists(obfuscated_dir):
        os.makedirs(obfuscated_dir)
    file_path = os.path.join(obfuscated_dir, contract.name + "_" + obf_type + '.obf')
    with open(file_path, 'w') as f:
        f.write(contract.get_full_bytecode())

def choose_file():
    files = [f for f in os.listdir('resources/original') if os.path.isfile(os.path.join('resources/original', f))]
    questions = [
        inquirer.List('selected_file',
                      message="Choose a file to obfuscate",
                      choices=files,
                      ),
    ]
    answers = inquirer.prompt(questions)
    return answers['selected_file']

def choose_obfuscation_type():
    obf_types = ["full"]#, "addmanip", "funcsigtransfo", "spamjumpdest", "jumptransfo"]
    questions = [
        inquirer.List('obf_type',
                      message="Choose obfuscation methods to apply",
                      choices=obf_types,
                      ),
    ]
    answers = inquirer.prompt(questions)
    return answers['obf_type']


@click.command()
def main():
    input_method = inquirer.prompt([
        inquirer.List('input_method',
                      message="Choose input method",
                      choices=['Paste Bytecode', 'Select File'],
                      ),
    ])['input_method']

    if input_method == 'Paste Bytecode':
        bytecode = click.prompt("Please paste the bytecode (might get truncated)")
        filename = click.prompt("What is the name of the contract ?")
        evmcode = evmcode_string_to_list(bytecode)
        contract = Contract(filename, evmcode)
    else:
        selected_file = choose_file()
        contract = analyze_evmcode_file(selected_file)

    selected_obf_type = choose_obfuscation_type()


    obfuscator = Obfuscator(contract, selected_obf_type)
    contract.update_pc()
    obfuscator.obfuscate_contract()
    contract.update_pc()
    click.echo(str(contract))
    click.echo("Contract functions :")
    click.echo(str(contract.func_sig))
    write_to_file(contract, obf_type=selected_obf_type)


if __name__ == '__main__':
    main()
