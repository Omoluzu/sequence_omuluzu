import os.path
from pathlib import Path

from src.sequence.script import sequence, get_sequence_all_name


def main(path: Path):
    data = get_sequence_all_name(path)

    for value in data.values():
        sequence(value)


if __name__ == '__main__':
    main(
        Path(r'files')
    )
