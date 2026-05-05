# Vue 3 最佳实践规范

> 参考阿里巴巴、字节跳动、腾讯等大厂 Vue 项目开发规范，结合 Vue 3 Composition API 特性制定。

***

## 一、项目结构规范

### 1.1 标准目录结构

```
src/
├── api/                    # API 接口层
│   ├── modules/            # 按业务模块划分
│   │   ├── user.js
│   │   └── order.js
│   └── index.js            # axios 实例配置
├── assets/                 # 静态资源（图片、字体等）
├── components/             # 公共组件
│   ├── common/             # 全局通用组件
│   └── business/           # 业务通用组件
├── composables/            # 组合式函数（hooks）
│   ├── useAuth.js
│   └── usePagination.js
├── directives/             # 自定义指令
├── layouts/                # 布局组件
├── router/                 # 路由配置
│   ├── index.js
│   └── guards.js           # 路由守卫
├── stores/                 # Pinia 状态管理
│   ├── modules/            # 按业务模块划分
│   └── index.js
├── styles/                 # 全局样式
│   ├── variables.scss      # CSS 变量
│   ├── mixins.scss         # SCSS mixins
│   └── main.css
├── utils/                  # 工具函数
│   ├── format.js
│   └── validate.js
├── views/                  # 页面组件
├── App.vue
└── main.js
```

***

## 二、组件开发规范

### 2.1 组件命名

```javascript
// ✅ 正确：PascalCase 文件名，多单词命名
UserList.vue
UserProfile.vue
OrderItem.vue

// ❌ 错误：单单词、保留字冲突
List.vue          // 与 HTML 元素冲突
User.vue          // 过于宽泛
```

### 2.2 Props 定义

```javascript
// ✅ 正确：完整类型定义 + 默认值 + 验证
const props = defineProps({
  title: {
    type: String,
    required: true,
  },
  count: {
    type: Number,
    default: 0,
    validator: (v) => v >= 0,
  },
  status: {
    type: String,
    default: 'pending',
    validator: (v) => ['pending', 'active', 'closed'].includes(v),
  },
  tags: {
    type: Array,
    default: () => [],
  },
})

// ❌ 错误：缺少类型和默认值
const props = defineProps(['title', 'count', 'status', 'tags'])
```

### 2.3 组件结构设计

```vue
<template>
  <div class="user-card">
    <!-- 模板内容 -->
  </div>
</template>

<script setup>
// 1. 导入
import { ref, computed, watch } from 'vue'
import { useUserStore } from '@/stores/user'

// 2. Props & Emits
const props = defineProps({ /* ... */ })
const emit = defineEmits(['update', 'delete'])

// 3. 状态
const loading = ref(false)
const userStore = useUserStore()

// 4. 计算属性
const displayName = computed(() => `${props.firstName} ${props.lastName}`)

// 5. 监听器
watch(() => props.id, async (newId) => {
  await fetchData(newId)
})

// 6. 生命周期
onMounted(() => {
  init()
})

// 7. 方法
async function fetchData(id) {
  loading.value = true
  try {
    await userStore.fetchUser(id)
  } finally {
    loading.value = false
  }
}

function init() {
  // 初始化逻辑
}

// 8. 暴露给父组件（如需要）
defineExpose({ fetchData })
</script>

<style scoped>
/* 样式 */
</style>
```

### 2.4 Emits 定义

```javascript
// ✅ 正确：使用 TypeScript 风格或对象风格完整定义
const emit = defineEmits({
  update: (payload) => payload.id && payload.data,
  delete: (id) => typeof id === 'number',
})

// 使用
emit('update', { id: 1, data: { name: 'test' } })

// ❌ 错误：未定义 emits
const emit = defineEmits(['update', 'delete'])  // 缺少验证
```

***

## 三、Composition API 最佳实践

### 3.1 Composables 编写

```javascript
// composables/usePagination.js
import { ref, computed } from 'vue'

export function usePagination(fetchFn, options = {}) {
  const { pageSize = 10 } = options
  
  const loading = ref(false)
  const data = ref([])
  const currentPage = ref(1)
  const total = ref(0)
  
  const totalPages = computed(() => Math.ceil(total.value / pageSize))
  const hasNext = computed(() => currentPage.value < totalPages.value)
  const hasPrev = computed(() => currentPage.value > 1)
  
  async function fetchData(page = currentPage.value) {
    loading.value = true
    try {
      const res = await fetchFn({ page, pageSize })
      data.value = res.items
      total.value = res.total
      currentPage.value = page
    } finally {
      loading.value = false
    }
  }
  
  function nextPage() {
    if (hasNext.value) fetchData(currentPage.value + 1)
  }
  
  function prevPage() {
    if (hasPrev.value) fetchData(currentPage.value - 1)
  }
  
  return {
    loading,
    data,
    currentPage,
    total,
    totalPages,
    hasNext,
    hasPrev,
    fetchData,
    nextPage,
    prevPage,
  }
}
```

### 3.2 Composables 使用

```vue
<script setup>
import { usePagination } from '@/composables/usePagination'
import { fetchUsers } from '@/api/user'

const {
  loading,
  data: users,
  currentPage,
  total,
  hasNext,
  hasPrev,
  fetchData,
  nextPage,
  prevPage,
} = usePagination(fetchUsers, { pageSize: 20 })

onMounted(() => fetchData())
</script>
```

### 3.3 避免的写法

```javascript
// ❌ 错误：在组件外直接调用 composable
const store = useUserStore()  // 只能在 setup 或 composable 中调用

// ❌ 错误：混用 Options API 和 Composition API
export default {
  data() { return { count: 0 } },
  setup() {
    const name = ref('test')
    return { name }
  }
}

// ✅ 正确：统一使用 Composition API
<script setup>
const count = ref(0)
const name = ref('test')
</script>
```

***

## 四、状态管理规范（Pinia）

### 4.1 Store 定义

```javascript
// stores/modules/user.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { fetchUser, updateUser } from '@/api/user'

export const useUserStore = defineStore('user', () => {
  // State
  const userInfo = ref(null)
  const token = ref('')
  const loading = ref(false)
  
  // Getters
  const isLoggedIn = computed(() => !!token.value)
  const userName = computed(() => userInfo.value?.name ?? '')
  
  // Actions
  async function fetchUserInfo() {
    loading.value = true
    try {
      userInfo.value = await fetchUser()
    } finally {
      loading.value = false
    }
  }
  
  async function updateProfile(data) {
    const res = await updateUser(data)
    userInfo.value = { ...userInfo.value, ...res }
  }
  
  function logout() {
    userInfo.value = null
    token.value = ''
  }
  
  return {
    userInfo,
    token,
    loading,
    isLoggedIn,
    userName,
    fetchUserInfo,
    updateProfile,
    logout,
  }
})
```

### 4.2 Store 使用

```vue
<script setup>
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()

// 直接访问
console.log(userStore.isLoggedIn)
console.log(userStore.userName)

// 调用 action
await userStore.fetchUserInfo()

// ❌ 错误：直接修改 state（应通过 action）
userStore.userInfo = null  // 不规范
userStore.logout()         // 规范
</script>
```

### 4.3 Store 拆分原则

| 原则           | 说明                   |
| ------------ | -------------------- |
| 按业务模块拆分      | user、order、product 等 |
| 单一职责         | 每个 store 只管理相关业务数据   |
| 避免循环依赖       | store 之间不要互相引用       |
| 全局状态才放 store | 组件内部状态用 ref/reactive |

***

## 五、API 层规范

### 5.1 Axios 实例配置

```javascript
// api/index.js
import axios from 'axios'

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// 请求拦截器
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// 响应拦截器
apiClient.interceptors.response.use(
  (response) => response.data,
  (error) => {
    if (error.response?.status === 401) {
      // 处理未授权
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default apiClient
```

### 5.2 API 模块划分

```javascript
// api/modules/user.js
import apiClient from '../index'

export function fetchUsers(params) {
  return apiClient.get('/api/users', { params })
}

export function fetchUser(id) {
  return apiClient.get(`/api/users/${id}`)
}

export function createUser(data) {
  return apiClient.post('/api/users', data)
}

export function updateUser(id, data) {
  return apiClient.put(`/api/users/${id}`, data)
}

export function deleteUser(id) {
  return apiClient.delete(`/api/users/${id}`)
}
```

### 5.3 API 使用

```vue
<script setup>
import { ref } from 'vue'
import { fetchUsers } from '@/api/user'

const users = ref([])

async function loadUsers() {
  const res = await fetchUsers({ page: 1, size: 20 })
  users.value = res.items
}

onMounted(loadUsers)
</script>
```

***

## 六、模板编写规范

### 6.1 指令使用

```vue
<template>
  <!-- ✅ 正确：使用 :key 绑定唯一值 -->
  <li v-for="item in items" :key="item.id">
    {{ item.name }}
  </li>

  <!-- ❌ 错误：使用 index 作为 key -->
  <li v-for="(item, index) in items" :key="index">

  <!-- ✅ 正确：使用 v-show 控制显隐（频繁切换） -->
  <div v-show="isVisible">内容</div>

  <!-- ✅ 正确：使用 v-if 条件渲染（不常切换） -->
  <div v-if="hasPermission">敏感内容</div>

  <!-- ✅ 正确：使用可选链避免空值报错 -->
  <p>{{ user?.profile?.name ?? '未设置' }}</p>
</template>
```

### 6.2 事件处理

```vue
<template>
  <!-- ✅ 正确：简单逻辑直接写 -->
  <button @click="count++">增加</button>

  <!-- ✅ 正确：复杂逻辑调用方法 -->
  <button @click="handleSubmit">提交</button>

  <!-- ✅ 正确：使用事件修饰符 -->
  <form @submit.prevent="handleSubmit">
    <input @keyup.enter="search" />
  </form>

  <!-- ❌ 错误：模板中写复杂逻辑 -->
  <button @click="if (count > 0) { count--; sendRequest(); logAction(); }">
    减少
  </button>
</template>
```

### 6.3 样式编写

```vue
<style scoped>
/* ✅ 正确：使用 scoped 避免全局污染 */
.user-card {
  padding: 16px;
  border-radius: 8px;
}

/* ✅ 正确：使用 BEM 或类命名规范 */
.user-card__header {
  font-size: 18px;
}

.user-card__header--active {
  color: #0071e3;
}

/* ✅ 正确：使用 CSS 变量 */
.user-card {
  background-color: var(--bg-color);
  color: var(--text-color);
}

/* ❌ 错误：使用深度选择器修改子组件样式（尽量避免） */
.user-card :deep(.child-component) {
  margin: 0;
}
</style>
```

***

## 七、性能优化规范

### 7.1 组件懒加载

```javascript
// router/index.js
import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/users',
    name: 'UserList',
    component: () => import('@/views/UserList.vue'),  // 路由懒加载
  },
]

export default createRouter({
  history: createWebHistory(),
  routes,
})
```

### 7.2 组件懒加载（动态组件）

```vue
<script setup>
import { defineAsyncComponent } from 'vue'

const HeavyComponent = defineAsyncComponent(() =>
  import('@/components/HeavyComponent.vue')
)
</script>
```

### 7.3 避免不必要的重新渲染

```vue
<script setup>
import { ref, computed } from 'vue'

// ✅ 正确：使用 computed 缓存计算结果
const filteredList = computed(() => 
  list.value.filter(item => item.status === 'active')
)

// ❌ 错误：在模板中直接调用函数
// <div v-for="item in getFilteredList()">

// ✅ 正确：大列表使用虚拟滚动（第三方库）
import { VueVirtualScroller } from 'vue-virtual-scroller'
</script>
```

### 7.4 合理使用 v-memo（Vue 3.2+）

```vue
<template>
  <!-- ✅ 正确：缓存不常变化的列表项 -->
  <div v-for="item in list" :key="item.id" v-memo="[item.status]">
    {{ item.name }}
  </div>
</template>
```

***

## 八、错误处理规范

### 8.1 全局错误处理

```javascript
// main.js
import { createApp } from 'vue'
import App from './App.vue'

const app = createApp(App)

app.config.errorHandler = (err, instance, info) => {
  console.error('Vue Error:', err)
  // 上报错误到监控平台
  reportError(err, info)
}

app.mount('#app')
```

### 8.2 组件级错误边界

```vue
<script setup>
import { onErrorCaptured } from 'vue'

const errorMessage = ref('')

onErrorCaptured((err, instance, info) => {
  errorMessage.value = `加载失败: ${err.message}`
  // 阻止错误继续向上传播
  return false
})
</script>

<template>
  <div v-if="errorMessage" class="error-boundary">
    {{ errorMessage }}
  </div>
  <slot v-else />
</template>
```

### 8.3 API 错误处理

```javascript
async function fetchData() {
  loading.value = true
  try {
    data.value = await apiClient.get('/data')
  } catch (error) {
    if (error.response?.status === 404) {
      errorMessage.value = '数据不存在'
    } else if (error.response?.status >= 500) {
      errorMessage.value = '服务器错误，请稍后重试'
    } else {
      errorMessage.value = '网络错误，请检查网络连接'
    }
  } finally {
    loading.value = false
  }
}
```

***

## 九、类型规范（如使用 TypeScript）

### 9.1 Props 类型定义

```typescript
interface UserCardProps {
  user: {
    id: number
    name: string
    email: string
  }
  showActions?: boolean
  onDelete?: (id: number) => void
}

const props = withDefaults(defineProps<UserCardProps>(), {
  showActions: true,
  onDelete: undefined,
})
```

### 9.2 Composables 类型定义

```typescript
interface UsePaginationOptions {
  pageSize?: number
  initialPage?: number
}

interface PaginationResult<T> {
  loading: Ref<boolean>
  data: Ref<T[]>
  currentPage: Ref<number>
  total: Ref<number>
  fetchData: (page?: number) => Promise<void>
  nextPage: () => void
  prevPage: () => void
}

export function usePagination<T>(
  fetchFn: (params: { page: number; pageSize: number }) => Promise<{ items: T[]; total: number }>,
  options: UsePaginationOptions = {}
): PaginationResult<T> {
  // 实现...
}
```

***

## 十、Git 提交规范

### 10.1 Commit Message 格式

```
<type>(<scope>): <subject>

<body>

type:
  feat:     新功能
  fix:      修复 bug
  docs:     文档更新
  style:    代码格式（不影响代码运行）
  refactor: 重构（既不是新功能也不是修复）
  perf:     性能优化
  test:     测试相关
  chore:    构建/工具相关
  ci:       CI 配置

示例:
feat(user): 添加用户列表分页功能
fix(order): 修复订单状态显示错误
docs: 更新 API 文档
refactor(store): 重构用户状态管理
```

### 10.2 .gitignore

```
# 依赖
node_modules/
dist/

# 环境变量
.env.local
.env.*.local

# 编辑器
.vscode/*
!.vscode/extensions.json
.idea/
*.swp

# 系统文件
.DS_Store
Thumbs.db

# 日志
*.log
logs/
```

***

## 十一、代码审查清单

### 11.1 提交前自查

- [ ] 是否使用 `<script setup>` 语法
- [ ] Props 是否有完整类型定义和默认值
- [ ] Emits 是否有明确定义
- [ ] 是否避免直接修改 props
- [ ] 异步操作是否有 loading/error 状态
- [ ] 组件是否使用 `scoped` 样式
- [ ] v-for 是否绑定了唯一 key
- [ ] 是否避免在模板中写复杂逻辑
- [ ] API 调用是否有错误处理
- [ ] 是否使用 composables 复用逻辑

### 11.2 性能检查

- [ ] 路由是否懒加载
- [ ] 大组件是否拆分
- [ ] 计算属性是否使用 computed
- [ ] 是否避免不必要的 watch
- [ ] 图片是否使用懒加载
- [ ] 列表是否考虑虚拟滚动

***

## 十二、常用工具推荐

| 用途      | 工具                                       |
| ------- | ---------------------------------------- |
| 状态管理    | Pinia                                    |
| HTTP 请求 | Axios                                    |
| 表单验证    | VeeValidate / FormKit                    |
| UI 组件库  | Element Plus / Naive UI / Ant Design Vue |
| 图标      | Unplugin Icons                           |
| 虚拟列表    | Vue Virtual Scroller                     |
| 表格      | Vue Data UI / AG Grid                    |
| 图表      | ECharts / Chart.js                       |
| 日期处理    | Day.js                                   |
| 工具函数    | Lodash-es / VueUse                       |
| 代码规范    | ESLint + Prettier                        |
| 提交规范    | Husky + Commitlint                       |

***

> **提示**：规范是指导而非束缚。团队应根据实际项目情况适当调整，保持一致性比严格遵守更重要。

