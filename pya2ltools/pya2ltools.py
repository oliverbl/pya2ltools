from pathlib import Path
from dwarf.reader import DwarfInfo


def main():
    path = Path("test_structs.o")

    dwarf_info: DwarfInfo = DwarfInfo.from_elffile(path)

    for name, var in dwarf_info.variables.items():
        print(var)


if __name__ == "__main__":
    main()
