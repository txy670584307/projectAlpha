from typing import Optional, List
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, distinct
from sqlalchemy.orm import selectinload
from app.models.ticket import Ticket
from app.models.tag import Tag, ticket_tags
from app.schemas.ticket import TicketCreate, TicketUpdate, TicketResponse


async def create_ticket(db: AsyncSession, ticket_in: TicketCreate) -> TicketResponse:
    ticket = Ticket(
        title=ticket_in.title,
        description=ticket_in.description,
        status="open"
    )
    if ticket_in.tags:
        tag_names = [tag_name.lower().strip() for tag_name in ticket_in.tags if tag_name.strip()]
        tags = []
        for tag_name in tag_names:
            result = await db.execute(select(Tag).where(Tag.name == tag_name))
            tag = result.scalar_one_or_none()
            if not tag:
                tag = Tag(name=tag_name)
                db.add(tag)
                await db.flush()
            tags.append(tag)
        ticket.tags = tags
    db.add(ticket)
    await db.commit()
    await db.refresh(ticket)
    return TicketResponse.model_validate(ticket)


async def get_ticket(db: AsyncSession, ticket_id: int) -> Optional[TicketResponse]:
    result = await db.execute(
        select(Ticket)
        .options(selectinload(Ticket.tags))
        .where(Ticket.id == ticket_id)
    )
    ticket = result.scalar_one_or_none()
    if ticket:
        return TicketResponse.model_validate(ticket)
    return None


async def get_tickets(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 20,
    tags: Optional[List[str]] = None,
    search: Optional[str] = None,
    status: Optional[str] = None,
    sort: str = "created_at"
) -> tuple[List[TicketResponse], int]:
    query = select(Ticket).options(selectinload(Ticket.tags))
    count_query = select(func.count(distinct(Ticket.id)))
    
    if status:
        query = query.where(Ticket.status == status)
        count_query = count_query.where(Ticket.status == status)
    
    if search:
        search_pattern = f"%{search}%"
        query = query.where(Ticket.title.ilike(search_pattern))
        count_query = count_query.where(Ticket.title.ilike(search_pattern))
    
    if tags:
        tag_names = [tag_name.lower().strip() for tag_name in tags if tag_name.strip()]
        if tag_names:
            tag_subquery = (
                select(Ticket.id)
                .join(ticket_tags, Ticket.id == ticket_tags.c.ticket_id)
                .join(Tag, ticket_tags.c.tag_id == Tag.id)
                .where(Tag.name.in_(tag_names))
                .group_by(Ticket.id)
                .having(func.count(distinct(Tag.name)) == len(tag_names))
            )
            query = query.where(Ticket.id.in_(tag_subquery))
            count_query = count_query.where(Ticket.id.in_(tag_subquery))
    
    sort_column = getattr(Ticket, sort, Ticket.created_at)
    query = query.order_by(sort_column.desc())
    
    count_result = await db.execute(count_query)
    total = count_result.scalar() or 0
    
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    tickets = result.scalars().all()
    
    return [TicketResponse.model_validate(ticket) for ticket in tickets], total


async def update_ticket(
    db: AsyncSession,
    ticket_id: int,
    ticket_in: TicketUpdate
) -> Optional[TicketResponse]:
    result = await db.execute(
        select(Ticket)
        .options(selectinload(Ticket.tags))
        .where(Ticket.id == ticket_id)
    )
    ticket = result.scalar_one_or_none()
    if not ticket:
        return None
    
    update_data = ticket_in.model_dump(exclude_unset=True)
    
    if "tags" in update_data:
        tag_names = [tag_name.lower().strip() for tag_name in update_data["tags"] if tag_name.strip()]
        tags = []
        for tag_name in tag_names:
            tag_result = await db.execute(select(Tag).where(Tag.name == tag_name))
            tag = tag_result.scalar_one_or_none()
            if not tag:
                tag = Tag(name=tag_name)
                db.add(tag)
                await db.flush()
            tags.append(tag)
        ticket.tags = tags
        del update_data["tags"]
    
    for field, value in update_data.items():
        setattr(ticket, field, value)
    
    await db.commit()
    await db.refresh(ticket)
    return TicketResponse.model_validate(ticket)


async def delete_ticket(db: AsyncSession, ticket_id: int) -> bool:
    result = await db.execute(select(Ticket).where(Ticket.id == ticket_id))
    ticket = result.scalar_one_or_none()
    if not ticket:
        return False
    await db.delete(ticket)
    await db.commit()
    return True


async def complete_ticket(db: AsyncSession, ticket_id: int) -> Optional[TicketResponse]:
    result = await db.execute(select(Ticket).where(Ticket.id == ticket_id))
    ticket = result.scalar_one_or_none()
    if not ticket:
        return None
    ticket.status = "closed"
    ticket.completed_at = datetime.now()
    await db.commit()
    await db.refresh(ticket)
    return TicketResponse.model_validate(ticket)


async def uncomplete_ticket(db: AsyncSession, ticket_id: int) -> Optional[TicketResponse]:
    result = await db.execute(select(Ticket).where(Ticket.id == ticket_id))
    ticket = result.scalar_one_or_none()
    if not ticket:
        return None
    ticket.status = "open"
    ticket.completed_at = None
    await db.commit()
    await db.refresh(ticket)
    return TicketResponse.model_validate(ticket)


async def search_tickets(
    db: AsyncSession,
    keyword: str,
    skip: int = 0,
    limit: int = 20
) -> List[TicketResponse]:
    result = await db.execute(
        select(Ticket)
        .options(selectinload(Ticket.tags))
        .where(Ticket.title.ilike(f"%{keyword}%"))
        .order_by(Ticket.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    tickets = result.scalars().all()
    return [TicketResponse.model_validate(ticket) for ticket in tickets]


async def filter_by_tags(
    db: AsyncSession,
    tag_names: List[str],
    skip: int = 0,
    limit: int = 20,
    match_all: bool = False
) -> List[TicketResponse]:
    tag_names = [name.lower().strip() for name in tag_names if name.strip()]
    if not tag_names:
        return []
    
    if match_all:
        subquery = (
            select(Ticket.id)
            .join(ticket_tags, Ticket.id == ticket_tags.c.ticket_id)
            .join(Tag, ticket_tags.c.tag_id == Tag.id)
            .where(Tag.name.in_(tag_names))
            .group_by(Ticket.id)
            .having(func.count(distinct(Tag.name)) == len(tag_names))
        )
    else:
        subquery = (
            select(Ticket.id)
            .join(ticket_tags, Ticket.id == ticket_tags.c.ticket_id)
            .join(Tag, ticket_tags.c.tag_id == Tag.id)
            .where(Tag.name.in_(tag_names))
        )
    
    result = await db.execute(
        select(Ticket)
        .options(selectinload(Ticket.tags))
        .where(Ticket.id.in_(subquery))
        .order_by(Ticket.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    tickets = result.scalars().all()
    return [TicketResponse.model_validate(ticket) for ticket in tickets]
