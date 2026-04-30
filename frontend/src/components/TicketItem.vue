<template>
  <div class="ticket-item" :class="{ completed: ticket.status === 'closed' }">
    <div class="ticket-content">
      <div class="ticket-header">
        <button class="checkbox-btn" @click="handleToggle" :aria-label="ticket.status === 'closed' ? '标记为未完成' : '标记为已完成'">
          <svg v-if="ticket.status === 'closed'" class="check-icon" width="18" height="18" viewBox="0 0 18 18" fill="none">
            <circle cx="9" cy="9" r="8" fill="#0071e3"/>
            <path d="M5 9.5L7.5 12L13 6" stroke="white" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <svg v-else class="circle-icon" width="18" height="18" viewBox="0 0 18 18" fill="none">
            <circle cx="9" cy="9" r="8" stroke="currentColor" stroke-width="1.5"/>
          </svg>
        </button>
        <span class="ticket-title">{{ ticket.title }}</span>
      </div>
      <div v-if="ticket.description" class="ticket-desc">
        {{ ticket.description }}
      </div>
    </div>
    <div class="ticket-footer">
      <div class="ticket-tags">
        <span v-for="tag in ticket.tags" :key="tag" class="tag-badge">{{ tag }}</span>
      </div>
      <div class="ticket-meta">
        <span class="ticket-time">{{ formatTime(ticket.created_at) }}</span>
        <div class="ticket-actions">
          <button class="action-btn" @click="$emit('edit', ticket)" aria-label="编辑">
            <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
              <path d="M9.5 2.5L11.5 4.5M10.2353 1.76471L12.2353 3.76471C12.6279 4.15724 12.6279 4.7924 12.2353 5.18493L6.44975 10.9705C6.11408 11.3061 5.67133 11.503 5.20073 11.5266L2.5 11.7273L2.29935 9.02657C2.27577 8.55597 2.47261 8.11322 2.80828 7.77755L8.59384 1.99199C8.98637 1.59946 9.62153 1.59946 10.0141 1.99199L10.2353 1.76471Z" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>
          <button class="action-btn delete-btn" @click="handleDelete" aria-label="删除">
            <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
              <path d="M2 3.5H12M5 3.5V2.5C5 1.94772 5.44772 1.5 6 1.5H8C8.55228 1.5 9 1.94772 9 2.5V3.5M11 3.5V10.5C11 11.0523 10.5523 11.5 10 11.5H4C3.44772 11.5 3 11.0523 3 10.5V3.5H11Z" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  ticket: { type: Object, required: true },
});

const emit = defineEmits(["edit", "delete", "toggle"]);

function handleToggle() {
  if (props.ticket.status === "closed") {
    emit("toggle", props.ticket.id, false);
  } else {
    emit("toggle", props.ticket.id, true);
  }
}

function handleDelete() {
  if (confirm("确定要删除这个 Ticket 吗？")) {
    emit("delete", props.ticket.id);
  }
}

function formatTime(dateStr) {
  const date = new Date(dateStr);
  const now = new Date();
  const diff = now - date;
  const minutes = Math.floor(diff / 60000);
  const hours = Math.floor(diff / 3600000);
  const days = Math.floor(diff / 86400000);

  if (minutes < 1) return "刚刚";
  if (minutes < 60) return `${minutes} 分钟前`;
  if (hours < 24) return `${hours} 小时前`;
  if (days < 7) return `${days} 天前`;

  return date.toLocaleString("zh-CN", {
    month: "2-digit",
    day: "2-digit",
  });
}
</script>

<style scoped>
.ticket-item {
  background-color: var(--bg-elevated);
  border-radius: var(--radius-lg);
  padding: 20px;
  margin-bottom: 12px;
  transition: all var(--transition-base);
  border: 1px solid var(--border-light);
}

.ticket-item:hover {
  box-shadow: var(--shadow-md);
  border-color: var(--border-color);
}

.ticket-item.completed {
  opacity: 0.6;
}

.ticket-header {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  margin-bottom: 8px;
}

.checkbox-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0;
  color: var(--text-tertiary);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  margin-top: 1px;
  transition: all var(--transition-fast);
}

.checkbox-btn:hover {
  color: var(--primary-color);
}

.ticket-title {
  font-size: 16px;
  font-weight: 600;
  letter-spacing: -0.021em;
  line-height: 1.3;
  color: var(--text-primary);
}

.ticket-item.completed .ticket-title {
  text-decoration: line-through;
  color: var(--text-tertiary);
}

.ticket-desc {
  font-size: 14px;
  color: var(--text-secondary);
  margin-bottom: 12px;
  line-height: 1.5;
  margin-left: 30px;
}

.ticket-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid var(--border-light);
}

.ticket-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.ticket-meta {
  display: flex;
  align-items: center;
  gap: 8px;
}

.ticket-time {
  font-size: 12px;
  color: var(--text-tertiary);
  letter-spacing: -0.01em;
}

.ticket-actions {
  display: flex;
  gap: 2px;
  opacity: 0;
  transition: opacity var(--transition-fast);
}

.ticket-item:hover .ticket-actions {
  opacity: 1;
}

.action-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px;
  color: var(--text-tertiary);
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
  transition: all var(--transition-fast);
}

.action-btn:hover {
  background-color: rgba(0, 0, 0, 0.06);
  color: var(--text-primary);
}

.delete-btn:hover {
  color: var(--danger-color);
  background-color: rgba(255, 69, 58, 0.08);
}

@media (max-width: 768px) {
  .ticket-actions {
    opacity: 1;
  }
}
</style>
