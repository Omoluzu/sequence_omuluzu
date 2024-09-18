import os.path
from pathlib import Path

from src.sequence.script import sequence, get_sequence_all_name


def main(path: Path):
    data = get_sequence_all_name(path)

    for name, value in data.items():
        sequence(
            input_pattern=os.path.join(value['path'], name),
            output_file=value['name'] + '.mp4',
            start_number=value['start_number']
        )


if __name__ == '__main__':
    main(
        Path(r'files')
    )
