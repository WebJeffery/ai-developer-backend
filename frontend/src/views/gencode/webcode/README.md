# 低代码页面生成器

一个基于 Vue3 + TypeScript + Element Plus 的可视化页面生成器，支持拖拽式组件设计和代码生成。

## 功能特性

- 🎨 **可视化设计**: 拖拽式组件设计，所见即所得
- 📦 **丰富组件**: 支持所有 Element Plus 组件
- ⚙️ **属性编辑**: 实时编辑组件属性
- 💾 **模板管理**: 保存和加载页面模板
- 🔧 **代码生成**: 生成完整的 Vue3 + TypeScript 代码
- 📱 **响应式**: 支持移动端适配

## 文件结构

```
src/views/gencode/backcode/
├── index.vue              # 主界面
├── components/
│   ├── Palette.vue        # 左侧组件库
│   ├── Canvas.vue         # 中间画布
│   ├── CanvasComponent.vue # 画布中的组件
│   ├── Inspector.vue      # 右侧属性面板
│   └── PropertyEditor.vue # 属性编辑器
└── utils/
    ├── schema.ts          # 组件 Schema 定义
    └── serializer.ts      # 代码生成器
```

## 使用方法

### 1. 添加组件
- 从左侧组件库拖拽组件到中间画布
- 或点击组件快速添加

### 2. 编辑组件
- 点击画布中的组件选中
- 在右侧属性面板编辑属性
- 支持样式、事件、插槽等设置

### 3. 生成代码
- 点击顶部"生成代码"按钮
- 代码会自动复制到剪贴板
- 可选择下载为 .vue 文件

### 4. 保存模板
- 点击"保存模板"按钮
- 输入模板名称和描述
- 模板会保存到本地存储

## 支持的组件类型

### 基础组件
- 按钮 (el-button)
- 链接 (el-link)
- 文本 (el-text)
- 图标 (el-icon)

### 布局组件
- 行 (el-row)
- 列 (el-col)
- 容器 (el-container)

### 表单组件
- 输入框 (el-input)
- 选择器 (el-select)
- 单选框 (el-radio)
- 复选框 (el-checkbox)
- 开关 (el-switch)
- 滑块 (el-slider)
- 日期选择器 (el-date-picker)
- 时间选择器 (el-time-picker)
- 上传 (el-upload)
- 评分 (el-rate)
- 颜色选择器 (el-color-picker)

### 数据展示组件
- 卡片 (el-card)
- 表格 (el-table)
- 轮播图 (el-carousel)
- 折叠面板 (el-collapse)
- 描述列表 (el-descriptions)
- 空状态 (el-empty)
- 图片 (el-image)
- 分页 (el-pagination)
- 进度条 (el-progress)
- 结果页 (el-result)
- 骨架屏 (el-skeleton)
- 统计数值 (el-statistic)
- 标签 (el-tag)
- 时间线 (el-timeline)
- 树形控件 (el-tree)

### 导航组件
- 固钉 (el-affix)
- 面包屑 (el-breadcrumb)
- 下拉菜单 (el-dropdown)
- 菜单 (el-menu)
- 页面头部 (el-page-header)
- 步骤条 (el-steps)
- 标签页 (el-tabs)

### 反馈组件
- 警告提示 (el-alert)
- 抽屉 (el-drawer)
- 加载 (el-loading)
- 消息提示 (el-message)
- 消息确认框 (el-message-box)
- 通知 (el-notification)
- 气泡确认框 (el-popconfirm)
- 弹出框 (el-popover)
- 文字提示 (el-tooltip)

### 其他组件
- 回到顶部 (el-backtop)
- 分割线 (el-divider)
- 水印 (el-watermark)

## 技术栈

- **Vue 3**: 使用 Composition API
- **TypeScript**: 完整的类型支持
- **Element Plus**: UI 组件库
- **Vite**: 构建工具
- **SCSS**: 样式预处理器

## 开发说明

### 添加新组件
1. 在 `utils/schema.ts` 中添加组件类型
2. 在 `COMPONENT_CONFIGS` 中配置组件属性
3. 在 `COMPONENT_CATEGORIES` 中分类组件

### 自定义属性编辑器
1. 在 `PropertyEditor.vue` 中添加新的属性类型
2. 实现对应的编辑器组件
3. 更新属性验证逻辑

### 扩展代码生成
1. 在 `serializer.ts` 中添加新的生成逻辑
2. 支持自定义模板和样式
3. 添加代码格式化功能

## 注意事项

- 组件 ID 必须唯一
- 属性值需要符合 Element Plus 组件规范
- 生成的代码需要手动验证和测试
- 复杂布局建议使用栅格系统

## 许可证

MIT License
