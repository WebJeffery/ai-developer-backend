<!--
  组件渲染器 - 根据组件类型渲染不同的 Element Plus 组件
  确保每个组件都能正确显示和交互
-->
<template>
  <div class="component-renderer">
    <!-- 按钮组件 -->
    <el-button 
      v-if="component.type === 'el-button'"
      v-bind="component.props"
      @click="handleClick"
    >
      {{ component.props?.children || '按钮' }}
    </el-button>
    
    <!-- 链接组件 -->
    <el-link 
      v-else-if="component.type === 'el-link'"
      v-bind="component.props"
      @click="handleClick"
    >
      {{ component.props?.children || '链接' }}
    </el-link>
    
    <!-- 文本组件 -->
    <el-text 
      v-else-if="component.type === 'el-text'"
      v-bind="component.props"
    >
      {{ component.props?.children || '文本内容' }}
    </el-text>
    
    <!-- 输入框组件 -->
    <el-input 
      v-else-if="component.type === 'el-input'"
      v-bind="component.props"
      :model-value="getInputValue()"
      @input="handleInput"
    />
    
    <!-- 数字输入框 -->
    <el-input-number 
      v-else-if="component.type === 'el-input-number'"
      v-bind="component.props"
      :model-value="getNumberValue()"
      @change="handleNumberChange"
    />
    
    <!-- 选择器 -->
    <el-select 
      v-else-if="component.type === 'el-select'"
      v-bind="component.props"
      :model-value="getSelectValue()"
      @change="handleSelectChange"
    >
      <el-option
        v-for="option in getSelectOptions()"
        :key="option.value"
        :label="option.label"
        :value="option.value"
      />
    </el-select>
    
    <!-- 单选框 -->
    <el-radio 
      v-else-if="component.type === 'el-radio'"
      v-bind="component.props"
      :model-value="getRadioValue()"
      @change="handleRadioChange"
    >
      {{ component.props?.label || '选项' }}
    </el-radio>
    
    <!-- 单选框组 -->
    <el-radio-group 
      v-else-if="component.type === 'el-radio-group'"
      v-bind="component.props"
      :model-value="getRadioGroupValue()"
      @change="handleRadioGroupChange"
    >
      <el-radio 
        v-for="option in getRadioOptions()"
        :key="option.value"
        :label="option.value"
      >
        {{ option.label }}
      </el-radio>
    </el-radio-group>
    
    <!-- 复选框 -->
    <el-checkbox 
      v-else-if="component.type === 'el-checkbox'"
      v-bind="component.props"
      :model-value="getCheckboxValue()"
      @change="handleCheckboxChange"
    >
      {{ component.props?.label || '选项' }}
    </el-checkbox>
    
    <!-- 复选框组 -->
    <el-checkbox-group 
      v-else-if="component.type === 'el-checkbox-group'"
      v-bind="component.props"
      :model-value="getCheckboxGroupValue()"
      @change="handleCheckboxGroupChange"
    >
      <el-checkbox 
        v-for="option in getCheckboxOptions()"
        :key="option.value"
        :label="option.value"
      >
        {{ option.label }}
      </el-checkbox>
    </el-checkbox-group>
    
    <!-- 开关 -->
    <el-switch 
      v-else-if="component.type === 'el-switch'"
      v-bind="component.props"
      :model-value="getSwitchValue()"
      @change="handleSwitchChange"
    />
    
    <!-- 滑块 -->
    <el-slider 
      v-else-if="component.type === 'el-slider'"
      v-bind="component.props"
      :model-value="getSliderValue()"
      @change="handleSliderChange"
    />
    
    <!-- 日期选择器 -->
    <el-date-picker 
      v-else-if="component.type === 'el-date-picker'"
      v-bind="component.props"
      :model-value="getDateValue()"
      @change="handleDateChange"
    />
    
    <!-- 时间选择器 -->
    <el-time-picker 
      v-else-if="component.type === 'el-time-picker'"
      v-bind="component.props"
      :model-value="getTimeValue()"
      @change="handleTimeChange"
    />
    
    <!-- 卡片 -->
    <el-card 
      v-else-if="component.type === 'el-card'"
      v-bind="component.props"
    >
      <slot name="children">
        <div class="card-placeholder">
          {{ component.props?.children || '卡片内容区域' }}
        </div>
      </slot>
    </el-card>
    
    <!-- 标签 -->
    <el-tag 
      v-else-if="component.type === 'el-tag'"
      v-bind="component.props"
    >
      {{ component.props?.children || '标签' }}
    </el-tag>
    
    <!-- 进度条 -->
    <el-progress 
      v-else-if="component.type === 'el-progress'"
      v-bind="component.props"
    />
    
    <!-- 警告 -->
    <el-alert 
      v-else-if="component.type === 'el-alert'"
      v-bind="component.props"
    />
    
    <!-- 分割线 -->
    <el-divider 
      v-else-if="component.type === 'el-divider'"
      v-bind="component.props"
    >
      {{ component.props?.children }}
    </el-divider>
    
    <!-- 表单 -->
    <el-form 
      v-else-if="component.type === 'el-form'"
      v-bind="component.props"
      class="form-container"
    >
      <slot name="children">
        <div class="form-placeholder">拖拽表单项到此处</div>
      </slot>
    </el-form>
    
    <!-- 表单项 -->
    <el-form-item 
      v-else-if="component.type === 'el-form-item'"
      v-bind="component.props"
    >
      <slot name="children">
        <div class="form-item-placeholder">拖拽表单控件到此处</div>
      </slot>
    </el-form-item>
    
    <!-- 行布局 -->
    <div 
      v-else-if="component.type === 'el-row'"
      class="row-layout"
      :style="getRowStyle()"
    >
      <slot name="children">
        <div class="layout-placeholder">
          <el-icon><Grid /></el-icon>
          <span>行布局 - 水平排列容器</span>
          <small>拖拽组件到此处，它们将水平排列</small>
        </div>
      </slot>
    </div>
    
    <!-- 列布局 -->
    <div 
      v-else-if="component.type === 'el-col'"
      class="col-layout"
      :style="getColStyle()"
    >
      <slot name="children">
        <div class="layout-placeholder">
          <el-icon><Grid /></el-icon>
          <span>列布局 - 垂直排列容器</span>
          <small>拖拽组件到此处，它们将垂直排列</small>
        </div>
      </slot>
    </div>
    
    <!-- 容器布局 -->
    <el-container 
      v-else-if="component.type === 'el-container'"
      v-bind="component.props"
      class="container-layout"
    >
      <slot name="children">
        <div class="container-placeholder">拖拽容器组件到此处</div>
      </slot>
    </el-container>
    
    <!-- 头部 -->
    <el-header 
      v-else-if="component.type === 'el-header'"
      v-bind="component.props"
      class="header-container"
    >
      <slot name="children">
        <div class="header-placeholder">头部内容</div>
      </slot>
    </el-header>
    
    <!-- 主要区域 -->
    <el-main 
      v-else-if="component.type === 'el-main'"
      v-bind="component.props"
      class="main-container"
    >
      <slot name="children">
        <div class="main-placeholder">主要内容区域</div>
      </slot>
    </el-main>
    
    <!-- 侧边栏 -->
    <el-aside 
      v-else-if="component.type === 'el-aside'"
      v-bind="component.props"
      class="aside-container"
    >
      <slot name="children">
        <div class="aside-placeholder">侧边栏内容</div>
      </slot>
    </el-aside>
    
    <!-- 底部 -->
    <el-footer 
      v-else-if="component.type === 'el-footer'"
      v-bind="component.props"
      class="footer-container"
    >
      <slot name="children">
        <div class="footer-placeholder">底部内容</div>
      </slot>
    </el-footer>
    
    <!-- 未知组件 -->
    <div v-else class="unknown-component">
      未知组件: {{ component.type }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { Grid, Plus } from '@element-plus/icons-vue';
import { ComponentSchema } from '../utils/schema';

// 定义 Props
interface Props {
  component: ComponentSchema;
}

const props = defineProps<Props>();

// 事件处理
function handleClick() {
  console.log('按钮点击');
}

function handleInput(value: string) {
  console.log('输入值:', value);
}

function handleNumberChange(value: number | undefined) {
  console.log('数字变化:', value);
}

function handleSelectChange(value: any) {
  console.log('选择变化:', value);
}

function handleRadioChange(value: any) {
  console.log('单选变化:', value);
}

function handleRadioGroupChange(value: any) {
  console.log('单选组变化:', value);
}

function handleCheckboxChange(value: any) {
  console.log('复选框变化:', value);
}

function handleCheckboxGroupChange(value: any[]) {
  console.log('复选框组变化:', value);
}

function handleSwitchChange(value: any) {
  console.log('开关变化:', value);
}

function handleSliderChange(value: any) {
  console.log('滑块变化:', value);
}

function handleDateChange(value: any) {
  console.log('日期变化:', value);
}

function handleTimeChange(value: any) {
  console.log('时间变化:', value);
}

// 获取各种组件的值
function getInputValue() {
  return props.component.props?.modelValue || '';
}

function getNumberValue() {
  return props.component.props?.modelValue || 0;
}

function getSelectValue() {
  return props.component.props?.modelValue || '';
}

function getRadioValue() {
  return props.component.props?.modelValue || false;
}

function getRadioGroupValue() {
  return props.component.props?.modelValue || '';
}

function getCheckboxValue() {
  return props.component.props?.modelValue || false;
}

function getCheckboxGroupValue() {
  return props.component.props?.modelValue || [];
}

function getSwitchValue() {
  return props.component.props?.modelValue || false;
}

function getSliderValue() {
  return props.component.props?.modelValue || 0;
}

function getDateValue() {
  return props.component.props?.modelValue || null;
}

function getTimeValue() {
  return props.component.props?.modelValue || null;
}

// 获取选项数据
function getSelectOptions() {
  return [
    { label: '选项一', value: 'option1' },
    { label: '选项二', value: 'option2' },
    { label: '选项三', value: 'option3' }
  ];
}

function getRadioOptions() {
  return [
    { label: '选项一', value: 'radio1' },
    { label: '选项二', value: 'radio2' }
  ];
}

function getCheckboxOptions() {
  return [
    { label: '选项一', value: 'checkbox1' },
    { label: '选项二', value: 'checkbox2' }
  ];
}

// 获取行布局样式
function getRowStyle() {
  const defaultStyle = {
    display: 'flex',
    flexDirection: 'row',
    gap: '12px',
    padding: '12px',
    border: '1px dashed var(--el-border-color)',
    borderRadius: '4px',
    minHeight: '60px',
    background: 'var(--el-fill-color-lighter)'
  };
  
  const customStyle = props.component.props?.style || {};
  const gap = props.component.props?.gap || '12px';
  const justifyContent = props.component.props?.justifyContent || 'flex-start';
  const alignItems = props.component.props?.alignItems || 'flex-start';
  
  return {
    ...defaultStyle,
    ...customStyle,
    gap,
    justifyContent,
    alignItems
  };
}

// 获取列布局样式
function getColStyle() {
  const defaultStyle = {
    display: 'flex',
    flexDirection: 'column',
    gap: '12px',
    padding: '12px',
    border: '1px dashed var(--el-border-color)',
    borderRadius: '4px',
    minHeight: '60px',
    background: 'var(--el-fill-color-lighter)'
  };
  
  const customStyle = props.component.props?.style || {};
  const gap = props.component.props?.gap || '12px';
  const justifyContent = props.component.props?.justifyContent || 'flex-start';
  const alignItems = props.component.props?.alignItems || 'flex-start';
  
  return {
    ...defaultStyle,
    ...customStyle,
    gap,
    justifyContent,
    alignItems
  };
}
</script>

<style scoped>
.component-renderer {
  width: 100%;
}

/* 占位符样式 */
.card-placeholder,
.form-placeholder,
.form-item-placeholder,
.row-placeholder,
.col-placeholder,
.container-placeholder,
.header-placeholder,
.main-placeholder,
.aside-placeholder,
.footer-placeholder {
  padding: 20px;
  text-align: center;
  color: var(--el-text-color-placeholder);
  background: var(--el-fill-color-lighter);
  border: 1px dashed var(--el-border-color);
  border-radius: 4px;
  min-height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
}

/* 容器组件样式 */
.form-container {
  border: 1px dashed var(--el-border-color);
  border-radius: 4px;
  padding: 20px;
  min-height: 120px;
  background: var(--el-fill-color-lighter);
  position: relative;
}

.row-layout,
.col-layout {
  position: relative;
  transition: all 0.2s ease;
  margin: 8px 0;
}

.row-layout:hover,
.col-layout:hover {
  border-color: var(--el-color-primary) !important;
  background: var(--el-color-primary-light-9) !important;
}

.layout-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;
  color: var(--el-text-color-placeholder);
  text-align: center;
  padding: 20px;
}

.layout-placeholder .el-icon {
  font-size: 24px;
}

.layout-placeholder span {
  font-size: 14px;
  font-weight: 500;
}

.layout-placeholder small {
  font-size: 12px;
  opacity: 0.8;
}

.container-layout {
  border: 1px dashed var(--el-border-color);
  border-radius: 4px;
  min-height: 200px;
  background: var(--el-fill-color-lighter);
  padding: 16px;
}

.header-container,
.footer-container {
  border: 1px dashed var(--el-border-color);
  border-radius: 4px;
  background: var(--el-fill-color-lighter);
}

.main-container {
  border: 1px dashed var(--el-border-color);
  border-radius: 4px;
  background: var(--el-fill-color-lighter);
  min-height: 200px;
}

.aside-container {
  border: 1px dashed var(--el-border-color);
  border-radius: 4px;
  background: var(--el-fill-color-lighter);
}

.unknown-component {
  padding: 16px;
  background: var(--el-color-danger-light-9);
  border: 1px dashed var(--el-color-danger);
  border-radius: 4px;
  color: var(--el-color-danger);
  text-align: center;
  font-size: 14px;
}

/* 组件间距 */
.component-renderer > * {
  margin: 4px 0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .card-placeholder,
  .form-placeholder,
  .form-item-placeholder,
  .row-placeholder,
  .col-placeholder,
  .container-placeholder,
  .header-placeholder,
  .main-placeholder,
  .aside-placeholder,
  .footer-placeholder {
    padding: 12px;
    min-height: 40px;
    font-size: 12px;
  }
  
  .form-container,
  .row-container,
  .col-container {
    padding: 8px;
    min-height: 60px;
  }
}
</style>
