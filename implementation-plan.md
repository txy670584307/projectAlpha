# projectAlpha - 实现计划

## 项目概述

projectAlpha 是一个基于标签分类的 Ticket 管理工具，采用 PostgreSQL + FastAPI + Vue 3 技术栈，面向个人或小团队使用，无需用户认证系统。

---

## 阶段一：环境准备与项目初始化

**目标**：搭建开发环境，创建项目结构，配置基础工具

**预计耗时**：1-2 天

### 任务 1.1：安装开发环境

| 序号 | 任务内容 | 详细说明 | 验收标准 |
|------|---------|---------|---------|
| 1.1.1 | 安装 Python 3.11+ | Windows 使用 winget 或官网安装包，macOS 使用 Homebrew，Linux 使用 deadsnakes PPA | `python --version` 显示 3.11+ |
| 1.1.2 | 安装 Node.js 18+ | 使用官网 LTS 版本或包管理器安装 | `node --version` 显示 v18+ |
| 1.1.3 | 安装 PostgreSQL 15+ | 下载官方安装包，设置超级用户密码，记录端口（默认 5432） | `psql --version` 显示 15+，服务正常运行 |
| 1.1.4 | 安装 Git | 配置用户名和邮箱 | `git --version` 正常输出 |
| 1.1.5 | 安装 IDE/编辑器 | 推荐 VS Code，安装 Python、Vue、ESLint 插件 | 编辑器可正常打开项目 |

### 任务 1.2：创建项目目录结构

```
projectAplha/
+-- backend/                 # 后端项目
|   +-- app/
|   |   +-- __init__.py
|   |   +-- main.py
|   |   +-- config.py
|   |   +-- database.py
|   |   +-- models/
|   |   |   +-- __init__.py
|   |   |   +-- ticket.py
|   |   |   +-- tag.py
|   |   +-- schemas/
|   |   |   +-- __init__.py
|   |   |   +-- ticket.py
|   |   |   +-- tag.py
|   |   +-- routers/
|   |   |   +-- __init__.py
|   |   |   +-- tickets.py
|   |   |   +-- tags.py
|   |   +-- services/
|   |   |   +-- __init__.py
|   |   |   +-- ticket_service.py
|   |   |   +-- tag_service.py
|   +-- alembic/
|   |   +-- versions/
|   |   +-- alembic.ini
|   +-- tests/
|   |   +-- __init__.py
|   |   +-- conftest.py
|   |   +-- test_tickets.py
|   |   +-- test_tags.py
|   +-- logs/
|   +-- requirements.txt
|   +-- requirements-dev.txt
|   +-- .env.example
|   +-- .gitignore
+-- frontend/                # 前端项目
|   +-- src/
|   |   +-- main.js
|   |   +-- App.vue
|   |   +-- api/
|   |   |   +-- index.js
|   |   |   +-- tickets.js
|   |   |   +-- tags.js
|   |   +-- components/
|   |   |   +-- TicketList.vue
|   |   |   +-- TicketItem.vue
|   |   |   +-- TicketForm.vue
|   |   |   +-- TagSidebar.vue
|   |   |   +-- SearchBar.vue
|   |   |   +-- StatusFilter.vue
|   |   +-- stores/
|   |   |   +-- ticket.js
|   |   |   +-- tag.js
|   |   +-- styles/
|   |   |   +-- main.css
|   |   +-- utils/
|   |   |   +-- helpers.js
|   +-- tests/
|   |   +-- unit/
|   |   +-- e2e/
|   +-- logs/
|   +-- package.json
|   +-- vite.config.js
|   +-- index.html
|   +-- .env.example
|   +-- .gitignore
+-- .gitignore               # 根目录 Git 忽略
```

### 任务 1.3：初始化后端项目

| 序号 | 任务内容 | 详细说明 | 验收标准 |
|------|---------|---------|---------|
| 1.3.1 | 创建 Python 虚拟环境 | `python -m venv backend/venv` | 虚拟环境目录创建成功 |
| 1.3.2 | 激活虚拟环境 | Windows: `backend\venv\Scripts\activate` | 命令行提示符显示 (venv) |
| 1.3.3 | 创建 requirements.txt | 包含 fastapi、uvicorn、sqlalchemy[asyncio]、asyncpg、psycopg2-binary、pydantic、pydantic-settings、python-dotenv、alembic、gunicorn、python-multipart、email-validator | 文件创建，内容正确 |
| 1.3.4 | 创建 requirements-dev.txt | 包含 pytest、pytest-asyncio、pytest-cov、httpx、black、flake8、mypy、pre-commit | 文件创建，内容正确 |
| 1.3.5 | 安装生产依赖 | `pip install -r requirements.txt` | 所有包安装成功，无报错 |
| 1.3.6 | 安装开发依赖 | `pip install -r requirements-dev.txt` | 所有包安装成功，无报错 |
| 1.3.7 | 初始化 Alembic | `cd backend && alembic init alembic` | alembic.ini 和 alembic/versions/ 目录创建 |
| 1.3.8 | 配置 alembic.ini | 修改 sqlalchemy.url 为环境变量引用，配置脚本目录 | 配置文件可正确读取数据库连接 |

### 任务 1.4：初始化前端项目

| 序号 | 任务内容 | 详细说明 | 验收标准 |
|------|---------|---------|---------|
| 1.4.1 | 使用 Vite 创建项目 | `npm create vite@latest frontend -- --template vue` | 项目创建成功 |
| 1.4.2 | 进入前端目录 | `cd frontend` | 当前目录为 frontend |
| 1.4.3 | 安装核心依赖 | `npm install vue@^3.5.0 pinia@^2.3.0 axios@^1.7.0` | package.json 中版本正确 |
| 1.4.4 | 安装开发依赖 | `npm install -D @vitejs/plugin-vue@^5.2.0 vitest@^2.1.0 @vue/test-utils@^2.4.0 cypress@^13.17.0 eslint@^9.17.0 prettier@^3.4.0` | 开发依赖安装成功 |
| 1.4.5 | 验证开发服务器 | `npm run dev` | 浏览器可访问 http://localhost:5173 |

### 任务 1.5：配置 Git 版本控制

| 序号 | 任务内容 | 详细说明 | 验收标准 |
|------|---------|---------|---------|
| 1.5.1 | 初始化 Git 仓库 | `git init` | .git 目录创建 |
| 1.5.2 | 创建根目录 .gitignore | 忽略 venv/、node_modules/、.env、logs/、dist/、__pycache__/ | 文件创建，规则正确 |
| 1.5.3 | 创建后端 .gitignore | 忽略 venv/、.env、logs/、*.pyc、__pycache__/、.coverage | 文件创建，规则正确 |
| 1.5.4 | 创建前端 .gitignore | 忽略 node_modules/、dist/、.env、logs/、coverage/ | 文件创建，规则正确 |
| 1.5.5 | 首次提交 | `git add . && git commit -m "init: 项目初始化和目录结构"` | 提交成功，无大文件 |

---

## 阶段二：数据库设计与实现

**目标**：创建数据库、定义数据模型、实现迁移脚本

**预计耗时**：1-2 天

### 任务 2.1：PostgreSQL 数据库配置

| 序号 | 任务内容 | 详细说明 | 验收标准 |
|------|---------|---------|---------|
| 2.1.1 | 创建数据库用户 | 在 psql 中执行 `CREATE USER projectalpha_user WITH PASSWORD 'your_password';` | 用户创建成功 |
| 2.1.2 | 创建数据库 | `CREATE DATABASE projectalpha OWNER projectalpha_user;` | 数据库创建成功 |
| 2.1.3 | 授予权限 | `GRANT ALL PRIVILEGES ON DATABASE projectalpha TO projectalpha_user;` | 权限授予成功 |
| 2.1.4 | 创建测试数据库 | `CREATE DATABASE projectalpha_test OWNER projectalpha_user;` | 测试数据库创建成功 |
| 2.1.5 | 验证连接 | `psql -h localhost -U projectalpha_user -d projectalpha` | 可正常连接并执行查询 |

### 任务 2.2：定义 SQLAlchemy 数据模型

**文件**：`backend/app/models/ticket.py`

| 序号 | 任务内容 | 详细说明 | 验收标准 |
|------|---------|---------|---------|
| 2.2.1 | 创建 Ticket 模型 | 定义 Ticket 类，包含 id、title、description、status、created_at、updated_at、completed_at 字段 | 模型定义完整，类型正确 |
| 2.2.2 | 配置字段约束 | title: VARCHAR(200) NOT NULL，status: VARCHAR(20) DEFAULT 'open' CHECK IN ('open', 'closed') | 约束配置正确 |
| 2.2.3 | 定义多对多关系 | Ticket.tags 关联到 Tag 模型，通过 ticket_tags 关联表 | 关系定义正确，级联删除配置 |
| 2.2.4 | 添加表注释 | 使用 `__table_args__` 或 comment 参数添加表和字段注释 | 注释完整 |

**文件**：`backend/app/models/tag.py`

| 序号 | 任务内容 | 详细说明 | 验收标准 |
|------|---------|---------|---------|
| 2.2.5 | 创建 Tag 模型 | 定义 Tag 类，包含 id、name、created_at 字段 | 模型定义完整 |
| 2.2.6 | 配置唯一约束 | name: VARCHAR(50) NOT NULL UNIQUE | 唯一约束配置正确 |
| 2.2.7 | 定义反向关系 | Tag.tickets 关联到 Ticket 模型 | 双向关系可用 |

### 任务 2.3：配置数据库连接

**文件**：`backend/app/database.py`

| 序号 | 任务内容 | 详细说明 | 验收标准 |
|------|---------|---------|---------|
| 2.3.1 | 创建异步引擎 | `create_async_engine(DATABASE_URL, echo=DEBUG)` | 引擎创建成功 |
| 2.3.2 | 创建异步会话工厂 | `async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)` | 会话工厂可用 |
| 2.3.3 | 定义 Base 类 | `from sqlalchemy.ext.asyncio import AsyncAttrs; class Base(AsyncAttrs, DeclarativeBase)` | 支持异步操作 |
| 2.3.4 | 创建 get_db 依赖 | 异步生成器，yield 会话，自动关闭 | FastAPI 依赖可用 |
| 2.3.5 | 创建初始化函数 | `init_db()` 用于创建所有表 | 可成功创建表 |

### 任务 2.4：配置 Alembic 迁移

| 序号 | 任务内容 | 详细说明 | 验收标准 |
|------|---------|---------|---------|
| 2.4.1 | 修改 alembic/env.py | 导入 Base 和 engine，配置 target_metadata | 迁移脚本可正确读取模型 |
| 2.4.2 | 修改 alembic.ini | 设置 sqlalchemy.url = %(DATABASE_URL)s | 从环境变量读取连接 |
| 2.4.3 | 创建初始迁移 | `alembic revision --autogenerate -m "initial schema"` | 迁移脚本生成成功 |
| 2.4.4 | 执行迁移 | `alembic upgrade head` | 数据库表创建成功 |
| 2.4.5 | 验证表结构 | 使用 psql 或 pgAdmin 查看表结构 | tickets、tags、ticket_tags 表存在 |

### 任务 2.5：创建数据库触发器

| 序号 | 任务内容 | 详细说明 | 验收标准 |
|------|---------|---------|---------|
| 2.5.1 | 创建更新触发器函数 | `update_updated_at_column()` 函数 | 函数创建成功 |
| 2.5.2 | 为 tickets 表添加触发器 | BEFORE UPDATE 触发器，自动更新 updated_at | 触发器工作正常 |
| 2.5.3 | 验证触发器 | 更新某条记录，检查 updated_at 是否变化 | 时间戳自动更新 |

---

## 阶段三：后端 API 开发

**目标**：实现所有 RESTful API 端点，包括 Ticket 和标签管理

**预计耗时**：3-4 天

### 任务 3.1：配置 FastAPI 应用

**文件**：`backend/app/main.py`、`backend/app/config.py`

| 序号 | 任务内容 | 详细说明 | 验收标准 |
|------|---------|---------|---------|
| 3.1.1 | 创建配置类 | 使用 Pydantic Settings，从 .env 读取配置 | 配置项可正确读取 |
| 3.1.2 | 创建 FastAPI 实例 | 配置 title、description、version、docs_url、redoc_url | Swagger UI 可访问 |
| 3.1.3 | 配置 CORS | 允许前端开发服务器地址（http://localhost:5173） | 前端可跨域访问 |
| 3.1.4 | 配置异常处理 | 全局 HTTPException 处理器，统一错误响应格式 | 错误响应格式一致 |
| 3.1.5 | 注册路由 | 包含 tickets 和 tags 路由，前缀 /api | 路由注册成功 |
| 3.1.6 | 添加健康检查 | GET /health 端点，检查数据库连接 | 返回健康状态 |

### 任务 3.2：定义 Pydantic 数据模型

**文件**：`backend/app/schemas/ticket.py`、`backend/app/schemas/tag.py`

| 序号 | 任务内容 | 详细说明 | 验收标准 |
|------|---------|---------|---------|
| 3.2.1 | 创建 TicketBase | title (str, max_length=200)、description (Optional[str])、tags (Optional[List[str]]) | 基础模型定义正确 |
| 3.2.2 | 创建 TicketCreate | 继承 TicketBase，title 必填 | 创建请求模型可用 |
| 3.2.3 | 创建 TicketUpdate | 继承 TicketBase，所有字段可选 | 更新请求模型可用 |
| 3.2.4 | 创建 TicketResponse | 继承 TicketBase，增加 id、status、created_at、updated_at、completed_at | 响应模型完整 |
| 3.2.5 | 创建 TagBase | name (str, max_length=50) | 基础模型定义正确 |
| 3.2.6 | 创建 TagResponse | 继承 TagBase，增加 id、ticket_count | 响应模型完整 |
| 3.2.7 | 创建列表响应模型 | TicketListResponse: items + total | 分页响应可用 |

### 任务 3.3：实现 Ticket 业务逻辑

**文件**：`backend/app/services/ticket_service.py`

| 序号 | 任务内容 | 详细说明 | 验收标准 |
|------|---------|---------|---------|
| 3.3.1 | 实现 create_ticket | 创建 Ticket，自动创建/关联标签，返回 TicketResponse | 可成功创建，标签正确关联 |
| 3.3.2 | 实现 get_ticket | 根据 ID 查询，不存在返回 None | 查询结果正确 |
| 3.3.3 | 实现 get_tickets | 支持分页、排序、标签筛选、状态筛选、搜索 | 筛选和搜索功能正常 |
| 3.3.4 | 实现 update_ticket | 更新标题、描述、标签，自动更新时间戳 | 更新成功，标签同步更新 |
| 3.3.5 | 实现 delete_ticket | 级联删除关联记录 | 删除成功，关联表数据清理 |
| 3.3.6 | 实现 complete_ticket | 设置 status='closed'，记录 completed_at | 状态变更正确 |
| 3.3.7 | 实现 uncomplete_ticket | 设置 status='open'，清空 completed_at | 状态恢复正确 |
| 3.3.8 | 实现 search_tickets | 使用 ILIKE 模糊匹配标题 | 搜索结果准确 |
| 3.3.9 | 实现 filter_by_tags | 支持单标签和多标签筛选 | 筛选结果正确 |

### 任务 3.4：实现标签业务逻辑

**文件**：`backend/app/services/tag_service.py`

| 序号 | 任务内容 | 详细说明 | 验收标准 |
|------|---------|---------|---------|
| 3.4.1 | 实现 get_or_create_tag | 根据名称获取或创建标签，名称转小写 | 标签唯一，不区分大小写 |
| 3.4.2 | 实现 get_tags | 查询所有标签，统计关联 Ticket 数量 | 返回标签列表和数量 |
| 3.4.3 | 实现 get_tag_by_name | 根据名称查询标签 | 查询结果正确 |
| 3.4.4 | 实现 delete_tag | 删除标签及其所有关联 | 删除成功，关联清理 |
| 3.4.5 | 实现 get_tickets_by_tag | 获取指定标签下的所有 Ticket | 返回结果正确 |

### 任务 3.5：实现 Ticket API 路由

**文件**：`backend/app/routers/tickets.py`

| 序号 | 任务内容 | 详细说明 | 验收标准 |
|------|---------|---------|---------|
| 3.5.1 | GET /api/tickets | 列表查询，支持 tags、search、status、sort 查询参数 | 返回正确数据 |
| 3.5.2 | GET /api/tickets/{id} | 单个查询，404 处理 | 返回正确数据或 404 |
| 3.5.3 | POST /api/tickets | 创建，201 状态码，验证输入 | 创建成功，返回 201 |
| 3.5.4 | PUT /api/tickets/{id} | 全量更新，404 处理 | 更新成功 |
| 3.5.5 | DELETE /api/tickets/{id} | 删除，204 状态码 | 删除成功，返回 204 |
| 3.5.6 | PATCH /api/tickets/{id}/complete | 完成操作 | 状态变为 closed |
| 3.5.7 | PATCH /api/tickets/{id}/uncomplete | 取消完成 | 状态变为 open |

### 任务 3.6：实现标签 API 路由

**文件**：`backend/app/routers/tags.py`

| 序号 | 任务内容 | 详细说明 | 验收标准 |
|------|---------|---------|---------|
| 3.6.1 | GET /api/tags | 获取所有标签及 Ticket 数量 | 返回正确数据 |
| 3.6.2 | GET /api/tags/{name}/tickets | 获取标签下 Ticket 列表 | 返回正确数据 |
| 3.6.3 | DELETE /api/tags/{name} | 删除标签及关联 | 删除成功，返回 204 |

### 任务 3.7：后端测试

| 序号 | 任务内容 | 详细说明 | 验收标准 |
|------|---------|---------|---------|
| 3.7.1 | 配置测试环境 | 创建 conftest.py，配置异步测试数据库 | 测试数据库隔离 |
| 3.7.2 | 编写 Ticket 单元测试 | 测试所有 Service 方法 | 覆盖率 > 80% |
| 3.7.3 | 编写 Ticket API 测试 | 测试所有 API 端点 | 覆盖率 > 90% |
| 3.7.4 | 编写标签测试 | 测试标签 Service 和 API | 覆盖率 > 80% |
| 3.7.5 | 运行测试 | `pytest --cov=app` | 所有测试通过 |

---

## 阶段四：前端开发

**目标**：实现用户界面，包括 Ticket 列表、表单、标签筛选、搜索等功能

**预计耗时**：4-5 天

### 任务 4.1：配置前端项目

| 序号 | 任务内容 | 详细说明 | 验收标准 |
|------|---------|---------|---------|
| 4.1.1 | 配置 Axios 实例 | `backend/app/api/index.js`，设置 baseURL、超时、拦截器 | 可正确发送请求 |
| 4.1.2 | 配置 Pinia Store | 创建 ticket.js 和 tag.js | Store 可正常使用 |
| 4.1.3 | 配置全局样式 | `styles/main.css`，设置基础样式、变量 | 样式生效 |
| 4.1.4 | 配置环境变量 | `.env` 设置 VITE_API_BASE_URL | 环境变量可用 |

### 任务 4.2：实现 API 调用层

**文件**：`frontend/src/api/tickets.js`、`frontend/src/api/tags.js`

| 序号 | 任务内容 | 详细说明 | 验收标准 |
|------|---------|---------|---------|
| 4.2.1 | tickets API | getTickets、getTicket、createTicket、updateTicket、deleteTicket、completeTicket、uncompleteTicket | 所有方法可用 |
| 4.2.2 | tags API | getTags、getTagTickets、deleteTag | 所有方法可用 |

### 任务 4.3：实现状态管理

**文件**：`frontend/src/stores/ticket.js`、`frontend/src/stores/tag.js`

| 序号 | 任务内容 | 详细说明 | 验收标准 |
|------|---------|---------|---------|
| 4.3.1 | ticket store | state: tickets, loading, error；actions: fetch、create、update、delete、complete | 状态管理正常 |
| 4.3.2 | tag store | state: tags, loading, error；actions: fetch、select、clear | 状态管理正常 |
| 4.3.3 | 筛选状态 | selectedTags、searchKeyword、statusFilter | 筛选状态同步 |

### 任务 4.4：实现基础组件

| 序号 | 任务内容 | 详细说明 | 验收标准 |
|------|---------|---------|---------|
| 4.4.1 | SearchBar.vue | 输入框，支持实时搜索，防抖处理（300ms） | 输入后自动搜索 |
| 4.4.2 | StatusFilter.vue | 三个选项：全部/未完成/已完成 | 切换筛选状态 |
| 4.4.3 | TagSidebar.vue | 标签列表，显示数量，点击筛选，多选支持 | 点击标签筛选 Ticket |

### 任务 4.5：实现 Ticket 列表组件

| 序号 | 任务内容 | 详细说明 | 验收标准 |
|------|---------|---------|---------|
| 4.5.1 | TicketItem.vue | 显示标题、标签、状态、时间，操作按钮 | 渲染正确 |
| 4.5.2 | 完成/取消功能 | 点击复选框切换状态 | 状态切换正确 |
| 4.5.3 | 删除功能 | 点击删除按钮，确认对话框 | 删除前确认 |
| 4.5.4 | 编辑功能 | 点击编辑按钮，打开表单 | 可进入编辑模式 |
| 4.5.5 | TicketList.vue | 列表容器，空状态处理，加载状态 | 列表展示正确 |

### 任务 4.6：实现 Ticket 表单组件

| 序号 | 任务内容 | 详细说明 | 验收标准 |
|------|---------|---------|---------|
| 4.6.1 | TicketForm.vue | 弹窗/抽屉形式，包含标题输入、描述文本域、标签输入 | 表单布局正确 |
| 4.6.2 | 表单验证 | 标题必填，最大长度 200，标签去重 | 验证提示正确 |
| 4.6.3 | 标签输入 | 支持逗号分隔、回车添加、点击删除 | 标签交互正常 |
| 4.6.4 | 创建模式 | 提交后清空表单，刷新列表 | 创建流程完整 |
| 4.6.5 | 编辑模式 | 回填数据，提交后更新列表 | 编辑流程完整 |

### 任务 4.7：实现主页面布局

**文件**：`frontend/src/App.vue`

| 序号 | 任务内容 | 详细说明 | 验收标准 |
|------|---------|---------|---------|
| 4.7.1 | 布局结构 | Header + 侧边栏 + 主内容区 | 布局正确 |
| 4.7.2 | 响应式适配 | 移动端侧边栏可折叠 | 适配不同屏幕 |
| 4.7.3 | 全局状态联动 | 筛选、搜索、列表联动更新 | 数据流正确 |

### 任务 4.8：前端测试

| 序号 | 任务内容 | 详细说明 | 验收标准 |
|------|---------|---------|---------|
| 4.8.1 | 组件单元测试 | TicketItem、TicketForm、TagSidebar | 测试通过 |
| 4.8.2 | Store 测试 | ticket store、tag store | 测试通过 |
| 4.8.3 | E2E 测试 | 创建、完成、删除、搜索完整流程 | 测试通过 |

---

## 阶段五：集成测试与优化

**目标**：前后端联调，修复 Bug，性能优化

**预计耗时**：2-3 天

### 任务 5.1：前后端联调

| 序号 | 任务内容 | 详细说明 | 验收标准 |
|------|---------|---------|---------|
| 5.1.1 | 启动后端服务 | `uvicorn app.main:app --reload` | 服务运行在 8000 端口 |
| 5.1.2 | 启动前端服务 | `npm run dev` | 服务运行在 5173 端口 |
| 5.1.3 | 验证 CORS | 前端可正常调用后端 API | 无跨域错误 |
| 5.1.4 | 完整功能测试 | 按功能需求逐一验证 | 所有功能正常 |

### 任务 5.2：Bug 修复

| 序号 | 任务内容 | 详细说明 | 验收标准 |
|------|---------|---------|---------|
| 5.2.1 | 记录 Bug | 使用 GitHub Issues 或本地文档记录 | 问题可追溯 |
| 5.2.2 | 修复高优先级 Bug | 影响核心功能的 Bug | 修复验证通过 |
| 5.2.3 | 修复中优先级 Bug | 影响体验的 Bug | 修复验证通过 |
| 5.2.4 | 回归测试 | 修复后重新测试相关功能 | 无引入新问题 |

### 任务 5.3：性能优化

| 序号 | 任务内容 | 详细说明 | 验收标准 |
|------|---------|---------|---------|
| 5.3.1 | 后端查询优化 | 检查慢查询，添加必要索引 | 查询响应 < 200ms |
| 5.3.2 | 前端加载优化 | 组件懒加载、资源压缩 | 首屏加载 < 3s |
| 5.3.3 | 防抖节流优化 | 搜索输入防抖，按钮点击节流 | 无频繁请求 |

### 任务 5.4：代码质量

| 序号 | 任务内容 | 详细说明 | 验收标准 |
|------|---------|---------|---------|
| 5.4.1 | 后端代码格式化 | `black app/ tests/` | 代码风格统一 |
| 5.4.2 | 后端代码检查 | `flake8 app/ tests/` | 无语法和风格错误 |
| 5.4.3 | 前端代码格式化 | `npm run format` | 代码风格统一 |
| 5.4.4 | 前端代码检查 | `npm run lint` | 无语法和风格错误 |

---

## 阶段六：部署与交付

**目标**：配置生产环境，完成本地部署，编写部署文档

**预计耗时**：1-2 天

### 任务 6.1：生产环境配置

| 序号 | 任务内容 | 详细说明 | 验收标准 |
|------|---------|---------|---------|
| 6.1.1 | 创建生产环境变量 | `.env.production`，DEBUG=False | 配置正确 |
| 6.1.2 | 配置日志 | 日志文件路径、轮转策略 | 日志正常写入 |
| 6.1.3 | 配置 CORS | 仅允许生产前端地址 | 安全配置正确 |

### 任务 6.2：本地部署

| 序号 | 任务内容 | 详细说明 | 验收标准 |
|------|---------|---------|---------|
| 6.2.1 | 生产数据库迁移 | `alembic upgrade head` | 生产数据库表创建 |
| 6.2.2 | 启动后端生产服务 | `uvicorn app.main:app --workers 4` | 服务稳定运行 |
| 6.2.3 | 构建前端生产包 | `npm run build` | dist 目录生成 |
| 6.2.4 | 配置前端静态服务 | 使用 serve 或 nginx | 前端可访问 |

### 任务 6.3：服务管理配置

| 序号 | 任务内容 | 详细说明 | 验收标准 |
|------|---------|---------|---------|
| 6.3.1 | Windows 服务配置 | 使用 NSSM 注册后端服务 | 可开机自启 |
| 6.3.2 | Linux 服务配置 | 创建 systemd 服务单元 | 可开机自启 |
| 6.3.3 | 数据库备份脚本 | 创建定时备份脚本 | 备份文件生成 |

### 任务 6.4：文档完善

| 序号 | 任务内容 | 详细说明 | 验收标准 |
|------|---------|---------|---------|
| 6.4.1 | 编写部署文档 | 包含环境准备、安装步骤、启动命令 | 文档完整 |
| 6.4.2 | 编写使用说明 | 功能介绍、操作指南 | 用户可上手 |
| 6.4.3 | 编写 API 文档 | 使用 Swagger UI 自动生成 | API 文档可访问 |

---

## 里程碑与交付物

### 里程碑一：环境就绪（阶段一完成）
- 开发环境安装完成
- 项目目录结构创建
- 前后端项目初始化成功
- Git 仓库配置完成

### 里程碑二：数据层完成（阶段二完成）
- PostgreSQL 数据库配置完成
- SQLAlchemy 模型定义完成
- Alembic 迁移配置完成
- 数据库表创建成功

### 里程碑三：API 完成（阶段三完成）
- 所有 API 端点实现完成
- Pydantic 模型定义完成
- 业务逻辑实现完成
- 后端测试通过

### 里程碑四：界面完成（阶段四完成）
- 所有前端组件实现完成
- 状态管理配置完成
- API 调用层实现完成
- 前端测试通过

### 里程碑五：系统可用（阶段五完成）
- 前后端联调成功
- 所有功能验证通过
- 主要 Bug 修复完成
- 性能达到要求

### 里程碑六：项目交付（阶段六完成）
- 生产环境部署完成
- 服务开机自启配置完成
- 部署文档编写完成
- 项目可稳定运行

---

## 时间规划

| 阶段 | 内容 | 预计耗时 | 累计耗时 |
|------|------|---------|---------|
| 阶段一 | 环境准备与项目初始化 | 1-2 天 | 1-2 天 |
| 阶段二 | 数据库设计与实现 | 1-2 天 | 2-4 天 |
| 阶段三 | 后端 API 开发 | 3-4 天 | 5-8 天 |
| 阶段四 | 前端开发 | 4-5 天 | 9-13 天 |
| 阶段五 | 集成测试与优化 | 2-3 天 | 11-16 天 |
| 阶段六 | 部署与交付 | 1-2 天 | 12-18 天 |

**总预计工期**：12-18 天（单人全职开发）

---

## 风险与应对

| 风险 | 影响 | 应对措施 |
|------|------|---------|
| PostgreSQL 安装配置问题 | 高 | 提前测试安装，准备多种安装方案 |
| 异步 SQLAlchemy 学习曲线 | 中 | 预留学习时间，参考官方文档示例 |
| 前端组件交互复杂度 | 中 | 先实现基础功能，再优化交互 |
| 跨域问题 | 低 | 提前配置 CORS，测试环境验证 |
| 数据库迁移失败 | 中 | 备份数据，使用 Alembic 回滚机制 |

---

## 开发规范

### Git 提交规范
```
<type>: <subject>

<body>

type 类型:
- feat: 新功能
- fix: 修复
- docs: 文档
- style: 格式
- refactor: 重构
- test: 测试
- chore: 构建/工具

示例:
feat: 实现 Ticket 创建 API
fix: 修复标签筛选逻辑错误
docs: 更新部署文档
```

### 代码风格
- **后端**：遵循 PEP 8，使用 Black 格式化，行宽 88 字符
- **前端**：遵循 Vue 风格指南，使用 Prettier 格式化
- **命名**：函数/变量使用 snake_case，类使用 PascalCase，常量使用 UPPER_SNAKE_CASE

### 分支策略
```
main        # 生产分支，稳定版本
develop     # 开发分支，日常开发
feature/*   # 功能分支，从 develop 创建
fix/*       # 修复分支，从 develop 创建
```