from datetime import datetime
from pydantic import BaseModel, HttpUrl


class LinkCreate(BaseModel):
    url: HttpUrl


class LinkResponse(BaseModel):
    code: str
    short_url: str


class LinkStats(BaseModel):
    code: str
    original_url: str
    clicks: int
    created_at: datetime
    last_clicked_at: datetime | None