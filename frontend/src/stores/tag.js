import { defineStore } from 'pinia';
import { getTags, deleteTag } from '@/api/tags';

export const useTagStore = defineStore('tag', {
  state: () => ({
    tags: [],
    loading: false,
    error: null,
  }),

  getters: {
    tagNames: (state) => state.tags.map((t) => t.name),
    tagsWithCount: (state) =>
      state.tags.map((t) => ({
        name: t.name,
        count: t.ticket_count || 0,
      })),
  },

  actions: {
    async fetchTags() {
      this.loading = true;
      this.error = null;
      try {
        const response = await getTags();
        this.tags = response.data;
      } catch (err) {
        this.error = err.message;
      } finally {
        this.loading = false;
      }
    },

    async removeTag(name) {
      try {
        await deleteTag(name);
        this.tags = this.tags.filter((t) => t.name !== name);
      } catch (err) {
        this.error = err.message;
        throw err;
      }
    },
  },
});
