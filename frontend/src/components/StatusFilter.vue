<template>
  <div class="status-filter">
    <button
      v-for="option in options"
      :key="option.value"
      :class="[
        'status-btn',
        { active: ticketStore.statusFilter === option.value },
      ]"
      @click="ticketStore.setStatusFilter(option.value)"
    >
      {{ option.label }}
    </button>
  </div>
</template>

<script setup>
import { useTicketStore } from "@/stores/ticket";

const ticketStore = useTicketStore();

const options = [
  { label: "全部", value: "" },
  { label: "未完成", value: "open" },
  { label: "已完成", value: "closed" },
];
</script>

<style scoped>
.status-filter {
  display: flex;
  gap: 8px;
  margin-bottom: 16px;
}

.status-btn {
  padding: 8px 16px;
  border: 1px solid var(--border-color);
  border-radius: 20px;
  background-color: var(--white);
  color: var(--text-light);
  cursor: pointer;
  transition: var(--transition);
  font-size: 14px;
}

.status-btn:hover {
  border-color: var(--primary-color);
  color: var(--primary-color);
}

.status-btn.active {
  background-color: var(--primary-color);
  border-color: var(--primary-color);
  color: var(--white);
}
</style>
