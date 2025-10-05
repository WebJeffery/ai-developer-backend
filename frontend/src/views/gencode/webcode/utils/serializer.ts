/**
 * 低代码页面生成器 - 序列化器
 * 将 JSON Schema 转换为 Vue3 + TypeScript 单文件组件
 */

import { ComponentSchema, PageSchema, ComponentType, COMPONENT_CONFIGS } from './schema';

// 生成 Vue 组件的模板字符串
export function generateVueTemplate(schema: PageSchema): string {
  const template = generateTemplateFromComponents(schema.components);
  const script = generateScriptSetup(schema);
  const style = generateStyle();
  
  return `<template>
${template}
</template>

${script}

${style}`;
}

// 递归生成组件模板
function generateTemplateFromComponents(components: ComponentSchema[], indent = 0): string {
  const spaces = '  '.repeat(indent);
  let template = '';
  
  for (const component of components) {
    template += generateComponentTemplate(component, indent);
  }
  
  return template;
}

// 生成单个组件的模板
function generateComponentTemplate(component: ComponentSchema, indent = 0): string {
  const spaces = '  '.repeat(indent);
  const { type, props = {}, children = [], events = {}, slots = {} } = component;
  
  // 对于行列布局，生成为div
  const actualType = (type === 'el-row' || type === 'el-col') ? 'div' : type;
  
  // 生成属性字符串
  const propsString = generatePropsString(props, type);
  
  // 生成事件字符串
  const eventsString = generateEventsString(events);
  
  // 获取组件内容
  const componentContent = getComponentContent(component, indent);
  
  // 生成子组件模板
  const childrenTemplate = children.length > 0 
    ? `\n${generateTemplateFromComponents(children, indent + 1)}\n${spaces}`
    : '';
  
  // 自闭合标签处理
  const isSelfClosing = isSelfClosingTag(actualType);
  
  if (isSelfClosing) {
    return `${spaces}<${actualType}${propsString}${eventsString} />\n`;
  } else {
    const content = componentContent || childrenTemplate;
    return `${spaces}<${actualType}${propsString}${eventsString}>${content}</${actualType}>\n`;
  }
}

// 获取组件内容
function getComponentContent(component: ComponentSchema, indent = 0): string {
  const spaces = '  '.repeat(indent + 1);
  
  // 有文本内容的组件
  if (component.props?.children && typeof component.props.children === 'string') {
    return component.props.children;
  }
  
  // 特殊组件的默认内容
  const defaultContent: Record<string, string> = {
    'el-button': '按钮',
    'el-link': '链接',
    'el-text': '文本',
    'el-tag': '标签',
    'el-alert': '', // alert 通过 title 属性显示内容
    'el-card': `\n${spaces}<div>卡片内容</div>\n${spaces.slice(2)}`,
    'el-form': `\n${spaces}<!-- 表单项 -->\n${spaces.slice(2)}`,
    'el-form-item': `\n${spaces}<!-- 表单控件 -->\n${spaces.slice(2)}`,
    'el-container': `\n${spaces}<!-- 容器内容 -->\n${spaces.slice(2)}`,
    'el-header': `\n${spaces}<!-- 头部内容 -->\n${spaces.slice(2)}`,
    'el-main': `\n${spaces}<!-- 主要内容 -->\n${spaces.slice(2)}`,
    'el-aside': `\n${spaces}<!-- 侧边栏内容 -->\n${spaces.slice(2)}`,
    'el-footer': `\n${spaces}<!-- 底部内容 -->\n${spaces.slice(2)}`
  };
  
  return defaultContent[component.type] || '';
}

// 生成属性字符串
function generatePropsString(props: Record<string, any>, componentType?: string): string {
  const propStrings: string[] = [];
  
  for (const [key, value] of Object.entries(props)) {
    if (value === null || value === undefined) continue;
    
    // 对于行列布局，将样式属性转换为style
    if ((componentType === 'el-row' || componentType === 'el-col') && key === 'style') {
      const styleString = Object.entries(value)
        .map(([k, v]) => `${k.replace(/([A-Z])/g, '-$1').toLowerCase()}: ${v}`)
        .join('; ');
      propStrings.push(`style="${styleString}"`);
      continue;
    }
    
    // 跳过布局组件的特殊属性
    if ((componentType === 'el-row' || componentType === 'el-col') && 
        ['gap', 'justifyContent', 'alignItems'].includes(key)) {
      continue;
    }
    
    if (typeof value === 'boolean') {
      if (value) {
        propStrings.push(key);
      }
    } else if (typeof value === 'string') {
      propStrings.push(`${key}="${escapeHtml(value)}"`);
    } else if (typeof value === 'number') {
      propStrings.push(`${key}="${value}"`);
    } else if (Array.isArray(value)) {
      propStrings.push(`:${key}="[${value.map(v => JSON.stringify(v)).join(', ')}]"`);
    } else if (typeof value === 'object') {
      propStrings.push(`:${key}="${JSON.stringify(value)}"`);
    } else {
      propStrings.push(`:${key}="${value}"`);
    }
  }
  
  return propStrings.length > 0 ? ` ${propStrings.join(' ')}` : '';
}

// 生成事件字符串
function generateEventsString(events: Record<string, string>): string {
  const eventStrings: string[] = [];
  
  for (const [event, handler] of Object.entries(events)) {
    eventStrings.push(`@${event}="${handler}"`);
  }
  
  return eventStrings.length > 0 ? ` ${eventStrings.join(' ')}` : '';
}

// 生成插槽字符串
function generateSlotsString(slots: Record<string, string>): string {
  const slotStrings: string[] = [];
  
  for (const [slotName, slotContent] of Object.entries(slots)) {
    if (slotName === 'default') {
      slotStrings.push(slotContent);
    } else {
      slotStrings.push(`<template #${slotName}>${slotContent}</template>`);
    }
  }
  
  return slotStrings.length > 0 ? ` ${slotStrings.join(' ')}` : '';
}

// 生成 Script Setup
function generateScriptSetup(schema: PageSchema): string {
  const imports = generateImports(schema);
  const reactiveData = generateReactiveData(schema);
  const methods = generateMethods(schema);
  const computed = generateComputed(schema);
  
  return `<script setup lang="ts">
${imports}

${reactiveData}

${computed}

${methods}
</script>`;
}

// 生成导入语句
function generateImports(schema: PageSchema): string {
  const componentTypes = new Set<string>();
  
  // 收集所有使用的组件类型
  function collectComponentTypes(components: ComponentSchema[]) {
    for (const component of components) {
      componentTypes.add(component.type);
      if (component.children) {
        collectComponentTypes(component.children);
      }
    }
  }
  
  collectComponentTypes(schema.components);
  
  // 生成导入语句
  const imports = [
    "import { ref, reactive, computed, onMounted } from 'vue'",
    "import { ElMessage } from 'element-plus'"
  ];
  
  // 添加 Element Plus 组件导入
  const elementComponents = Array.from(componentTypes).filter(type => 
    type.startsWith('el-') && !['el-icon', 'el-text'].includes(type)
  );
  
  if (elementComponents.length > 0) {
    imports.push(`import { ${elementComponents.join(', ')} } from 'element-plus'`);
  }
  
  return imports.join('\n');
}

// 生成响应式数据
function generateReactiveData(schema: PageSchema): string {
  const dataProperties: string[] = [];
  
  // 收集所有需要的数据属性
  function collectDataProperties(components: ComponentSchema[]) {
    for (const component of components) {
      if (component.type === ComponentType.FORM) {
        dataProperties.push('formData: {}');
        dataProperties.push('formRules: {}');
      } else if (component.type === ComponentType.INPUT || 
                 component.type === ComponentType.SELECT ||
                 component.type === ComponentType.INPUT_NUMBER) {
        const fieldName = component.props?.model || `field_${component.id}`;
        dataProperties.push(`${fieldName}: ""`);
      }
      
      if (component.children) {
        collectDataProperties(component.children);
      }
    }
  }
  
  collectDataProperties(schema.components);
  
  if (dataProperties.length === 0) {
    return '// 响应式数据\nconst data = reactive({})';
  }
  
  return `// 响应式数据
const data = reactive({
  ${dataProperties.join(',\n  ')}
})`;
}

// 生成计算属性
function generateComputed(schema: PageSchema): string {
  return `// 计算属性
const computedValue = computed(() => {
  // 在这里添加计算逻辑
  return 'computed value'
})`;
}

// 生成方法
function generateMethods(schema: PageSchema): string {
  const methods: string[] = [];
  
  // 收集所有需要的方法
  function collectMethods(components: ComponentSchema[]) {
    for (const component of components) {
      if (component.events) {
        for (const [event, handler] of Object.entries(component.events)) {
          if (!methods.includes(handler)) {
            methods.push(handler);
          }
        }
      }
      
      if (component.children) {
        collectMethods(component.children);
      }
    }
  }
  
  collectMethods(schema.components);
  
  // 添加默认方法
  methods.push('handleSubmit');
  methods.push('handleReset');
  
  const methodBodies = methods.map(method => {
    switch (method) {
      case 'handleSubmit':
        return `function handleSubmit() {
  ElMessage.success('提交成功')
}`;
      case 'handleReset':
        return `function handleReset() {
  // 重置表单逻辑
}`;
      default:
        return `function ${method}() {
  // ${method} 方法实现
}`;
    }
  });
  
  return `// 方法
${methodBodies.join('\n\n')}

// 生命周期
onMounted(() => {
  // 组件挂载后的逻辑
})`;
}

// 生成样式
function generateStyle(): string {
  return `<style scoped>
/* 页面样式 */
.page-container {
  padding: 20px;
}

/* 组件样式 */
.component-wrapper {
  margin-bottom: 16px;
}

/* 响应式样式 */
@media (max-width: 768px) {
  .page-container {
    padding: 10px;
  }
}
</style>`;
}

// 判断是否为自闭合标签
function isSelfClosingTag(tag: string): boolean {
  const selfClosingTags = [
    'el-input',
    'el-input-number',
    'el-icon',
    'el-image',
    'el-progress',
    'el-skeleton',
    'el-empty',
    'el-backtop'
  ];
  
  return selfClosingTags.includes(tag);
}

// HTML 转义
function escapeHtml(text: string): string {
  const map: Record<string, string> = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#039;'
  };
  
  return text.replace(/[&<>"']/g, (m) => map[m]);
}

// 生成完整的 Vue 文件内容
export function generateVueFile(schema: PageSchema, filename?: string): string {
  const template = generateVueTemplate(schema);
  const header = `<!--
  文件名: ${filename || 'generated-page.vue'}
  生成时间: ${new Date().toLocaleString()}
  描述: 由低代码页面生成器自动生成
-->

`;
  
  return header + template;
}

// 导出为文件
export function exportAsFile(schema: PageSchema, filename: string = 'generated-page.vue'): void {
  const content = generateVueFile(schema, filename);
  const blob = new Blob([content], { type: 'text/plain;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  
  URL.revokeObjectURL(url);
}

// 复制到剪贴板
export async function copyToClipboard(schema: PageSchema): Promise<void> {
  const content = generateVueFile(schema);
  
  try {
    await navigator.clipboard.writeText(content);
    console.log('代码已复制到剪贴板');
  } catch (err) {
    console.error('复制失败:', err);
    // 降级方案
    const textArea = document.createElement('textarea');
    textArea.value = content;
    document.body.appendChild(textArea);
    textArea.select();
    document.execCommand('copy');
    document.body.removeChild(textArea);
  }
}
