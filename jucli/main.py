import os
from pathlib import Path
import json
from jucli.cli.cli import cli


def main() -> None:
    # Load config
    config_path = Path().home() / '.juclirc.json'
    if config_path.is_file():
        with open(config_path) as file:
            config = json.load(file)
            for key, value in config.items():
                os.environ[f"JUCLI_{key.upper()}"] = value

    cli()


if __name__ == "__main__":
    main()
