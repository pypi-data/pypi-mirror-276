class APIResponse:
    def __init__(self, success: bool, code: int, response: any, error: any):
        self.success = success
        self.code = code
        self.response = response
        self.error = error


def SuccessResponse(response: any):
    return {
        "success": True,
        "response": response,
    }


def FailResponse(code: int, error: any, requestId: str = None):
    return {
        "success": False,
        "error": {
            "message": error,
            "code": code,
        },
        "requestId": requestId,
    }
