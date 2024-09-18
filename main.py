import os.path
from pathlib import Path

from src.sequence.script import sequence, get_sequence_all_name


def main(path: Path):
    sequences = get_sequence_all_name(path)

    for name_sequences in sequences.names:
        sequence(sequences.get_sequence(name_sequences))


if __name__ == '__main__':
    main(
        Path(r'files')
    )
