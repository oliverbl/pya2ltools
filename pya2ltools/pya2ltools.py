from pathlib import Path
from a2l.reader.reader import read_a2l
from argparse import ArgumentParser

from update_a2l import update_a2l


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


def main():
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(
        dest="command", help="Available subcommands", required=True
    )
    subcommand_update_a2l(subparsers.add_parser("update_a2l", help="Update A2L file"))

    args = parser.parse_args()
    func_args = {
        t[0]: t[1] for t in args._get_kwargs() if t[0] != "func" and t[0] != "command"
    }
    args.func(**func_args)


if __name__ == "__main__":
    main()
