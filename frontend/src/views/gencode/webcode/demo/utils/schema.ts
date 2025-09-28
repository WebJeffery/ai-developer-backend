/**
 * 低代码页面生成器 - 组件 Schema 定义
 * 定义组件的 JSON 结构和类型
 */

// 基础组件属性接口
export interface BaseComponentProps {
  id: string;
  type: string;
  label?: string;
  children?: ComponentSchema[];
  style?: Record<string, any>;
  class?: string | string[];
}

// Element Plus 组件类型枚举（只包含已配置的组件）
export enum ComponentType {
  // 基础组件
  BUTTON = 'el-button',
  LINK = 'el-link',
  TEXT = 'el-text',
  
  // 布局组件
  ROW = 'el-row',
  COL = 'el-col',
  CONTAINER = 'el-container',
  HEADER = 'el-header',
  MAIN = 'el-main',
  ASIDE = 'el-aside',
  FOOTER = 'el-footer',
  
  // 表单组件
  FORM = 'el-form',
  FORM_ITEM = 'el-form-item',
  INPUT = 'el-input',
  INPUT_NUMBER = 'el-input-number',
  SELECT = 'el-select',
  RADIO = 'el-radio',
  RADIO_GROUP = 'el-radio-group',
  CHECKBOX = 'el-checkbox',
  CHECKBOX_GROUP = 'el-checkbox-group',
  SWITCH = 'el-switch',
  SLIDER = 'el-slider',
  TIME_PICKER = 'el-time-picker',
  DATE_PICKER = 'el-date-picker',
  
  // 数据展示组件
  CARD = 'el-card',
  TAG = 'el-tag',
  PROGRESS = 'el-progress',
  
  // 反馈组件
  ALERT = 'el-alert',
  
  // 其他组件
  DIVIDER = 'el-divider'
}

// 组件 Schema 接口
export interface ComponentSchema extends BaseComponentProps {
  props?: Record<string, any>;
  events?: Record<string, string>;
  slots?: Record<string, string>;
}

// 页面 Schema 接口
export interface PageSchema {
  id: string;
  name: string;
  components: ComponentSchema[];
  globalStyle?: Record<string, any>;
}

// 组件配置接口
export interface ComponentConfig {
  type: ComponentType;
  label: string;
  icon: string;
  category: string;
  defaultProps: Record<string, any>;
  editableProps: string[];
  canHaveChildren: boolean;
  maxChildren?: number;
}

// 组件库配置
export const COMPONENT_CONFIGS: Record<ComponentType, ComponentConfig> = {
  // 基础组件
  [ComponentType.BUTTON]: {
    type: ComponentType.BUTTON,
    label: '按钮',
    icon: 'el-icon-edit',
    category: '基础',
    defaultProps: {
      type: 'primary',
      size: 'default',
      plain: false,
      round: false,
      circle: false,
      disabled: false,
      loading: false,
      children: '按钮'
    },
    editableProps: ['type', 'size', 'plain', 'round', 'circle', 'disabled', 'loading', 'children'],
    canHaveChildren: false
  },
  
  [ComponentType.LINK]: {
    type: ComponentType.LINK,
    label: '链接',
    icon: 'el-icon-link',
    category: '基础',
    defaultProps: {
      type: 'primary',
      href: '',
      disabled: false,
      underline: true,
      children: '链接文本'
    },
    editableProps: ['type', 'href', 'disabled', 'underline', 'children'],
    canHaveChildren: false
  },
  
  [ComponentType.TEXT]: {
    type: ComponentType.TEXT,
    label: '文本',
    icon: 'el-icon-document',
    category: '基础',
    defaultProps: {
      type: 'primary',
      size: 'default',
      tag: 'span',
      children: '文本内容'
    },
    editableProps: ['type', 'size', 'tag', 'children'],
    canHaveChildren: false
  },
  
  [ComponentType.INPUT]: {
    type: ComponentType.INPUT,
    label: '输入框',
    icon: 'el-icon-edit',
    category: '表单',
    defaultProps: {
      type: 'text',
      placeholder: '请输入内容',
      clearable: true,
      disabled: false,
      readonly: false,
      maxlength: null,
      showWordLimit: false,
      size: 'default'
    },
    editableProps: ['type', 'placeholder', 'clearable', 'disabled', 'readonly', 'maxlength', 'showWordLimit', 'size'],
    canHaveChildren: false
  },
  
  [ComponentType.INPUT_NUMBER]: {
    type: ComponentType.INPUT_NUMBER,
    label: '数字输入框',
    icon: 'el-icon-plus',
    category: '表单',
    defaultProps: {
      min: 0,
      max: 100,
      step: 1,
      precision: 0,
      size: 'default',
      disabled: false,
      controls: true,
      controlsPosition: ''
    },
    editableProps: ['min', 'max', 'step', 'precision', 'size', 'disabled', 'controls', 'controlsPosition'],
    canHaveChildren: false
  },
  
  [ComponentType.SELECT]: {
    type: ComponentType.SELECT,
    label: '选择器',
    icon: 'el-icon-arrow-down',
    category: '表单',
    defaultProps: {
      placeholder: '请选择',
      clearable: true,
      disabled: false,
      multiple: false,
      filterable: false,
      size: 'default'
    },
    editableProps: ['placeholder', 'clearable', 'disabled', 'multiple', 'filterable', 'size'],
    canHaveChildren: true
  },
  
  [ComponentType.RADIO]: {
    type: ComponentType.RADIO,
    label: '单选框',
    icon: 'el-icon-check',
    category: '表单',
    defaultProps: {
      label: '选项',
      disabled: false,
      border: false,
      size: 'default'
    },
    editableProps: ['label', 'disabled', 'border', 'size'],
    canHaveChildren: false
  },
  
  [ComponentType.RADIO_GROUP]: {
    type: ComponentType.RADIO_GROUP,
    label: '单选框组',
    icon: 'el-icon-check',
    category: '表单',
    defaultProps: {
      disabled: false,
      size: 'default',
      textColor: '#ffffff',
      fill: '#409eff'
    },
    editableProps: ['disabled', 'size', 'textColor', 'fill'],
    canHaveChildren: true
  },
  
  [ComponentType.CHECKBOX]: {
    type: ComponentType.CHECKBOX,
    label: '复选框',
    icon: 'el-icon-check',
    category: '表单',
    defaultProps: {
      label: '选项',
      disabled: false,
      border: false,
      size: 'default',
      indeterminate: false
    },
    editableProps: ['label', 'disabled', 'border', 'size', 'indeterminate'],
    canHaveChildren: false
  },
  
  [ComponentType.CHECKBOX_GROUP]: {
    type: ComponentType.CHECKBOX_GROUP,
    label: '复选框组',
    icon: 'el-icon-check',
    category: '表单',
    defaultProps: {
      disabled: false,
      min: null,
      max: null,
      size: 'default',
      textColor: '#ffffff',
      fill: '#409eff'
    },
    editableProps: ['disabled', 'min', 'max', 'size', 'textColor', 'fill'],
    canHaveChildren: true
  },
  
  [ComponentType.SWITCH]: {
    type: ComponentType.SWITCH,
    label: '开关',
    icon: 'el-icon-switch-button',
    category: '表单',
    defaultProps: {
      disabled: false,
      width: 40,
      activeText: '',
      inactiveText: '',
      activeValue: true,
      inactiveValue: false,
      activeColor: '#409eff',
      inactiveColor: '#dcdfe6'
    },
    editableProps: ['disabled', 'width', 'activeText', 'inactiveText', 'activeValue', 'inactiveValue', 'activeColor', 'inactiveColor'],
    canHaveChildren: false
  },
  
  [ComponentType.SLIDER]: {
    type: ComponentType.SLIDER,
    label: '滑块',
    icon: 'el-icon-minus',
    category: '表单',
    defaultProps: {
      min: 0,
      max: 100,
      step: 1,
      disabled: false,
      showStops: false,
      showTooltip: true,
      range: false
    },
    editableProps: ['min', 'max', 'step', 'disabled', 'showStops', 'showTooltip', 'range'],
    canHaveChildren: false
  },
  
  [ComponentType.DATE_PICKER]: {
    type: ComponentType.DATE_PICKER,
    label: '日期选择器',
    icon: 'el-icon-date',
    category: '表单',
    defaultProps: {
      type: 'date',
      placeholder: '选择日期',
      format: 'YYYY-MM-DD',
      valueFormat: 'YYYY-MM-DD',
      disabled: false,
      clearable: true,
      size: 'default'
    },
    editableProps: ['type', 'placeholder', 'format', 'valueFormat', 'disabled', 'clearable', 'size'],
    canHaveChildren: false
  },
  
  [ComponentType.TIME_PICKER]: {
    type: ComponentType.TIME_PICKER,
    label: '时间选择器',
    icon: 'el-icon-time',
    category: '表单',
    defaultProps: {
      placeholder: '选择时间',
      format: 'HH:mm:ss',
      valueFormat: 'HH:mm:ss',
      disabled: false,
      clearable: true,
      size: 'default'
    },
    editableProps: ['placeholder', 'format', 'valueFormat', 'disabled', 'clearable', 'size'],
    canHaveChildren: false
  },
  
  [ComponentType.CARD]: {
    type: ComponentType.CARD,
    label: '卡片',
    icon: 'el-icon-document',
    category: '数据展示',
    defaultProps: {
      header: '卡片标题',
      shadow: 'always',
      bodyStyle: {}
    },
    editableProps: ['header', 'shadow', 'bodyStyle'],
    canHaveChildren: true
  },
  
  [ComponentType.TAG]: {
    type: ComponentType.TAG,
    label: '标签',
    icon: 'el-icon-price-tag',
    category: '数据展示',
    defaultProps: {
      type: 'primary',
      closable: false,
      disableTransitions: false,
      hit: false,
      color: '',
      size: 'default',
      effect: 'light',
      children: '标签'
    },
    editableProps: ['type', 'closable', 'disableTransitions', 'hit', 'color', 'size', 'effect', 'children'],
    canHaveChildren: false
  },
  
  [ComponentType.PROGRESS]: {
    type: ComponentType.PROGRESS,
    label: '进度条',
    icon: 'el-icon-loading',
    category: '数据展示',
    defaultProps: {
      percentage: 50,
      type: 'line',
      strokeWidth: 6,
      textInside: false,
      status: '',
      color: '#409eff',
      showText: true,
      format: null
    },
    editableProps: ['percentage', 'type', 'strokeWidth', 'textInside', 'status', 'color', 'showText'],
    canHaveChildren: false
  },
  
  [ComponentType.ALERT]: {
    type: ComponentType.ALERT,
    label: '警告',
    icon: 'el-icon-warning',
    category: '反馈',
    defaultProps: {
      title: '警告标题',
      type: 'info',
      description: '',
      closable: true,
      center: false,
      closeText: '',
      showIcon: false,
      effect: 'light'
    },
    editableProps: ['title', 'type', 'description', 'closable', 'center', 'closeText', 'showIcon', 'effect'],
    canHaveChildren: false
  },
  
  [ComponentType.FORM]: {
    type: ComponentType.FORM,
    label: '表单',
    icon: 'el-icon-document',
    category: '表单',
    defaultProps: {
      model: 'formData',
      rules: 'formRules',
      labelWidth: '120px',
      labelPosition: 'right',
      inline: false,
      labelSuffix: '',
      hideRequiredAsterisk: false,
      showMessage: true,
      inlineMessage: false,
      statusIcon: false,
      validateOnRuleChange: true,
      size: 'default',
      disabled: false
    },
    editableProps: ['labelWidth', 'labelPosition', 'inline', 'labelSuffix', 'hideRequiredAsterisk', 'showMessage', 'inlineMessage', 'statusIcon', 'validateOnRuleChange', 'size', 'disabled'],
    canHaveChildren: true
  },
  
  [ComponentType.FORM_ITEM]: {
    type: ComponentType.FORM_ITEM,
    label: '表单项',
    icon: 'el-icon-tickets',
    category: '表单',
    defaultProps: {
      label: '标签',
      labelWidth: '',
      required: false,
      rules: null,
      error: '',
      showMessage: true,
      inlineMessage: false,
      size: 'default'
    },
    editableProps: ['label', 'labelWidth', 'required', 'showMessage', 'inlineMessage', 'size'],
    canHaveChildren: true
  },
  
  [ComponentType.ROW]: {
    type: ComponentType.ROW,
    label: '行布局',
    icon: 'el-icon-menu',
    category: '布局',
    defaultProps: {
      style: {
        display: 'flex',
        flexDirection: 'row',
        gap: '12px',
        padding: '12px',
        border: '1px dashed #dcdfe6',
        borderRadius: '4px',
        minHeight: '60px'
      }
    },
    editableProps: ['gap', 'justifyContent', 'alignItems'],
    canHaveChildren: true
  },
  
  [ComponentType.COL]: {
    type: ComponentType.COL,
    label: '列布局',
    icon: 'el-icon-menu',
    category: '布局',
    defaultProps: {
      style: {
        display: 'flex',
        flexDirection: 'column',
        gap: '12px',
        padding: '12px',
        border: '1px dashed #dcdfe6',
        borderRadius: '4px',
        minHeight: '60px'
      }
    },
    editableProps: ['gap', 'justifyContent', 'alignItems'],
    canHaveChildren: true
  },
  
  [ComponentType.CONTAINER]: {
    type: ComponentType.CONTAINER,
    label: '容器',
    icon: 'el-icon-s-grid',
    category: '布局',
    defaultProps: {
      direction: 'vertical'
    },
    editableProps: ['direction'],
    canHaveChildren: true
  },
  
  [ComponentType.HEADER]: {
    type: ComponentType.HEADER,
    label: '头部',
    icon: 'el-icon-top',
    category: '布局',
    defaultProps: {
      height: '60px'
    },
    editableProps: ['height'],
    canHaveChildren: true
  },
  
  [ComponentType.MAIN]: {
    type: ComponentType.MAIN,
    label: '主要区域',
    icon: 'el-icon-s-grid',
    category: '布局',
    defaultProps: {},
    editableProps: [],
    canHaveChildren: true
  },
  
  [ComponentType.ASIDE]: {
    type: ComponentType.ASIDE,
    label: '侧边栏',
    icon: 'el-icon-s-unfold',
    category: '布局',
    defaultProps: {
      width: '300px'
    },
    editableProps: ['width'],
    canHaveChildren: true
  },
  
  [ComponentType.FOOTER]: {
    type: ComponentType.FOOTER,
    label: '底部',
    icon: 'el-icon-bottom',
    category: '布局',
    defaultProps: {
      height: '60px'
    },
    editableProps: ['height'],
    canHaveChildren: true
  },
  
  [ComponentType.DIVIDER]: {
    type: ComponentType.DIVIDER,
    label: '分割线',
    icon: 'el-icon-minus',
    category: '其他',
    defaultProps: {
      direction: 'horizontal',
      contentPosition: 'center',
      children: ''
    },
    editableProps: ['direction', 'contentPosition', 'children'],
    canHaveChildren: false
  }
};

// 组件分类
export const COMPONENT_CATEGORIES = {
  '基础': [ComponentType.BUTTON, ComponentType.LINK, ComponentType.TEXT],
  '布局': [ComponentType.ROW, ComponentType.COL, ComponentType.CONTAINER, ComponentType.HEADER, ComponentType.MAIN, ComponentType.ASIDE, ComponentType.FOOTER],
  '表单': [ComponentType.FORM, ComponentType.FORM_ITEM, ComponentType.INPUT, ComponentType.INPUT_NUMBER, ComponentType.SELECT, ComponentType.RADIO, ComponentType.RADIO_GROUP, ComponentType.CHECKBOX, ComponentType.CHECKBOX_GROUP, ComponentType.SWITCH, ComponentType.SLIDER, ComponentType.TIME_PICKER, ComponentType.DATE_PICKER],
  '数据展示': [ComponentType.CARD, ComponentType.TAG, ComponentType.PROGRESS],
  '反馈': [ComponentType.ALERT],
  '其他': [ComponentType.DIVIDER]
};

// 生成唯一 ID
export function generateId(): string {
  return `component_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
}

// 创建组件实例
export function createComponent(type: ComponentType, props: Record<string, any> = {}): ComponentSchema {
  const config = COMPONENT_CONFIGS[type];
  if (!config) {
    throw new Error(`Unknown component type: ${type}`);
  }
  
  const component: ComponentSchema = {
    id: generateId(),
    type,
    props: { ...config.defaultProps, ...props },
    children: config.canHaveChildren ? [] : undefined
  };
  
  // 布局组件初始化为空容器，不自动生成子组件
  
  return component;
}

// 验证组件 Schema
export function validateComponentSchema(schema: ComponentSchema): boolean {
  if (!schema.id || !schema.type) {
    return false;
  }
  
  const config = COMPONENT_CONFIGS[schema.type as ComponentType];
  if (!config) {
    return false;
  }
  
  if (config.canHaveChildren && schema.children) {
    return schema.children.every(child => validateComponentSchema(child));
  }
  
  return true;
}
