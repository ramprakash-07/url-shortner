from pydantic import BaseModel

class URLBase(BaseModel):
    Value: str
class URL(URLBase):
    is_active: bool
    click: int