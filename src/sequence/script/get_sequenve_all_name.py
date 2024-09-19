import re
from pathlib import Path

from src import sequence


def get_sequence_all_name(path: Path) -> 'sequence.Sequences':
    """Getting information about all possible sequences
    :param path: The path to finding sequences
    :return: information about sequences
    :except OSError: file read error
    """
    sequences = sequence.Sequences()

    for file in path.rglob('*.jpg'):  # todo: и даже инициализацию, см комментарий ниже
        file_match = re.match(  # todo: Весь данный функционал можно закинуть я думаю в add_sequence
            r"^(?P<name>.+?)((?P<number>\d+)(?:\.jpg))$",
            file.name
        )

        try:
            number = str(len(file_match.group('number')))
        except AttributeError:
            pass  # todo:  наверное тут надо как то сохранить информацию об ошибке и передать конечному пользователю.
            continue

        regular_number = '%0' + number + 'd' + file.suffix
        regular_name = file_match.group('name') + regular_number

        if not sequences.check_sequence(regular_name):
            sequences.add_sequence(
                sequence.SequenceInfo(
                    regular=regular_name,
                    full_path=file.absolute().parent,
                    output_name=file_match.group('name').strip() + '.mp4',  # todo: позаботиться о лишней точке иногда бывает ..mp4
                    start_number=int(file_match.group('number'))
                )
            )

    return sequences
