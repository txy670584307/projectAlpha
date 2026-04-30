<template>
  <div class="search-bar">
    <input
      type="text"
      v-model="localKeyword"
      placeholder="搜索 Ticket..."
      @input="handleInput"
    />
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from "vue";
import { useTicketStore } from "@/stores/ticket";

const ticketStore = useTicketStore();
const localKeyword = ref(ticketStore.searchKeyword);
let debounceTimer = null;

const handleInput = () => {
  clearTimeout(debounceTimer);
  debounceTimer = setTimeout(() => {
    ticketStore.setSearchKeyword(localKeyword.value);
  }, 300);
};

watch(
  () => ticketStore.searchKeyword,
  (newVal) => {
    localKeyword.value = newVal;
  },
);
</script>

<style scoped>
.search-bar {
  margin-bottom: 16px;
}

.search-bar input {
  padding: 10px 14px;
  width: 100%;
}
</style>
