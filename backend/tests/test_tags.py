import pytest
from app.services import tag_service, ticket_service
from app.schemas.ticket import TicketCreate


class TestTagService:
    @pytest.mark.asyncio
    async def test_get_or_create_tag(self, db_session):
        tag = await tag_service.get_or_create_tag(db_session, "NewTag")
        assert tag.name == "newtag"
        tag2 = await tag_service.get_or_create_tag(db_session, "NEWTAG")
        assert tag2.id == tag.id

    @pytest.mark.asyncio
    async def test_get_tags(self, db_session):
        await tag_service.get_or_create_tag(db_session, "tag1")
        await tag_service.get_or_create_tag(db_session, "tag2")
        tags = await tag_service.get_tags(db_session)
        assert len(tags) == 2
        assert any(t.name == "tag1" for t in tags)

    @pytest.mark.asyncio
    async def test_get_tag_by_name(self, db_session):
        await tag_service.get_or_create_tag(db_session, "TestTag")
        tag = await tag_service.get_tag_by_name(db_session, "testtag")
        assert tag is not None
        assert tag.name == "testtag"

    @pytest.mark.asyncio
    async def test_get_tag_by_name_not_found(self, db_session):
        tag = await tag_service.get_tag_by_name(db_session, "nonexistent")
        assert tag is None

    @pytest.mark.asyncio
    async def test_delete_tag(self, db_session):
        await tag_service.get_or_create_tag(db_session, "DeleteMe")
        result = await tag_service.delete_tag(db_session, "deleteme")
        assert result is True
        tag = await tag_service.get_tag_by_name(db_session, "deleteme")
        assert tag is None

    @pytest.mark.asyncio
    async def test_delete_tag_not_found(self, db_session):
        result = await tag_service.delete_tag(db_session, "nonexistent")
        assert result is False

    @pytest.mark.asyncio
    async def test_get_tickets_by_tag(self, db_session):
        await ticket_service.create_ticket(
            db_session, TicketCreate(title="T1", tags=["work"])
        )
        await ticket_service.create_ticket(
            db_session, TicketCreate(title="T2", tags=["work", "urgent"])
        )
        await ticket_service.create_ticket(
            db_session, TicketCreate(title="T3", tags=["personal"])
        )
        tickets, total = await tag_service.get_tickets_by_tag(db_session, "work")
        assert total == 2
        assert len(tickets) == 2

    @pytest.mark.asyncio
    async def test_get_tickets_by_tag_not_found(self, db_session):
        tickets, total = await tag_service.get_tickets_by_tag(db_session, "nonexistent")
        assert total == 0
        assert len(tickets) == 0
