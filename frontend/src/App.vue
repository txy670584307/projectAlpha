<template>
  <div id="app">
    <header class="app-header">
      <h1>projectAlpha</h1>
      <button class="btn btn-primary" @click="openCreateForm">+ 新建 Ticket</button>
    </header>
    <div class="app-layout">
      <aside class="app-sidebar">
        <TagSidebar />
      </aside>
      <main class="app-main">
        <SearchBar />
        <StatusFilter />
        <TicketList @edit="openEditForm" @delete="handleDelete" />
      </main>
    </div>
    <TicketForm :visible="formVisible" :ticket="editingTicket" @close="closeForm" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useTicketStore } from '@/stores/ticket'
import TagSidebar from '@/components/TagSidebar.vue'
import SearchBar from '@/components/SearchBar.vue'
import StatusFilter from '@/components/StatusFilter.vue'
import TicketList from '@/components/TicketList.vue'
import TicketForm from '@/components/TicketForm.vue'

const ticketStore = useTicketStore()

const formVisible = ref(false)
const editingTicket = ref(null)

onMounted(async () => {
  await ticketStore.fetchTickets()
})

function openCreateForm() {
  editingTicket.value = null
  formVisible.value = true
}

function openEditForm(ticket) {
  editingTicket.value = ticket
  formVisible.value = true
}

function closeForm() {
  formVisible.value = false
  editingTicket.value = null
}

async function handleDelete(id) {
  await ticketStore.deleteTicket(id)
}
</script>

<style scoped>
.app-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
