import apiClient from "./index";

export function getTickets(params = {}) {
  return apiClient.get("/api/tickets", { params });
}

export function getTicket(id) {
  return apiClient.get(`/api/tickets/${id}`);
}

export function createTicket(data) {
  return apiClient.post("/api/tickets", data);
}

export function updateTicket(id, data) {
  return apiClient.put(`/api/tickets/${id}`, data);
}

export function deleteTicket(id) {
  return apiClient.delete(`/api/tickets/${id}`);
}

export function completeTicket(id) {
  return apiClient.patch(`/api/tickets/${id}/complete`);
}

export function uncompleteTicket(id) {
  return apiClient.patch(`/api/tickets/${id}/uncomplete`);
}
