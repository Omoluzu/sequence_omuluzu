import os.path
from pathlib import Path

from src.sequence.script import sequence, get_sequence_all_name


def main(path: Path):
    data = get_sequence_all_name(path)

    need_file = list(data.keys())[3]
    # print(need_file)
    print(data[need_file])
    #
    sequence(
        input_pattern=os.path.join(data[need_file]['path'], need_file),
        output_file=data[need_file]['name'] + '.mp4'
    )




if __name__ == '__main__':
    main(
        # Path(r'D:\Python\AlgousStudio\pythonProject\files\Explosion Huge')
        Path(r'files')
    )