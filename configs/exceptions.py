from fastapi import HTTPException


class BadRequest(HTTPException):
    def __init__(self, detail: str = "Invalid request") -> None:
        self.status_code = 400
        super().__init__(status_code=self.status_code, detail=detail)


class NotFound(HTTPException):
    def __init__(self, detail: str = "ID not found") -> None:
        self.status_code = 404
        super().__init__(status_code=self.status_code, detail=detail)


class Forbidden(HTTPException):
    def __init__(self, detail: str = "Invalid credentials") -> None:
        self.status_code = 401
        self.headers = {"WWW-Authenticate": "Bearer"}
        super().__init__(
            status_code=self.status_code, detail=detail, headers=self.headers
        )
