class InvaildCredentials(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class DrivePathException(FileNotFoundError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)