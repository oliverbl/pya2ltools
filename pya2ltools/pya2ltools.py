from argparse import ArgumentParser

from a2l.tools.update_a2l import subcommand_update_a2l
from a2l.tools.merge_a2l import subcommand_merge_a2l


def main():
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(
        dest="command", help="Available subcommands", required=True
    )
    subcommand_update_a2l(subparsers.add_parser("update_a2l", help="Update A2L file"))
    subcommand_merge_a2l(subparsers.add_parser("merge_a2l", help="Merge A2L files"))

    args = parser.parse_args()
    func_args = {
        t[0]: t[1] for t in args._get_kwargs() if t[0] != "func" and t[0] != "command"
    }
    args.func(**func_args)


if __name__ == "__main__":
    main()
