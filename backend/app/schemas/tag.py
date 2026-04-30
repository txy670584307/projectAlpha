from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class TagBase(BaseModel):
    name: str = Field(..., max_length=50, description="标签名称")


class TagCreate(TagBase):
    pass


class TagResponse(TagBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    ticket_count: Optional[int] = Field(0, description="关联的 Ticket 数量")
