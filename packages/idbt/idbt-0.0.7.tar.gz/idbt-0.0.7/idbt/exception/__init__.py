class ParsingException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class FileNotFoundException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
