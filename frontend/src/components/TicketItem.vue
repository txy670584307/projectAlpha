<template>
  <div class="ticket-item" :class="{ completed: ticket.status === 'closed' }">
    <div class="ticket-header">
      <input type="checkbox" :checked="ticket.status === 'closed'" @change="handleToggle" />
      <span class="ticket-title">{{ ticket.title }}</span>
    </div>
    <div v-if="ticket.description" class="ticket-desc">{{ ticket.description }}</div>
    <div class="ticket-tags">
      <span v-for="tag in ticket.tags" :key="tag" class="tag-badge">{{ tag }}</span>
    </div>
    <div class="ticket-meta">
      <span class="ticket-time">{{ formatTime(ticket.created_at) }}</span>
    </div>
    <div class="ticket-actions">
      <button class="btn btn-text btn-sm" @click="$emit('edit', ticket)">编辑</button>
      <button class="btn btn-text btn-sm" style="color: var(--danger-color)" @click="handleDelete">删除</button>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  ticket: { type: Object, required: true },
});

const emit = defineEmits(['edit', 'delete', 'toggle']);

function handleToggle() {
  if (props.ticket.status === 'closed') {
    emit('toggle', props.ticket.id, false);
  } else {
    emit('toggle', props.ticket.id, true);
  }
}

function handleDelete() {
  if (confirm('确定要删除这个 Ticket 吗？')) {
    emit('delete', props.ticket.id);
  }
}

function formatTime(dateStr) {
  const date = new Date(dateStr);
  return date.toLocaleString('zh-CN', {
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  });
}
</script>

<style scoped>
.ticket-item {
  background-color: var(--white);
  border-radius: var(--radius);
  padding: 16px;
  margin-bottom: 12px;
  box-shadow: var(--shadow);
  transition: var(--transition);
}

.ticket-item:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.12);
}

.ticket-item.completed {
  opacity: 0.7;
}

.ticket-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 8px;
}

.ticket-header input[type='checkbox'] {
  width: 18px;
  height: 18px;
  cursor: pointer;
}

.ticket-title {
  font-size: 16px;
  font-weight: 500;
}

.ticket-item.completed .ticket-title {
  text-decoration: line-through;
  color: var(--text-light);
}

.ticket-desc {
  font-size: 14px;
  color: var(--text-light);
  margin-bottom: 10px;
  line-height: 1.5;
}

.ticket-tags {
  display: flex;
  flex-wrap: wrap;
  margin-bottom: 8px;
}

.ticket-meta {
  font-size: 12px;
  color: var(--text-light);
}

.ticket-actions {
  display: flex;
  gap: 8px;
  margin-top: 10px;
  padding-top: 10px;
  border-top: 1px solid var(--border-color);
}
</style>
