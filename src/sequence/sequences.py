from collections import namedtuple
from typing import Set

SequenceInfo = namedtuple(  # todo: Все таки он должен быть не namedtupled
    'SequenceInfo',
    ['regular', 'full_path', 'output_name', 'start_number']
)


class Sequences:
    __data_sequence: dict[str, SequenceInfo] = {}
    __names_sequence: Set[str]

    def __init__(self):
        self.__names_sequence = set()

    @property
    def names(self) -> Set[str]:
        """getting reserved names sequences
        :return: names sequences
        """
        return self.__names_sequence

    def add_sequence(self, sequence: SequenceInfo) -> None:
        """Added new sequence
        :param sequence: Information sequence
        """
        self.__names_sequence.add(sequence.regular)
        self.__data_sequence[sequence.regular] = sequence

    def get_sequence(self, name: str) -> SequenceInfo:
        """Getting sequence by his name.
        :param name: name of the sought sequences
        :return: Information sequence
        """
        return self.__data_sequence[name]

    def check_sequence(self, name: str) -> bool:
        """Check for the presence of sequences
        :param name: name of the sought sequences
        :return: check flag
        """
        return name in self.__names_sequence
