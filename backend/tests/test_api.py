import pytest


class TestTicketAPI:
    @pytest.mark.asyncio
    async def test_create_ticket(self, async_client, sample_ticket_data):
        response = await async_client.post("/api/tickets", json=sample_ticket_data)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == sample_ticket_data["title"]
        assert data["status"] == "open"

    @pytest.mark.asyncio
    async def test_get_tickets_empty(self, async_client):
        response = await async_client.get("/api/tickets")
        assert response.status_code == 200
        data = response.json()
        assert data["items"] == []
        assert data["total"] == 0

    @pytest.mark.asyncio
    async def test_get_ticket_not_found(self, async_client):
        response = await async_client.get("/api/tickets/99999")
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_create_and_get_ticket(self, async_client, sample_ticket_data):
        create_resp = await async_client.post("/api/tickets", json=sample_ticket_data)
        assert create_resp.status_code == 201
        ticket_id = create_resp.json()["id"]

        get_resp = await async_client.get(f"/api/tickets/{ticket_id}")
        assert get_resp.status_code == 200
        assert get_resp.json()["title"] == sample_ticket_data["title"]

    @pytest.mark.asyncio
    async def test_update_ticket(self, async_client, sample_ticket_data):
        create_resp = await async_client.post("/api/tickets", json=sample_ticket_data)
        ticket_id = create_resp.json()["id"]

        update_data = {"title": "Updated", "description": "New desc", "tags": ["updated"]}
        update_resp = await async_client.put(f"/api/tickets/{ticket_id}", json=update_data)
        assert update_resp.status_code == 200
        assert update_resp.json()["title"] == "Updated"

    @pytest.mark.asyncio
    async def test_update_ticket_not_found(self, async_client):
        response = await async_client.put("/api/tickets/99999", json={"title": "Nope"})
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_delete_ticket(self, async_client, sample_ticket_data):
        create_resp = await async_client.post("/api/tickets", json=sample_ticket_data)
        ticket_id = create_resp.json()["id"]

        delete_resp = await async_client.delete(f"/api/tickets/{ticket_id}")
        assert delete_resp.status_code == 204

        get_resp = await async_client.get(f"/api/tickets/{ticket_id}")
        assert get_resp.status_code == 404

    @pytest.mark.asyncio
    async def test_complete_ticket(self, async_client, sample_ticket_data):
        create_resp = await async_client.post("/api/tickets", json=sample_ticket_data)
        ticket_id = create_resp.json()["id"]

        complete_resp = await async_client.patch(f"/api/tickets/{ticket_id}/complete")
        assert complete_resp.status_code == 200
        assert complete_resp.json()["status"] == "closed"
        assert complete_resp.json()["completed_at"] is not None

    @pytest.mark.asyncio
    async def test_uncomplete_ticket(self, async_client, sample_ticket_data):
        create_resp = await async_client.post("/api/tickets", json=sample_ticket_data)
        ticket_id = create_resp.json()["id"]

        await async_client.patch(f"/api/tickets/{ticket_id}/complete")
        uncomplete_resp = await async_client.patch(f"/api/tickets/{ticket_id}/uncomplete")
        assert uncomplete_resp.status_code == 200
        assert uncomplete_resp.json()["status"] == "open"
        assert uncomplete_resp.json()["completed_at"] is None

    @pytest.mark.asyncio
    async def test_get_tickets_with_search(self, async_client):
        await async_client.post("/api/tickets", json={"title": "Python Bug"})
        await async_client.post("/api/tickets", json={"title": "JavaScript Issue"})

        response = await async_client.get("/api/tickets?search=Python")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert "Python" in data["items"][0]["title"]

    @pytest.mark.asyncio
    async def test_get_tickets_with_tags_filter(self, async_client):
        await async_client.post("/api/tickets", json={"title": "T1", "tags": ["work"]})
        await async_client.post("/api/tickets", json={"title": "T2", "tags": ["personal"]})

        response = await async_client.get("/api/tickets?tags=work")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1


class TestTagAPI:
    @pytest.mark.asyncio
    async def test_get_tags_empty(self, async_client):
        response = await async_client.get("/api/tags")
        assert response.status_code == 200
        assert response.json() == []

    @pytest.mark.asyncio
    async def test_get_tags_with_data(self, async_client, sample_ticket_data):
        await async_client.post("/api/tickets", json=sample_ticket_data)

        response = await async_client.get("/api/tags")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert any(t["name"] == "work" for t in data)
        assert any(t["name"] == "urgent" for t in data)

    @pytest.mark.asyncio
    async def test_get_tag_tickets(self, async_client):
        await async_client.post("/api/tickets", json={"title": "T1", "tags": ["work"]})
        await async_client.post("/api/tickets", json={"title": "T2", "tags": ["work", "urgent"]})

        response = await async_client.get("/api/tags/work/tickets")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

    @pytest.mark.asyncio
    async def test_delete_tag(self, async_client, sample_ticket_data):
        await async_client.post("/api/tickets", json=sample_ticket_data)

        delete_resp = await async_client.delete("/api/tags/work")
        assert delete_resp.status_code == 204

        tags_resp = await async_client.get("/api/tags")
        tag_names = [t["name"] for t in tags_resp.json()]
        assert "work" not in tag_names

    @pytest.mark.asyncio
    async def test_delete_tag_not_found(self, async_client):
        response = await async_client.delete("/api/tags/nonexistent")
        assert response.status_code == 404


class TestHealthAndRoot:
    @pytest.mark.asyncio
    async def test_health_check(self, async_client):
        response = await async_client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"

    @pytest.mark.asyncio
    async def test_root(self, async_client):
        response = await async_client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "projectAlpha" in data["message"]
