# Cursor Rules 说明

本目录包含项目开发规范和使用指南。

## 📋 规则文件列表

### 1. project-structure.mdc
**作用范围**: 始终应用  
**说明**: 项目整体结构和架构指南

包含内容：
- 项目目录结构
- 后端架构（FastAPI MVC 模式）
- 前端架构（Vue3 + TypeScript）
- 移动端架构（uni-app）
- 关键原则

### 2. backend-python.mdc
**作用范围**: `backend/**/*.py`  
**说明**: Python/FastAPI 后端开发规范

包含内容：
- 模块化组织规范
- 核心原则（继承体系、异步优先、数据权限）
- 注释规范
- 数据库操作示例
- CRUD 最佳实践

### 3. frontend-vue.mdc
**作用范围**: `frontend/**/*.{vue,ts,js}`, `fastapp/**/*.{vue,ts,js}`  
**说明**: Vue3 + TypeScript 前端开发规范

包含内容：
- 标准组件结构
- `<script setup>` 使用规范
- TypeScript 类型安全
- 页面开发标准结构
- Composable 函数
- Pinia 状态管理
- 移动端开发指南

### 4. database-models.mdc
**作用范围**: `backend/**/*model.py`, `backend/**/*crud.py`  
**说明**: 数据库模型和 CRUD 操作规范

包含内容：
- ORM 模型定义
- 字段类型和约束
- 关系定义
- CRUD 操作示例
- 高级查询语法
- 数据权限处理
- 关系加载策略

### 5. api-design.mdc
**作用范围**: `backend/app/api/**/*.py`  
**说明**: API 设计和接口规范

包含内容：
- RESTful API 规范
- URL 设计
- HTTP 方法使用
- 响应格式
- 权限控制
- 查询参数
- 文件上传/下载
- 流式响应
- WebSocket 接口

### 6. coding-conventions.mdc
**作用范围**: 始终应用  
**说明**: 通用编码规范和约定

包含内容：
- 命名规范（Python、TypeScript）
- 注释规范
- Git 提交规范
- 代码格式化
- 导入顺序
- 错误处理
- 响应式数据

## 🎯 如何使用

这些规则会自动在 AI 助手工作时应用，帮助你：

1. **理解项目结构**: AI 会自动识别项目的目录组织和架构设计
2. **遵循代码规范**: 生成或修改代码时会自动应用相应的规范
3. **提供最佳实践**: 根据项目模式提供更准确的代码建议
4. **保持一致性**: 确保代码风格和模式与项目保持一致

## 📝 规则应用机制

### 始终应用（alwaysApply: true）
这些规则会在每次对话中自动应用：
- `project-structure.mdc` - 项目结构
- `coding-conventions.mdc` - 编码规范

### 按文件类型应用（globs）
这些规则会在处理特定文件时应用：
- Python 文件 (`*.py`) → `backend-python.mdc`, `database-models.mdc`, `api-design.mdc`
- Vue/TS 文件 (`*.vue`, `*.ts`, `*.js`) → `frontend-vue.mdc`

### 按需应用（description）
这些规则可以通过描述手动触发：
- 在对话中提到 "API 设计" → 应用 `api-design.mdc`
- 提到 "数据库模型" → 应用 `database-models.mdc`

## 🔧 自定义规则

如果需要添加新的规则文件：

1. 在 `.cursor/rules/` 目录下创建 `.mdc` 文件
2. 在文件开头添加 frontmatter：

```markdown
---
alwaysApply: true  # 或
globs: **/*.py     # 或
description: 规则描述
---

# 规则标题
规则内容...
```

3. 规则会自动被 AI 识别和应用

## 💡 提示

- 规则采用 Markdown 格式，支持标准的 Markdown 语法
- 使用 `[filename.ext](mdc:filename.ext)` 引用项目文件
- 规则内容越详细，AI 提供的帮助越准确
- 定期更新规则以保持与项目演变同步

## 📚 更多信息

- [Cursor Rules 官方文档](https://cursor.sh/docs)
- 项目 README: [backend/README.md](../../backend/README.md)
