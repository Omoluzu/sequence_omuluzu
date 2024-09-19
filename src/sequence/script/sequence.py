import os
import sys
import ffmpeg

from src.sequence import SequenceInfo, Config


def sequence(
        sequence_info: SequenceInfo, output_adapter, frame_rate: int = 25
) -> None:
    """file sequence
    :param sequence_info: Input file
    :param output_adapter: todo
    :param frame_rate: frame rate
    """
    process = (
        ffmpeg.output(
            ffmpeg.input(
                os.path.join(sequence_info.full_path, sequence_info.regular),
                start_number=sequence_info.start_number,
                framerate=frame_rate
            ),
            os.path.join(str(Config.output_path), sequence_info.output_name),
            vcodec='mjpeg',
            qscale=1,
            an=None
        ).global_args(
            '-progress', 'pipe:1'
        ).run_async(
            pipe_stdout=True,
            pipe_stderr=True
        )
    )

    while True:
        output = process.stdout.readline()
        if output == b'' and process.poll() is not None:
            break
        if output:
            output_adapter.input(output.decode().strip())

            """
            ---frame=118
            ---fps=22.59
            ---stream_0_0_q=-1.0
            ---bitrate=2841.9kbits/s
            ---total_size=1634131
            ---out_time_us=4600078
            ---out_time_ms=4600078
            ---out_time=00:00:04.600078
            ---dup_frames=0
            ---drop_frames=0
            ---speed=0.881x
            ---progress=end
            """

    # Получение ошибок, если они есть
    stderr = process.stderr.read()
    if stderr:
        print(stderr.decode(), file=sys.stderr)
