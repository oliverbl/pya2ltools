from argparse import ArgumentParser
from pathlib import Path
import struct
from a2l.reader.reader import read_a2l
from intelhex import IntelHex


def subcommand_read_calibration_data(parser: ArgumentParser):
    parser.add_argument(
        "--a2l_file", help="A2L file to create Data Model for", required=True, type=Path
    )
    parser.add_argument(
        "--hex_file",
        help="Hex file to read data from",
        required=True,
        type=Path,
    )
    parser.add_argument("--output", help="Output file", required=True, type=Path)
    parser.set_defaults(func=create_calibration_data)


def create_calibration_data(a2l_file: Path, hex_file: Path, output: Path = None):
    if output is None:
        output = a2l_file

    print(f"Creating calibration data from A2L file {a2l_file} and hex file {hex_file}")
    a2l = read_a2l(a2l_file)
    hex = IntelHex(str(hex_file))

    for module in a2l.project.modules:
        for c in module.get_addressable_objects():
            var = struct.unpack(">B", hex.gets(c.ecu_address, 1))[0]
            print(f"{c.name} = {var}")
