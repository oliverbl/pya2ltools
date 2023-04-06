from argparse import ArgumentParser
from pathlib import Path
from a2l.reader.reader import read_a2l
from a2l.writer.writer import write_a2l_file


def subcommand_merge_a2l(parser: ArgumentParser):
    parser.add_argument(
        "--main", help="Main A2L file to merge into", required=True, type=Path
    )
    parser.add_argument(
        "--secondary",
        help="A2l Files to merge into main",
        required=True,
        nargs="+",
        type=Path,
    )
    parser.add_argument("--output", help="Output file", required=False, type=Path)
    parser.set_defaults(func=merge_a2l)


def merge_a2l(main: Path, secondary: list[Path], output: Path = None):
    if output is None:
        output = main

    print(f"Merging A2L file {main} with {secondary}")
    main_a2l = read_a2l(main)
    for a2l_file in secondary:
        secondary_a2l = read_a2l(a2l_file)
        main_a2l += secondary_a2l

    write_a2l_file(main_a2l, output)
