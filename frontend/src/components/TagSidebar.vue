<template>
  <div class="tag-sidebar">
    <h3>标签筛选</h3>
    <div v-if="loading" class="loading-spinner">加载中...</div>
    <div v-else-if="tags.length === 0" class="empty-state">暂无标签</div>
    <ul v-else class="tag-list">
      <li
        v-for="tag in tags"
        :key="tag.name"
        :class="['tag-item', { active: ticketStore.selectedTags.includes(tag.name) }]"
        @click="ticketStore.toggleTag(tag.name)"
      >
        <span class="tag-name">{{ tag.name }}</span>
        <span class="tag-count">{{ tag.ticket_count || 0 }}</span>
      </li>
    </ul>
    <button v-if="ticketStore.selectedTags.length > 0" class="btn btn-text btn-sm" @click="ticketStore.clearFilters">
      清除筛选
    </button>
  </div>
</template>

<script setup>
import { onMounted, computed } from 'vue';
import { useTagStore } from '@/stores/tag';
import { useTicketStore } from '@/stores/ticket';

const tagStore = useTagStore();
const ticketStore = useTicketStore();

const tags = computed(() => tagStore.tagsWithCount);
const loading = computed(() => tagStore.loading);

onMounted(async () => {
  await tagStore.fetchTags();
});
</script>

<style scoped>
.tag-sidebar h3 {
  font-size: 16px;
  margin-bottom: 12px;
  color: var(--text-color);
}

.tag-list {
  list-style: none;
}

.tag-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  border-radius: var(--radius);
  cursor: pointer;
  transition: var(--transition);
  margin-bottom: 4px;
}

.tag-item:hover {
  background-color: rgba(0, 0, 0, 0.05);
}

.tag-item.active {
  background-color: #e8f0fe;
  color: var(--primary-color);
}

.tag-name {
  font-size: 14px;
}

.tag-count {
  font-size: 12px;
  background-color: var(--border-color);
  padding: 2px 8px;
  border-radius: 10px;
  color: var(--text-light);
}

.tag-item.active .tag-count {
  background-color: var(--primary-color);
  color: var(--white);
}
</style>
