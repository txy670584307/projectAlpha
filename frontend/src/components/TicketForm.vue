<template>
  <Transition name="modal">
    <div v-if="visible" class="modal-overlay" @click.self="close">
      <div class="modal-content">
        <div class="modal-header">
          <h2>{{ isEdit ? "编辑 Ticket" : "新建 Ticket" }}</h2>
          <button class="btn-close" @click="close" aria-label="关闭">
            <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
              <path d="M1 1L13 13M1 13L13 1" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
            </svg>
          </button>
        </div>
        <form @submit.prevent="handleSubmit">
          <div class="form-group">
            <label>标题</label>
            <input
              type="text"
              v-model="form.title"
              maxlength="200"
              required
              placeholder="输入标题"
              autofocus
            />
            <span v-if="titleError" class="error-msg">{{ titleError }}</span>
          </div>
          <div class="form-group">
            <label>描述</label>
            <textarea
              v-model="form.description"
              placeholder="输入描述（可选）"
            ></textarea>
          </div>
          <div class="form-group">
            <label>标签</label>
            <div class="existing-tags">
              <span
                v-for="tag in existingTags"
                :key="tag.name"
                :class="['existing-tag', { selected: form.tags.includes(tag.name) }]"
                @click="toggleExistingTag(tag.name)"
              >
                {{ tag.name }}
                <span class="existing-tag-count">{{ tag.count }}</span>
              </span>
            </div>
            <div class="tag-input-container">
              <input
                type="text"
                v-model="tagInput"
                placeholder="输入新标签后按回车"
                @keydown.enter.prevent="addTag"
                @keydown.,.prevent="addTag"
              />
            </div>
            <div v-if="form.tags.length > 0" class="tag-list">
              <span
                v-for="(tag, index) in form.tags"
                :key="index"
                class="tag-badge"
              >
                {{ tag }}
                <span class="tag-remove" @click="removeTag(index)">&times;</span>
              </span>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="close">
              取消
            </button>
            <button type="submit" class="btn btn-primary" :disabled="submitting">
              {{ submitting ? "提交中..." : "提交" }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { ref, watch, computed, onMounted } from "vue";
import { useTicketStore } from "@/stores/ticket";
import { useTagStore } from "@/stores/tag";

const props = defineProps({
  ticket: { type: Object, default: null },
  visible: { type: Boolean, default: false },
});

const emit = defineEmits(["close"]);

const ticketStore = useTicketStore();
const tagStore = useTagStore();
const tagInput = ref("");
const submitting = ref(false);
const titleError = ref("");

const form = ref({
  title: "",
  description: "",
  tags: [],
});

const isEdit = computed(() => !!props.ticket);
const existingTags = computed(() => tagStore.tagsWithCount);

onMounted(async () => {
  await tagStore.fetchTags();
});

watch(
  () => props.visible,
  (val) => {
    if (val && props.ticket) {
      form.value.title = props.ticket.title;
      form.value.description = props.ticket.description || "";
      form.value.tags = [...(props.ticket.tags || [])];
    } else if (val) {
      form.value = { title: "", description: "", tags: [] };
    }
    titleError.value = "";
  },
);

function toggleExistingTag(tagName) {
  const index = form.value.tags.indexOf(tagName);
  if (index === -1) {
    form.value.tags.push(tagName);
  } else {
    form.value.tags.splice(index, 1);
  }
}

function addTag() {
  const tag = tagInput.value.trim().toLowerCase();
  if (tag && !form.value.tags.includes(tag)) {
    form.value.tags.push(tag);
  }
  tagInput.value = "";
}

function removeTag(index) {
  form.value.tags.splice(index, 1);
}

function validate() {
  if (!form.value.title.trim()) {
    titleError.value = "标题不能为空";
    return false;
  }
  if (form.value.title.length > 200) {
    titleError.value = "标题不能超过 200 个字符";
    return false;
  }
  titleError.value = "";
  return true;
}

async function handleSubmit() {
  if (!validate()) return;
  submitting.value = true;
  try {
    if (isEdit.value) {
      await ticketStore.updateTicket(props.ticket.id, form.value);
    } else {
      await ticketStore.createTicket(form.value);
    }
    close();
  } catch {
  } finally {
    submitting.value = false;
  }
}

function close() {
  form.value = { title: "", description: "", tags: [] };
  tagInput.value = "";
  titleError.value = "";
  emit("close");
}
</script>

<style scoped>
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.2s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-content {
  animation: modalSlideIn 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

@keyframes modalSlideIn {
  from {
    opacity: 0;
    transform: translateY(16px) scale(0.98);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.btn-close {
  background: none;
  border: none;
  cursor: pointer;
  padding: 6px;
  color: var(--text-tertiary);
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  transition: all var(--transition-fast);
}

.btn-close:hover {
  background-color: rgba(0, 0, 0, 0.06);
  color: var(--text-primary);
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
  letter-spacing: -0.01em;
}

.error-msg {
  color: var(--danger-color);
  font-size: 12px;
  margin-top: 6px;
  display: block;
}

.existing-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-bottom: 10px;
}

.existing-tag {
  display: inline-flex;
  align-items: center;
  padding: 5px 10px;
  border: 1px solid var(--border-color);
  border-radius: 980px;
  cursor: pointer;
  font-size: 13px;
  font-weight: 500;
  transition: all var(--transition-fast);
  background-color: var(--bg-elevated);
  color: var(--text-secondary);
  letter-spacing: -0.01em;
}

.existing-tag:hover {
  border-color: var(--primary-color);
  color: var(--primary-color);
}

.existing-tag.selected {
  background-color: var(--primary-color);
  border-color: var(--primary-color);
  color: #ffffff;
}

.existing-tag-count {
  margin-left: 4px;
  font-size: 11px;
  opacity: 0.7;
}

.tag-input-container {
  margin-bottom: 10px;
}

.tag-list {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  margin-top: 8px;
}

.tag-badge {
  display: inline-flex;
  align-items: center;
  padding: 4px 10px;
  background-color: var(--primary-color);
  color: #ffffff;
  border-radius: 980px;
  font-size: 12px;
  font-weight: 500;
}

.tag-remove {
  margin-left: 4px;
  cursor: pointer;
  opacity: 0.7;
  transition: opacity var(--transition-fast);
}

.tag-remove:hover {
  opacity: 1;
}
</style>
