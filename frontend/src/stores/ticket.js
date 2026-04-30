import { defineStore } from 'pinia';
import { getTickets, createTicket, updateTicket, deleteTicket, completeTicket, uncompleteTicket } from '@/api/tickets';

export const useTicketStore = defineStore('ticket', {
  state: () => ({
    tickets: [],
    total: 0,
    loading: false,
    error: null,
    selectedTags: [],
    searchKeyword: '',
    statusFilter: '',
    sort: 'created_at',
    page: 1,
    pageSize: 20,
  }),

  getters: {
    filteredTickets: (state) => state.tickets,
    hasTickets: (state) => state.tickets.length > 0,
    isEmpty: (state) => !state.loading && state.tickets.length === 0,
  },

  actions: {
    async fetchTickets() {
      this.loading = true;
      this.error = null;
      try {
        const params = {
          skip: (this.page - 1) * this.pageSize,
          limit: this.pageSize,
          sort: this.sort,
        };
        if (this.searchKeyword) params.search = this.searchKeyword;
        if (this.statusFilter) params.status = this.statusFilter;
        if (this.selectedTags.length > 0) params.tags = this.selectedTags;

        const response = await getTickets(params);
        this.tickets = response.data.items;
        this.total = response.data.total;
      } catch (err) {
        this.error = err.message;
      } finally {
        this.loading = false;
      }
    },

    async createTicket(data) {
      try {
        await createTicket(data);
        await this.fetchTickets();
      } catch (err) {
        this.error = err.message;
        throw err;
      }
    },

    async updateTicket(id, data) {
      try {
        await updateTicket(id, data);
        await this.fetchTickets();
      } catch (err) {
        this.error = err.message;
        throw err;
      }
    },

    async deleteTicket(id) {
      try {
        await deleteTicket(id);
        await this.fetchTickets();
      } catch (err) {
        this.error = err.message;
        throw err;
      }
    },

    async completeTicket(id) {
      try {
        await completeTicket(id);
        await this.fetchTickets();
      } catch (err) {
        this.error = err.message;
        throw err;
      }
    },

    async uncompleteTicket(id) {
      try {
        await uncompleteTicket(id);
        await this.fetchTickets();
      } catch (err) {
        this.error = err.message;
        throw err;
      }
    },

    setSearchKeyword(keyword) {
      this.searchKeyword = keyword;
      this.page = 1;
      this.fetchTickets();
    },

    setStatusFilter(status) {
      this.statusFilter = status;
      this.page = 1;
      this.fetchTickets();
    },

    toggleTag(tag) {
      const index = this.selectedTags.indexOf(tag);
      if (index === -1) {
        this.selectedTags.push(tag);
      } else {
        this.selectedTags.splice(index, 1);
      }
      this.page = 1;
      this.fetchTickets();
    },

    clearFilters() {
      this.selectedTags = [];
      this.searchKeyword = '';
      this.statusFilter = '';
      this.page = 1;
      this.fetchTickets();
    },

    setPage(page) {
      this.page = page;
      this.fetchTickets();
    },
  },
});
