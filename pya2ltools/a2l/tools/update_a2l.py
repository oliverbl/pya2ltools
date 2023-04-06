from argparse import ArgumentParser
from pathlib import Path
from a2l.reader.reader import read_a2l
from dwarf.reader import DwarfInfo
from a2l.writer.writer import write_a2l_file


def subcommand_update_a2l(parser: ArgumentParser):
    parser.add_argument(
        "--a2l_file", help="A2L file to update", required=True, type=Path
    )
    parser.add_argument(
        "--elf_file",
        help="ELF file to read ECU address info from",
        required=True,
        type=Path,
    )
    parser.add_argument("--output", help="Output file", required=False, type=Path)
    parser.set_defaults(func=update_a2l)


def update_a2l(a2l_file: Path, elf_file: Path, output: Path = None):
    if output is None:
        output = a2l_file

    print(f"Updating A2L file {a2l_file} with info from ELF file {elf_file}")
    a2l = read_a2l(a2l_file)
    dwarf_info: DwarfInfo = DwarfInfo.from_elffile(elf_file)

    for module in a2l.project.modules:
        for c in module.get_addressable_objects():
            print(c)
            name = c.name
            offset = 0
            if c.symbol_link is not None:
                offset = c.symbol_link.offset
                name = c.symbol_link.symbol_name
            c.ecu_address = dwarf_info.get_address_by_variable_path(name) + offset
            print(f"{c.name} = {c.ecu_address}")
    write_a2l_file(a2l, output)
