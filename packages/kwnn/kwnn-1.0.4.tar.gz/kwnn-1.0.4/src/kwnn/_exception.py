class KwnnException(BaseException):
    code: int
    message: str

    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message

        msg = f"{message}, code: {code}"
        super().__init__(msg)
