<!--
  低代码页面生成器 - 主界面
  整合 Palette、Canvas、Inspector 三个核心组件
-->
<template>
  <div class="container">
    <!-- 左侧组件库 -->
    <Palette @add-component="handleAddComponent" />
    
    <!-- 中间画布 -->
    <Canvas
      :components="components"
      :selected-component-id="selectedComponentId || undefined"
      @update-components="handleUpdateComponents"
      @select-component="handleSelectComponent"
      @update-component="handleUpdateComponent"
      @delete-component="handleDeleteComponent"
      @move-component="handleMoveComponent"
    />
    
    <!-- 右侧属性面板 -->
    <Inspector
      :selected-component="selectedComponent"
      @update-component="handleUpdateComponent"
      @delete-component="handleDeleteComponent"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue';
import { ElMessage } from 'element-plus';
import Palette from './components/Palette.vue';
import Canvas from './components/Canvas.vue';
import Inspector from './components/Inspector.vue';
import { ComponentSchema } from './utils/schema';

// 响应式数据
const components = ref<ComponentSchema[]>([]);
const selectedComponentId = ref<string | null>(null);


// 计算属性
const selectedComponent = computed(() => {
  if (!selectedComponentId.value) return null;
  return findComponentById(components.value, selectedComponentId.value);
});

// 查找组件
function findComponentById(components: ComponentSchema[], id: string): ComponentSchema | null {
  for (const component of components) {
    if (component.id === id) {
      return component;
    }
    if (component.children) {
      const found = findComponentById(component.children, id);
      if (found) return found;
    }
  }
  return null;
}

// 处理添加组件
function handleAddComponent(component: ComponentSchema) {
  components.value.push(component);
  selectedComponentId.value = component.id;
  ElMessage.success(`已添加 ${component.type} 组件`);
}

// 处理更新组件列表
function handleUpdateComponents(newComponents: ComponentSchema[]) {
  components.value = newComponents;
}

// 处理选择组件
function handleSelectComponent(component: ComponentSchema | null) {
  selectedComponentId.value = component?.id || null;
}

// 处理更新组件
function handleUpdateComponent(component: ComponentSchema) {
  updateComponentById(components.value, component);
}

// 更新组件
function updateComponentById(components: ComponentSchema[], updatedComponent: ComponentSchema) {
  for (let i = 0; i < components.length; i++) {
    if (components[i].id === updatedComponent.id) {
      components[i] = updatedComponent;
      return;
    }
    if (components[i].children) {
      updateComponentById(components[i].children!, updatedComponent);
    }
  }
}

// 处理删除组件
function handleDeleteComponent(componentId: string) {
  deleteComponentById(components.value, componentId);
  if (selectedComponentId.value === componentId) {
    selectedComponentId.value = null;
  }
}

// 删除组件
function deleteComponentById(components: ComponentSchema[], id: string): boolean {
  for (let i = 0; i < components.length; i++) {
    if (components[i].id === id) {
      components.splice(i, 1);
      return true;
    }
    if (components[i].children) {
      if (deleteComponentById(components[i].children!, id)) {
        return true;
      }
    }
  }
  return false;
}

// 处理移动组件
function handleMoveComponent(fromIndex: number, toIndex: number) {
  const component = components.value.splice(fromIndex, 1)[0];
  components.value.splice(toIndex, 0, component);
}


// 组件挂载时加载本地数据
onMounted(() => {
  try {
    const savedComponents = localStorage.getItem('lowcode-components');
    if (savedComponents) {
      components.value = JSON.parse(savedComponents);
    }
  } catch (error) {
    console.warn('加载本地数据失败:', error);
  }
});

// 监听组件变化，自动保存到本地存储
watch(() => components.value, (newComponents) => {
  try {
    localStorage.setItem('lowcode-components', JSON.stringify(newComponents));
  } catch (error) {
    console.warn('保存到本地存储失败:', error);
  }
}, { deep: true });
</script>

<style scoped>
.container {
  position: relative;
  width: 100%;
  background-color: var(--el-bg-color-overlay);
  height: calc(100vh - 50px - 40px);
  overflow: hidden;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .container {
    height: calc(100vh - 40px);
  }
}

@media (max-width: 768px) {
  .container {
    height: calc(100vh - 30px);
  }
}
</style>
