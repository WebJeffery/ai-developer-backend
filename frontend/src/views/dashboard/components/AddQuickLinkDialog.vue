<template>
  <ElDialog
    v-model="dialogVisible"
    :title="isEditMode ? '编辑快速链接' : '添加快速链接'"
    width="500px"
    :before-close="handleClose"
  >
    <ElForm
      ref="formRef"
      :model="form"
      :rules="rules"
      label-width="80px"
      label-position="left"
    >
      <ElFormItem label="标题" prop="title">
        <ElInput
          v-model="form.title"
          placeholder="请输入链接标题"
          maxlength="20"
          show-word-limit
        />
      </ElFormItem>

      <ElFormItem label="描述" prop="description">
        <ElInput
          v-model="form.description"
          placeholder="请输入链接描述"
          maxlength="50"
          show-word-limit
        />
      </ElFormItem>

      <ElFormItem label="链接地址" prop="href">
        <ElInput
          v-model="form.href"
          placeholder="请输入链接地址，如：/user 或 https://www.example.com"
        />
      </ElFormItem>

      <ElFormItem label="链接类型" prop="action">
        <ElRadioGroup v-model="form.action">
          <ElRadio label="navigate">内部链接</ElRadio>
          <ElRadio label="external">外部链接</ElRadio>
        </ElRadioGroup>
      </ElFormItem>

      <ElFormItem label="图标" prop="icon">
        <div class="icon-selector">
          <div class="selected-icon">
            <el-icon :size="24" :color="form.color">
              <component :is="form.icon" />
            </el-icon>
            <span class="ml-2">{{ getIconName(form.icon) }}</span>
          </div>
          <ElButton size="small" @click="showIconPicker = true">选择图标</ElButton>
        </div>
      </ElFormItem>

      <ElFormItem label="颜色" prop="color">
        <ElColorPicker v-model="form.color" />
      </ElFormItem>
    </ElForm>

    <!-- 图标选择器 -->
    <ElDialog
      v-model="showIconPicker"
      title="选择图标"
      width="600px"
      append-to-body
    >
      <div class="icon-grid">
        <div
          v-for="icon in availableIcons"
          :key="icon.name"
          class="icon-item"
          :class="{ active: form.icon === icon.name }"
          @click="selectIcon(icon.name)"
        >
          <el-icon :size="24">
            <component :is="icon.name" />
          </el-icon>
          <span class="icon-name">{{ icon.label }}</span>
        </div>
      </div>
      <template #footer>
        <ElButton @click="showIconPicker = false">取消</ElButton>
        <ElButton type="primary" @click="showIconPicker = false">确定</ElButton>
      </template>
    </ElDialog>

    <template #footer>
      <span class="dialog-footer">
        <ElButton @click="handleClose">取消</ElButton>
        <ElButton type="primary" @click="handleConfirm">确定</ElButton>
      </span>
    </template>
  </ElDialog>
</template>

<script setup lang="ts">
import {
  User,
  Setting,
  Document,
  DataAnalysis,
  Monitor,
  Tools,
  Bell,
  Message,
  Search,
  House,
  Files,
  Calendar,
  ChatDotRound,
  Connection,
  DataBoard,
  Histogram,
  PieChart,
  TrendCharts,
  Operation,
  Service,
  Guide,
  Link
} from "@element-plus/icons-vue";
import { ElMessage, FormInstance, FormRules } from 'element-plus';

interface Props {
  visible: boolean;
  editData?: QuickLink | null;
}

interface Emits {
  (e: 'update:visible', value: boolean): void;
  (e: 'confirm', value: QuickLink): void;
}

interface QuickLink {
  title: string;
  description: string;
  icon: string;
  color: string;
  href: string;
  action: 'navigate' | 'external';
}

const props = defineProps<Props>();
const emit = defineEmits<Emits>();

const formRef = ref<FormInstance>();
const showIconPicker = ref(false);

// 对话框显示状态
const dialogVisible = computed({
  get: () => props.visible,
  set: (value) => emit('update:visible', value)
});

// 是否为编辑模式
const isEditMode = computed(() => !!props.editData);

// 表单数据
const form = reactive<QuickLink>({
  title: '',
  description: '',
  icon: 'User',
  color: '#409EFF',
  href: '',
  action: 'navigate'
});

// 可用图标列表
const availableIcons = [
  { name: 'User', label: '用户' },
  { name: 'Setting', label: '设置' },
  { name: 'Document', label: '文档' },
  { name: 'DataAnalysis', label: '分析' },
  { name: 'Monitor', label: '监控' },
  { name: 'Tools', label: '工具' },
  { name: 'Bell', label: '通知' },
  { name: 'Message', label: '消息' },
  { name: 'Search', label: '搜索' },
  { name: 'House', label: '首页' },
  { name: 'Files', label: '文件' },
  { name: 'Calendar', label: '日历' },
  { name: 'ChatDotRound', label: '聊天' },
  { name: 'Connection', label: '连接' },
  { name: 'DataBoard', label: '数据' },
  { name: 'Histogram', label: '柱状图' },
  { name: 'PieChart', label: '饼图' },
  { name: 'TrendCharts', label: '趋势图' },
  { name: 'Operation', label: '操作' },
  { name: 'Service', label: '服务' },
  { name: 'Guide', label: '指南' },
  { name: 'Link', label: '链接' }
];

// 表单验证规则
const rules: FormRules = {
  title: [
    { required: true, message: '请输入链接标题', trigger: 'blur' },
    { min: 1, max: 20, message: '标题长度在 1 到 20 个字符', trigger: 'blur' }
  ],
  description: [
    { required: true, message: '请输入链接描述', trigger: 'blur' },
    { min: 1, max: 50, message: '描述长度在 1 到 50 个字符', trigger: 'blur' }
  ],
  href: [
    { required: true, message: '请输入链接地址', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (form.action === 'external') {
          // 外部链接需要是完整的URL
          const urlPattern = /^https?:\/\/.+/;
          if (!urlPattern.test(value)) {
            callback(new Error('外部链接必须以 http:// 或 https:// 开头'));
          } else {
            callback();
          }
        } else {
          // 内部链接需要以 / 开头
          if (!value.startsWith('/')) {
            callback(new Error('内部链接必须以 / 开头'));
          } else {
            callback();
          }
        }
      },
      trigger: 'blur'
    }
  ],
  action: [
    { required: true, message: '请选择链接类型', trigger: 'change' }
  ]
};

// 获取图标名称
const getIconName = (iconName: string) => {
  const icon = availableIcons.find(item => item.name === iconName);
  return icon ? icon.label : iconName;
};

// 选择图标
const selectIcon = (iconName: string) => {
  form.icon = iconName;
};

// 重置表单
const resetForm = () => {
  Object.assign(form, {
    title: '',
    description: '',
    icon: 'User',
    color: '#409EFF',
    href: '',
    action: 'navigate'
  });
  formRef.value?.clearValidate();
};

// 处理关闭
const handleClose = () => {
  resetForm();
  emit('update:visible', false);
};

// 处理确认
const handleConfirm = async () => {
  if (!formRef.value) return;
  
  try {
    await formRef.value.validate();
    emit('confirm', { ...form });
    handleClose();
  } catch (error) {
    ElMessage.error('请检查表单输入');
  }
};

// 监听对话框显示状态，处理表单数据
watch(() => props.visible, (visible) => {
  if (visible) {
    if (props.editData) {
      // 编辑模式：填充现有数据
      console.log('编辑模式 - 填充数据:', props.editData);
      Object.assign(form, {
        title: props.editData.title,
        description: props.editData.description,
        icon: props.editData.icon,
        color: props.editData.color,
        href: props.editData.href,
        action: props.editData.action
      });
      console.log('表单数据已填充:', form);
    } else {
      // 新增模式：重置表单
      console.log('新增模式 - 重置表单');
      resetForm();
    }
  }
});

// 监听编辑数据变化（当对话框已经打开时）
watch(() => props.editData, (editData) => {
  if (props.visible && editData) {
    // 编辑模式：填充现有数据
    Object.assign(form, {
      title: editData.title,
      description: editData.description,
      icon: editData.icon,
      color: editData.color,
      href: editData.href,
      action: editData.action
    });
  }
}, { immediate: false });

// 监听链接类型变化，自动调整链接地址格式
watch(() => form.action, (newAction) => {
  if (newAction === 'external' && form.href && !form.href.startsWith('http')) {
    form.href = 'https://';
  } else if (newAction === 'navigate' && form.href && !form.href.startsWith('/')) {
    form.href = '/';
  }
});
</script>

<style lang="scss" scoped>
.icon-selector {
  display: flex;
  align-items: center;
  gap: 12px;

  .selected-icon {
    display: flex;
    align-items: center;
    padding: 8px 12px;
    border: 1px solid #dcdfe6;
    border-radius: 4px;
    background-color: #f5f7fa;
  }
}

.icon-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(80px, 1fr));
  gap: 12px;
  max-height: 300px;
  overflow-y: auto;

  .icon-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 12px 8px;
    border: 1px solid #e4e7ed;
    border-radius: 6px;
    cursor: pointer;
    transition: all 0.3s ease;

    &:hover {
      border-color: #409EFF;
      background-color: #f0f9ff;
    }

    &.active {
      border-color: #409EFF;
      background-color: #e1f3ff;
    }

    .icon-name {
      font-size: 12px;
      color: #606266;
      margin-top: 4px;
      text-align: center;
    }
  }
}
</style>
