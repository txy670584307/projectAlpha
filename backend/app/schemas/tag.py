from pydantic import BaseModel, Field
from typing import Optional


class TagBase(BaseModel):
    name: str = Field(..., max_length=50, description="标签名称")


class TagCreate(TagBase):
    pass


class TagResponse(TagBase):
    id: int
    ticket_count: Optional[int] = Field(0, description="关联的 Ticket 数量")

    class Config:
        from_attributes = True
