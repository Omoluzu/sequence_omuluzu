import configparser


class Config:
    instance = None
    config = None

    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super().__new__(cls)
            cls.config = configparser.ConfigParser()
            cls.config.read('config.ini')

        return cls.instance

    @classmethod
    @property
    def output_path(cls) -> str:
        return cls.config.get('base', 'output_path')
