import re
from pathlib import Path
from typing import Any


def get_sequence_all_name(path: Path) -> dict[str, Any]:
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

        number = '%0' + number + 'd' + file.suffix
        name = file_match.group('name') + number

        if not data.get(name):  # todo. Скорее всего тут нужен namedtuple или кастомный класс
            data[name] = {
                'path': file.absolute().parent,
                'name': file_match.group('name').strip()
            }

    return data  # todo: общий класс со всей информацией.
