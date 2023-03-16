from pathlib import Path
from dwarf.reader import DwarfInfo
from a2l.reader import read_a2l


def test_dwarf():
    path = Path("test_structs.o")

    dwarf_info: DwarfInfo = DwarfInfo.from_elffile(path)

    for name, var in dwarf_info.variables.items():
        print(var)


def test_a2l():
    path = Path("test") / "ECU_Description" / "ASAP2_Demo_V171 simplified.a2l"
    a2l_file = read_a2l(path)
    # print(a2l_file)
    for c in a2l_file.project.modules[0].characteristics:
        print(c)


def main():
    test_a2l()


if __name__ == "__main__":
    main()
