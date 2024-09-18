import ffmpeg


def sequence(input_pattern, output_file, frame_rate=25) -> None:
    """file sequence
    :param input_pattern: Input file
    :param output_file: output_file
    :param frame_rate: frame rate
    """
    ffmpeg.input(
        input_pattern, framerate=frame_rate
    ).output(
        output_file
    ).run()

