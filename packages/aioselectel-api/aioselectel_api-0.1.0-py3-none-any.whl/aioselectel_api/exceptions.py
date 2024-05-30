class SelectelError(Exception):
    pass


class SelectelAuthError(SelectelError):
    pass


class SelectelRequestError(SelectelError):
    pass


class AuthError(Exception):
    pass


class RequestError(Exception):
    pass
