class SelectelError(Exception):
    pass


class SelectelAuthError(SelectelError):
    pass


class SelectelRequestError(SelectelError):
    def __init__(self, message: str):
        self.message = message
        super().__init__(f'Error while setting container options: {message}')


class AuthError(Exception):
    pass


class RequestError(Exception):
    pass
