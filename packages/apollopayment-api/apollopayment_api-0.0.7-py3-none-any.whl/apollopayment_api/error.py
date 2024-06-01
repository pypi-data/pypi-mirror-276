class apollopayment_sdkError(Exception):
    def __init__(
            self,
            message: str,
    ):
        super(apollopayment_sdkError, self).__init__(message)


class AuthenticationError(apollopayment_sdkError):
    def __init__(self, message: str):
        super(AuthenticationError, self).__init__(message)


class InternalSDKError(apollopayment_sdkError):
    def __init__(self, message: str):
        super(InternalSDKError, self).__init__(message)
