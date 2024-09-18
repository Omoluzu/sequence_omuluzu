from pathlib import Path

from src.sequence.script import sequence


def main():

    # path = Path(r'D:\Python\AlgousStudio\pythonProject\files\Explosion Huge')
    #
    # for file in path.rglob('*.jpg'):
    #     print(file)

    sequence(
        'files/blood_and_blood/blood.%03d.jpg', 'blood_and_blood.mp4'
    )


if __name__ == '__main__':
    main()