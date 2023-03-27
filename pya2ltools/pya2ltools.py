from pathlib import Path
from dwarf.reader import DwarfInfo
from a2l.reader.reader import read_a2l


def test_dwarf():
    path = Path("test_structs.o")

    dwarf_info: DwarfInfo = DwarfInfo.from_elffile(path)

    for name, var in dwarf_info.variables.items():
        print(var)


def test_a2l():
    # path = Path("test") / "ECU_Description" / "ASAP2_Demo_V171 simplified.a2l"
    # path = Path("test") / "ECU_Description" / "ASAP2_Demo_V171_reduced.a2l"
    path = Path("test") / "ECU_Description" / "ASAP2_Demo_V171.a2l"
    a2l_file = read_a2l(path)
    # print(a2l_file)


def main():
    test_a2l()
    test_dwarf()


if __name__ == "__main__":
    main()
