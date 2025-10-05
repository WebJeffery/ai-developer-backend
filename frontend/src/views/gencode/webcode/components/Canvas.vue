<!--
  低代码页面生成器 - 画布组件
  中间可放置和编辑组件的画布区域
-->
<template>
  <div class="center-board">
    <div class="action-bar">
      <el-button icon="Download" type="primary" text @click="generateCode">
        导出vue文件
      </el-button>
      <el-button class="copy-btn-main" icon="DocumentCopy" type="primary" text @click="copyCode">
        复制代码
      </el-button>
      <el-button class="delete-btn" icon="Delete" text @click="clearCanvas" type="danger">
        清空
      </el-button>
    </div>
    
    <el-scrollbar class="center-scrollbar">
      <el-row class="center-board-row" :gutter="20">
        <div class="drawing-board-container">
          <draggable 
            class="drawing-board" 
            :list="components" 
            :animation="340" 
            group="componentsGroup"
            item-key="id"
            @add="handleAdd"
            @change="handleChange"
          >
            <template #item="{ element, index }">
              <CanvasComponent
                :key="element.id"
                :component="element"
                :index="index"
                :selected-id="selectedComponentId"
                :drawing-list="components"
                @select="handleSelectComponent"
                @update="handleUpdateComponent"
                @delete="handleDeleteComponent"
                @copy="handleCopyComponent"
              />
            </template>
          </draggable>
          
          <div v-show="!components.length" class="empty-info">
            从左侧拖入或点选组件进行页面设计
          </div>
        </div>
      </el-row>
    </el-scrollbar>
    
    <!-- 预览对话框 -->
    <el-dialog
      v-model="previewVisible"
      title="页面预览"
      width="80%"
      :before-close="handlePreviewClose"
    >
      <div class="preview-content">
        <iframe
          v-if="previewUrl"
          :src="previewUrl"
          frameborder="0"
          class="preview-iframe"
        />
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import { Delete, View, Download, Plus, DocumentCopy } from '@element-plus/icons-vue';
import draggable from 'vuedraggable';
import CanvasComponent from './CanvasComponent.vue';
import { ComponentSchema, generateId } from '../utils/schema';
import { generateVueFile, exportAsFile, copyToClipboard } from '../utils/serializer';

// 定义 Props
interface Props {
  components: ComponentSchema[];
  selectedComponentId?: string;
}

// 定义 Emits
interface Emits {
  updateComponents: [components: ComponentSchema[]];
  selectComponent: [component: ComponentSchema | null];
  updateComponent: [component: ComponentSchema];
  deleteComponent: [componentId: string];
  moveComponent: [fromIndex: number, toIndex: number];
}

const props = defineProps<Props>();
const emit = defineEmits<Emits>();

// 响应式数据
const previewVisible = ref(false);
const previewUrl = ref('');

// 处理拖拽添加
function handleAdd(event: any) {
  console.log('添加组件:', event);
}

// 处理拖拽变化
function handleChange(event: any) {
  console.log('组件变化:', event);
  emit('updateComponents', props.components);
}

// 处理组件选择
function handleSelectComponent(component: ComponentSchema) {
  emit('selectComponent', component);
}

// 处理组件更新
function handleUpdateComponent(component: ComponentSchema) {
  emit('updateComponent', component);
}

// 处理组件删除
function handleDeleteComponent(componentId: string) {
  emit('deleteComponent', componentId);
}

// 处理组件复制
function handleCopyComponent(component: ComponentSchema) {
  const newComponent = JSON.parse(JSON.stringify(component));
  newComponent.id = generateId();
  const newComponents = [...props.components, newComponent];
  emit('updateComponents', newComponents);
  ElMessage.success('组件已复制');
}

// 清空画布
function clearCanvas() {
  ElMessageBox.confirm('确定要清空所有组件吗？', '确认清空', {
    type: 'warning',
    confirmButtonText: '确定',
    cancelButtonText: '取消'
  }).then(() => {
    emit('updateComponents', []);
    emit('selectComponent', null);
    ElMessage.success('画布已清空');
  }).catch(() => {
    // 用户取消清空
  });
}

// 复制代码
async function copyCode() {
  if (props.components.length === 0) {
    ElMessage.warning('请先添加组件');
    return;
  }
  
  const pageSchema = {
    id: 'generated-page',
    name: '生成的页面',
    components: props.components
  };
  
  try {
    await copyToClipboard(pageSchema);
    ElMessage.success('代码已复制到剪贴板');
  } catch (error) {
    console.error('复制代码失败:', error);
    ElMessage.error('复制代码失败');
  }
}

// 预览页面
function previewPage() {
  if (props.components.length === 0) {
    ElMessage.warning('请先添加组件');
    return;
  }
  
  // 生成预览代码
  const pageSchema = {
    id: 'preview-page',
    name: '预览页面',
    components: props.components
  };
  
  const vueCode = generateVueFile(pageSchema);
  
  // 创建预览 URL
  const blob = new Blob([vueCode], { type: 'text/html' });
  previewUrl.value = URL.createObjectURL(blob);
  previewVisible.value = true;
}

// 关闭预览
function handlePreviewClose() {
  previewVisible.value = false;
  if (previewUrl.value) {
    URL.revokeObjectURL(previewUrl.value);
    previewUrl.value = '';
  }
}

// 生成代码
async function generateCode() {
  if (props.components.length === 0) {
    ElMessage.warning('请先添加组件');
    return;
  }
  
  const pageSchema = {
    id: 'generated-page',
    name: '生成的页面',
    components: props.components
  };
  
  try {
    // 复制到剪贴板
    await copyToClipboard(pageSchema);
    ElMessage.success('代码已复制到剪贴板');
    
    // 同时提供下载选项
    ElMessageBox.confirm('代码已复制到剪贴板，是否同时下载文件？', '生成完成', {
      confirmButtonText: '下载',
      cancelButtonText: '取消',
      type: 'success'
    }).then(() => {
      exportAsFile(pageSchema, 'generated-page.vue');
    }).catch(() => {
      // 用户取消下载
    });
  } catch (error) {
    console.error('生成代码失败:', error);
    ElMessage.error('生成代码失败');
  }
}

// 获取组件标签
function getComponentLabel(componentType: string): string {
  // 这里可以根据组件类型返回对应的标签
  const typeMap: Record<string, string> = {
    'el-button': '按钮',
    'el-input': '输入框',
    'el-select': '选择器',
    'el-card': '卡片',
    'el-form': '表单',
    'el-row': '行',
    'el-col': '列'
  };
  
  return typeMap[componentType] || componentType;
}

// 监听组件变化，自动保存到本地存储
watch(() => props.components, (newComponents) => {
  try {
    localStorage.setItem('lowcode-canvas-components', JSON.stringify(newComponents));
  } catch (error) {
    console.warn('保存到本地存储失败:', error);
  }
}, { deep: true });
</script>

<style scoped>
.center-board {
  height: calc(100vh - 50px - 40px);
  width: auto;
  margin: 0 350px 0 260px;
  box-sizing: border-box;
  background: var(--el-bg-color);

  .action-bar {
    position: relative;
    height: 42px;
    padding: 0 15px;
    box-sizing: border-box;
    border: 1px solid var(--el-border-color-extra-light);
    border-top: none;
    border-left: none;
    display: flex;
    align-items: center;
    justify-content: flex-end;
    background: var(--el-bg-color);
    gap: 8px;

    .delete-btn {
      color: var(--el-color-danger);
    }
  }

  .center-scrollbar {
    height: calc(100vh - 50px - 40px - 42px);
    overflow: hidden;
    border-left: 1px solid var(--el-border-color-extra-light);
    border-right: 1px solid var(--el-border-color-extra-light);
    box-sizing: border-box;
    background: var(--el-bg-color-page);

    .el-scrollbar__view {
      overflow-x: hidden;
    }

    .center-board-row {
      padding: 12px 12px 15px 12px;
      box-sizing: border-box;

      .drawing-board-container {
        width: 100%;
        min-height: calc(100vh - 50px - 40px - 69px);
        position: relative;

        .drawing-board {
          min-height: calc(100vh - 50px - 40px - 69px);
          position: relative;
          padding: 20px;
          background: var(--el-bg-color);
          border-radius: 6px;
          box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);

          .sortable-ghost {
            position: relative;
            display: block;
            overflow: hidden;

            &::before {
              content: " ";
              position: absolute;
              left: 0;
              right: 0;
              top: 0;
              height: 3px;
              background: var(--el-color-primary);
              z-index: 2;
            }
          }
        }

        .empty-info {
          position: absolute;
          top: 46%;
          left: 0;
          right: 0;
          text-align: center;
          font-size: 18px;
          color: var(--el-text-color-placeholder);
          letter-spacing: 4px;
          pointer-events: none;
        }
      }
    }
  }
}

.preview-content {
  height: 70vh;
  border: 1px solid var(--el-border-color);
  border-radius: 4px;
  overflow: hidden;
}

.preview-iframe {
  width: 100%;
  height: 100%;
  border: none;
}

/* 滚动条样式 */
.center-scrollbar::-webkit-scrollbar {
  width: 6px;
}

.center-scrollbar::-webkit-scrollbar-track {
  background: var(--el-fill-color-light);
  border-radius: 3px;
}

.center-scrollbar::-webkit-scrollbar-thumb {
  background: var(--el-border-color);
  border-radius: 3px;
}

.center-scrollbar::-webkit-scrollbar-thumb:hover {
  background: var(--el-border-color-dark);
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .center-board {
    margin: 0 300px 0 240px;
  }
}

@media (max-width: 768px) {
  .center-board {
    margin: 0;
    width: 100%;
  }
  
  .action-bar {
    padding: 0 8px;
    flex-wrap: wrap;
    gap: 4px;
  }
}
</style>
