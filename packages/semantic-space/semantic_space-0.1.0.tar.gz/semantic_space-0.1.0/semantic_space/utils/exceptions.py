class FileCorruptedError(Exception):

    def __init__(self, hint: str = ""):
        super().__init__(f"File is corrupted{': ' + hint if hint else '.'}")

class ArgumentError(Exception):

    def __init__(self, hint: str = ""):
        super().__init__(f"Argument is incorrect{': ' + hint if hint else '.'}")


