from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.tag import TagResponse
from app.schemas.ticket import TicketResponse
from app.services import tag_service

router = APIRouter()


@router.get("/tags", response_model=List[TagResponse], tags=["tags"])
async def get_tags(db: AsyncSession = Depends(get_db)):
    return await tag_service.get_tags(db)


@router.get("/tags/{name}/tickets", response_model=List[TicketResponse], tags=["tags"])
async def get_tag_tickets(
    name: str,
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(20, ge=1, le=100, description="返回记录数"),
    db: AsyncSession = Depends(get_db)
):
    tickets, total = await tag_service.get_tickets_by_tag(db, name, skip=skip, limit=limit)
    return tickets


@router.delete("/tags/{name}", status_code=204, tags=["tags"])
async def delete_tag(name: str, db: AsyncSession = Depends(get_db)):
    success = await tag_service.delete_tag(db, name)
    if not success:
        raise HTTPException(status_code=404, detail="Tag not found")
