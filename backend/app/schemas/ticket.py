from typing import Optional, List, Any
from datetime import datetime
from pydantic import BaseModel, Field, field_validator, ConfigDict


class TicketBase(BaseModel):
    title: str = Field(..., max_length=200, description="Ticket 标题")
    description: Optional[str] = Field(None, description="Ticket 描述")
    tags: Optional[List[str]] = Field(default=[], description="标签列表")


class TicketCreate(TicketBase):
    pass


class TicketUpdate(TicketBase):
    title: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = None
    tags: Optional[List[str]] = []


class TicketResponse(TicketBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    status: str
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None

    @field_validator("tags", mode="before")
    @classmethod
    def convert_tags(cls, v: Any) -> List[str]:
        if v is None:
            return []
        if isinstance(v, list):
            return [
                tag if isinstance(tag, str) else getattr(tag, "name", str(tag))
                for tag in v
            ]
        return []


class TicketListResponse(BaseModel):
    items: List[TicketResponse]
    total: int
