<template>
  <div class="tag-sidebar">
    <h3 class="sidebar-title">标签</h3>
    <div v-if="loading" class="loading-spinner">加载中...</div>
    <div v-else-if="tags.length === 0" class="empty-tags">
      <span>暂无标签</span>
    </div>
    <ul v-else class="tag-list">
      <li
        v-for="tag in tags"
        :key="tag.name"
        :class="[
          'tag-item',
          { active: ticketStore.selectedTags.includes(tag.name) },
        ]"
        @click="ticketStore.toggleTag(tag.name)"
      >
        <span class="tag-name">{{ tag.name }}</span>
        <span class="tag-count">{{ tag.count || 0 }}</span>
      </li>
    </ul>
    <button
      v-if="ticketStore.selectedTags.length > 0"
      class="btn-clear"
      @click="ticketStore.clearFilters"
    >
      清除筛选
    </button>
  </div>
</template>

<script setup>
import { onMounted, computed, watch } from "vue";
import { useTagStore } from "@/stores/tag";
import { useTicketStore } from "@/stores/ticket";

const tagStore = useTagStore();
const ticketStore = useTicketStore();

const tags = computed(() => tagStore.tagsWithCount);
const loading = computed(() => tagStore.loading);

onMounted(async () => {
  await tagStore.fetchTags();
});

watch(
  () => ticketStore.total,
  async () => {
    await tagStore.fetchTags();
  }
);
</script>

<style scoped>
.sidebar-title {
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-tertiary);
  margin-bottom: 12px;
}

.tag-list {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.tag-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 10px;
  border-radius: 8px;
  cursor: pointer;
  transition: all var(--transition-fast);
}

.tag-item:hover {
  background-color: rgba(0, 0, 0, 0.04);
}

.tag-item.active {
  background-color: var(--primary-color);
  color: #ffffff;
}

.tag-item.active .tag-count {
  background-color: rgba(255, 255, 255, 0.25);
  color: #ffffff;
}

.tag-name {
  font-size: 14px;
  font-weight: 400;
  letter-spacing: -0.01em;
}

.tag-count {
  font-size: 11px;
  font-weight: 500;
  background-color: rgba(0, 0, 0, 0.06);
  padding: 2px 7px;
  border-radius: 980px;
  color: var(--text-tertiary);
  min-width: 20px;
  text-align: center;
  transition: all var(--transition-fast);
}

.btn-clear {
  margin-top: 12px;
  background: none;
  border: none;
  color: var(--primary-color);
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  padding: 8px 12px;
  border-radius: 8px;
  transition: all var(--transition-fast);
  font-family: var(--font-sans);
  letter-spacing: -0.01em;
}

.btn-clear:hover {
  background-color: rgba(0, 113, 227, 0.08);
}

.empty-tags {
  font-size: 13px;
  color: var(--text-tertiary);
  padding: 8px 0;
}
</style>
