<template>
  <div v-if="visible" class="modal-overlay" @click.self="close">
    <div class="modal-content">
      <div class="modal-header">
        <h2>{{ isEdit ? "编辑 Ticket" : "新建 Ticket" }}</h2>
        <button class="btn btn-text" @click="close">&times;</button>
      </div>
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label>标题 *</label>
          <input
            type="text"
            v-model="form.title"
            maxlength="200"
            required
            placeholder="输入标题"
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
              placeholder="输入新标签后按回车或逗号"
              @keydown.enter.prevent="addTag"
              @keydown.,.prevent="addTag"
            />
          </div>
          <div class="tag-list">
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
          <button type="button" class="btn btn-text" @click="close">
            取消
          </button>
          <button type="submit" class="btn btn-primary" :disabled="submitting">
            {{ submitting ? "提交中..." : "提交" }}
          </button>
        </div>
      </form>
    </div>
  </div>
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
.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  margin-bottom: 6px;
  font-size: 14px;
  font-weight: 500;
}

.existing-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-bottom: 8px;
}

.existing-tag {
  display: inline-flex;
  align-items: center;
  padding: 4px 8px;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
  transition: all 0.2s;
  background-color: var(--white);
}

.existing-tag:hover {
  border-color: var(--primary-color);
  background-color: #f0f7ff;
}

.existing-tag.selected {
  background-color: var(--primary-color);
  border-color: var(--primary-color);
  color: var(--white);
}

.existing-tag-count {
  margin-left: 4px;
  font-size: 10px;
  opacity: 0.7;
}

.tag-input-container {
  margin-bottom: 8px;
}

.tag-list {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.tag-badge {
  display: inline-flex;
  align-items: center;
  padding: 4px 8px;
  background-color: var(--primary-color);
  color: var(--white);
  border-radius: 4px;
  font-size: 12px;
}

.tag-remove {
  margin-left: 4px;
  cursor: pointer;
  font-weight: bold;
}

.error-msg {
  color: var(--danger-color);
  font-size: 12px;
  margin-top: 4px;
  display: block;
}
</style>
