from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.ticket import TicketCreate, TicketUpdate, TicketResponse, TicketListResponse
from app.services import ticket_service

router = APIRouter()


@router.get("/tickets", response_model=TicketListResponse, tags=["tickets"])
async def get_tickets(
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(20, ge=1, le=100, description="返回记录数"),
    tags: Optional[List[str]] = Query(None, description="标签筛选"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    status: Optional[str] = Query(None, description="状态筛选"),
    sort: str = Query("created_at", description="排序字段"),
    db: AsyncSession = Depends(get_db)
):
    tickets, total = await ticket_service.get_tickets(
        db, skip=skip, limit=limit, tags=tags, search=search, status=status, sort=sort
    )
    return TicketListResponse(items=tickets, total=total)


@router.get("/tickets/{ticket_id}", response_model=TicketResponse, tags=["tickets"])
async def get_ticket(ticket_id: int, db: AsyncSession = Depends(get_db)):
    ticket = await ticket_service.get_ticket(db, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket


@router.post("/tickets", response_model=TicketResponse, status_code=201, tags=["tickets"])
async def create_ticket(ticket_in: TicketCreate, db: AsyncSession = Depends(get_db)):
    return await ticket_service.create_ticket(db, ticket_in)


@router.put("/tickets/{ticket_id}", response_model=TicketResponse, tags=["tickets"])
async def update_ticket(
    ticket_id: int,
    ticket_in: TicketUpdate,
    db: AsyncSession = Depends(get_db)
):
    ticket = await ticket_service.update_ticket(db, ticket_id, ticket_in)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket


@router.delete("/tickets/{ticket_id}", status_code=204, tags=["tickets"])
async def delete_ticket(ticket_id: int, db: AsyncSession = Depends(get_db)):
    success = await ticket_service.delete_ticket(db, ticket_id)
    if not success:
        raise HTTPException(status_code=404, detail="Ticket not found")


@router.patch("/tickets/{ticket_id}/complete", response_model=TicketResponse, tags=["tickets"])
async def complete_ticket(ticket_id: int, db: AsyncSession = Depends(get_db)):
    ticket = await ticket_service.complete_ticket(db, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket


@router.patch("/tickets/{ticket_id}/uncomplete", response_model=TicketResponse, tags=["tickets"])
async def uncomplete_ticket(ticket_id: int, db: AsyncSession = Depends(get_db)):
    ticket = await ticket_service.uncomplete_ticket(db, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket
