from pydantic import BaseModel, HttpUrl

class URLBase(BaseModel):
    Key: str | None = None
    Value: HttpUrl
class URL(URLBase):
    is_active: bool
    click: int