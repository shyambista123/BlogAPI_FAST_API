# Custom exception handling
from fastapi import HTTPException

class NotFoundException(HTTPException):
    def __init__(self, detail="Resource not found"):
        super().__init__(status_code=404, detail=detail)
