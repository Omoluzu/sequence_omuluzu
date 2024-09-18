import re
from pathlib import Path
from collections import namedtuple


SequenceInfo = namedtuple(
    'SequenceInfo',
    ['regular', 'full_path', 'output_name', 'start_number']
)


def get_sequence_all_name(path: Path) -> dict[str, SequenceInfo]:
    """Getting information about all possible sequences
    :param path: The path to finding sequences
    :return: information about sequences
    """
    data = {}

    for file in path.rglob('*.jpg'):
        file_match = re.match(
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

        if not data.get(regular_name):
            data[regular_name] = SequenceInfo(
                regular=regular_name,
                full_path=file.absolute().parent,
                output_name=file_match.group('name').strip() + '.mp4',
                start_number=int(file_match.group('number'))
            )

    return data  # todo: общий класс со всей информацией.
