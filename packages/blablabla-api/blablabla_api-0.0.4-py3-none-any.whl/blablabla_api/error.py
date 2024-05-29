class blablabla_sdkError(Exception):
    def __init__(
            self,
            message: str,
    ):
        super(blablabla_sdkError, self).__init__(message)


class AuthenticationError(blablabla_sdkError):
    def __init__(self, message: str):
        super(AuthenticationError, self).__init__(message)


class InternalSDKError(blablabla_sdkError):
    def __init__(self, message: str):
        super(InternalSDKError, self).__init__(message)
