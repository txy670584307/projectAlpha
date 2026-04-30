<template>
  <div id="app">
    <div class="app-layout">
      <aside class="app-sidebar">
        <div class="sidebar-header">
          <h1 class="logo">projectAlpha</h1>
          <button class="btn btn-primary btn-create" @click="openCreateForm">
            <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
              <path d="M7 1V13M1 7H13" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
            </svg>
            新建
          </button>
        </div>
        <TagSidebar />
      </aside>
      <main class="app-main">
        <SearchBar />
        <StatusFilter />
        <TicketList @edit="openEditForm" @delete="handleDelete" />
      </main>
    </div>
    <TicketForm
      :visible="formVisible"
      :ticket="editingTicket"
      @close="closeForm"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useTicketStore } from "@/stores/ticket";
import TagSidebar from "@/components/TagSidebar.vue";
import SearchBar from "@/components/SearchBar.vue";
import StatusFilter from "@/components/StatusFilter.vue";
import TicketList from "@/components/TicketList.vue";
import TicketForm from "@/components/TicketForm.vue";

const ticketStore = useTicketStore();

const formVisible = ref(false);
const editingTicket = ref(null);

onMounted(async () => {
  await ticketStore.fetchTickets();
});

function openCreateForm() {
  editingTicket.value = null;
  formVisible.value = true;
}

function openEditForm(ticket) {
  editingTicket.value = ticket;
  formVisible.value = true;
}

function closeForm() {
  formVisible.value = false;
  editingTicket.value = null;
}

async function handleDelete(id) {
  await ticketStore.deleteTicket(id);
}
</script>

<style scoped>
.logo {
  font-size: 18px;
  font-weight: 600;
  letter-spacing: -0.021em;
  color: var(--text-primary);
}

.sidebar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--border-light);
}

.btn-create {
  padding: 7px 14px;
  font-size: 13px;
  font-weight: 500;
  letter-spacing: -0.01em;
}

.btn-create svg {
  width: 14px;
  height: 14px;
}
</style>
