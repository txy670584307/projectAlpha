import apiClient from './index';

export function getTags() {
  return apiClient.get('/api/tags');
}

export function getTagTickets(name, params = {}) {
  return apiClient.get(`/api/tags/${name}/tickets`, { params });
}

export function deleteTag(name) {
  return apiClient.delete(`/api/tags/${name}`);
}
