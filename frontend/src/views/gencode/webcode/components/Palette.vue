<!--
  低代码页面生成器 - 组件库面板
  左侧可拖拽的 Element Plus 组件库
-->
<template>
  <div class="left-board">
    <div class="logo-wrapper">
      <div class="logo">
        <el-icon class="logo-icon"><Tools /></el-icon>
        低代码生成器
      </div>
    </div>
    
    <el-scrollbar class="left-scrollbar">
      <div class="components-list">
        <div
          v-for="(components, category) in filteredCategories"
          :key="category"
          class="component-category"
        >
          <div class="components-title">
            <el-icon><Grid /></el-icon>
            {{ category }}
          </div>
          <draggable
            class="components-draggable"
            :list="getComponentList(components)"
            :group="{ name: 'componentsGroup', pull: 'clone', put: false }"
            :clone="cloneComponent"
            draggable=".components-item"
            :sort="false"
            @end="onEnd"
            item-key="type"
          >
            <template #item="{ element }">
              <div class="components-item" @click="addComponent(element)">
                <div class="components-body">
                  <el-icon class="component-icon">
                    <component :is="getComponentIcon(element.type)" />
                  </el-icon>
                  <span class="component-label">{{ element.label }}</span>
                </div>
              </div>
            </template>
          </draggable>
        </div>
      </div>
    </el-scrollbar>
    
    <!-- 搜索框 -->
    <div class="search-wrapper">
      <el-input
        v-model="searchText"
        placeholder="搜索组件"
        clearable
        size="small"
        prefix-icon="Search"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import draggable from 'vuedraggable';
import { Tools, Grid, Search } from '@element-plus/icons-vue';
import { 
  ComponentType, 
  COMPONENT_CONFIGS, 
  COMPONENT_CATEGORIES,
  createComponent 
} from '../utils/schema';

// 定义事件
const emit = defineEmits<{
  addComponent: [component: any];
}>();

// 响应式数据
const searchText = ref('');

// 计算属性 - 过滤后的组件分类
const filteredCategories = computed(() => {
  if (!searchText.value) {
    return COMPONENT_CATEGORIES;
  }
  
  const filtered: Record<string, ComponentType[]> = {};
  
  for (const [category, components] of Object.entries(COMPONENT_CATEGORIES)) {
    const filteredComponents = components.filter(componentType => {
      const config = COMPONENT_CONFIGS[componentType];
      return config?.label?.toLowerCase().includes(searchText.value.toLowerCase());
    });
    
    if (filteredComponents.length > 0) {
      filtered[category] = filteredComponents;
    }
  }
  
  return filtered;
});

// 获取组件列表
function getComponentList(components: ComponentType[]) {
  return components.map(type => {
    const config = COMPONENT_CONFIGS[type];
    return {
      type,
      label: config?.label || type,
      icon: config?.icon || 'Grid'
    };
  });
}

// 克隆组件
function cloneComponent(element: any) {
  const component = createComponent(element.type);
  return component;
}

// 处理拖拽结束
function onEnd(event: any) {
  // 拖拽结束后的处理
}

// 处理组件点击
function addComponent(element: any) {
  const component = createComponent(element.type);
  emit('addComponent', component);
}

// 获取组件图标
function getComponentIcon(componentType: ComponentType): string {
  const iconMap: Record<string, string> = {
    'el-button': 'Connection',
    'el-link': 'Link',
    'el-text': 'Document',
    'el-input': 'Edit',
    'el-input-number': 'Plus',
    'el-select': 'ArrowDown',
    'el-radio': 'CircleCheck',
    'el-radio-group': 'CircleCheck',
    'el-checkbox': 'Check',
    'el-checkbox-group': 'Check',
    'el-switch': 'Switch',
    'el-slider': 'Minus',
    'el-date-picker': 'Calendar',
    'el-time-picker': 'Clock',
    'el-card': 'Document',
    'el-tag': 'PriceTag',
    'el-progress': 'Loading',
    'el-alert': 'Warning',
    'el-form': 'List',
    'el-form-item': 'Tickets',
    'el-row': 'Right',
    'el-col': 'Bottom',
    'el-container': 'Grid',
    'el-header': 'Top',
    'el-main': 'Grid',
    'el-aside': 'Operation',
    'el-footer': 'Bottom',
    'el-divider': 'Minus'
  };
  return iconMap[componentType] || 'Grid';
}
</script>

<style scoped>
.left-board {
  width: 260px;
  position: absolute;
  left: 0;
  top: 0;
  height: calc(100vh - 50px - 40px);
  background: var(--el-bg-color);
  border-right: 1px solid var(--el-border-color-light);

  .logo-wrapper {
    position: relative;
    height: 42px;
    border-bottom: 1px solid var(--el-border-color-extra-light);
    box-sizing: border-box;
    background: var(--el-bg-color);

    .logo {
      position: absolute;
      left: 12px;
      top: 6px;
      line-height: 30px;
      color: var(--el-color-primary);
      font-weight: 600;
      font-size: 16px;
      white-space: nowrap;
      display: flex;
      align-items: center;
      gap: 8px;

      .logo-icon {
        font-size: 20px;
      }
    }
  }

  .left-scrollbar {
    height: calc(100% - 42px - 60px);
    
    .el-scrollbar__wrap {
      box-sizing: border-box;
      overflow-x: hidden !important;
      margin-bottom: 0 !important;
    }

    .components-list {
      padding: 8px;
      box-sizing: border-box;
      height: 100%;

      .component-category {
        margin-bottom: 16px;
      }

      .components-title {
        font-size: 14px;
        color: var(--el-text-color-regular);
        margin: 6px 2px 8px 2px;
        display: flex;
        align-items: center;
        gap: 6px;
        font-weight: 500;

        .el-icon {
          font-size: 16px;
          color: var(--el-color-primary);
        }
      }

      .components-draggable {
        padding-bottom: 8px;

        .components-item {
          display: inline-block;
          width: 48%;
          margin: 1%;
          transition: transform 0.2s ease;
          cursor: grab;

          .components-body {
            padding: 10px 8px;
            background: var(--el-fill-color-light);
            font-size: 12px;
            border: 1px solid var(--el-border-color-light);
            border-radius: 4px;
            text-align: center;
            transition: all 0.2s ease;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 4px;
            min-height: 60px;
            justify-content: center;

            .component-icon {
              font-size: 18px;
              color: var(--el-text-color-regular);
            }

            .component-label {
              color: var(--el-text-color-regular);
              line-height: 1.2;
              word-break: break-all;
            }

            &:hover {
              border: 1px solid var(--el-color-primary);
              background: var(--el-color-primary-light-9);
              color: var(--el-color-primary);
              transform: translateY(-1px);

              .component-icon,
              .component-label {
                color: var(--el-color-primary);
              }
            }
          }

          &:active {
            cursor: grabbing;
            
            .components-body {
              transform: scale(0.95);
            }
          }
        }
      }
    }
  }

  .search-wrapper {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    padding: 12px;
    background: var(--el-bg-color);
    border-top: 1px solid var(--el-border-color-extra-light);
  }
}

/* 滚动条样式 */
.left-scrollbar::-webkit-scrollbar {
  width: 6px;
}

.left-scrollbar::-webkit-scrollbar-track {
  background: var(--el-fill-color-light);
  border-radius: 3px;
}

.left-scrollbar::-webkit-scrollbar-thumb {
  background: var(--el-border-color);
  border-radius: 3px;
}

.left-scrollbar::-webkit-scrollbar-thumb:hover {
  background: var(--el-border-color-dark);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .left-board {
    width: 240px;
  }
  
  .components-item {
    width: 98% !important;
    margin: 1% !important;
  }
}

/* 空状态 */
.components-draggable:empty::after {
  content: '暂无组件';
  display: flex;
  align-items: center;
  justify-content: center;
  height: 60px;
  color: var(--el-text-color-placeholder);
  font-size: 12px;
  border: 1px dashed var(--el-border-color);
  border-radius: 4px;
  margin: 1%;
  width: 48%;
}
</style>
