from lib.cli import cli
from lib.options import Options

if __name__ == "__main__":
    # TODO: Load .juclirc.yml
    obj = { "options": Options() }
    cli(obj = obj)
