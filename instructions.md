# projectAlpha - AI 辅助开发提示词文档

> 本文档总结了在 projectAlpha 项目开发过程中，与 AI Agent 交互时使用的高效提示词。按照开发阶段分类整理，供后续项目参考。

---

## 一、项目初始化阶段

### 1.1 需求分析与文档生成
```
构建一个简单的，使用标签分类和管理的 ticket 工具，它基于 PostgreSQL 数据库，
使用 FastAPI 作为后端，使用 Vue 作为前端，无需用户系统。
当前用户可以：
- 创建/编辑/删除/完成/取消完成 ticket
- 添加/删除 ticket 的标签
- 按照不同的标签查看 ticket 列表
- 按照 title 搜索 ticket

按照这个想法帮我生成详细的需求和设计文档，保存为 spec.md 文件中，输出为中文
```

### 1.2 制定实现计划
```
按照 `c:\AI\project\myLearningProject\w1\projectAplha\implementation-plan.md`
完整实现这个项目的 phase X 代码
```
> 将 X 替换为阶段编号（1-6），AI 会按阶段逐步实现代码

---

## 二、开发阶段高效提示词

### 2.1 按阶段实现代码
```
按照 `implementation-plan.md` 完整实现这个项目的 phase 1 代码
```
```
按照 `implementation-plan.md` 完整实现这个项目的 phase 2 代码
```
```
按照 `implementation-plan.md` 完整实现这个项目的 phase 3 代码
```
```
按照 `implementation-plan.md` 完整实现这个项目的 phase 4 代码
```
```
按照 `implementation-plan.md` 完整实现这个项目的 phase 5 代码
```
```
按照 `implementation-plan.md` 完整实现这个项目的 phase 6 代码
```

### 2.2 启动和验证
```
启动项目，让我检查一下
```

### 2.3 问题反馈与修复
```
标签筛选和计数功能都有问题。检查一下。
并且我需要在添加标签时可以选择已添加的标签
```
> 技巧：指出具体问题 + 明确期望的新功能

### 2.4 UI/UX 优化
```
按照 apple website 的设计风格，think ultra hard，优化UI和UX
```
> 关键词说明：
> - 指定参考设计风格（如 apple website）
> - "think ultra hard" 提示 AI 深入思考
> - 明确优化目标（UI 和 UX）

### 2.5 服务管理
```
关闭所有的前后端重新启动
```

### 2.6 代码提交
```
提交github
```
```
https://github.com/用户名/仓库名.git 远程仓库
```

### 2.7 脚本整理
```
根目录下的那些bat文件还有用么
```
```
帮我删除
```

---

## 三、提示词最佳实践

### 3.1 任务分解
- **不要一次性让 AI 实现所有功能**
- 按照实现计划分阶段（Phase 1-6）逐步推进
- 每个阶段完成后验证再进入下一阶段

### 3.2 问题描述
- **明确指出问题**：说明具体哪个功能有问题
- **提供期望结果**：告诉 AI 你希望得到什么
- **示例**：`"标签筛选和计数功能都有问题。检查一下。并且我需要在添加标签时可以选择已添加的标签"`

### 3.3 设计风格指定
- **给出具体参考**：如"按照 apple website 的设计风格"
- **使用强化词**：如"think ultra hard"、"complete redesign"
- **明确范围**：如"优化UI和UX"、"重写所有组件"

### 3.4 服务管理
- 重启服务时用简洁指令：`"关闭所有的前后端重新启动"`
- AI 会自动查找并终止相关进程

### 3.5 代码管理
- 提交代码只需说：`"提交github"`
- 如果是首次推送，需要提供仓库地址
- 删除无用文件：先询问 `"XXX 文件还有用么"`，确认后 `"帮我删除"`

### 3.6 文件操作
- 查看文件状态：AI 会使用 `git status` 自动检查
- 清理重复文件：定期询问根目录脚本是否还需要

---

## 四、项目技术栈参考

| 层级 | 技术选型 |
|------|---------|
| 数据库 | PostgreSQL 15+ |
| 后端框架 | FastAPI + SQLAlchemy (异步) |
| 后端工具 | Alembic (迁移)、Pydantic (验证)、Uvicorn (服务器) |
| 前端框架 | Vue 3 + Pinia (状态管理) |
| 前端工具 | Vite (构建)、Axios (HTTP)、Vue Router |
| 设计语言 | Apple-inspired 极简风格 |
| 部署 | Windows (NSSM) / Linux (systemd) + Nginx |

---

## 五、常见问题及解决提示词

| 问题 | 提示词 |
|------|--------|
| 功能有问题 | `"XXX功能有问题。检查一下。"` |
| 需要新功能 | `"我需要XXX功能"` |
| UI 不满意 | `"按照 XXX 风格重新设计 UI"` |
| 服务连不上 | `"后端连不上了"` |
| 需要重启 | `"关闭所有的前后端重新启动"` |
| 清理无用文件 | `"根目录下的XXX文件还有用么"` → `"帮我删除"` |
| 提交代码 | `"提交github"` |
| 推送新仓库 | `"https://github.com/xxx.git 远程仓库"` |

---

## 六、项目目录结构

```
projectAlpha/
├── backend/              # 后端代码
│   ├── app/             # FastAPI 应用
│   ├── alembic/         # 数据库迁移
│   ├── tests/           # 测试代码
│   └── requirements.txt # Python 依赖
├── frontend/            # 前端代码
│   ├── src/             # Vue 源码
│   ├── dist/            # 构建产物
│   └── package.json     # Node 依赖
├── scripts/             # 部署脚本
│   ├── backup_database.bat    # Windows 数据库备份
│   ├── backup_database.sh     # Linux 数据库备份
│   ├── install_windows_service.bat  # Windows 服务注册
│   └── projectalpha-backend.service  # Linux 服务单元
├── DEPLOY.md            # 部署文档
├── USAGE.md             # 使用手册
├── implementation-plan.md  # 实现计划
└── spec.md              # 需求规格说明
```

---

## 七、完整开发流程回顾

```
1. 需求分析 → 生成 spec.md
2. 制定计划 → 生成 implementation-plan.md
3. Phase 1 → 环境准备和初始化
4. Phase 2 → 数据库设计和实现
5. Phase 3 → 后端 API 开发
6. Phase 4 → 前端开发
7. Phase 5 → 集成测试和优化
8. Phase 6 → 部署与交付
9. UI 重设计 → Apple 风格全面升级
10. Bug 修复 → 标签功能完善
11. 代码提交 → 推送到 GitHub
```

---

> **提示**：使用 AI 辅助开发时，最重要的是**分阶段推进**、**及时反馈**、**明确需求**。不要试图让 AI 一次性完成所有工作，而是按照计划逐步实现、验证、再推进。
