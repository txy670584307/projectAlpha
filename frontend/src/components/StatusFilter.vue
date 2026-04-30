<template>
  <div class="status-filter">
    <div class="segmented-control">
      <div
        class="segment-indicator"
        :style="indicatorStyle"
      ></div>
      <button
        v-for="(option, index) in options"
        :key="option.value"
        :class="['segment-btn', { active: ticketStore.statusFilter === option.value }]"
        @click="ticketStore.setStatusFilter(option.value)"
        :ref="el => setButtonRef(el, index)"
      >
        <span>{{ option.label }}</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, nextTick } from "vue";
import { useTicketStore } from "@/stores/ticket";

const ticketStore = useTicketStore();
const buttonRefs = ref([]);
const activeIndex = computed(() => {
  if (ticketStore.statusFilter === "open") return 1;
  if (ticketStore.statusFilter === "closed") return 2;
  return 0;
});

const indicatorStyle = computed(() => {
  const btn = buttonRefs.value[activeIndex.value];
  if (!btn) return {};
  return {
    width: `${btn.offsetWidth}px`,
    transform: `translateX(${btn.offsetLeft}px)`,
  };
});

function setButtonRef(el, index) {
  if (el) {
    buttonRefs.value[index] = el;
  }
}

const options = [
  { label: "全部", value: "" },
  { label: "未完成", value: "open" },
  { label: "已完成", value: "closed" },
];
</script>

<style scoped>
.status-filter {
  margin-bottom: 32px;
}

.segmented-control {
  position: relative;
  display: inline-flex;
  background-color: rgba(0, 0, 0, 0.04);
  border-radius: 9px;
  padding: 2px;
  gap: 0;
}

.segment-indicator {
  position: absolute;
  top: 2px;
  bottom: 2px;
  background-color: #ffffff;
  border-radius: 7px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08), 0 0 1px rgba(0, 0, 0, 0.12);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  z-index: 1;
}

.segment-btn {
  position: relative;
  z-index: 2;
  padding: 6px 16px;
  border: none;
  background: none;
  color: var(--text-secondary);
  cursor: pointer;
  transition: color 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  font-size: 13px;
  font-weight: 500;
  font-family: var(--font-sans);
  letter-spacing: -0.01em;
  white-space: nowrap;
  border-radius: 7px;
}

.segment-btn.active {
  color: var(--text-primary);
}

.segment-btn:hover:not(.active) {
  color: var(--text-primary);
}
</style>
