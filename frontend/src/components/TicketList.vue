<template>
  <div class="ticket-list">
    <div v-if="loading" class="loading-spinner">
      <div class="spinner"></div>
      <span>加载中...</span>
    </div>
    <div v-else-if="isEmpty" class="empty-state">
      <svg class="empty-icon" width="48" height="48" viewBox="0 0 48 48" fill="none">
        <rect x="8" y="4" width="32" height="40" rx="4" stroke="currentColor" stroke-width="2" fill="none"/>
        <line x1="16" y1="14" x2="32" y2="14" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
        <line x1="16" y1="22" x2="28" y2="22" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
        <line x1="16" y1="30" x2="24" y2="30" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
      </svg>
      <p>暂无 Ticket</p>
      <p>创建你的第一个任务</p>
    </div>
    <TransitionGroup v-else name="ticket-list" tag="div">
      <TicketItem
        v-for="ticket in tickets"
        :key="ticket.id"
        :ticket="ticket"
        @edit="$emit('edit', $event)"
        @delete="$emit('delete', $event)"
        @toggle="handleToggle"
      />
    </TransitionGroup>
  </div>
</template>

<script setup>
import { computed } from "vue";
import { useTicketStore } from "@/stores/ticket";
import TicketItem from "./TicketItem.vue";

const ticketStore = useTicketStore();
const tickets = computed(() => ticketStore.tickets);
const loading = computed(() => ticketStore.loading);
const isEmpty = computed(() => ticketStore.isEmpty);

const emit = defineEmits(["edit", "delete"]);

function handleToggle(id, toComplete) {
  if (toComplete) {
    ticketStore.completeTicket(id);
  } else {
    ticketStore.uncompleteTicket(id);
  }
}
</script>

<style scoped>
.loading-spinner {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  padding: 80px;
}

.spinner {
  width: 24px;
  height: 24px;
  border: 2px solid var(--border-color);
  border-top-color: var(--primary-color);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 80px 24px;
}

.empty-icon {
  color: var(--border-color);
  margin-bottom: 16px;
}

.ticket-list-enter-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.ticket-list-leave-active {
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.ticket-list-enter-from {
  opacity: 0;
  transform: translateY(10px);
}

.ticket-list-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

.ticket-list-move {
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
</style>
