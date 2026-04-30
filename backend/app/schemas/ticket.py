from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field


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
    id: int
    status: str
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class TicketListResponse(BaseModel):
    items: List[TicketResponse]
    total: int
