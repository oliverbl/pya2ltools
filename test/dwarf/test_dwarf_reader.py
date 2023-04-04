import unittest
from parameterized import parameterized_class
import itertools
import subprocess
from pya2ltools.dwarf.model import (
    DwarfArray,
    DwarfBaseType,
    DwarfEnum,
    DwarfMember,
    DwarfStructure,
    DwarfVariable,
)
from pya2ltools.dwarf.reader import DwarfInfo
import pathlib

current_folder = pathlib.Path(__file__).parent.resolve()

c_base = """
#include <stdint.h>

{typedefs}

{variables}

int main(int argc, char** argv) {{

{content}
}}
"""


@parameterized_class(
    ("compiler", "dwarf_version"),
    itertools.product(
        ["gcc", "clang", "arm-none-eabi-gcc"], ["-gdwarf-3", "-gdwarf-4", "-gdwarf-5"]
    ),
)
class TestDwarfReader(unittest.TestCase):
    def setUp(self):
        self.input = (
            current_folder / f"{self.compiler}_{self.dwarf_version}_test_structs_temp.c"
        )
        self.output = (
            current_folder / f"{self.compiler}_{self.dwarf_version}_test_structs_temp.o"
        )

    def compiler_call(self, input=None, output=None):
        if input is None:
            input = self.input
        if output is None:
            output = self.output
        args = [
            self.compiler,
            "-g",
            self.dwarf_version,
            "-c",
            input,
            "-o",
            output,
        ]
        subprocess.run(args, check=True, cwd=current_folder)

    def create_c_file(self, c_struct, variable, content):
        with self.input.open("w") as f:
            f.write(
                c_base.format(typedefs=c_struct, variables=variable, content=content)
            )

    def compare_dwarf_infos(self, expected: DwarfInfo, actual: DwarfInfo):
        self.assertEqual(len(expected.variables), len(actual.variables))
        for name, var in expected.variables.items():
            self.assertIn(name, actual.variables)
            actual_var = actual.variables[name]
            self.assertEqual(var[0].datatype, actual_var[0].datatype)

    def generate_info_and_compare(
        self, c_struct: str, variable: str, content: str, expected: DwarfInfo
    ):
        self.create_c_file(c_struct, variable, content)
        self.compiler_call()
        dwarf_info: DwarfInfo = DwarfInfo.from_elffile(self.output)
        self.compare_dwarf_infos(expected, dwarf_info)

    def test_simple_struct(self):
        a = DwarfMember(name="a", offset=0, datatype=DwarfBaseType("uint8_t", size=1))
        b = DwarfMember(name="b", offset=1, datatype=DwarfBaseType("uint8_t", size=1))

        struct = DwarfStructure(name="SomeA", members={"a": a, "b": b}, size=2)
        var = DwarfVariable(name="some_a", location=0, datatype=struct, file="", line=0)

        expected = DwarfInfo(variables={"some_a": [var]})

        c_struct = """
        typedef struct
        {
            uint8_t a;
            uint8_t b;
        } SomeA;
        """
        variable = "static SomeA some_a;"
        content = "some_a.a = 1;"
        self.generate_info_and_compare(c_struct, variable, content, expected)

    def test_enum(self):
        enum = DwarfEnum(
            name="SomeEnum", members={"SomeEnumA": 0, "SomeEnumB": 1, "SomeEnumC": 2}
        )
        var = DwarfVariable(name="someEnum", location=0, datatype=enum, file="", line=0)
        expected = DwarfInfo(variables={"someEnum": [var]})
        c_enum = """
        typedef enum SomeEnum
        {
            SomeEnumA,
            SomeEnumB,
            SomeEnumC
        } SomeEnum;
        """
        variable = "static SomeEnum someEnum = SomeEnumA;"
        content = "someEnum = SomeEnumB;"
        self.generate_info_and_compare(c_enum, variable, content, expected)

    def test_recursive_struct(self):
        struct = DwarfStructure(
            size=8,
            name="RecursiveStruct",
            members={
                "a": DwarfMember(
                    name="a", offset=4, datatype=DwarfBaseType("uint8_t", size=1)
                ),
                "next": None,
            },
        )
        var = DwarfVariable(
            name="recursiveStruct", location=0, datatype=struct, file="", line=0
        )
        expected = DwarfInfo(variables={"recursiveStruct": [var]})
        c_enum = """
        typedef struct RecursiveStruct
        {
            struct RecursiveStruct* next;
            uint8_t a;
        } RecursiveStruct;
        """
        variable = "static RecursiveStruct recursiveStruct = { 0 };"
        content = "recursiveStruct.a = 3;"
        self.create_c_file(c_enum, variable, content)
        self.compiler_call()
        actual: DwarfInfo = DwarfInfo.from_elffile(self.output)
        self.assertEqual(len(expected.variables), len(actual.variables))
        for name, var in expected.variables.items():
            self.assertIn(name, actual.variables)
            actual_var = actual.variables[name]
            self.assertEqual(var[0].datatype.name, actual_var[0].datatype.name)

    def test_nested_struct(self):
        a = DwarfMember(name="a", offset=0, datatype=DwarfBaseType("uint8_t", size=1))
        b = DwarfMember(name="b", offset=1, datatype=DwarfBaseType("uint8_t", size=1))

        inner_struct = DwarfStructure(name="SomeA", members={"a": a, "b": b}, size=2)

        outer_struct = DwarfStructure(
            size=3,
            name="NestedStruct",
            members={
                "someA": DwarfMember(name="someA", offset=0, datatype=inner_struct),
                "c": DwarfMember(
                    name="c", offset=2, datatype=DwarfBaseType("uint8_t", size=1)
                ),
            },
        )
        var = DwarfVariable(
            name="nestedStruct", location=0, datatype=outer_struct, file="", line=0
        )
        expected = DwarfInfo(variables={"nestedStruct": [var]})
        c_enum = """
        typedef struct
        {
            uint8_t a;
            uint8_t b;
        } SomeA;

        typedef struct NestedStruct
        {
            SomeA someA;
            uint8_t c;
        } NestedStruct;
        """
        variable = "static NestedStruct nestedStruct = { 0 };"
        content = "nestedStruct.c = 3;"
        self.generate_info_and_compare(c_enum, variable, content, expected)

    def test_array(self):
        array = DwarfArray(
            datatype=DwarfBaseType("uint8_t", size=1), size=0, dimensions=[3]
        )
        var = DwarfVariable(
            name="someArray", location=0, datatype=array, file="", line=0
        )
        expected = DwarfInfo(variables={"someArray": [var]})
        c_struct = ""
        variable = "static uint8_t someArray[3];"
        content = "someArray[0] = 3;"
        self.generate_info_and_compare(c_struct, variable, content, expected)

    def tearDown(self) -> None:
        self.input.unlink()
        self.output.unlink()
