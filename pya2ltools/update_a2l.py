from pathlib import Path
from a2l.reader.reader import read_a2l
from dwarf.reader import DwarfInfo
from a2l.writer.writer import write_a2l_file


def update_a2l(a2l_file: Path, elf_file: Path, output: Path = None):
    if output is None:
        output = a2l_file

    print(f"Updating A2L file {a2l_file} with info from ELF file {elf_file}")
    a2l = read_a2l(a2l_file)
    dwarf_info: DwarfInfo = DwarfInfo.from_elffile(elf_file)

    for module in a2l.project.modules:
        for c in module.get_addressable_objects():
            c.ecu_address = dwarf_info.get_address_by_variable_path(c.name)
            print(f"{c.name} = {c.ecu_address}")
    write_a2l_file(a2l, output)
