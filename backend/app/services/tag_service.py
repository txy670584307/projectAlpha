from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from app.models.tag import Tag, ticket_tags
from app.models.ticket import Ticket
from app.schemas.tag import TagResponse


async def get_or_create_tag(db: AsyncSession, name: str) -> Tag:
    name = name.lower().strip()
    result = await db.execute(select(Tag).where(Tag.name == name))
    tag = result.scalar_one_or_none()
    if not tag:
        tag = Tag(name=name)
        db.add(tag)
        await db.commit()
        await db.refresh(tag)
    return tag


async def get_tags(db: AsyncSession) -> List[TagResponse]:
    result = await db.execute(
        select(Tag, func.count(ticket_tags.c.ticket_id).label("ticket_count"))
        .outerjoin(ticket_tags, Tag.id == ticket_tags.c.tag_id)
        .group_by(Tag.id)
        .order_by(Tag.name)
    )
    rows = result.all()
    tag_responses = []
    for tag, ticket_count in rows:
        tag_dict = {"id": tag.id, "name": tag.name, "ticket_count": ticket_count}
        tag_responses.append(TagResponse(**tag_dict))
    return tag_responses


async def get_tag_by_name(db: AsyncSession, name: str) -> Optional[Tag]:
    name = name.lower().strip()
    result = await db.execute(select(Tag).where(Tag.name == name))
    return result.scalar_one_or_none()


async def delete_tag(db: AsyncSession, name: str) -> bool:
    name = name.lower().strip()
    result = await db.execute(select(Tag).where(Tag.name == name))
    tag = result.scalar_one_or_none()
    if not tag:
        return False
    await db.delete(tag)
    await db.commit()
    return True


async def get_tickets_by_tag(
    db: AsyncSession, tag_name: str, skip: int = 0, limit: int = 20
) -> tuple[List[Ticket], int]:
    tag_name = tag_name.lower().strip()

    count_result = await db.execute(
        select(func.count(Ticket.id))
        .join(ticket_tags, Ticket.id == ticket_tags.c.ticket_id)
        .join(Tag, ticket_tags.c.tag_id == Tag.id)
        .where(Tag.name == tag_name)
    )
    total = count_result.scalar() or 0

    result = await db.execute(
        select(Ticket)
        .options(selectinload(Ticket.tags))
        .join(ticket_tags, Ticket.id == ticket_tags.c.ticket_id)
        .join(Tag, ticket_tags.c.tag_id == Tag.id)
        .where(Tag.name == tag_name)
        .order_by(Ticket.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    tickets = result.scalars().all()

    return tickets, total
