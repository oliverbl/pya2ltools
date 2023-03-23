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
    # path = Path("test") / "ECU_Description" / "ASAP2_Demo_V171_reduced.a2l"
    a2l_file = read_a2l(path)
    print(a2l_file)
    # for c in a2l_file.project.modules[0].characteristics:
    #     print(c)

    # for m in a2l_file.project.modules[0].measurements:
    #     print(m)

    # for compu_method in a2l_file.project.modules[0].compu_methods:
    #     print(compu_method)

    # for compu_tab in a2l_file.project.modules[0].compu_tabs:
    #     print(compu_tab)

    # for compu_vtab in a2l_file.project.modules[0].compu_vtabs:
    #     print(compu_vtab)

    # for compu_tab_range in a2l_file.project.modules[0].compu_vtab_ranges:
    #     print(compu_tab_range)

    # for record_layout in a2l_file.project.modules[0].record_layouts:
    #     print(record_layout)

    for transformer in a2l_file.project.modules[0].transformers:
        print(transformer)


def main():
    test_a2l()
    # test_dwarf()


if __name__ == "__main__":
    main()
