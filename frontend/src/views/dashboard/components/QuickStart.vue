<template>
  <ElCard class="mb-4" shadow="hover">
    <template #header>
      <div class="flex justify-between items-center">
        <div class="flex items-center gap-2">
          <el-tooltip content="快速访问常用功能，支持内部路由跳转和外部链接打开。可以自定义添加、编辑和删除快捷方式。" placement="top">
            <el-icon class="cursor-help" size="16">
              <QuestionFilled />
            </el-icon>
          </el-tooltip>
          <span class="font-bold text-16px">快速开始 / 便捷导航</span>
        </div>
        <ElButton size="small" type="primary" plain @click="handleAddQuickLink">
          <el-icon>
            <Plus />
          </el-icon>
          {{ t('common.add') }}
        </ElButton>
      </div>
    </template>
    <div class="quick-links-container">
      <div class="quick-links-grid">
        <div
          v-for="(item, index) in quickLinks"
          :key="index"
          class="quick-link-item"
          @click="handleQuickLinkClick(item)"
        >
          <!-- 为快速链接添加右键菜单 -->
          <el-dropdown
            trigger="contextmenu"
            @click.stop
            @visible-change="(visible) => onContextMenuChange(visible, item)"
          >
            <div class="link-content-wrapper">
              <div class="link-icon">
                <el-icon :size="24">
                  <component :is="item.icon" />
                </el-icon>
              </div>
              <div class="link-content">
                <div class="link-title">
                  {{ item.title }}
                  <span v-if="item.action === 'external'" class="external-link-badge">外链</span>
                </div>
              </div>
            </div>

            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="handleEditLink(item)">
                  <el-icon>
                    <Edit />
                  </el-icon>
                  编辑链接
                </el-dropdown-item>
                <el-dropdown-item
                  @click="handleDeleteLink(item)"
                  :disabled="!item.id"
                  class="delete-item"
                >
                  <el-icon>
                    <Delete />
                  </el-icon>
                  删除链接
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </div>
    </div>

    <!-- 添加/编辑快速链接对话框 -->
    <AddQuickLinkDialog
      v-model:visible="addDialogVisible"
      :edit-data="selectedLink"
      @confirm="handleAddConfirm"
    />
  </ElCard>
</template>

<script setup lang="ts">
import {
  Plus,
  ArrowRight,
  Edit,
  Delete,
  QuestionFilled
} from "@element-plus/icons-vue";
import { ElMessage, ElMessageBox } from 'element-plus';
import { useRouter } from 'vue-router';
import AddQuickLinkDialog from './AddQuickLinkDialog.vue';
import { quickStartManager, type QuickLink } from '@/utils/quickStartManager';

const { t } = useI18n();
const router = useRouter();

// 添加对话框显示状态
const addDialogVisible = ref(false);

// 快速链接数据 - 使用全局管理器
const quickLinks = ref<QuickLink[]>(quickStartManager.getQuickLinks());

// 处理快速链接点击
const handleQuickLinkClick = (item: QuickLink) => {
  if (item.action === 'navigate' && item.href) {
    // 内部路由跳转
    router.push(item.href).catch(() => {
      ElMessage.warning(`路由 ${item.href} 不存在，请检查配置`);
    });
    ElMessage.success(`正在跳转到：${item.title}`);
  } else if (item.action === 'external' && item.href) {
    // 外部链接跳转
    window.open(item.href, '_blank', 'noopener,noreferrer');
    ElMessage.success(`正在打开外部链接：${item.title}`);
  } else {
    ElMessage.info(`${item.title} 功能待开发`);
  }
};

// 当前选中的链接（用于右键菜单）
const selectedLink = ref<QuickLink | null>(null);

// 处理添加快速链接
const handleAddQuickLink = () => {
  selectedLink.value = null; // 清空选中项，表示新增
  addDialogVisible.value = true;
};

// 处理右键菜单显示状态变化
const onContextMenuChange = (visible: boolean, item?: QuickLink) => {
  if (visible && item) {
    selectedLink.value = item;
  } else {
    selectedLink.value = null;
  }
};

// 处理编辑链接
const handleEditLink = (item: QuickLink) => {
  // 深拷贝链接数据，避免直接修改原数据
  console.log('开始编辑链接:', item);
  selectedLink.value = { ...item };
  console.log('设置选中链接:', selectedLink.value);
  addDialogVisible.value = true;
};

// 处理删除链接
const handleDeleteLink = (item: QuickLink) => {
  ElMessageBox.confirm(
    `确定要删除快速链接"${item.title}"吗？`,
    '删除确认',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    }
  ).then(() => {
    if (item.id) {
      quickStartManager.removeQuickLink(item.id);
    }
  }).catch(() => {
    // 用户取消删除
  });
};

// 处理添加/编辑确认
const handleAddConfirm = (newLink: QuickLink) => {
  if (selectedLink.value?.id) {
    // 编辑模式：更新现有链接
    newLink.id = selectedLink.value.id;
    quickStartManager.addQuickLink(newLink); // addQuickLink 方法会处理更新逻辑
  } else {
    // 新增模式：添加新链接
    quickStartManager.addQuickLink(newLink);
  }
  selectedLink.value = null;
};

// 监听快速链接变化
const updateQuickLinks = (links: QuickLink[]) => {
  quickLinks.value = links;
};

// 组件挂载时添加监听器
onMounted(() => {
  quickStartManager.addListener(updateQuickLinks);
});

// 组件卸载时移除监听器
onUnmounted(() => {
  quickStartManager.removeListener(updateQuickLinks);
});
</script>

<style lang="scss" scoped>
// 快速链接容器样式
.quick-links-container {
  padding: 16px 0;

  .quick-links-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
  }

  .quick-link-item {
    border-radius: 6px;
    border: 1px solid #e4e7ed;
    transition: all 0.3s ease;
    width: 100%;
    height: 100px;
    max-width: 120px;
    display: flex;
    align-items: center;
    justify-content: center;

    &:hover {
      transform: translateY(-2px);
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }

    .link-content-wrapper {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 8px;
      cursor: pointer;
      width: 100%;
      text-align: center;
    }

    .link-icon {
      display: flex;
      align-items: center;
      justify-content: center;
      width: 40px;
      height: 40px;
      border-radius: 8px;
      margin-bottom: 8px;
      transition: all 0.3s ease;
    }

    .link-content {
      width: 100%;
      display: flex;
      justify-content: center;

      .link-title {
        font-size: 14px;
        font-weight: 500;
        line-height: 1.4;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 6px;
        text-align: center;

        .external-link-badge {
          font-size: 10px;
          font-weight: 400;
          background-color: var(--el-color-primary);
          color: #ffffff;
          padding: 1px 4px;
          border-radius: 2px;
          line-height: 1.2;
          transition: all 0.3s ease;
        }

        // 暗色主题适配 - 使用项目标准的暗色主题选择器
        html.dark .external-link-badge {
          background-color: var(--el-color-primary-dark-2);
          color: var(--el-text-color-primary);
        }
      }
    }

    &:hover {
      .link-icon {
        background-color: #e8f4ff;
      }
    }
  }
}

// 删除菜单项样式
:deep(.delete-item) {
  color: #f56c6c;

  &:hover {
    background-color: #fef0f0;
    color: #f56c6c;
  }
}
</style>
