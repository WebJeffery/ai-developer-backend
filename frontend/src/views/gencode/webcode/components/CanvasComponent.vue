<!--
  低代码页面生成器 - 画布中的单个组件
  渲染和编辑画布中的组件
-->
<template>
  <div
    class="drawing-item"
    :class="{
      'active-from-item': isSelected,
      'unfocus-bordered': !isSelected
    }"
    @click.stop="handleSelect"
  >
    <!-- 组件操作按钮 -->
    <div class="drawing-item-copy" title="复制" @click.stop="handleCopy">
      <el-icon><CopyDocument /></el-icon>
    </div>
    <div class="drawing-item-delete" title="删除" @click.stop="handleDelete">
      <el-icon><Delete /></el-icon>
    </div>
    
    <!-- 组件内容区域 -->
    <div class="component-wrapper">
      <ComponentRenderer
        :component="component"
        @click.stop="handleSelect"
      >
        <template #children>
          <!-- 容器组件的拖拽区域 -->
          <draggable 
            v-if="isContainer()"
            class="drag-wrapper"
            :list="component.children || []"
            group="componentsGroup"
            :animation="340"
            item-key="id"
            @add="handleAdd"
            @change="handleChange"
          >
            <template #item="{ element }">
              <CanvasComponent
                :key="element.id"
                :component="element"
                :selected-id="selectedId"
                :drawing-list="component.children"
                @select="$emit('select', $event)"
                @update="$emit('update', $event)"
                @delete="$emit('delete', $event)"
                @copy="$emit('copy', $event)"
              />
            </template>
          </draggable>
          
          <!-- 非容器组件的子组件 -->
          <template v-else>
            <CanvasComponent
              v-for="child in component.children"
              :key="child.id"
              :component="child"
              :selected-id="selectedId"
              :drawing-list="drawingList"
              @select="$emit('select', $event)"
              @update="$emit('update', $event)"
              @delete="$emit('delete', $event)"
              @copy="$emit('copy', $event)"
            />
          </template>
          
          <!-- 容器占位符 -->
          <div v-if="needsPlaceholder()" class="component-placeholder">
            {{ getPlaceholderText() }}
          </div>
        </template>
      </ComponentRenderer>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { ElMessage } from 'element-plus';
import { Delete, CopyDocument } from '@element-plus/icons-vue';
import draggable from 'vuedraggable';
import ComponentRenderer from './ComponentRenderer.vue';
import { ComponentSchema, generateId } from '../utils/schema';

// 定义 Props
interface Props {
  component: ComponentSchema;
  selectedId?: string;
  drawingList?: ComponentSchema[];
  index?: number;
}

// 定义 Emits
interface Emits {
  select: [component: ComponentSchema];
  update: [component: ComponentSchema];
  delete: [componentId: string];
  copy: [component: ComponentSchema];
}

const props = defineProps<Props>();
const emit = defineEmits<Emits>();

// 计算属性
const isSelected = computed(() => props.selectedId === props.component.id);

// 处理选择
function handleSelect() {
  emit('select', props.component);
}

// 处理删除
function handleDelete() {
  emit('delete', props.component.id);
}

// 处理复制
function handleCopy() {
  emit('copy', props.component);
}

// 判断是否为容器组件
function isContainer(): boolean {
  const containerTypes = [
    'el-card', 'el-form', 'el-form-item', 'el-row', 'el-col', 
    'el-container', 'el-header', 'el-main', 'el-aside', 'el-footer'
  ];
  return containerTypes.includes(props.component.type);
}

// 处理拖拽添加
function handleAdd(event: any) {
  console.log('子组件拖拽添加:', event);
  emit('update', props.component);
}

// 处理拖拽变化
function handleChange(event: any) {
  console.log('子组件拖拽变化:', event);
  emit('update', props.component);
}


// 判断是否需要占位符
function needsPlaceholder() {
  const hasChildren = props.component.children && props.component.children.length > 0;
  const containerComponents = ['el-card', 'el-form', 'el-form-item', 'el-row', 'el-col', 'el-container', 'el-header', 'el-main', 'el-aside', 'el-footer'];
  const isContainer = containerComponents.includes(props.component.type);
  
  return isContainer && !hasChildren;
}

// 获取占位符文本
function getPlaceholderText(): string {
  const typeMap: Record<string, string> = {
    'el-card': '拖拽组件到此处',
    'el-form': '拖拽表单项到此处',
    'el-form-item': '拖拽表单控件到此处',
    'el-row': '拖拽列到此处',
    'el-col': '拖拽组件到此处',
    'el-container': '拖拽容器组件到此处',
    'el-header': '头部区域',
    'el-main': '主要内容区域',
    'el-aside': '侧边栏区域',
    'el-footer': '底部区域'
  };
  
  return typeMap[props.component.type] || '空容器';
}
</script>

<style scoped>
.drawing-item {
  position: relative;
  cursor: move;
  margin-bottom: 15px;
  transition: all 0.2s ease;

  &.unfocus-bordered:not(.active-from-item) {
    border: 1px dashed var(--el-border-color);
    border-radius: 4px;
    padding: 8px;
  }

  .component-wrapper {
    position: relative;
    min-height: 40px;
  }

  &.active-from-item {
    .component-wrapper {
      background: var(--el-fill-color-light);
      border-radius: 6px;
      padding: 8px;
    }

    .drawing-item-copy,
    .drawing-item-delete {
      display: initial;
    }
  }

  &:hover {
    .component-wrapper {
      background: var(--el-fill-color-light);
      border-radius: 6px;
      padding: 8px;
    }

    .drawing-item-copy,
    .drawing-item-delete {
      display: initial;
    }
  }

  .drawing-item-copy,
  .drawing-item-delete {
    display: none;
    position: absolute;
    top: -10px;
    width: 22px;
    height: 22px;
    line-height: 22px;
    text-align: center;
    border-radius: 50%;
    font-size: 12px;
    border: 1px solid;
    cursor: pointer;
    z-index: 10;
    background: var(--el-bg-color);
    
    .el-icon {
      font-size: 12px;
    }
  }

  .drawing-item-copy {
    right: 56px;
    border-color: var(--el-color-primary);
    color: var(--el-color-primary);

    &:hover {
      background: var(--el-color-primary);
      color: var(--el-color-white);
    }
  }

  .drawing-item-delete {
    right: 24px;
    border-color: var(--el-color-danger);
    color: var(--el-color-danger);

    &:hover {
      background: var(--el-color-danger);
      color: var(--el-color-white);
    }
  }
}

.component-placeholder {
  color: var(--el-text-color-placeholder);
  font-size: 12px;
  font-style: italic;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 40px;
  border: 1px dashed var(--el-border-color);
  border-radius: 4px;
  background: var(--el-fill-color-lighter);
  margin: 8px 0;
}

/* 组件特定样式 */
:deep(.el-button) {
  margin: 4px;
}

:deep(.el-input) {
  margin: 4px 0;
}

:deep(.el-select) {
  margin: 4px 0;
}

:deep(.el-card) {
  margin: 8px 0;
  
  .el-card__body {
    min-height: 60px;
  }
}

:deep(.el-form) {
  margin: 8px 0;
  padding: 16px;
  border: 1px dashed var(--el-border-color);
  border-radius: 4px;
  min-height: 80px;
}

:deep(.el-row) {
  margin: 8px 0;
  padding: 12px;
  border: 1px dashed var(--el-border-color);
  border-radius: 4px;
  min-height: 60px;
}

:deep(.el-col) {
  padding: 8px;
  border: 1px dashed var(--el-border-color-lighter);
  border-radius: 4px;
  min-height: 40px;
  margin: 4px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .drawing-item-copy {
    right: 40px;
    top: -8px;
  }
  
  .drawing-item-delete {
    right: 12px;
    top: -8px;
  }
}

/* 拖拽区域样式 */
.drag-wrapper {
  min-height: 40px;
  width: 100%;
  border-radius: 4px;
  transition: all 0.2s ease;
}

.drag-wrapper:empty {
  min-height: 60px;
  border: 1px dashed var(--el-border-color);
  background: var(--el-fill-color-lighter);
  display: flex;
  align-items: center;
  justify-content: center;
}

.drag-wrapper:empty::after {
  content: '拖拽组件到此处';
  color: var(--el-text-color-placeholder);
  font-size: 12px;
}

/* 拖拽排序样式 */
.sortable-ghost {
  opacity: 0.5;
  background: var(--el-color-primary-light-9);
  border: 2px dashed var(--el-color-primary);
}

.sortable-chosen {
  transform: scale(1.02);
  box-shadow: 0 4px 12px var(--el-color-primary-light-3);
}

/* 容器组件特殊样式 */
.drawing-item .drag-wrapper {
  padding: 8px;
}

.drawing-item:hover .drag-wrapper {
  border-color: var(--el-color-primary);
  background: var(--el-color-primary-light-9);
}
</style>
