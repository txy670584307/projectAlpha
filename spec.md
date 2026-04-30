# projectAlpha - 标签化 Ticket 管理工具

## 1. 项目概述

### 1.1 项目背景
projectAlpha 是一个简单轻量级的 Ticket 管理工具，核心特色是使用标签（Tag）对 Ticket 进行分类和管理。项目面向个人或小团队使用，无需用户认证系统，开箱即用。

### 1.2 项目目标
- 提供一个简洁直观的 Ticket 管理界面
- 通过标签系统实现灵活的分类和筛选
- 支持 Ticket 的全生命周期管理（创建、编辑、完成、取消）

---

## 2. 技术栈详细说明

### 2.1 后端技术栈

#### 2.1.1 FastAPI
| 属性 | 详情 |
|------|------|
| 版本 | 0.115.x |
| 官网 | https://fastapi.tiangolo.com/ |
| 特性 | 基于 ASGI 的高性能 Web 框架，自动生成交互式 API 文档（Swagger UI + ReDoc），原生异步支持，基于 Pydantic 的数据验证 |
| 选择理由 | 性能优异（与 NodeJS 和 Go 相当），开发效率高，类型提示完善，适合快速构建 RESTful API |

#### 2.1.2 SQLAlchemy
| 属性 | 详情 |
|------|------|
| 版本 | 2.0.36+ |
| 官网 | https://www.sqlalchemy.org/ |
| 特性 | Python 最流行的 ORM 框架，支持声明式模型、关系映射、事务管理、连接池 |
| 选择理由 | 功能强大且成熟稳定，与 FastAPI 完美集成，支持异步操作 |

#### 2.1.3 Alembic
| 属性 | 详情 |
|------|------|
| 版本 | 1.14.x |
| 官网 | https://alembic.sqlalchemy.org/ |
| 特性 | SQLAlchemy 官方数据库迁移工具，支持版本控制、自动迁移脚本生成、回滚 |
| 选择理由 | 与 SQLAlchemy 无缝集成，管理数据库 schema 变更 |

#### 2.1.4 Uvicorn
| 属性 | 详情 |
|------|------|
| 版本 | 0.34.x |
| 官网 | https://www.uvicorn.org/ |
| 特性 | 基于 uvloop 和 httptools 的 ASGI 服务器，高性能异步 HTTP 服务 |
| 选择理由 | FastAPI 推荐的 ASGI 服务器，生产环境可配合 Gunicorn 使用 |

#### 2.1.5 Pydantic
| 属性 | 详情 |
|------|------|
| 版本 | 2.10.x |
| 官网 | https://docs.pydantic.dev/ |
| 特性 | 基于 Python 类型提示的数据验证库，FastAPI 内置使用 |
| 选择理由 | 强大的数据验证和序列化能力，自动生成 JSON Schema |

#### 2.1.6 psycopg2-binary
| 属性 | 详情 |
|------|------|
| 版本 | 2.9.10+ |
| 官网 | https://www.psycopg.org/ |
| 特性 | PostgreSQL 数据库适配器，支持同步连接 |
| 选择理由 | 稳定可靠的 PostgreSQL 驱动，开发环境使用 binary 版本简化安装 |

#### 2.1.7 asyncpg
| 属性 | 详情 |
|------|------|
| 版本 | 0.30.x |
| 官网 | https://magicstack.github.io/asyncpg/ |
| 特性 | 高性能异步 PostgreSQL 驱动，支持原生 PostgreSQL 协议 |
| 选择理由 | 配合 SQLAlchemy 异步模式使用，性能优于同步驱动 |

### 2.2 前端技术栈

#### 2.2.1 Vue 3
| 属性 | 详情 |
|------|------|
| 版本 | 3.5.x |
| 官网 | https://vuejs.org/ |
| 特性 | 组合式 API、响应式系统、组件化开发、虚拟 DOM |
| 选择理由 | 渐进式框架，学习曲线平缓，生态完善，适合中小型项目 |

#### 2.2.2 Vite
| 属性 | 详情 |
|------|------|
| 版本 | 6.x |
| 官网 | https://vitejs.dev/ |
| 特性 | 基于 ESM 的下一代前端构建工具，极速冷启动，热模块替换（HMR） |
| 选择理由 | 构建速度远超 Webpack，开发体验优秀 |

#### 2.2.3 Pinia
| 属性 | 详情 |
|------|------|
| 版本 | 2.3.x |
| 官网 | https://pinia.vuejs.org/ |
| 特性 | Vue 官方推荐的状态管理库，支持 TypeScript，模块化设计 |
| 选择理由 | 比 Vuex 更简洁，更好的 TypeScript 支持，Vue 3 官方推荐 |

#### 2.2.4 Axios
| 属性 | 详情 |
|------|------|
| 版本 | 1.7.x |
| 官网 | https://axios-http.com/ |
| 特性 | 基于 Promise 的 HTTP 客户端，支持请求/响应拦截器，自动 JSON 转换 |
| 选择理由 | 简单易用，功能完善，社区活跃 |

### 2.3 数据库技术栈

#### 2.3.1 PostgreSQL
| 属性 | 详情 |
|------|------|
| 版本 | 15.x 或更高 |
| 官网 | https://www.postgresql.org/ |
| 特性 | 开源关系型数据库，支持 ACID 事务、复杂查询、外键、触发器、视图、存储过程 |
| 选择理由 | 功能强大，可靠性高，支持复杂数据类型和高级查询特性 |

### 2.4 开发工具

| 工具 | 用途 |
|------|------|
| Python 3.11+ | 后端运行时 |
| Node.js 18+ | 前端运行时 |
| pip / venv | Python 包管理和虚拟环境 |
| npm / pnpm | 前端包管理 |
| Git | 版本控制 |
| Postman / Swagger UI | API 测试 |

---

## 3. 功能需求

### 3.1 Ticket 管理

#### 3.1.1 创建 Ticket
- 用户可以创建新的 Ticket
- 必填字段：标题（title）
- 可选字段：描述（description）、标签（tags）
- 创建后状态默认为"未完成"

#### 3.1.2 编辑 Ticket
- 用户可以修改已有 Ticket 的标题和描述
- 可以添加或移除标签
- 修改后自动保存

#### 3.1.3 删除 Ticket
- 用户可以永久删除 Ticket
- 删除前应有确认提示（前端实现）

#### 3.1.4 完成 Ticket
- 用户可以将 Ticket 标记为"已完成"
- 完成后显示完成时间

#### 3.1.5 取消完成 Ticket
- 用户可以将已完成的 Ticket 重新标记为"未完成"
- 清除完成时间

### 3.2 标签管理

#### 3.2.1 添加标签
- 创建或编辑 Ticket 时可以为其添加标签
- 标签支持自定义输入
- 标签名称不区分大小写，同一标签不会重复创建

#### 3.2.2 删除标签
- 可以从 Ticket 上移除标签
- 删除标签不影响其他带有该标签的 Ticket

### 3.3 查看与筛选

#### 3.3.1 按标签查看
- 用户可以点击某个标签，查看该标签下的所有 Ticket
- 支持同时选择多个标签进行筛选（与/或逻辑）
- 显示每个标签关联的 Ticket 数量

#### 3.3.2 按标题搜索
- 提供搜索框，支持通过标题关键词搜索 Ticket
- 支持模糊匹配
- 搜索结果实时更新

### 3.4 Ticket 列表展示
- 以列表形式展示 Ticket
- 显示字段：标题、标签列表、状态（已完成/未完成）、创建时间
- 支持按状态筛选（全部/未完成/已完成）
- 支持按创建时间排序

---

## 4. 系统设计

### 4.1 系统架构

```
+-------------------------------------------------+
|                   前端 (Vue 3)                   |
|  +-------------+ +-------------+ +-------------+ |
|  | Ticket列表   | | Ticket编辑   | |  标签筛选器  | |
|  +-------------+ +-------------+ +-------------+ |
+-------------------------------------------------+
                        |
                        | HTTP/REST API
                        v
+-------------------------------------------------+
|              后端 (FastAPI)                       |
|  +-------------+ +-------------+ +-------------+ |
|  | Ticket API  | |  Tag API    | |  Search API | |
|  +-------------+ +-------------+ +-------------+ |
+-------------------------------------------------+
                        |
                        | SQLAlchemy ORM
                        v
+-------------------------------------------------+
|             数据库 (PostgreSQL)                   |
|  +-------------+ +-------------+ +-------------+ |
|  |  tickets    | |   tags      | |ticket_tags  | |
|  +-------------+ +-------------+ +-------------+ |
+-------------------------------------------------+
```

### 4.2 数据库设计

#### 4.2.1 数据表结构

**tickets 表**
| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | INTEGER | PRIMARY KEY, GENERATED ALWAYS AS IDENTITY | 主键 |
| title | VARCHAR(200) | NOT NULL | 标题 |
| description | TEXT | NULL | 描述 |
| status | VARCHAR(20) | NOT NULL, DEFAULT 'open' | 状态：open/closed |
| created_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 更新时间 |
| completed_at | TIMESTAMP | NULL | 完成时间 |

**tags 表**
| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | INTEGER | PRIMARY KEY, GENERATED ALWAYS AS IDENTITY | 主键 |
| name | VARCHAR(50) | NOT NULL, UNIQUE | 标签名称 |
| created_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |

**ticket_tags 表**（关联表）
| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| ticket_id | INTEGER | PRIMARY KEY, FOREIGN KEY -> tickets(id) ON DELETE CASCADE | 关联 tickets.id |
| tag_id | INTEGER | PRIMARY KEY, FOREIGN KEY -> tags(id) ON DELETE CASCADE | 关联 tags.id |

#### 4.2.2 ER 图
```
+-------------+       +--------------+       +-------------+
|   tickets   |       | ticket_tags  |       |    tags     |
+-------------+       +--------------+       +-------------+
| id (PK)     |--+  +--| ticket_id(PK)|    +--| id (PK)     |
| title       |  |  |  | tag_id (PK)  |--+ |  | name        |
| description |  +--|  |              |  | |  | created_at  |
| status      |     |  +--------------+  | |  +-------------+
| created_at  |     |                    | |
| updated_at  |     +--------------------+ |
| completed_at|                            |
+-------------+                            +-------------+
```

#### 4.2.3 数据库建表语句

```sql
-- ============================================
-- projectAlpha 数据库建表脚本
-- 数据库: PostgreSQL 15+
-- 字符集: UTF8
-- ============================================

-- 创建数据库（如果不存在）
-- CREATE DATABASE projectalpha WITH ENCODING 'UTF8';

-- 连接到数据库后执行以下语句

-- 启用 UUID 扩展（可选，未来扩展使用）
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================
-- 1. 创建 tickets 表
-- ============================================
CREATE TABLE tickets (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    status VARCHAR(20) NOT NULL DEFAULT 'open' CHECK (status IN ('open', 'closed')),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP
);

-- 创建索引以提升查询性能
CREATE INDEX idx_tickets_status ON tickets(status);
CREATE INDEX idx_tickets_created_at ON tickets(created_at DESC);

-- 创建全文搜索索引用于标题搜索
CREATE INDEX idx_tickets_title_search ON tickets USING gin(to_tsvector('simple', title));

-- 添加表注释
COMMENT ON TABLE tickets IS 'Ticket 主表，存储所有工单信息';
COMMENT ON COLUMN tickets.id IS '主键 ID';
COMMENT ON COLUMN tickets.title IS 'Ticket 标题';
COMMENT ON COLUMN tickets.description IS 'Ticket 详细描述';
COMMENT ON COLUMN tickets.status IS '状态：open-未完成, closed-已完成';
COMMENT ON COLUMN tickets.created_at IS '创建时间';
COMMENT ON COLUMN tickets.updated_at IS '最后更新时间';
COMMENT ON COLUMN tickets.completed_at IS '完成时间';

-- ============================================
-- 2. 创建 tags 表
-- ============================================
CREATE TABLE tags (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 创建索引
CREATE INDEX idx_tags_name ON tags(name);

-- 添加表注释
COMMENT ON TABLE tags IS '标签表，存储所有可用的标签';
COMMENT ON COLUMN tags.id IS '主键 ID';
COMMENT ON COLUMN tags.name IS '标签名称，唯一';
COMMENT ON COLUMN tags.created_at IS '创建时间';

-- ============================================
-- 3. 创建 ticket_tags 关联表
-- ============================================
CREATE TABLE ticket_tags (
    ticket_id INTEGER NOT NULL REFERENCES tickets(id) ON DELETE CASCADE,
    tag_id INTEGER NOT NULL REFERENCES tags(id) ON DELETE CASCADE,
    PRIMARY KEY (ticket_id, tag_id)
);

-- 创建索引以提升反向查询性能
CREATE INDEX idx_ticket_tags_tag_id ON ticket_tags(tag_id);

-- 添加表注释
COMMENT ON TABLE ticket_tags IS 'Ticket 和 Tag 的多对多关联表';
COMMENT ON COLUMN ticket_tags.ticket_id IS '关联的 Ticket ID';
COMMENT ON COLUMN ticket_tags.tag_id IS '关联的 Tag ID';

-- ============================================
-- 4. 创建自动更新时间戳的触发器函数
-- ============================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- 为 tickets 表添加触发器
CREATE TRIGGER update_tickets_updated_at
    BEFORE UPDATE ON tickets
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- 5. 创建常用视图和查询函数
-- ============================================

-- 创建标签统计视图（显示每个标签关联的 Ticket 数量）
CREATE OR REPLACE VIEW tag_statistics AS
SELECT 
    t.id,
    t.name,
    COUNT(tt.ticket_id) AS ticket_count,
    COUNT(CASE WHEN tk.status = 'open' THEN 1 END) AS open_ticket_count,
    COUNT(CASE WHEN tk.status = 'closed' THEN 1 END) AS closed_ticket_count
FROM tags t
LEFT JOIN ticket_tags tt ON t.id = tt.tag_id
LEFT JOIN tickets tk ON tt.ticket_id = tk.id
GROUP BY t.id, t.name;

COMMENT ON VIEW tag_statistics IS '标签统计视图，包含每个标签的 Ticket 数量统计';

-- ============================================
-- 6. 插入测试数据（可选）
-- ============================================

-- 插入示例标签
INSERT INTO tags (name) VALUES 
    ('bug'),
    ('feature'),
    ('urgent'),
    ('frontend'),
    ('backend'),
    ('documentation'),
    ('enhancement'),
    ('wontfix')
ON CONFLICT (name) DO NOTHING;

-- 插入示例 Ticket
INSERT INTO tickets (title, description, status) VALUES 
    ('修复登录页面布局问题', '用户反馈登录页面在移动端显示异常，按钮重叠', 'open'),
    ('实现用户注册功能', '添加用户注册表单和验证逻辑', 'closed'),
    ('优化数据库查询性能', '对慢查询进行优化，添加必要索引', 'open'),
    ('更新 API 文档', '补充缺失的 API 接口文档', 'open'),
    ('添加标签筛选功能', '在 Ticket 列表页面添加按标签筛选的功能', 'closed');

-- 关联 Ticket 和标签
INSERT INTO ticket_tags (ticket_id, tag_id) VALUES 
    (1, 1),  -- bug
    (1, 4),  -- frontend
    (1, 3),  -- urgent
    (2, 2),  -- feature
    (2, 5),  -- backend
    (3, 5),  -- backend
    (3, 7),  -- enhancement
    (4, 6),  -- documentation
    (5, 2),  -- feature
    (5, 4)   -- frontend
ON CONFLICT (ticket_id, tag_id) DO NOTHING;

-- ============================================
-- 完成
-- ============================================
```

### 4.3 API 设计

#### 4.3.1 Ticket 相关 API

| 方法 | 路径 | 说明 | 请求体 | 响应 |
|------|------|------|--------|------|
| GET | /api/tickets | 获取 Ticket 列表 | query: tags, search, status, sort | Ticket[] |
| GET | /api/tickets/{id} | 获取单个 Ticket | - | Ticket |
| POST | /api/tickets | 创建 Ticket | {title, description, tags} | Ticket |
| PUT | /api/tickets/{id} | 更新 Ticket | {title, description, tags} | Ticket |
| DELETE | /api/tickets/{id} | 删除 Ticket | - | 204 No Content |
| PATCH | /api/tickets/{id}/complete | 完成 Ticket | - | Ticket |
| PATCH | /api/tickets/{id}/uncomplete | 取消完成 | - | Ticket |

#### 4.3.2 标签相关 API

| 方法 | 路径 | 说明 | 请求体 | 响应 |
|------|------|------|--------|------|
| GET | /api/tags | 获取所有标签及数量 | - | Tag[] |
| GET | /api/tags/{name}/tickets | 获取某标签下的 Ticket | query: status | Ticket[] |
| DELETE | /api/tags/{name} | 删除标签（所有关联） | - | 204 No Content |

#### 4.3.3 搜索 API

| 方法 | 路径 | 说明 | 请求体 | 响应 |
|------|------|------|--------|------|
| GET | /api/tickets?search=keyword | 按标题搜索 | search (query param) | Ticket[] |

#### 4.3.4 数据模型定义

**Ticket 响应模型**
```json
{
  "id": 1,
  "title": "修复登录页面bug",
  "description": "用户反馈登录页面在移动端显示异常",
  "status": "open",
  "tags": ["bug", "frontend", "urgent"],
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T14:20:00",
  "completed_at": null
}
```

**Tag 响应模型**
```json
{
  "id": 1,
  "name": "bug",
  "ticket_count": 5
}
```

### 4.4 前端设计

#### 4.4.1 页面结构
```
+----------------------------------------------------------+
|  Header: projectAlpha - Ticket 管理                       |
+----------------------+-----------------------------------+
|  侧边栏              |           主内容区                  |
|  +----------------+  |  +-------------------------------+ |
|  | 标签列表        |  |  | 搜索框                        | |
|  | - bug (5)      |  |  +-------------------------------+ |
|  | - feature (3)  |  |  | 状态筛选: 全部 / 未完成 / 已完成| |
|  | - urgent (2)   |  |  +-------------------------------+ |
|  | - backend (4)  |  |  | Ticket 列表                   | |
|  | ...            |  |  | +---------------------------+ | |
|  +----------------+  |  | | [ ] 修复登录页面bug        | | |
|                      |  | |   [bug] [frontend] [urgent]| | |
|  新建 Ticket 按钮     |  | |   2024-01-15       [edit][del]| |
|                      |  | +---------------------------+ | |
|                      |  | | [x] 实现用户注册功能        | | |
|                      |  | |   [feature] [backend]      | | |
|                      |  | |   2024-01-14       [edit][del]| |
|                      |  | +---------------------------+ | |
|                      |  +-------------------------------+ |
+----------------------+-----------------------------------+
```

#### 4.4.2 组件设计

| 组件名 | 说明 | 主要功能 |
|--------|------|----------|
| App.vue | 根组件 | 布局容器，全局状态管理 |
| TicketList.vue | Ticket 列表 | 展示 Ticket 列表，支持分页/排序 |
| TicketItem.vue | Ticket 项 | 单个 Ticket 展示，状态切换，删除 |
| TicketForm.vue | Ticket 表单 | 创建/编辑 Ticket 的弹窗表单 |
| TagSidebar.vue | 标签侧边栏 | 标签列表展示，点击筛选 |
| SearchBar.vue | 搜索栏 | 关键词搜索输入 |
| StatusFilter.vue | 状态筛选 | 按状态筛选 Ticket |

#### 4.4.3 状态管理
使用 Vue 3 的 Composition API + Pinia 进行状态管理

**主要状态**
- tickets: Ticket[] - 当前 Ticket 列表
- tags: Tag[] - 所有标签列表
- selectedTags: string[] - 当前选中的筛选标签
- searchKeyword: string - 当前搜索关键词
- statusFilter: string - 状态筛选条件

---

## 5. 项目结构

### 5.1 后端目录结构
```
backend/
+-- app/
|   +-- __init__.py
|   +-- main.py              # FastAPI 应用入口
|   +-- config.py            # 配置文件
|   +-- database.py          # 数据库连接
|   +-- models/
|   |   +-- __init__.py
|   |   +-- ticket.py        # Ticket 数据模型
|   |   +-- tag.py           # Tag 数据模型
|   +-- schemas/
|   |   +-- __init__.py
|   |   +-- ticket.py        # Ticket Pydantic 模型
|   |   +-- tag.py           # Tag Pydantic 模型
|   +-- routers/
|   |   +-- __init__.py
|   |   +-- tickets.py       # Ticket API 路由
|   |   +-- tags.py          # Tag API 路由
|   +-- services/
|   |   +-- __init__.py
|   |   +-- ticket_service.py    # Ticket 业务逻辑
|   |   +-- tag_service.py       # Tag 业务逻辑
+-- alembic/                 # 数据库迁移
|   +-- versions/
|   +-- alembic.ini
+-- tests/
|   +-- __init__.py
|   +-- conftest.py          # pytest 配置
|   +-- test_tickets.py      # Ticket API 测试
|   +-- test_tags.py         # Tag API 测试
+-- venv/                    # Python 虚拟环境
+-- logs/                    # 日志目录
|   +-- access.log
|   +-- error.log
+-- requirements.txt
+-- requirements-dev.txt     # 开发依赖
+-- .env                     # 环境变量
+-- .env.example             # 环境变量示例
+-- .gitignore               # Git 忽略文件
```

### 5.2 前端目录结构
```
frontend/
+-- src/
|   +-- main.js              # 入口文件
|   +-- App.vue              # 根组件
|   +-- api/
|   |   +-- index.js         # Axios 实例配置
|   |   +-- tickets.js       # Ticket API 调用
|   |   +-- tags.js          # Tag API 调用
|   +-- components/
|   |   +-- TicketList.vue
|   |   +-- TicketItem.vue
|   |   +-- TicketForm.vue
|   |   +-- TagSidebar.vue
|   |   +-- SearchBar.vue
|   |   +-- StatusFilter.vue
|   +-- stores/
|   |   +-- ticket.js        # Ticket 状态管理
|   |   +-- tag.js           # Tag 状态管理
|   +-- styles/
|   |   +-- main.css         # 全局样式
|   +-- utils/
|   |   +-- helpers.js       # 工具函数
+-- tests/
|   +-- unit/                # 单元测试
|   +-- e2e/                 # 端到端测试
+-- logs/                    # 日志目录
|   +-- frontend.log
+-- package.json
+-- vite.config.js
+-- index.html
+-- .env                     # 环境变量
+-- .env.example             # 环境变量示例
```

---

## 6. 环境配置

### 6.1 环境变量

#### 6.1.1 开发环境 (.env.development)
```env
# 数据库配置
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/projectalpha_dev

# 应用配置
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# 日志配置
LOG_LEVEL=DEBUG
```

#### 6.1.2 生产环境 (.env.production)
```env
# 数据库配置
DATABASE_URL=postgresql://projectalpha_user:YOUR_SECURE_PASSWORD@localhost:5432/projectalpha

# 应用配置
API_HOST=127.0.0.1
API_PORT=8000
DEBUG=False

# CORS 配置（根据实际部署调整）
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# 日志配置
LOG_LEVEL=INFO
```

#### 6.1.3 测试环境 (.env.test)
```env
# 测试数据库配置
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/projectalpha_test

# 应用配置
DEBUG=True
TESTING=True
```

### 6.2 依赖清单

#### 6.2.1 后端生产依赖 (requirements.txt)
```
fastapi==0.115.0
uvicorn[standard]==0.34.0
sqlalchemy[asyncio]==2.0.36
asyncpg==0.30.0
psycopg2-binary==2.9.10
pydantic==2.10.0
pydantic-settings==2.7.0
python-dotenv==1.0.1
alembic==1.14.0
gunicorn==23.0.0
python-multipart==0.0.20
email-validator==2.2.0
```

#### 6.2.2 后端开发依赖 (requirements-dev.txt)
```
-r requirements.txt
pytest==8.3.0
pytest-asyncio==0.25.0
pytest-cov==6.0.0
httpx==0.28.0
black==24.10.0
flake8==7.1.0
mypy==1.14.0
pre-commit==4.0.0
```

#### 6.2.3 前端依赖 (package.json)
```json
{
  "name": "projectalpha-frontend",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "test:unit": "vitest",
    "test:e2e": "cypress run",
    "lint": "eslint . --ext .vue,.js,.jsx --ignore-path .gitignore",
    "format": "prettier --write src/"
  },
  "dependencies": {
    "vue": "^3.5.0",
    "pinia": "^2.3.0",
    "axios": "^1.7.0"
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^5.2.0",
    "vite": "^6.0.0",
    "vitest": "^2.1.0",
    "@vue/test-utils": "^2.4.0",
    "cypress": "^13.17.0",
    "eslint": "^9.17.0",
    "prettier": "^3.4.0"
  }
}
```

---

## 7. 开发计划

### 7.1 阶段一：后端开发
1. 初始化 FastAPI 项目结构
2. 配置 PostgreSQL 数据库连接
3. 实现数据模型和数据库迁移
4. 实现 Ticket CRUD API
5. 实现 Tag 管理 API
6. 实现搜索和筛选功能
7. 添加 CORS 支持
8. API 测试验证

### 7.2 阶段二：前端开发
1. 初始化 Vue 3 项目
2. 配置 Axios 和 API 调用层
3. 实现 Pinia 状态管理
4. 开发基础 UI 组件
5. 实现 Ticket 列表和详情展示
6. 实现 Ticket 创建/编辑功能
7. 实现标签筛选和搜索功能
8. UI 优化和响应式适配

### 7.3 阶段三：集成与测试
1. 前后端联调
2. 功能测试
3. Bug 修复
4. 部署配置

---

## 8. 接口详细说明

### 8.1 获取 Ticket 列表

**请求**
```
GET /api/tickets?tags=bug,feature&search=登录&status=open&sort=desc
```

**查询参数**
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| tags | string | 否 | 标签过滤，多个标签用逗号分隔 |
| search | string | 否 | 标题搜索关键词 |
| status | string | 否 | 状态过滤：open/closed/all |
| sort | string | 否 | 排序方式：asc/desc，默认desc |

**响应 (200 OK)**
```json
{
  "items": [
    {
      "id": 1,
      "title": "修复登录页面bug",
      "description": "用户反馈登录页面在移动端显示异常",
      "status": "open",
      "tags": ["bug", "frontend", "urgent"],
      "created_at": "2024-01-15T10:30:00",
      "updated_at": "2024-01-15T14:20:00",
      "completed_at": null
    }
  ],
  "total": 1
}
```

### 8.2 创建 Ticket

**请求**
```
POST /api/tickets
Content-Type: application/json

{
  "title": "新增用户反馈功能",
  "description": "在设置页面添加用户反馈入口",
  "tags": ["feature", "frontend"]
}
```

**响应 (201 Created)**
```json
{
  "id": 2,
  "title": "新增用户反馈功能",
  "description": "在设置页面添加用户反馈入口",
  "status": "open",
  "tags": ["feature", "frontend"],
  "created_at": "2024-01-16T09:00:00",
  "updated_at": "2024-01-16T09:00:00",
  "completed_at": null
}
```

### 8.3 完成 Ticket

**请求**
```
PATCH /api/tickets/1/complete
```

**响应 (200 OK)**
```json
{
  "id": 1,
  "title": "修复登录页面bug",
  "description": "用户反馈登录页面在移动端显示异常",
  "status": "closed",
  "tags": ["bug", "frontend", "urgent"],
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-16T11:00:00",
  "completed_at": "2024-01-16T11:00:00"
}
```

### 8.4 获取所有标签

**请求**
```
GET /api/tags
```

**响应 (200 OK)**
```json
[
  {"id": 1, "name": "bug", "ticket_count": 5},
  {"id": 2, "name": "feature", "ticket_count": 3},
  {"id": 3, "name": "urgent", "ticket_count": 2}
]
```

---

## 9. 错误处理

### 9.1 错误响应格式
```json
{
  "detail": "错误描述信息",
  "error_code": "ERROR_CODE"
}
```

### 9.2 常见错误码
| HTTP 状态码 | 错误码 | 说明 |
|-------------|--------|------|
| 400 | VALIDATION_ERROR | 请求参数验证失败 |
| 404 | TICKET_NOT_FOUND | Ticket 不存在 |
| 404 | TAG_NOT_FOUND | 标签不存在 |
| 409 | TAG_ALREADY_EXISTS | 标签已存在 |
| 500 | INTERNAL_ERROR | 服务器内部错误 |

---

## 10. 测试策略

### 10.1 测试层次

```
+-----------------------------------+
|         E2E 测试 (Cypress)         |  <-- 用户场景测试
+-----------------------------------+
|        集成测试 (pytest)           |  <-- API 端点测试
+-----------------------------------+
|        单元测试 (pytest)           |  <-- 业务逻辑测试
+-----------------------------------+
```

### 10.2 后端测试

#### 10.2.1 单元测试

**测试框架**: pytest + pytest-asyncio

**测试范围**:
- 数据模型验证
- 业务逻辑函数
- 数据转换和序列化
- 工具函数

**测试文件结构**:
```
tests/
+-- unit/
    +-- test_models/
    |   +-- test_ticket_model.py
    |   +-- test_tag_model.py
    +-- test_services/
    |   +-- test_ticket_service.py
    |   +-- test_tag_service.py
    +-- test_schemas/
        +-- test_ticket_schema.py
        +-- test_tag_schema.py
```

**示例测试用例**:
```python
# tests/unit/test_services/test_ticket_service.py
import pytest
from app.services.ticket_service import TicketService
from app.schemas.ticket import TicketCreate

class TestTicketService:
    """Ticket 服务单元测试"""

    async def test_create_ticket_success(self, db_session):
        """测试成功创建 Ticket"""
        service = TicketService(db_session)
        ticket_data = TicketCreate(
            title="测试 Ticket",
            description="测试描述",
            tags=["bug", "urgent"]
        )
        ticket = await service.create_ticket(ticket_data)
        
        assert ticket.title == "测试 Ticket"
        assert ticket.status == "open"
        assert len(ticket.tags) == 2
        assert "bug" in [t.name for t in ticket.tags]

    async def test_create_ticket_missing_title(self, db_session):
        """测试缺少标题时创建失败"""
        service = TicketService(db_session)
        
        with pytest.raises(ValueError):
            await service.create_ticket(TicketCreate(title=""))

    async def test_complete_ticket(self, db_session):
        """测试完成 Ticket"""
        service = TicketService(db_session)
        ticket = await service.create_ticket(
            TicketCreate(title="待完成 Ticket")
        )
        
        completed = await service.complete_ticket(ticket.id)
        
        assert completed.status == "closed"
        assert completed.completed_at is not None

    async def test_uncomplete_ticket(self, db_session):
        """测试取消完成 Ticket"""
        service = TicketService(db_session)
        ticket = await service.create_ticket(
            TicketCreate(title="已完成 Ticket")
        )
        await service.complete_ticket(ticket.id)
        
        reopened = await service.uncomplete_ticket(ticket.id)
        
        assert reopened.status == "open"
        assert reopened.completed_at is None

    async def test_delete_ticket(self, db_session):
        """测试删除 Ticket"""
        service = TicketService(db_session)
        ticket = await service.create_ticket(
            TicketCreate(title="待删除 Ticket")
        )
        
        await service.delete_ticket(ticket.id)
        
        deleted = await service.get_ticket(ticket.id)
        assert deleted is None

    async def test_search_tickets_by_title(self, db_session):
        """测试按标题搜索 Ticket"""
        service = TicketService(db_session)
        await service.create_ticket(TicketCreate(title="前端bug修复"))
        await service.create_ticket(TicketCreate(title="后端性能优化"))
        await service.create_ticket(TicketCreate(title="前端UI调整"))
        
        results = await service.search_tickets("前端")
        
        assert len(results) == 2
        assert all("前端" in t.title for t in results)

    async def test_filter_tickets_by_tags(self, db_session):
        """测试按标签筛选 Ticket"""
        service = TicketService(db_session)
        await service.create_ticket(
            TicketCreate(title="Ticket A", tags=["bug", "urgent"])
        )
        await service.create_ticket(
            TicketCreate(title="Ticket B", tags=["feature"])
        )
        await service.create_ticket(
            TicketCreate(title="Ticket C", tags=["bug", "frontend"])
        )
        
        results = await service.filter_by_tags(["bug"])
        
        assert len(results) == 2
```

#### 10.2.2 集成测试

**测试范围**:
- API 端点请求/响应
- 数据库交互
- 中间件和依赖注入

**测试文件结构**:
```
tests/
+-- integration/
    +-- test_api/
    |   +-- test_tickets_api.py
    |   +-- test_tags_api.py
    +-- test_database/
        +-- test_migrations.py
```

**示例测试用例**:
```python
# tests/integration/test_api/test_tickets_api.py
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
class TestTicketsAPI:
    """Ticket API 集成测试"""

    async def test_get_tickets_empty(self, async_client):
        """测试获取空 Ticket 列表"""
        response = await async_client.get("/api/tickets")
        
        assert response.status_code == 200
        data = response.json()
        assert data["items"] == []
        assert data["total"] == 0

    async def test_create_ticket(self, async_client):
        """测试创建 Ticket"""
        payload = {
            "title": "API 测试 Ticket",
            "description": "通过 API 创建",
            "tags": ["test", "api"]
        }
        response = await async_client.post("/api/tickets", json=payload)
        
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "API 测试 Ticket"
        assert data["status"] == "open"
        assert len(data["tags"]) == 2

    async def test_get_single_ticket(self, async_client):
        """测试获取单个 Ticket"""
        # 先创建一个 Ticket
        create_resp = await async_client.post("/api/tickets", json={
            "title": "获取测试"
        })
        ticket_id = create_resp.json()["id"]
        
        response = await async_client.get(f"/api/tickets/{ticket_id}")
        
        assert response.status_code == 200
        assert response.json()["id"] == ticket_id

    async def test_get_nonexistent_ticket(self, async_client):
        """测试获取不存在的 Ticket"""
        response = await async_client.get("/api/tickets/99999")
        
        assert response.status_code == 404

    async def test_update_ticket(self, async_client):
        """测试更新 Ticket"""
        create_resp = await async_client.post("/api/tickets", json={
            "title": "原始标题"
        })
        ticket_id = create_resp.json()["id"]
        
        response = await async_client.put(f"/api/tickets/{ticket_id}", json={
            "title": "更新后的标题",
            "description": "新描述"
        })
        
        assert response.status_code == 200
        assert response.json()["title"] == "更新后的标题"

    async def test_complete_ticket(self, async_client):
        """测试完成 Ticket"""
        create_resp = await async_client.post("/api/tickets", json={
            "title": "待完成测试"
        })
        ticket_id = create_resp.json()["id"]
        
        response = await async_client.patch(f"/api/tickets/{ticket_id}/complete")
        
        assert response.status_code == 200
        assert response.json()["status"] == "closed"
        assert response.json()["completed_at"] is not None

    async def test_delete_ticket(self, async_client):
        """测试删除 Ticket"""
        create_resp = await async_client.post("/api/tickets", json={
            "title": "待删除测试"
        })
        ticket_id = create_resp.json()["id"]
        
        response = await async_client.delete(f"/api/tickets/{ticket_id}")
        
        assert response.status_code == 204
        
        # 验证已删除
        get_resp = await async_client.get(f"/api/tickets/{ticket_id}")
        assert get_resp.status_code == 404

    async def test_search_tickets(self, async_client):
        """测试搜索 Ticket"""
        await async_client.post("/api/tickets", json={"title": "前端bug"})
        await async_client.post("/api/tickets", json={"title": "后端优化"})
        
        response = await async_client.get("/api/tickets?search=前端")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 1
        assert "前端" in data["items"][0]["title"]

    async def test_filter_by_tags(self, async_client):
        """测试按标签筛选"""
        await async_client.post("/api/tickets", json={
            "title": "Ticket A", "tags": ["bug", "urgent"]
        })
        await async_client.post("/api/tickets", json={
            "title": "Ticket B", "tags": ["feature"]
        })
        
        response = await async_client.get("/api/tickets?tags=bug")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 1

    async def test_validation_error(self, async_client):
        """测试验证错误"""
        response = await async_client.post("/api/tickets", json={
            "title": ""
        })
        
        assert response.status_code == 422
```

#### 10.2.3 测试配置 (conftest.py)
```python
# tests/conftest.py
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.database import Base, get_db
from app.main import app

TEST_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/projectalpha_test"

@pytest_asyncio.fixture(scope="session")
async def test_engine():
    """创建测试数据库引擎"""
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()

@pytest_asyncio.fixture
async def db_session(test_engine) -> AsyncSession:
    """创建测试数据库会话，每个测试独立事务"""
    async_session = async_sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session
        await session.rollback()

@pytest_asyncio.fixture
async def async_client(db_session):
    """创建异步测试客户端"""
    async def override_get_db():
        yield db_session
    
    app.dependency_overrides[get_db] = override_get_db
    
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
    
    app.dependency_overrides.clear()
```

#### 10.2.4 测试运行命令
```bash
# 运行所有测试
pytest

# 运行单元测试
pytest tests/unit/

# 运行集成测试
pytest tests/integration/

# 生成覆盖率报告
pytest --cov=app --cov-report=html

# 运行特定测试文件
pytest tests/unit/test_services/test_ticket_service.py -v

# 异步测试
pytest --asyncio-mode=auto
```

### 10.3 前端测试

#### 10.3.1 单元测试 (Vitest + Vue Test Utils)

**测试范围**:
- 组件渲染
- 用户交互
- 状态管理
- 工具函数

**测试文件结构**:
```
tests/
+-- unit/
    +-- components/
    |   +-- TicketItem.spec.js
    |   +-- TicketForm.spec.js
    |   +-- TagSidebar.spec.js
    |   +-- SearchBar.spec.js
    +-- stores/
    |   +-- ticket.spec.js
    |   +-- tag.spec.js
    +-- utils/
        +-- helpers.spec.js
```

**示例测试用例**:
```javascript
// tests/unit/components/TicketItem.spec.js
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import TicketItem from '@/components/TicketItem.vue'

describe('TicketItem', () => {
  const mockTicket = {
    id: 1,
    title: '测试 Ticket',
    description: '测试描述',
    status: 'open',
    tags: ['bug', 'urgent'],
    created_at: '2024-01-15T10:30:00',
    completed_at: null
  }

  it('正确渲染 Ticket 信息', () => {
    const wrapper = mount(TicketItem, {
      props: { ticket: mockTicket }
    })

    expect(wrapper.text()).toContain('测试 Ticket')
    expect(wrapper.text()).toContain('bug')
    expect(wrapper.text()).toContain('urgent')
  })

  it('已完成 Ticket 显示复选框选中状态', () => {
    const completedTicket = { ...mockTicket, status: 'closed' }
    const wrapper = mount(TicketItem, {
      props: { ticket: completedTicket }
    })

    expect(wrapper.find('input[type="checkbox"]').element.checked).toBe(true)
  })

  it('点击完成按钮触发 complete 事件', async () => {
    const wrapper = mount(TicketItem, {
      props: { ticket: mockTicket }
    })

    await wrapper.find('.complete-btn').trigger('click')

    expect(wrapper.emitted('complete')).toBeTruthy()
    expect(wrapper.emitted('complete')[0]).toEqual([1])
  })

  it('点击删除按钮触发 delete 事件', async () => {
    const wrapper = mount(TicketItem, {
      props: { ticket: mockTicket }
    })

    await wrapper.find('.delete-btn').trigger('click')

    expect(wrapper.emitted('delete')).toBeTruthy()
    expect(wrapper.emitted('delete')[0]).toEqual([1])
  })

  it('点击编辑按钮触发 edit 事件', async () => {
    const wrapper = mount(TicketItem, {
      props: { ticket: mockTicket }
    })

    await wrapper.find('.edit-btn').trigger('click')

    expect(wrapper.emitted('edit')).toBeTruthy()
    expect(wrapper.emitted('edit')[0]).toEqual([1])
  })
})
```

#### 10.3.2 端到端测试 (Cypress)

**测试范围**:
- 完整用户流程
- 页面导航
- 表单提交
- 数据持久化

**测试文件结构**:
```
tests/
+-- e2e/
    +-- tickets.cy.js
    +-- tags.cy.js
    +-- search.cy.js
+-- support/
    +-- commands.js
    +-- e2e.js
```

**示例测试用例**:
```javascript
// tests/e2e/tickets.cy.js
describe('Ticket 管理功能', () => {
  beforeEach(() => {
    cy.visit('/')
  })

  it('创建新 Ticket', () => {
    cy.get('[data-cy="new-ticket-btn"]').click()
    
    cy.get('[data-cy="ticket-title"]').type('E2E 测试 Ticket')
    cy.get('[data-cy="ticket-description"]').type('这是端到端测试创建的 Ticket')
    cy.get('[data-cy="ticket-tags"]').type('test{enter}')
    
    cy.get('[data-cy="submit-btn"]').click()
    
    cy.contains('E2E 测试 Ticket').should('be.visible')
    cy.contains('test').should('be.visible')
  })

  it('完成 Ticket', () => {
    // 先创建一个 Ticket
    cy.get('[data-cy="new-ticket-btn"]').click()
    cy.get('[data-cy="ticket-title"]').type('待完成 Ticket')
    cy.get('[data-cy="submit-btn"]').click()
    
    // 点击完成按钮
    cy.contains('待完成 Ticket')
      .parent()
      .find('[data-cy="complete-btn"]')
      .click()
    
    // 验证状态已变更
    cy.contains('待完成 Ticket')
      .parent()
      .find('input[type="checkbox"]')
      .should('be.checked')
  })

  it('删除 Ticket', () => {
    // 创建 Ticket
    cy.get('[data-cy="new-ticket-btn"]').click()
    cy.get('[data-cy="ticket-title"]').type('待删除 Ticket')
    cy.get('[data-cy="submit-btn"]').click()
    
    // 确认删除对话框
    cy.on('window:confirm', () => true)
    
    // 点击删除按钮
    cy.contains('待删除 Ticket')
      .parent()
      .find('[data-cy="delete-btn"]')
      .click()
    
    // 验证已删除
    cy.contains('待删除 Ticket').should('not.exist')
  })

  it('编辑 Ticket', () => {
    // 创建 Ticket
    cy.get('[data-cy="new-ticket-btn"]').click()
    cy.get('[data-cy="ticket-title"]').type('原始标题')
    cy.get('[data-cy="submit-btn"]').click()
    
    // 点击编辑按钮
    cy.contains('原始标题')
      .parent()
      .find('[data-cy="edit-btn"]')
      .click()
    
    // 修改标题
    cy.get('[data-cy="ticket-title"]').clear().type('修改后的标题')
    cy.get('[data-cy="submit-btn"]').click()
    
    // 验证修改
    cy.contains('修改后的标题').should('be.visible')
    cy.contains('原始标题').should('not.exist')
  })
})
```

#### 10.3.3 前端测试运行命令
```bash
# 运行单元测试
npm run test:unit

# 运行 E2E 测试（交互模式）
npx cypress open

# 运行 E2E 测试（无头模式）
npm run test:e2e

# 生成覆盖率报告
npm run test:unit -- --coverage
```

### 10.4 测试覆盖率要求

| 模块 | 最低覆盖率 |
|------|----------|
| 后端业务逻辑 (services/) | 80% |
| 后端 API 路由 (routers/) | 90% |
| 后端数据模型 (models/) | 90% |
| 前端组件 (components/) | 70% |
| 前端状态管理 (stores/) | 80% |
| 前端工具函数 (utils/) | 90% |

### 10.5 CI/CD 测试集成

```yaml
# .github/workflows/test.yml (GitHub Actions 示例)
name: Test

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  backend-test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: projectalpha_test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
    
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements-dev.txt
      - name: Run tests
        run: |
          cd backend
          pytest --cov=app --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v4

  frontend-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
      - name: Install dependencies
        run: |
          cd frontend
          npm install
      - name: Run unit tests
        run: |
          cd frontend
          npm run test:unit
      - name: Run E2E tests
        uses: cypress-io/github-action@v6
        with:
          working-directory: frontend
          start: npm run dev
          wait-on: 'http://localhost:5173'
```

---

## 11. 本地部署

### 11.1 部署架构

```
+------------------+
|    用户浏览器     |
+--------+---------+
         |
         | HTTP (localhost:5173)
         v
+------------------+          +------------------+
|   前端开发服务器  |----+     |   后端 API 服务   |
|   (Vite Dev)      |    |    |  (Uvicorn)        |
|   localhost:5173  |    |    |  localhost:8000   |
+------------------+    |    +--------+---------+
                        |             |
                        |             | localhost:5432
                        |             v
                        |    +------------------+
                        |    |   PostgreSQL      |
                        |    |   localhost:5432  |
                        |    +------------------+
                        |
                        +---- 前端直接调用后端 API
                              (CORS 已配置)
```

### 11.2 前置环境准备

#### 11.2.1 安装 Python 3.11+

**Windows 系统**
```powershell
# 使用 winget 安装
winget install Python.Python.3.11

# 或使用 Chocolatey
choco install python --version=3.11

# 验证安装
python --version
```

**macOS 系统**
```bash
# 使用 Homebrew 安装
brew install python@3.11

# 验证安装
python3.11 --version
```

**Linux 系统 (Ubuntu/Debian)**
```bash
# 添加 deadsnakes PPA
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-dev

# 验证安装
python3.11 --version
```

#### 11.2.2 安装 Node.js 18+

**Windows 系统**
```powershell
# 使用 winget 安装
winget install OpenJS.NodeJS.LTS

# 或使用 Chocolatey
choco install nodejs-lts
```

**macOS 系统**
```bash
# 使用 Homebrew 安装
brew install node@18
```

**Linux 系统 (Ubuntu/Debian)**
```bash
# 使用 NodeSource 仓库
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs
```

**验证安装**
```bash
node --version    # 应显示 v18.x.x
npm --version     # 应显示 9.x.x 或更高
```

#### 11.2.3 安装 PostgreSQL 15

**Windows 系统**
1. 下载 PostgreSQL 安装包：https://www.postgresql.org/download/windows/
2. 运行安装程序，按向导完成安装
   - 设置端口：5432（默认）
   - 设置超级用户密码（请妥善保管）
   - 安装 pgAdmin（可选，数据库管理工具）
3. 将 PostgreSQL bin 目录添加到 PATH 环境变量
   ```powershell
   # 通常路径：C:\Program Files\PostgreSQL\15\bin
   [Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\Program Files\PostgreSQL\15\bin", "Machine")
   ```
4. 验证安装
   ```powershell
   psql --version
   ```

**macOS 系统**
```bash
# 使用 Homebrew 安装
brew install postgresql@15

# 启动 PostgreSQL 服务
brew services start postgresql@15

# 验证安装
psql --version
```

**Linux 系统 (Ubuntu/Debian)**
```bash
# 安装 PostgreSQL
sudo apt update
sudo apt install postgresql postgresql-contrib

# 启动服务
sudo systemctl start postgresql
sudo systemctl enable postgresql

# 验证安装
psql --version
```

#### 11.2.4 配置 PostgreSQL 数据库

**创建数据库和用户**
```bash
# Windows: 使用 pgAdmin 或打开 psql
# macOS/Linux: 切换到 postgres 用户
sudo -u postgres psql

# 在 psql 中执行以下 SQL 命令：

-- 创建数据库用户
CREATE USER projectalpha_user WITH PASSWORD 'your_secure_password_here';

-- 创建数据库
CREATE DATABASE projectalpha OWNER projectalpha_user;

-- 授予权限
GRANT ALL PRIVILEGES ON DATABASE projectalpha TO projectalpha_user;

-- 连接到数据库
\c projectalpha

-- 授予 schema 权限
GRANT ALL ON SCHEMA public TO projectalpha_user;

-- 退出 psql
\q
```

**验证数据库连接**
```bash
# 测试连接
psql -h localhost -U projectalpha_user -d projectalpha

# 连接成功后执行简单查询
SELECT version();
\q
```

### 11.3 后端本地部署

#### 11.3.1 项目初始化

```bash
# 1. 克隆或进入项目目录
cd c:\AI\project\myLearningProject\w1\projectAplha

# 2. 创建 Python 虚拟环境
python -m venv backend/venv

# 3. 激活虚拟环境
# Windows:
backend\venv\Scripts\activate
# macOS/Linux:
source backend/venv/bin/activate

# 4. 安装依赖
pip install -r backend/requirements.txt
```

#### 11.3.2 配置环境变量

创建后端环境配置文件：
```bash
# 复制示例配置
copy backend/.env.example backend/.env  # Windows
cp backend/.env.example backend/.env    # macOS/Linux
```

编辑 `.env` 文件：
```env
# backend/.env

# 数据库配置
DATABASE_URL=postgresql://projectalpha_user:your_secure_password_here@localhost:5432/projectalpha

# 应用配置
API_HOST=127.0.0.1
API_PORT=8000
DEBUG=False

# CORS 配置（允许前端访问）
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# 日志配置
LOG_LEVEL=INFO
```

**安全提示**：
- 生产环境请使用强密码替换 `your_secure_password_here`
- 将 `.env` 文件添加到 `.gitignore`，不要提交到版本控制
- 备份 `.env` 文件到安全位置

#### 11.3.3 执行数据库迁移

```bash
# 进入后端目录
cd backend

# 初始化 Alembic（如果还未初始化）
alembic init alembic

# 创建数据库迁移脚本
alembic revision --autogenerate -m "initial schema"

# 执行迁移，创建数据表
alembic upgrade head

# 验证数据表已创建
# Windows:
psql -h localhost -U projectalpha_user -d projectalpha -c "\dt"
# macOS/Linux:
psql -h localhost -U projectalpha_user -d projectalpha -c "\dt"
```

**预期输出**：
```
            List of relations
 Schema |     Name     | Type  |     Owner      
--------+--------------+-------+----------------
 public | tickets      | table | projectalpha_user
 public | tags         | table | projectalpha_user
 public | ticket_tags  | table | projectalpha_user
(3 rows)
```

#### 11.3.4 启动后端服务

**开发环境启动（带自动重载）**
```bash
# 在 backend 目录下
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

**生产环境启动（使用 Uvicorn）**
```bash
# 单进程模式（适合轻量使用）
uvicorn app.main:app --host 127.0.0.1 --port 8000 --workers 1

# 多进程模式（推荐生产环境）
uvicorn app.main:app --host 127.0.0.1 --port 8000 --workers 4
```

**生产环境启动（使用 Gunicorn + Uvicorn Worker）**
```bash
# 仅适用于 Linux/macOS
gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 127.0.0.1:8000 \
  --timeout 120 \
  --access-logfile logs/access.log \
  --error-logfile logs/error.log
```

**验证后端服务**
```bash
# 访问 API 文档
curl http://localhost:8000/docs

# 健康检查（如果实现了健康检查端点）
curl http://localhost:8000/health

# 测试 API 端点
curl http://localhost:8000/api/tickets
```

**预期输出**：
```json
{"items": [], "total": 0}
```

#### 11.3.5 Windows 服务配置（可选）

使用 NSSM (Non-Sucking Service Manager) 将后端注册为 Windows 服务：

```powershell
# 1. 下载并安装 NSSM
# 从 https://nssm.cc/download 下载
# 解压到 C:\nssm

# 2. 安装服务
C:\nssm\win64\nssm.exe install projectalpha-backend

# 3. 配置服务参数
# Path: C:\AI\project\myLearningProject\w1\projectAplha\backend\venv\Scripts\uvicorn.exe
# Arguments: app.main:app --host 127.0.0.1 --port 8000 --workers 4
# Startup directory: C:\AI\project\myLearningProject\w1\projectAplha\backend

# 4. 设置环境变量（在 NSSM GUI 的 Environment 选项卡中）
# DATABASE_URL=postgresql://projectalpha_user:password@localhost:5432/projectalpha
# DEBUG=False

# 5. 启动服务
net start projectalpha-backend

# 6. 设置开机自启
# NSSM 默认已配置开机自启
```

**服务管理命令**
```powershell
# 启动服务
net start projectalpha-backend

# 停止服务
net stop projectalpha-backend

# 重启服务
net stop projectalpha-backend && net start projectalpha-backend

# 查看服务状态
sc query projectalpha-backend
```

#### 11.3.6 Linux/macOS 服务配置（可选）

创建 systemd 服务单元文件：

```bash
# 创建服务文件
sudo nano /etc/systemd/system/projectalpha-backend.service
```

**服务文件内容**：
```ini
[Unit]
Description=projectAlpha Backend API
After=network.target postgresql.service
Wants=postgresql.service

[Service]
Type=notify
User=your_username
Group=your_group
WorkingDirectory=/path/to/projectAplha/backend
Environment="PATH=/path/to/projectAplha/backend/venv/bin"
ExecStart=/path/to/projectAplha/backend/venv/bin/uvicorn app.main:app \
  --host 127.0.0.1 \
  --port 8000 \
  --workers 4
EnvironmentFile=/path/to/projectAplha/backend/.env
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal

# 安全设置
NoNewPrivileges=true
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

**启用和管理服务**
```bash
# 重新加载 systemd 配置
sudo systemctl daemon-reload

# 启用开机自启
sudo systemctl enable projectalpha-backend

# 启动服务
sudo systemctl start projectalpha-backend

# 查看服务状态
sudo systemctl status projectalpha-backend

# 查看日志
sudo journalctl -u projectalpha-backend -f

# 重启服务
sudo systemctl restart projectalpha-backend

# 停止服务
sudo systemctl stop projectalpha-backend
```

### 11.4 前端本地部署

#### 11.4.1 项目初始化

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install
# 或使用 pnpm
pnpm install
```

#### 11.4.2 配置环境变量

创建前端环境配置文件：
```bash
# 复制示例配置
copy .env.example .env  # Windows
cp .env.example .env    # macOS/Linux
```

编辑 `.env` 文件：
```env
# frontend/.env

# API 基础 URL
VITE_API_BASE_URL=http://localhost:8000

# 应用标题
VITE_APP_TITLE=projectAlpha
```

#### 11.4.3 启动前端服务

**开发环境启动（带热重载）**
```bash
# 在 frontend 目录下
npm run dev
```

**生产环境构建和启动**
```bash
# 构建生产版本
npm run build

# 预览构建结果（用于测试）
npm run preview

# 使用静态文件服务器（生产环境推荐）
# 安装 serve
npm install -g serve

# 启动服务
serve -s dist -l 3000
```

**验证前端服务**
```bash
# 访问前端应用
curl http://localhost:5173

# 或在浏览器中打开
# Windows:
start http://localhost:5173
# macOS:
open http://localhost:5173
# Linux:
xdg-open http://localhost:5173
```

### 11.5 完整启动流程

#### 11.5.1 启动顺序

```
1. 确保 PostgreSQL 服务正在运行
   ↓
2. 启动后端 API 服务 (localhost:8000)
   ↓
3. 启动前端开发服务器 (localhost:5173)
   ↓
4. 在浏览器中访问 http://localhost:5173
```

#### 11.5.2 Windows 启动脚本

创建启动批处理文件 `start_project.bat`：
```batch
@echo off
echo ========================================
echo   projectAlpha - 本地启动脚本
echo ========================================

REM 检查 PostgreSQL 服务
echo.
echo [1/3] 检查 PostgreSQL 服务...
REM PostgreSQL 服务名称可能为 postgresql-x64-15 或 PostgreSQL，尝试多种可能
sc query postgresql-x64-15 >nul 2>&1
if %errorlevel% equ 0 (
    echo [成功] PostgreSQL 服务正在运行
    goto :pg_ok
)
sc query PostgreSQL >nul 2>&1
if %errorlevel% equ 0 (
    echo [成功] PostgreSQL 服务正在运行
    goto :pg_ok
)
echo [警告] PostgreSQL 服务未运行，请手动启动
:pg_ok

REM 启动后端服务
echo.
echo [2/3] 启动后端 API 服务...
start "projectAlpha Backend" cmd /k "cd backend && venv\Scripts\activate && uvicorn app.main:app --reload --host 127.0.0.1 --port 8000"

REM 等待后端启动
timeout /t 3 /nobreak >nul

REM 启动前端服务
echo.
echo [3/3] 启动前端开发服务器...
start "projectAlpha Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ========================================
echo   启动完成！
echo   后端: http://localhost:8000/docs
echo   前端: http://localhost:5173
echo ========================================
echo.

REM 等待用户确认后打开浏览器
pause
start http://localhost:5173
```

#### 11.5.3 macOS/Linux 启动脚本

创建启动脚本 `start_project.sh`：
```bash
#!/bin/bash

echo "========================================"
echo "  projectAlpha - 本地启动脚本"
echo "========================================"

# 检查 PostgreSQL 服务
echo ""
echo "[1/3] 检查 PostgreSQL 服务..."
if pg_isready -q; then
    echo "[成功] PostgreSQL 服务正在运行"
else
    echo "[警告] PostgreSQL 服务未运行"
    read -p "是否尝试启动? (y/n): " start_pg
    if [ "$start_pg" = "y" ]; then
        sudo systemctl start postgresql 2>/dev/null || brew services start postgresql@15 2>/dev/null
    fi
fi

# 启动后端服务
echo ""
echo "[2/3] 启动后端 API 服务..."
cd backend
source venv/bin/activate
nohup uvicorn app.main:app --reload --host 127.0.0.1 --port 8000 > logs/backend.log 2>&1 &
BACKEND_PID=$!
echo "后端服务已启动 (PID: $BACKEND_PID)"
cd ..

# 等待后端启动
sleep 3

# 启动前端服务
echo ""
echo "[3/3] 启动前端开发服务器..."
cd frontend
nohup npm run dev > logs/frontend.log 2>&1 &
FRONTEND_PID=$!
echo "前端服务已启动 (PID: $FRONTEND_PID)"
cd ..

echo ""
echo "========================================"
echo "  启动完成！"
echo "  后端: http://localhost:8000/docs"
echo "  前端: http://localhost:5173"
echo "========================================"
echo ""
echo "服务进程信息："
echo "  后端 PID: $BACKEND_PID"
echo "  前端 PID: $FRONTEND_PID"
echo ""
echo "停止服务："
echo "  kill $BACKEND_PID $FRONTEND_PID"
echo ""

# 打开浏览器
if [[ "$OSTYPE" == "darwin"* ]]; then
    open http://localhost:5173
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    xdg-open http://localhost:5173
fi
```

### 11.6 服务管理与维护

#### 11.6.1 查看服务状态

```bash
# 检查 PostgreSQL
pg_isready

# 检查后端服务
curl http://localhost:8000/health

# 检查前端服务
curl http://localhost:5173

# 查看端口占用
# Windows:
netstat -ano | findstr :8000
netstat -ano | findstr :5173
netstat -ano | findstr :5432

# macOS/Linux:
lsof -i :8000
lsof -i :5173
lsof -i :5432
```

#### 11.6.2 日志管理

```bash
# 后端日志（如果使用 systemd）
sudo journalctl -u projectalpha-backend -f

# 后端日志（如果使用 nohup）
tail -f backend/logs/backend.log

# 前端日志
tail -f frontend/logs/frontend.log

# PostgreSQL 日志
# Windows: C:\Program Files\PostgreSQL\15\data\log
# Linux: /var/log/postgresql/
# macOS (Homebrew): /opt/homebrew/var/log/postgresql/
```

**日志轮转配置（Linux）**

创建 `/etc/logrotate.d/projectalpha`：
```
/var/log/projectalpha/*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 your_username your_group
    sharedscripts
    postrotate
        systemctl reload projectalpha-backend > /dev/null 2>&1 || true
    endscript
}
```

#### 11.6.3 数据备份

**数据库备份脚本**

Windows (`backup_db.bat`)：
```batch
@echo off
set BACKUP_DIR=C:\backups\projectalpha
set TIMESTAMP=%date:~0,4%%date:~5,2%%date:~8,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set TIMESTAMP=%TIMESTAMP: =0%

if not exist %BACKUP_DIR% mkdir %BACKUP_DIR%

REM 设置 PostgreSQL 密码环境变量（避免手动输入）
set PGPASSWORD=your_secure_password_here

pg_dump -h localhost -U projectalpha_user -d projectalpha > %BACKUP_DIR%\projectalpha_%TIMESTAMP%.sql

REM 清除密码环境变量
set PGPASSWORD=

echo 数据库备份完成：%BACKUP_DIR%\projectalpha_%TIMESTAMP%.sql
```

Linux/macOS (`backup_db.sh`)：
```bash
#!/bin/bash

BACKUP_DIR=~/backups/projectalpha
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

pg_dump -h localhost -U projectalpha_user -d projectalpha > $BACKUP_DIR/projectalpha_$TIMESTAMP.sql

# 保留最近 30 天的备份
find $BACKUP_DIR -name "projectalpha_*.sql" -mtime +30 -delete

echo "数据库备份完成：$BACKUP_DIR/projectalpha_$TIMESTAMP.sql"
```

**设置定时备份（Linux）**
```bash
# 编辑 crontab
crontab -e

# 添加每天凌晨 2 点备份
0 2 * * * /path/to/backup_db.sh >> /var/log/projectalpha/backup.log 2>&1
```

**设置定时备份（Windows）**
```powershell
# 使用任务计划程序
# 1. 打开"任务计划程序"
# 2. 创建基本任务
# 3. 设置触发器：每天 02:00
# 4. 设置操作：启动程序 -> backup_db.bat
```

#### 11.6.4 版本更新流程

```bash
# 1. 停止服务
# Windows (如果使用服务):
net stop projectalpha-backend
# Linux:
sudo systemctl stop projectalpha-backend

# 2. 备份数据库
pg_dump -h localhost -U projectalpha_user -d projectalpha > backup_before_update.sql

# 3. 拉取最新代码
git pull origin main

# 4. 更新后端依赖
cd backend
pip install -r requirements.txt

# 5. 执行数据库迁移
alembic upgrade head

# 6. 更新前端依赖
cd ../frontend
npm install

# 7. 重新构建前端（如果是生产环境）
npm run build

# 8. 启动服务
# Windows:
net start projectalpha-backend
# Linux:
sudo systemctl start projectalpha-backend

# 9. 验证服务
curl http://localhost:8000/health
```

### 11.7 故障排查

#### 11.7.1 常见问题

**PostgreSQL 连接失败**
```bash
# 检查服务是否运行
pg_isready

# 检查端口是否监听
netstat -ano | findstr :5432  # Windows
lsof -i :5432                  # macOS/Linux

# 检查 pg_hba.conf 配置
# Windows: C:\Program Files\PostgreSQL\15\data\pg_hba.conf
# Linux: /etc/postgresql/15/main/pg_hba.conf

# 确保有此行：
# local   all   all   md5
# host    all   all   127.0.0.1/32   md5
```

**端口被占用**
```bash
# 查找占用端口的进程
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux:
lsof -i :8000
kill -9 <PID>
```

**后端启动失败**
```bash
# 查看详细错误信息
cd backend
uvicorn app.main:app --reload --log-level debug

# 检查依赖是否完整
pip install -r requirements.txt --force-reinstall

# 检查数据库连接
python -c "from app.database import engine; print('Database OK')"
```

**前端无法连接后端**
```bash
# 检查 CORS 配置
# 确保 backend/.env 中包含前端地址
# CORS_ORIGINS=http://localhost:5173

# 测试后端 API
curl http://localhost:8000/api/tickets

# 检查浏览器控制台的网络请求
```

#### 11.7.2 性能调优

**PostgreSQL 配置优化**

编辑 `postgresql.conf`：
```ini
# 内存配置（根据服务器配置调整）
shared_buffers = 256MB          # 系统内存的 25%
effective_cache_size = 1GB      # 系统内存的 50-75%
work_mem = 16MB
maintenance_work_mem = 128MB

# 连接配置
max_connections = 50            # 根据实际需求调整
superuser_reserved_connections = 3

# 日志配置
log_min_duration_statement = 500  # 记录超过 500ms 的查询
log_checkpoints = on
log_connections = on
log_disconnections = on
```

**后端性能调优**
```bash
# 增加 Worker 数量（根据 CPU 核心数）
# Workers = CPU 核心数 * 2 + 1
uvicorn app.main:app --workers 9

# 调整超时时间
uvicorn app.main:app --timeout 120

# 启用 HTTP/2（如果需要）
uvicorn app.main:app --http httptools
```

### 11.8 安全建议

#### 11.8.1 数据库安全
- 使用强密码保护 PostgreSQL 用户
- 限制数据库用户权限，仅授予必要的权限
- 定期备份数据库并加密备份文件
- 仅监听 localhost，不暴露到公网

#### 11.8.2 应用安全
- 生产环境设置 `DEBUG=False`
- 配置 CORS 白名单，仅允许受信任的前端域名
- 使用环境变量存储敏感信息，不要硬编码
- 定期更新依赖包，修复安全漏洞

```bash
# 检查依赖安全漏洞
pip audit      # Python
npm audit      # Node.js
```

#### 11.8.3 系统安全
- 使用防火墙限制端口访问（仅开放必要端口）
- 定期更新操作系统和软件
- 监控日志文件，及时发现异常
- 使用非 root 用户运行服务

#### 11.8.4 输入安全与 XSS 防护
- 后端使用 Pydantic 模型自动验证和清理输入数据
- 前端使用 Vue 的模板语法（`{{ }}`）自动转义 HTML，防止 XSS
- 如需渲染富文本，使用 `v-html` 前必须进行 HTML 净化（如 DOMPurify）
- 标签名称限制为字母、数字、连字符和下划线，避免特殊字符

#### 11.8.5 SQL 注入防护
- 使用 SQLAlchemy ORM 进行所有数据库操作，避免直接拼接 SQL
- 搜索功能使用参数化查询：
```python
# 安全示例
from sqlalchemy import text
query = text("SELECT * FROM tickets WHERE title ILIKE :pattern")
result = await db.execute(query, {"pattern": f"%{keyword}%"})
```
- 避免使用 `f-string` 或字符串拼接构建 SQL

---

## 12. 扩展性考虑

### 12.1 未来可能的扩展功能
- [ ] Ticket 优先级设置（低/中/高）
- [ ] Ticket 评论/备注功能
- [ ] Ticket 导出为 CSV/Excel
- [ ] 标签颜色自定义
- [ ] 拖拽排序
- [ ] 批量操作（批量完成、批量添加标签）
- [ ] 数据备份与恢复
- [ ] 用户认证系统
- [ ] 团队协作功能
- [ ] 邮件通知

### 12.2 架构扩展
- 当前为本地部署，后续可按需迁移到 Docker 容器化部署
- 可引入 Nginx 反向代理提升性能和安全性
- 数据库支持读写分离
- 可添加 Redis 缓存提升查询性能
- 可引入消息队列处理异步任务（如邮件发送）

---

## 13. 附录

### 13.1 常用命令速查

#### 后端开发
```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 运行开发服务器
uvicorn app.main:app --reload --port 8000

# 数据库迁移
alembic revision --autogenerate -m "描述"
alembic upgrade head
alembic downgrade -1

# 运行测试
pytest
pytest --cov=app

# 代码格式化
black app/ tests/
flake8 app/ tests/
```

#### 前端开发
```bash
# 安装依赖
npm install

# 运行开发服务器
npm run dev

# 构建生产版本
npm run build

# 运行测试
npm run test:unit
npm run test:e2e

# 代码检查和格式化
npm run lint
npm run format
```

### 13.2 数据库管理命令
```sql
-- 查看表结构
\d tickets
\d tags
\d ticket_tags

-- 查看索引
\di

-- 查看视图
\dv

-- 分析查询性能
EXPLAIN ANALYZE SELECT * FROM tickets WHERE status = 'open';

-- 查看表大小
SELECT pg_size_pretty(pg_total_relation_size('tickets'));

-- 备份数据库
pg_dump -U username -d projectalpha > backup.sql

-- 恢复数据库
psql -U username -d projectalpha < backup.sql
```

### 13.3 .gitignore 配置示例

**后端 .gitignore**
```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/

# 环境变量（包含敏感信息）
.env
.env.local

# 日志
logs/
*.log

# 数据库
*.db
*.sqlite3

# IDE
.vscode/
.idea/
*.swp
*.swo

# 测试覆盖率
.coverage
htmlcov/
.pytest_cache/

# Alembic 迁移缓存
alembic/versions/__pycache__/
```

**前端 .gitignore**
```gitignore
# 依赖
node_modules/
.pnpm-store/

# 构建输出
dist/
build/

# 环境变量
.env
.env.local
.env.*.local

# 日志
logs/
*.log
npm-debug.log*

# IDE
.vscode/
.idea/
*.swp

# 测试
coverage/
.nyc_output/

# Cypress
videos/
screenshots/
```

### 13.4 参考资料
- FastAPI 官方文档: https://fastapi.tiangolo.com/
- SQLAlchemy 官方文档: https://docs.sqlalchemy.org/
- Vue 3 官方文档: https://vuejs.org/
- PostgreSQL 官方文档: https://www.postgresql.org/docs/
- Alembic 官方文档: https://alembic.sqlalchemy.org/
