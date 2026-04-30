<template>
  <div class="ticket-list">
    <div v-if="loading" class="loading-spinner">加载中...</div>
    <div v-else-if="isEmpty" class="empty-state">
      <p>暂无 Ticket</p>
      <p>点击下方"新建"按钮创建第一个 Ticket</p>
    </div>
    <template v-else>
      <TicketItem
        v-for="ticket in tickets"
        :key="ticket.id"
        :ticket="ticket"
        @edit="$emit('edit', $event)"
        @delete="$emit('delete', $event)"
        @toggle="handleToggle"
      />
    </template>
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
