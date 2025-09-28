<!--
  低代码页面生成器 - 属性检查器
  右侧编辑选中组件属性的面板
-->
<template>
  <div class="right-board">
    <el-tabs v-model="currentTab" stretch class="center-tabs">
      <el-tab-pane label="组件属性" name="field" />
      <el-tab-pane label="样式设置" name="style" />
    </el-tabs>
    
    <div class="field-box">
      <!-- 文档链接 -->
      <a 
        v-if="selectedComponent && getDocumentLink()"
        class="document-link" 
        target="_blank" 
        :href="getDocumentLink()" 
        title="查看组件文档"
      >
        <el-icon><Link /></el-icon>
      </a>
      
      <el-scrollbar class="right-scrollbar">
        <!-- 未选中组件 -->
        <div v-if="!selectedComponent" class="empty-inspector">
          <el-icon class="empty-icon"><Setting /></el-icon>
          <p>请选择一个组件来编辑属性</p>
        </div>
        
        <!-- 组件属性 -->
        <el-form 
          v-show="currentTab === 'field' && selectedComponent" 
          size="small" 
          label-width="90px" 
          label-position="top"
        >
          <!-- 基本信息 -->
          <el-form-item label="组件类型">
            <el-input :value="getComponentLabel(selectedComponent?.type || '')" disabled />
          </el-form-item>
          
          <el-form-item v-if="selectedComponent?.label !== undefined" label="标签">
            <el-input v-model="selectedComponent.label" placeholder="请输入标签" />
          </el-form-item>
          
          <!-- 布局组件特殊配置 -->
          <template v-if="selectedComponent?.type === 'el-row' || selectedComponent?.type === 'el-col'">
            <el-form-item label="间隔">
              <el-input
                :model-value="selectedComponent?.props?.gap || '12px'"
                placeholder="如: 12px, 1rem"
                @update:model-value="(value) => handlePropertyUpdate('gap', value)"
              />
            </el-form-item>
            
            <el-form-item label="主轴对齐">
              <el-select
                :model-value="selectedComponent?.props?.justifyContent || 'flex-start'"
                @update:model-value="(value) => handlePropertyUpdate('justifyContent', value)"
              >
                <el-option label="起始对齐" value="flex-start" />
                <el-option label="居中对齐" value="center" />
                <el-option label="末尾对齐" value="flex-end" />
                <el-option label="两端对齐" value="space-between" />
                <el-option label="环绕对齐" value="space-around" />
                <el-option label="平均对齐" value="space-evenly" />
              </el-select>
            </el-form-item>
            
            <el-form-item label="交叉轴对齐">
              <el-select
                :model-value="selectedComponent?.props?.alignItems || 'flex-start'"
                @update:model-value="(value) => handlePropertyUpdate('alignItems', value)"
              >
                <el-option label="起始对齐" value="flex-start" />
                <el-option label="居中对齐" value="center" />
                <el-option label="末尾对齐" value="flex-end" />
                <el-option label="拉伸对齐" value="stretch" />
              </el-select>
            </el-form-item>
          </template>
          
          <!-- 组件属性 -->
          <template v-for="propKey in getEditableProps()" :key="propKey">
            <el-form-item v-if="propKey !== 'columnCount'" :label="getPropertyLabel(propKey)">
              <PropertyEditor
                :prop-key="propKey"
                :prop-value="selectedComponent?.props?.[propKey]"
                :component-type="selectedComponent?.type || ''"
                @update="handlePropertyUpdate"
              />
            </el-form-item>
          </template>
        </el-form>
        
        <!-- 样式设置 -->
        <el-form 
          v-show="currentTab === 'style' && selectedComponent" 
          size="small" 
          label-width="90px" 
          label-position="top"
        >
          <el-form-item label="宽度">
            <el-input v-model="styleProps.width" placeholder="如: 100px, 50%, auto" />
          </el-form-item>
          <el-form-item label="高度">
            <el-input v-model="styleProps.height" placeholder="如: 100px, 50vh, auto" />
          </el-form-item>
          <el-form-item label="外边距">
            <el-input v-model="styleProps.margin" placeholder="如: 10px, 10px 20px" />
          </el-form-item>
          <el-form-item label="内边距">
            <el-input v-model="styleProps.padding" placeholder="如: 10px, 10px 20px" />
          </el-form-item>
          <el-form-item label="背景色">
            <el-color-picker v-model="styleProps.backgroundColor" show-alpha />
          </el-form-item>
          <el-form-item label="边框">
            <el-input v-model="styleProps.border" placeholder="如: 1px solid #ccc" />
          </el-form-item>
          <el-form-item label="圆角">
            <el-input v-model="styleProps.borderRadius" placeholder="如: 4px, 50%" />
          </el-form-item>
        </el-form>
      </el-scrollbar>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import { Setting, Link } from '@element-plus/icons-vue';
import PropertyEditor from './PropertyEditor.vue';
import { ComponentSchema, COMPONENT_CONFIGS, generateId } from '../utils/schema';

// 定义 Props
interface Props {
  selectedComponent: ComponentSchema | null;
}

// 定义 Emits
interface Emits {
  updateComponent: [component: ComponentSchema];
  deleteComponent: [componentId: string];
}

const props = defineProps<Props>();
const emit = defineEmits<Emits>();

// 响应式数据
const currentTab = ref('field');

// 计算属性 - 样式属性
const styleProps = computed({
  get() {
    return props.selectedComponent?.style || {};
  },
  set(value) {
    if (props.selectedComponent) {
      props.selectedComponent.style = { ...props.selectedComponent.style, ...value };
      emit('updateComponent', props.selectedComponent);
    }
  }
});


// 处理属性更新
function handlePropertyUpdate(key: string, value: any) {
  if (props.selectedComponent) {
    if (!props.selectedComponent.props) {
      props.selectedComponent.props = {};
    }
    props.selectedComponent.props[key] = value;
    emit('updateComponent', props.selectedComponent);
  }
}


// 获取文档链接
function getDocumentLink(): string {
  if (!props.selectedComponent) return '';
  const config = COMPONENT_CONFIGS[props.selectedComponent.type as keyof typeof COMPONENT_CONFIGS];
  return `https://element-plus.org/zh-CN/component/${props.selectedComponent.type.replace('el-', '')}`;
}

// 获取可编辑的属性列表
function getEditableProps(): string[] {
  if (!props.selectedComponent) return [];
  const config = COMPONENT_CONFIGS[props.selectedComponent.type as keyof typeof COMPONENT_CONFIGS];
  return config?.editableProps || [];
}

// 获取组件标签
function getComponentLabel(componentType: string): string {
  const config = COMPONENT_CONFIGS[componentType as keyof typeof COMPONENT_CONFIGS];
  return config?.label || componentType;
}

// 获取属性标签
function getPropertyLabel(key: string): string {
  const labelMap: Record<string, string> = {
    // 基础属性
    type: '类型',
    size: '尺寸',
    disabled: '禁用',
    children: '内容',
    
    // 按钮属性
    plain: '朴素按钮',
    round: '圆角',
    circle: '圆形',
    loading: '加载中',
    
    // 输入框属性
    placeholder: '占位符',
    clearable: '可清空',
    readonly: '只读',
    maxlength: '最大长度',
    showWordLimit: '显示字数统计',
    
    // 数字输入框
    min: '最小值',
    max: '最大值',
    step: '步长',
    precision: '精度',
    controls: '显示控制按钮',
    controlsPosition: '控制按钮位置',
    
    // 选择器
    multiple: '多选',
    filterable: '可筛选',
    
    // 单选/复选框
    border: '带边框',
    textColor: '文字颜色',
    fill: '填充色',
    indeterminate: '半选状态',
    
    // 开关
    width: '开关宽度',
    activeText: '打开文字',
    inactiveText: '关闭文字',
    activeValue: '打开值',
    inactiveValue: '关闭值',
    activeColor: '打开颜色',
    inactiveColor: '关闭颜色',
    
    // 滑块
    showStops: '显示间断点',
    showTooltip: '显示提示',
    range: '范围选择',
    
    // 日期/时间选择器
    format: '显示格式',
    valueFormat: '绑定值格式',
    
    // 表单
    model: '表单数据对象',
    rules: '表单验证规则',
    labelWidth: '标签宽度',
    labelPosition: '标签位置',
    inline: '行内表单',
    labelSuffix: '标签后缀',
    hideRequiredAsterisk: '隐藏必填星号',
    showMessage: '显示错误信息',
    inlineMessage: '行内显示错误信息',
    statusIcon: '显示状态图标',
    validateOnRuleChange: '规则改变时验证',
    
    // 表单项
    required: '必填',
    error: '错误信息',
    
    // 布局
    gap: '间隔',
    justifyContent: '主轴对齐',
    alignItems: '交叉轴对齐',
    gutter: '栅格间隔',
    justify: '水平排列',
    align: '垂直排列',
    span: '栅格占据列数',
    offset: '栅格左侧间隔',
    push: '栅格向右移动',
    pull: '栅格向左移动',
    tag: '自定义元素标签',
    direction: '排列方向',
    height: '高度',
    
    // 卡片
    header: '卡片标题',
    shadow: '阴影显示时机',
    bodyStyle: '内容区域样式',
    
    // 标签
    closable: '可关闭',
    disableTransitions: '禁用渐变动画',
    hit: '是否有边框描边',
    color: '背景色',
    effect: '主题',
    
    // 进度条
    percentage: '百分比',
    strokeWidth: '进度条宽度',
    textInside: '文字内显',
    status: '状态',
    showText: '显示文字',
    
    // 警告
    title: '标题',
    description: '描述',
    center: '文字居中',
    closeText: '关闭按钮文字',
    showIcon: '显示图标',
    
    // 分割线
    contentPosition: '内容位置',
    
    // 链接
    href: '链接地址',
    underline: '下划线'
  };
  
  return labelMap[key] || key;
}
</script>

<style scoped>
.right-board {
  width: 350px;
  position: absolute;
  right: 0;
  top: 0;
  padding-top: 3px;
  height: calc(100vh - 50px - 40px);
  background: var(--el-bg-color);
  border-left: 1px solid var(--el-border-color-light);

  :deep(.el-tabs__header) {
    margin: 0;
    background: var(--el-bg-color);
  }

  :deep(.el-input-group__append .el-button) {
    display: inline-flex;
  }

  .field-box {
    position: relative;
    height: calc(100vh - 50px - 40px - 42px);
    box-sizing: border-box;
    overflow: hidden;
  }

  .right-scrollbar {
    height: 100%;

    :deep(.el-scrollbar__view) {
      padding: 20px;
    }
  }
}

.empty-inspector {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 300px;
  color: var(--el-text-color-placeholder);
  text-align: center;

  .empty-icon {
    font-size: 48px;
    margin-bottom: 16px;
    color: var(--el-border-color);
  }

  p {
    margin: 8px 0;
    font-size: 14px;
  }
}

.document-link {
  position: absolute;
  display: flex;
  width: 26px;
  height: 26px;
  top: 0;
  left: 0;
  cursor: pointer;
  background: var(--el-color-primary);
  z-index: 10;
  border-radius: 0 0 6px 0;
  justify-content: center;
  align-items: center;
  color: var(--el-color-white);
  font-size: 14px;

  &:hover {
    background: var(--el-color-primary-dark-2);
  }
}

/* 表单样式 */
:deep(.el-form-item) {
  margin-bottom: 18px;
}

:deep(.el-form-item__label) {
  font-weight: 500;
  color: var(--el-text-color-regular);
  margin-bottom: 6px;
}

:deep(.el-input) {
  width: 100%;
}

:deep(.el-select) {
  width: 100%;
}

:deep(.el-color-picker) {
  width: 100%;
}

:deep(.el-slider) {
  width: 100%;
}

/* 提示文字样式 */
.form-item-tip {
  font-size: 12px;
  color: var(--el-text-color-placeholder);
  margin-top: 4px;
  line-height: 1.4;
}

/* 滚动条样式 */
.right-scrollbar::-webkit-scrollbar {
  width: 6px;
}

.right-scrollbar::-webkit-scrollbar-track {
  background: var(--el-fill-color-light);
  border-radius: 3px;
}

.right-scrollbar::-webkit-scrollbar-thumb {
  background: var(--el-border-color);
  border-radius: 3px;
}

.right-scrollbar::-webkit-scrollbar-thumb:hover {
  background: var(--el-border-color-dark);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .right-board {
    width: 300px;
  }
  
  .right-scrollbar {
    :deep(.el-scrollbar__view) {
      padding: 16px;
    }
  }
}
</style>
