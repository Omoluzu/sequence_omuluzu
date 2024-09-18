import ffmpeg


def sequence(input_pattern, output_file, frame_rate=25, start_number=1) -> None:
    """file sequence
    :param input_pattern: Input file
    :param output_file: output_file
    :param frame_rate: frame rate
    :param start_number: Number of starts position
    """
    test = ffmpeg.input(
        input_pattern,
        start_number=start_number,
        framerate=frame_rate
    )

    ffmpeg.output(test, output_file).run()
