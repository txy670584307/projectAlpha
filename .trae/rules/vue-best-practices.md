# Vue 3 项目开发规则

> AI Agent 在开发本项目时必须遵守的 Vue 最佳实践规范。

---

## 1. 组件开发

### 1.1 必须使用 `<script setup>` 语法
- 统一使用 Composition API
- 禁止混用 Options API 和 Composition API

### 1.2 Props 必须完整定义
- 明确 `type`、`default`、`required`
- 使用 `validator` 进行值验证
- 禁止使用数组形式定义 props

### 1.3 Emits 必须显式定义
- 使用 `defineEmits()` 声明所有事件
- 提供验证函数

### 1.4 组件命名
- PascalCase，多单词命名
- 避免与 HTML 元素冲突
- 文件名与组件名一致

---

## 2. 组合式函数 (Composables)

### 2.1 命名规范
- 以 `use` 开头，如 `usePagination`、`useAuth`
- 放在 `src/composables/` 目录

### 2.2 编写规范
- 只能在 `setup` 或其他 composable 中调用
- 返回纯对象或响应式引用
- 封装完整的功能逻辑，遵循单一职责

---

## 3. 状态管理 (Pinia)

### 3.1 使用 Composition API 风格定义 Store
```javascript
export const useUserStore = defineStore('user', () => {
  const data = ref(null)
  const loading = ref(false)
  const isLoggedIn = computed(() => !!data.value)
  async function fetch() { /* ... */ }
  return { data, loading, isLoggedIn, fetch }
})
```

### 3.2 按业务模块拆分
- `stores/modules/user.js`
- `stores/modules/ticket.js`
- 禁止 store 之间循环引用

### 3.3 禁止直接修改 state
- 必须通过 action 修改状态

---

## 4. API 层

### 4.1 目录结构
```
src/api/
├── index.js          # axios 实例 + 拦截器
├── modules/          # 按业务模块划分
│   ├── user.js
│   └── ticket.js
```

### 4.2 拦截器配置
- 请求拦截：自动添加 token
- 响应拦截：统一错误处理、401 跳转

### 4.3 错误处理
- 所有异步操作必须有 try/catch
- 设置 loading/error 状态

---

## 5. 模板规范

### 5.1 列表渲染
- `v-for` 必须绑定唯一 `:key`（使用 id，禁止用 index）
- 避免 `v-for` 和 `v-if` 同时用在同一元素上

### 5.2 事件处理
- 简单逻辑可直接写（如 `@click="count++"`）
- 复杂逻辑必须调用方法
- 善用事件修饰符（`.prevent`、`.stop`、`.enter`）

### 5.3 样式
- 必须使用 `scoped`
- 使用 CSS 变量
- 避免使用 `:deep()` 修改子组件样式

---

## 6. 性能优化

### 6.1 路由懒加载
```javascript
component: () => import('@/views/UserList.vue')
```

### 6.2 计算缓存
- 使用 `computed` 替代模板中的函数调用

### 6.3 大组件拆分
- 超过 300 行的组件考虑拆分
- 公共逻辑提取为 composable

---

## 7. 错误处理

### 7.1 全局错误处理
- 配置 `app.config.errorHandler`

### 7.2 组件级错误边界
- 使用 `onErrorCaptured`

### 7.3 API 错误处理
- 区分网络错误、4xx、5xx 错误
- 提供用户友好的错误提示

---

## 8. Git 提交规范

### 8.1 Commit Message 格式
```
<type>(<scope>): <subject>

type: feat | fix | docs | style | refactor | perf | test | chore | ci
```

### 8.2 示例
```
feat(user): 添加用户列表分页功能
fix(order): 修复订单状态显示错误
refactor(store): 重构用户状态管理
```

---

## 9. 代码提交前自查清单

- [ ] 使用 `<script setup>` 语法
- [ ] Props 有完整类型定义和默认值
- [ ] Emits 有明确定义
- [ ] 避免直接修改 props
- [ ] 异步操作有 loading/error 状态
- [ ] 使用 scoped 样式
- [ ] v-for 绑定了唯一 key
- [ ] 模板中无复杂逻辑
- [ ] API 调用有错误处理
- [ ] 使用了 composables 复用逻辑

---

> **重要**：生成或修改 Vue 代码时，必须遵守以上所有规则。如有冲突，以本规则为准。
