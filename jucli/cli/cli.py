import argparse
import logging

from jucli.lib.options import Options


def parse() -> Options:
    parser = argparse.ArgumentParser(description='JuCLI')

    parser.add_argument(
        'commands',
        metavar='command',
        type=str,
        nargs='+',
        help='command/commands'
    )

    parser.add_argument(
        '-v',
        '--verbose',
        action='store_true',
        help='Set logging to verbose'
    )

    args = parser.parse_args()

    return Options(
        log_level=logging.DEBUG if args.verbose else logging.INFO,
        commands=args.commands
    )
