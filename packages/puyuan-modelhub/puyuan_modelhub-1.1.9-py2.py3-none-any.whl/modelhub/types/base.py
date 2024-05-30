from modelhub.utils import BaseModel as PydanticBaseModel
from fastapi.responses import JSONResponse

class BaseModel(PydanticBaseModel):
    def to_event(self, prefix="data: ") -> str:
        return f"{prefix}{self.json()}\r\n\r\n"

    class Config:
        arbitrary_types_allowed = True


class BaseOutput(BaseModel):
    success: bool = True
    code: int = 200
    msg: str = "success"

    def to_response(self):
        return JSONResponse(self.dict(), status_code=self.code)

    class Config:
        extra = "allow"
