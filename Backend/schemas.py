from pydantic import BaseModel

class URLBase(BaseModel):
    Key: str | None = None
    Value: str
class URL(URLBase):
    is_active: bool
    click: int