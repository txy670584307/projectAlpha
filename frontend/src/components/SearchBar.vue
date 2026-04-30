<template>
  <div class="search-bar">
    <div class="search-container">
      <svg class="search-icon" width="18" height="18" viewBox="0 0 18 18" fill="none">
        <path d="M12.5 12.5L16 16M13 8C13 11.0376 10.5376 13.5 7.5 13.5C4.46243 13.5 2 11.0376 2 8C2 4.96243 4.46243 2.5 7.5 2.5C10.5376 2.5 13 4.96243 13 8Z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
      </svg>
      <input
        type="text"
        v-model="localKeyword"
        placeholder="搜索"
        @input="handleInput"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from "vue";
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
  margin-bottom: 24px;
}

.search-container {
  position: relative;
  display: flex;
  align-items: center;
}

.search-icon {
  position: absolute;
  left: 14px;
  color: var(--text-tertiary);
  pointer-events: none;
  z-index: 1;
}

.search-container input {
  padding-left: 42px;
  height: 40px;
  font-size: 15px;
  border-radius: 10px;
  background: var(--bg-elevated);
  border: 1px solid var(--border-color);
  transition: all var(--transition-fast);
  width: 100%;
}

.search-container input:focus {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(0, 113, 227, 0.12);
}

.search-container input::placeholder {
  color: var(--text-tertiary);
}
</style>
