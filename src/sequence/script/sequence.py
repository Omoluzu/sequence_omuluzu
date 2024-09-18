import os
import ffmpeg
from src.sequence import SequenceInfo


def sequence(sequence_info: SequenceInfo, frame_rate: int = 25) -> None:
    """file sequence
    :param sequence_info: Input file
    :param frame_rate: frame rate
    """
    ffmpeg.output(
        ffmpeg.input(
            os.path.join(sequence_info.full_path, sequence_info.regular),
            start_number=sequence_info.start_number,
            framerate=frame_rate
        ),
        sequence_info.output_name
    ).run()
