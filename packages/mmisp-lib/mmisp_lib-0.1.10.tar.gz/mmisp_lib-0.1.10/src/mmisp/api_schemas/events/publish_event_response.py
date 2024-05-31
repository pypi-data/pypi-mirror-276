from pydantic import BaseModel


class PublishEventResponse(BaseModel):
    saved: bool | None = None
    success: bool | None = None
    name: str
    message: str
    url: str
    id: str | None = None

    class Config:
        orm_mode = True
