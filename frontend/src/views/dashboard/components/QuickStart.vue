<template>
  <ElCard class="mb-4" shadow="hover">
    <template #header>
      <div class="flex justify-between items-center">
        <span class="font-bold text-16px">快速开始 / 便捷导航</span>
        <ElButton size="small" type="primary" plain @click="handleAddQuickLink">
          <el-icon>
            <Plus />
          </el-icon>
          {{ t('common.add') }}
        </ElButton>
      </div>
    </template>
    <div class="quick-links-container">
      <div class="quick-links-scroll">
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
                <el-icon :size="20" :color="item.color">
                  <component :is="item.icon" />
                </el-icon>
              </div>
              <div class="link-content">
                <div class="link-title">
                  {{ item.title }}
                  <span v-if="item.action === 'external'" class="external-link-badge">外链</span>
                </div>
                <div class="link-description">{{ item.description }}</div>
              </div>
              <div class="link-arrow">
                <el-icon size="14" color="#999">
                  <ArrowRight />
                </el-icon>
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
  Delete
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
  height: 280px; // 固定容器高度
  overflow: hidden;

  .quick-links-scroll {
    height: 100%;
    overflow-y: auto;
    padding: 8px 0;
    padding-right: 4px; // 为滚动条留出空间

    // 自定义滚动条样式
    &::-webkit-scrollbar {
      width: 6px;
    }

    &::-webkit-scrollbar-track {
      border-radius: 3px;
    }

    &::-webkit-scrollbar-thumb {
      border-radius: 3px;

      &:hover {
        background: #a8a8a8;
      }
    }
  }

  .quick-link-item {
    margin-bottom: 8px;
    border-radius: 8px;
    border: 1px solid transparent;
    transition: all 0.3s ease;

    &:hover {
      background-color: #f5f7fa;
      border-color: #e4e7ed;
      transform: translateX(4px);
    }

    &:last-child {
      margin-bottom: 0;
    }

    .link-content-wrapper {
      display: flex;
      align-items: center;
      padding: 12px 16px;
      cursor: pointer;
      width: 100%;
    }

    .link-icon {
      display: flex;
      align-items: center;
      justify-content: center;
      width: 40px;
      height: 40px;
      border-radius: 8px;
      background-color: #f0f2f5;
      margin-right: 12px;
      transition: all 0.3s ease;
    }

    .link-content {
      flex: 1;

      .link-title {
        font-size: 14px;
        font-weight: 500;
        margin-bottom: 2px;
        line-height: 1.4;
        display: flex;
        align-items: center;
        gap: 6px;

        .external-link-badge {
          font-size: 10px;
          font-weight: 400;
          color: #fff;
          background-color: #409EFF;
          padding: 1px 4px;
          border-radius: 2px;
          line-height: 1.2;
        }
      }

      .link-description {
        font-size: 12px;
        color: #909399;
        line-height: 1.3;
      }
    }

    .link-arrow {
      display: flex;
      align-items: center;
      opacity: 0;
      transition: all 0.3s ease;
    }

    &:hover {
      .link-icon {
        background-color: #e8f4ff;
      }

      .link-arrow {
        opacity: 1;
        transform: translateX(4px);
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
