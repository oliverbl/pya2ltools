from pathlib import Path
from typing import Any, Self
import re

from elftools.elf.elffile import ELFFile

from dataclasses import dataclass, field
from dataclasses_json import dataclass_json

from model import DwarfVariable

def str_to_variable_path(path: str) -> list[str | int]:
    path = []
    # split variable_path by . and [] and return list of strings and indexes between []
    # e.g. "a.b[0].c" -> ["a", "b", 0, "c"]
    for part in re.split(r"(\[|\]|\.)", path):
        if part == ".":
            continue
        if part == "[":
            continue
        if part == "]":
            continue
        if part == "":
            continue
        if part.isdigit():
            path.append(int(part))
        else:
            path.append(part)
    return path


@dataclass_json
@dataclass
class DwarfInfo:
    variables: dict[str, DwarfVariable] = field(default_factory=dict)
    # CU to datatype cache
    cache: dict[Any, Any] = field(default_factory=dict)

    @staticmethod
    def from_elffile(file, variable_name: str = None) -> Self:
        _self = DwarfInfo()

        with open(file, "rb") as f:
            elffile = ELFFile(f)

            if not elffile.has_dwarf_info():
                print("  file has no DWARF info")
                return
            dwarfinfo = elffile.get_dwarf_info()

            for CU in dwarfinfo.iter_CUs():
                top_DIE = CU.get_top_DIE()
                _self.die_info_rec(top_DIE, variable_name=variable_name)
            return _self

    def get_address_by_variable_path(self, variable_path: str) -> int:
        path = str_to_variable_path(variable_path)
        var = self.variables[path[0]]
        address = var.location
        for part in path[1:]:
            if isinstance(part, int):
                address += part * var.datatype.datatype.size
                var = var.datatype
            else:
                address += var.datatype.members[part].offset
                var = var.datatype.members[part]
        return address

    def die_info_rec(self, die, variable_name: str = None):
        tags_to_skip = ["DW_TAG_subprogram", "DW_TAG_user"]

        if die.tag in tags_to_skip:
            return

        if die.tag == "DW_TAG_variable":
            if "DW_AT_location" not in die.attributes:
                return

            if variable_name is not None:
                if die.attributes["DW_AT_name"].value.decode("utf-8") != variable_name:
                    return

            v = DwarfVariable.from_die(die, self.cache)
            self.variables[v.name] = v

        for child in die.iter_children():
            self.die_info_rec(child, variable_name)


def main():
    path = Path("test") / "ots_HIL.out"

    dwarf_info: DwarfInfo = DwarfInfo.from_elffile(path)

    var = dwarf_info.variables["demQueue"]
    print(var)

    with open("test.json", "w") as f:
        f.write(dwarf_info.to_json())


if __name__ == "__main__":
    main()
