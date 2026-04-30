import pytest
from app.services import ticket_service
from app.schemas.ticket import TicketCreate, TicketUpdate


class TestTicketService:
    @pytest.mark.asyncio
    async def test_create_ticket(self, db_session, sample_ticket_data):
        ticket_in = TicketCreate(**sample_ticket_data)
        result = await ticket_service.create_ticket(db_session, ticket_in)
        assert result.title == "Test Ticket"
        assert result.description == "Test Description"
        assert result.status == "open"
        assert len(result.tags) == 2

    @pytest.mark.asyncio
    async def test_create_ticket_without_tags(self, db_session):
        ticket_in = TicketCreate(title="No Tags Ticket")
        result = await ticket_service.create_ticket(db_session, ticket_in)
        assert result.title == "No Tags Ticket"
        assert result.tags == []

    @pytest.mark.asyncio
    async def test_get_ticket(self, db_session, sample_ticket_data):
        ticket_in = TicketCreate(**sample_ticket_data)
        created = await ticket_service.create_ticket(db_session, ticket_in)
        result = await ticket_service.get_ticket(db_session, created.id)
        assert result is not None
        assert result.title == "Test Ticket"

    @pytest.mark.asyncio
    async def test_get_ticket_not_found(self, db_session):
        result = await ticket_service.get_ticket(db_session, 99999)
        assert result is None

    @pytest.mark.asyncio
    async def test_get_tickets_with_pagination(self, db_session):
        for i in range(5):
            ticket_in = TicketCreate(title=f"Ticket {i}")
            await ticket_service.create_ticket(db_session, ticket_in)
        results, total = await ticket_service.get_tickets(db_session, skip=2, limit=2)
        assert len(results) == 2
        assert total == 5

    @pytest.mark.asyncio
    async def test_get_tickets_filter_by_status(self, db_session):
        ticket_open = TicketCreate(title="Open Ticket")
        await ticket_service.create_ticket(db_session, ticket_open)
        ticket_closed_in = TicketCreate(title="Closed Ticket")
        closed = await ticket_service.create_ticket(db_session, ticket_closed_in)
        await ticket_service.complete_ticket(db_session, closed.id)
        results, total = await ticket_service.get_tickets(db_session, status="open")
        assert total >= 1
        for r in results:
            assert r.status == "open"

    @pytest.mark.asyncio
    async def test_update_ticket(self, db_session, sample_ticket_data):
        ticket_in = TicketCreate(**sample_ticket_data)
        created = await ticket_service.create_ticket(db_session, ticket_in)
        update_data = TicketUpdate(title="Updated Title", description="Updated Desc")
        result = await ticket_service.update_ticket(db_session, created.id, update_data)
        assert result is not None
        assert result.title == "Updated Title"
        assert result.description == "Updated Desc"

    @pytest.mark.asyncio
    async def test_update_ticket_not_found(self, db_session):
        update_data = TicketUpdate(title="Updated")
        result = await ticket_service.update_ticket(db_session, 99999, update_data)
        assert result is None

    @pytest.mark.asyncio
    async def test_delete_ticket(self, db_session, sample_ticket_data):
        ticket_in = TicketCreate(**sample_ticket_data)
        created = await ticket_service.create_ticket(db_session, ticket_in)
        result = await ticket_service.delete_ticket(db_session, created.id)
        assert result is True
        deleted = await ticket_service.get_ticket(db_session, created.id)
        assert deleted is None

    @pytest.mark.asyncio
    async def test_delete_ticket_not_found(self, db_session):
        result = await ticket_service.delete_ticket(db_session, 99999)
        assert result is False

    @pytest.mark.asyncio
    async def test_complete_ticket(self, db_session, sample_ticket_data):
        ticket_in = TicketCreate(**sample_ticket_data)
        created = await ticket_service.create_ticket(db_session, ticket_in)
        result = await ticket_service.complete_ticket(db_session, created.id)
        assert result is not None
        assert result.status == "closed"
        assert result.completed_at is not None

    @pytest.mark.asyncio
    async def test_complete_ticket_not_found(self, db_session):
        result = await ticket_service.complete_ticket(db_session, 99999)
        assert result is None

    @pytest.mark.asyncio
    async def test_uncomplete_ticket(self, db_session, sample_ticket_data):
        ticket_in = TicketCreate(**sample_ticket_data)
        created = await ticket_service.create_ticket(db_session, ticket_in)
        await ticket_service.complete_ticket(db_session, created.id)
        result = await ticket_service.uncomplete_ticket(db_session, created.id)
        assert result is not None
        assert result.status == "open"
        assert result.completed_at is None

    @pytest.mark.asyncio
    async def test_search_tickets(self, db_session):
        await ticket_service.create_ticket(db_session, TicketCreate(title="Python Bug"))
        await ticket_service.create_ticket(
            db_session, TicketCreate(title="JavaScript Issue")
        )
        results = await ticket_service.search_tickets(db_session, "Python")
        assert len(results) == 1
        assert "Python" in results[0].title

    @pytest.mark.asyncio
    async def test_filter_by_tags(self, db_session):
        await ticket_service.create_ticket(
            db_session, TicketCreate(title="T1", tags=["work"])
        )
        await ticket_service.create_ticket(
            db_session, TicketCreate(title="T2", tags=["personal"])
        )
        await ticket_service.create_ticket(
            db_session, TicketCreate(title="T3", tags=["work", "urgent"])
        )
        results = await ticket_service.filter_by_tags(db_session, ["work"])
        assert len(results) == 2
