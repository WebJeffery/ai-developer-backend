<!--
  低代码页面生成器 - 属性编辑器
  根据属性类型渲染不同的编辑器
-->
<template>
  <div class="property-editor">
    <!-- 字符串输入 -->
    <el-input
      v-if="isStringType"
      :model-value="propValue"
      :placeholder="getPlaceholder()"
      @update:model-value="handleUpdate"
    />
    
    <!-- 数字输入 -->
    <el-input-number
      v-else-if="isNumberType"
      :model-value="propValue"
      :min="getMinValue()"
      :max="getMaxValue()"
      :step="getStepValue()"
      :precision="getPrecision()"
      @update:model-value="handleUpdate"
    />
    
    <!-- 布尔开关 -->
    <el-switch
      v-else-if="isBooleanType"
      :model-value="propValue"
      @update:model-value="handleUpdate"
    />
    
    <!-- 选择器 -->
    <el-select
      v-else-if="isSelectType"
      :model-value="propValue"
      :placeholder="getPlaceholder()"
      @update:model-value="handleUpdate"
    >
      <el-option
        v-for="option in getSelectOptions()"
        :key="option.value"
        :label="option.label"
        :value="option.value"
      />
    </el-select>
    
    <!-- 颜色选择器 -->
    <el-color-picker
      v-else-if="isColorType"
      :model-value="propValue"
      :show-alpha="getShowAlpha()"
      :color-format="getColorFormat()"
      @update:model-value="handleUpdate"
    />
    
    <!-- 滑块 -->
    <el-slider
      v-else-if="isSliderType"
      :model-value="propValue"
      :min="getMinValue()"
      :max="getMaxValue()"
      :step="getStepValue()"
      :show-stops="getShowStops()"
      :range="getRange()"
      @update:model-value="handleUpdate"
    />
    
    <!-- 文本域 -->
    <el-input
      v-else-if="isTextareaType"
      :model-value="propValue"
      type="textarea"
      :rows="getTextareaRows()"
      :placeholder="getPlaceholder()"
      @update:model-value="handleUpdate"
    />
    
    <!-- 对象编辑器 -->
    <div v-else-if="isObjectType" class="object-editor">
      <el-input
        :model-value="JSON.stringify(propValue, null, 2)"
        type="textarea"
        :rows="4"
        placeholder="JSON 对象"
        @update:model-value="handleObjectUpdate"
      />
    </div>
    
    <!-- 数组编辑器 -->
    <div v-else-if="isArrayType" class="array-editor">
      <div v-for="(item, index) in propValue" :key="index" class="array-item">
        <el-input
          :model-value="item"
          :placeholder="`项目 ${index + 1}`"
          @update:model-value="handleArrayItemUpdate(index, $event)"
        />
        <el-button
          size="small"
          type="danger"
          @click="removeArrayItem(index)"
        >
          <el-icon><Delete /></el-icon>
        </el-button>
      </div>
      <el-button size="small" @click="addArrayItem">
        <el-icon><Plus /></el-icon>
        添加项目
      </el-button>
    </div>
    
    <!-- 默认输入框 -->
    <el-input
      v-else
      :model-value="String(propValue)"
      :placeholder="getPlaceholder()"
      @update:model-value="handleUpdate"
    />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { Delete, Plus } from '@element-plus/icons-vue';

// 定义 Props
interface Props {
  propKey: string;
  propValue: any;
  componentType: string;
}

// 定义 Emits
interface Emits {
  update: [key: string, value: any];
}

const props = defineProps<Props>();
const emit = defineEmits<Emits>();

// 计算属性 - 判断属性类型
const isStringType = computed(() => {
  return typeof props.propValue === 'string' && !isSelectType.value && !isTextareaType.value;
});

const isNumberType = computed(() => {
  return typeof props.propValue === 'number' || 
         (typeof props.propValue === 'string' && !isNaN(Number(props.propValue)));
});

const isBooleanType = computed(() => {
  return typeof props.propValue === 'boolean';
});

const isSelectType = computed(() => {
  const selectProps = ['type', 'size', 'status', 'position', 'placement', 'trigger'];
  return selectProps.includes(props.propKey);
});

const isColorType = computed(() => {
  return props.propKey.includes('color') || props.propKey.includes('Color');
});

const isSliderType = computed(() => {
  return ['min', 'max', 'step', 'value'].includes(props.propKey);
});

const isTextareaType = computed(() => {
  return props.propKey.includes('text') || 
         props.propKey.includes('content') || 
         props.propKey.includes('description');
});

const isObjectType = computed(() => {
  return typeof props.propValue === 'object' && !Array.isArray(props.propValue);
});

const isArrayType = computed(() => {
  return Array.isArray(props.propValue);
});

// 处理更新
function handleUpdate(value: any) {
  emit('update', props.propKey, value);
}

// 处理对象更新
function handleObjectUpdate(value: string) {
  try {
    const obj = JSON.parse(value);
    emit('update', props.propKey, obj);
  } catch (error) {
    console.error('JSON 解析错误:', error);
  }
}

// 处理数组项更新
function handleArrayItemUpdate(index: number, value: any) {
  const newArray = [...props.propValue];
  newArray[index] = value;
  emit('update', props.propKey, newArray);
}

// 添加数组项
function addArrayItem() {
  const newArray = [...props.propValue, ''];
  emit('update', props.propKey, newArray);
}

// 删除数组项
function removeArrayItem(index: number) {
  const newArray = props.propValue.filter((_: any, i: number) => i !== index);
  emit('update', props.propKey, newArray);
}

// 获取占位符
function getPlaceholder(): string {
  const placeholders: Record<string, string> = {
    placeholder: '请输入占位符',
    label: '请输入标签',
    text: '请输入文本',
    value: '请输入值',
    name: '请输入名称',
    id: '请输入ID',
    class: '请输入CSS类名',
    style: '请输入样式',
    title: '请输入标题',
    content: '请输入内容',
    description: '请输入描述'
  };
  
  return placeholders[props.propKey] || '请输入值';
}

// 获取选择器选项
function getSelectOptions() {
  const optionMap: Record<string, Array<{ label: string; value: any }>> = {
    type: getTypeOptions(),
    size: [
      { label: '大', value: 'large' },
      { label: '默认', value: 'default' },
      { label: '小', value: 'small' }
    ],
    shadow: [
      { label: '总是显示', value: 'always' },
      { label: '悬停时显示', value: 'hover' },
      { label: '从不显示', value: 'never' }
    ],
    justify: [
      { label: '左对齐', value: 'start' },
      { label: '居中', value: 'center' },
      { label: '右对齐', value: 'end' },
      { label: '两端对齐', value: 'space-between' },
      { label: '环绕对齐', value: 'space-around' },
      { label: '平均对齐', value: 'space-evenly' }
    ],
    align: [
      { label: '顶部', value: 'top' },
      { label: '中间', value: 'middle' },
      { label: '底部', value: 'bottom' }
    ],
    labelPosition: [
      { label: '右侧', value: 'right' },
      { label: '左侧', value: 'left' },
      { label: '顶部', value: 'top' }
    ],
    direction: [
      { label: '垂直', value: 'vertical' },
      { label: '水平', value: 'horizontal' }
    ],
    contentPosition: [
      { label: '左侧', value: 'left' },
      { label: '居中', value: 'center' },
      { label: '右侧', value: 'right' }
    ],
    effect: [
      { label: '浅色', value: 'light' },
      { label: '深色', value: 'dark' }
    ]
  };
  
  return optionMap[props.propKey] || [];
}

// 根据组件类型获取type选项
function getTypeOptions() {
  const componentTypeOptions: Record<string, Array<{ label: string; value: any }>> = {
    'el-button': [
      { label: '默认', value: 'default' },
      { label: '主要', value: 'primary' },
      { label: '成功', value: 'success' },
      { label: '信息', value: 'info' },
      { label: '警告', value: 'warning' },
      { label: '危险', value: 'danger' },
      { label: '文本', value: 'text' }
    ],
    'el-input': [
      { label: '文本', value: 'text' },
      { label: '密码', value: 'password' },
      { label: '数字', value: 'number' },
      { label: '邮箱', value: 'email' },
      { label: '电话', value: 'tel' },
      { label: 'URL', value: 'url' }
    ],
    'el-alert': [
      { label: '成功', value: 'success' },
      { label: '信息', value: 'info' },
      { label: '警告', value: 'warning' },
      { label: '错误', value: 'error' }
    ],
    'el-tag': [
      { label: '默认', value: '' },
      { label: '成功', value: 'success' },
      { label: '信息', value: 'info' },
      { label: '警告', value: 'warning' },
      { label: '危险', value: 'danger' }
    ],
    'el-link': [
      { label: '默认', value: 'default' },
      { label: '主要', value: 'primary' },
      { label: '成功', value: 'success' },
      { label: '信息', value: 'info' },
      { label: '警告', value: 'warning' },
      { label: '危险', value: 'danger' }
    ],
    'el-text': [
      { label: '主要', value: 'primary' },
      { label: '常规', value: 'regular' },
      { label: '次要', value: 'secondary' },
      { label: '占位符', value: 'placeholder' },
      { label: '禁用', value: 'disabled' }
    ],
    'el-progress': [
      { label: '线形', value: 'line' },
      { label: '环形', value: 'circle' },
      { label: '仪表盘', value: 'dashboard' }
    ],
    'el-date-picker': [
      { label: '日期', value: 'date' },
      { label: '周', value: 'week' },
      { label: '月', value: 'month' },
      { label: '年', value: 'year' },
      { label: '日期时间', value: 'datetime' },
      { label: '日期范围', value: 'daterange' },
      { label: '月范围', value: 'monthrange' },
      { label: '日期时间范围', value: 'datetimerange' }
    ]
  };
  
  return componentTypeOptions[props.componentType] || [
    { label: '默认', value: 'default' },
    { label: '主要', value: 'primary' },
    { label: '成功', value: 'success' },
    { label: '信息', value: 'info' },
    { label: '警告', value: 'warning' },
    { label: '危险', value: 'danger' }
  ];
}

// 获取最小值
function getMinValue(): number {
  const minMap: Record<string, number> = {
    min: 0,
    max: 0,
    step: 0,
    value: 0,
    span: 1,
    offset: 0,
    push: 0,
    pull: 0,
    columnCount: 1,
    percentage: 0,
    width: 0
  };
  
  return minMap[props.propKey] ?? -Infinity;
}

// 获取最大值
function getMaxValue(): number {
  const maxMap: Record<string, number> = {
    span: 24,
    offset: 23,
    push: 23,
    pull: 23,
    maxlength: 1000,
    columnCount: 6,
    percentage: 100,
    width: 200
  };
  
  return maxMap[props.propKey] ?? Infinity;
}

// 获取步长
function getStepValue(): number {
  return props.propKey === 'step' ? 1 : 0.1;
}

// 获取精度
function getPrecision(): number {
  return props.propKey === 'precision' ? 0 : 2;
}

// 获取是否显示透明度
function getShowAlpha(): boolean {
  return props.propKey.includes('alpha') || props.propKey === 'backgroundColor';
}

// 获取颜色格式
function getColorFormat(): string {
  return props.propKey.includes('alpha') ? 'rgba' : 'hex';
}

// 获取是否显示间断点
function getShowStops(): boolean {
  return props.propKey === 'step' || props.propKey === 'value';
}

// 获取是否范围选择
function getRange(): boolean {
  return props.propKey === 'value' && props.componentType === 'el-slider';
}

// 获取文本域行数
function getTextareaRows(): number {
  return props.propKey.includes('description') ? 4 : 2;
}
</script>

<style scoped>
.property-editor {
  width: 100%;
}

.object-editor {
  width: 100%;
}

.array-editor {
  width: 100%;
}

.array-item {
  display: flex;
  gap: 8px;
  margin-bottom: 8px;
  align-items: center;
}

.array-item .el-input {
  flex: 1;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .array-item {
    flex-direction: column;
    align-items: stretch;
  }
  
  .array-item .el-button {
    width: 100%;
  }
}
</style>
