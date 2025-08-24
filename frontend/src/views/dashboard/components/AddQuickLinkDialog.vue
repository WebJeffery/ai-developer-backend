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
        <IconSelect v-model="form.icon" width="400px" />
      </ElFormItem>


    </ElForm>



    <template #footer>
      <span class="dialog-footer">
        <ElButton @click="handleClose">取消</ElButton>
        <ElButton type="primary" @click="handleConfirm">确定</ElButton>
      </span>
    </template>
  </ElDialog>
</template>

<script setup lang="ts">
import { ElMessage, FormInstance, FormRules } from 'element-plus';
import IconSelect from '@/components/IconSelect/index.vue';

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
  href: string;
  action: 'navigate' | 'external';
}

const props = defineProps<Props>();
const emit = defineEmits<Emits>();

const formRef = ref<FormInstance>();

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
  icon: 'user',
  href: '',
  action: 'navigate'
});



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



// 重置表单
const resetForm = () => {
  Object.assign(form, {
    title: '',
    description: '',
    icon: 'user',
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

</style>
