import unittest
from parameterized import parameterized
import itertools
import subprocess
from pya2ltools.dwarf.reader import DwarfInfo
import pathlib

current_folder = pathlib.Path(__file__).parent.resolve()


def custom_name_func(testcase_func, param_num, param):
    return "%s_%s" % (
        testcase_func.__name__,
        parameterized.to_safe_name("_".join(str(x) for x in param.args)),
    )


class TestDwarfReader(unittest.TestCase):
    @parameterized.expand(
        itertools.product(
            ["gcc", "clang", "arm-none-eabi-gcc"],
            ["-gdwarf-3", "-gdwarf-4", "-gdwarf-5"],
        ),
        name_func=custom_name_func,
    )
    def test_compiler_and_dwarf_combination(self, compiler, dwarf):
        input = "test_structs.c"
        output = "test_structs.o"

        args = [
            compiler,
            "-g",
            dwarf,
            "-c",
            input,
            "-o",
            output,
        ]
        print(" ".join(args))
        subprocess.run(args, check=True, cwd=current_folder)
        try:
            dwarf_info = DwarfInfo.from_elffile(current_folder / output)
        except Exception as e:
            self.fail(f"Failed to parse dwarf info with {compiler} and {dwarf}: {e}")

    def tearDown(self) -> None:
        (current_folder / "test_structs.o").unlink()
