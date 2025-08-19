<template>
  <div class="app-container">
    <ElCard>
      <template #header>
        <div class="card-header">
          <span class="font-bold text-18px">快速开始收藏功能测试</span>
        </div>
      </template>
      
      <div class="content">
        <ElAlert
          title="功能说明"
          type="info"
          :closable="false"
          show-icon
        >
          <p>在任意标签页上右击，选择"收藏到快速开始"即可将当前页面添加到快速开始列表中。</p>
          <p>已收藏的页面会显示"已收藏"状态，无法重复收藏。</p>
        </ElAlert>

        <div class="mt-4">
          <h3>测试步骤：</h3>
          <ol class="test-steps">
            <li><strong>收藏功能：</strong>在当前页面的标签上右击，选择"收藏到快速开始"</li>
            <li><strong>取消收藏：</strong>在已收藏页面的标签上右击，选择"取消收藏"</li>
            <li><strong>自动图标：</strong>收藏时会自动获取路由配置的图标</li>
            <li><strong>查看收藏：</strong>前往工作台页面查看快速开始组件</li>
            <li><strong>编辑链接：</strong>在快速开始组件中右击任意链接，选择"编辑链接"</li>
            <li><strong>删除链接：</strong>在快速开始组件中右击任意链接，选择"删除链接"</li>
            <li><strong>验证跳转：</strong>点击收藏的链接验证跳转功能</li>
          </ol>
        </div>

        <div class="mt-4">
          <h3>当前页面信息：</h3>
          <ElDescriptions :column="1" border>
            <ElDescriptionsItem label="页面标题">
              {{ $route.meta?.title || '快速开始测试页面' }}
            </ElDescriptionsItem>
            <ElDescriptionsItem label="路由路径">
              {{ $route.path }}
            </ElDescriptionsItem>
            <ElDescriptionsItem label="完整路径">
              {{ $route.fullPath }}
            </ElDescriptionsItem>
            <ElDescriptionsItem label="路由图标">
              <div class="flex items-center">
                <el-icon v-if="$route.meta?.icon" :size="20" class="mr-2">
                  <component :is="$route.meta.icon" />
                </el-icon>
                <span>{{ $route.meta?.icon || '无图标配置' }}</span>
              </div>
            </ElDescriptionsItem>
            <ElDescriptionsItem label="收藏状态">
              <ElTag :type="isBookmarked ? 'success' : 'info'">
                {{ isBookmarked ? '已收藏' : '未收藏' }}
              </ElTag>
            </ElDescriptionsItem>
          </ElDescriptions>
        </div>

        <div class="mt-4">
          <ElButton 
            type="primary" 
            @click="testBookmark"
            :disabled="isBookmarked"
          >
            {{ isBookmarked ? '已收藏' : '手动收藏此页面' }}
          </ElButton>
          
          <ElButton
            type="success"
            @click="goToWorkplace"
            class="ml-2"
          >
            前往工作台查看
          </ElButton>

          <ElButton
            type="danger"
            @click="removeBookmark"
            :disabled="!isBookmarked"
            class="ml-2"
          >
            删除收藏
          </ElButton>

          <ElButton
            type="info"
            @click="previewQuickLink"
            class="ml-2"
          >
            预览收藏信息
          </ElButton>

          <ElButton
            type="warning"
            @click="testEditFunction"
            class="ml-2"
          >
            测试编辑功能
          </ElButton>
        </div>

        <div class="mt-4">
          <h3>当前快速开始列表：</h3>
          <div class="quick-links-preview">
            <div 
              v-for="(link, index) in quickLinks" 
              :key="index"
              class="link-item"
            >
              <el-icon :color="link.color" class="mr-2">
                <component :is="link.icon" />
              </el-icon>
              <span class="link-title">{{ link.title }}</span>
              <ElTag size="small" class="ml-2">{{ link.action }}</ElTag>
            </div>
          </div>
        </div>
      </div>
    </ElCard>
  </div>
</template>

<script setup lang="ts">
import { useRoute, useRouter } from 'vue-router';
import { quickStartManager, type QuickLink } from '@/utils/quickStartManager';
import { ElMessageBox } from 'element-plus';

defineOptions({
  name: "QuickStartTest",
});

const route = useRoute();
const router = useRouter();

// 快速链接列表
const quickLinks = ref<QuickLink[]>(quickStartManager.getQuickLinks());

// 检查当前页面是否已收藏
const isBookmarked = computed(() => {
  return quickStartManager.isLinkExists(route.fullPath);
});

// 手动收藏当前页面
const testBookmark = () => {
  const quickLink = quickStartManager.createQuickLinkFromRoute(
    route,
    '快速开始测试页面',
    '用于测试快速开始收藏功能的演示页面'
  );
  quickStartManager.addQuickLink(quickLink);
  
  // 更新快速链接列表
  quickLinks.value = quickStartManager.getQuickLinks();
};

// 删除收藏
const removeBookmark = () => {
  const links = quickStartManager.getQuickLinks();
  const targetLink = links.find(link => link.href === route.fullPath);

  if (targetLink?.id) {
    quickStartManager.removeQuickLink(targetLink.id);
    // 更新快速链接列表
    quickLinks.value = quickStartManager.getQuickLinks();
  }
};

// 预览收藏信息
const previewQuickLink = () => {
  const quickLink = quickStartManager.createQuickLinkFromRoute(
    route,
    '快速开始测试页面',
    '用于测试快速开始收藏功能的演示页面'
  );

  ElMessageBox.alert(
    `<div style="text-align: left;">
      <p><strong>标题：</strong>${quickLink.title}</p>
      <p><strong>描述：</strong>${quickLink.description}</p>
      <p><strong>图标：</strong>${quickLink.icon}</p>
      <p><strong>颜色：</strong><span style="color: ${quickLink.color};">${quickLink.color}</span></p>
      <p><strong>链接：</strong>${quickLink.href}</p>
      <p><strong>类型：</strong>${quickLink.action}</p>
    </div>`,
    '收藏信息预览',
    {
      dangerouslyUseHTMLString: true,
      confirmButtonText: '确定'
    }
  );
};

// 测试编辑功能
const testEditFunction = () => {
  const links = quickStartManager.getQuickLinks();
  if (links.length === 0) {
    ElMessage.warning('没有可编辑的快速链接，请先添加一些链接');
    return;
  }

  ElMessageBox.alert(
    `<div style="text-align: left;">
      <p><strong>测试说明：</strong></p>
      <ol>
        <li>前往工作台页面</li>
        <li>在快速开始组件中右击任意链接</li>
        <li>选择"编辑链接"</li>
        <li>验证表单是否预填充了现有数据</li>
        <li>修改任意字段后保存</li>
        <li>确认修改是否生效</li>
      </ol>
      <p><strong>当前可编辑的链接：</strong></p>
      <ul>
        ${links.slice(0, 3).map(link => `<li>${link.title} (${link.href})</li>`).join('')}
        ${links.length > 3 ? `<li>... 还有 ${links.length - 3} 个链接</li>` : ''}
      </ul>
    </div>`,
    '编辑功能测试指南',
    {
      dangerouslyUseHTMLString: true,
      confirmButtonText: '前往工作台测试',
      cancelButtonText: '取消',
      showCancelButton: true
    }
  ).then(() => {
    goToWorkplace();
  }).catch(() => {
    // 用户取消
  });
};

// 前往工作台
const goToWorkplace = () => {
  router.push('/dashboard/workplace');
};

// 监听快速链接变化
const updateQuickLinks = (links: QuickLink[]) => {
  quickLinks.value = links;
};

onMounted(() => {
  quickStartManager.addListener(updateQuickLinks);
});

onUnmounted(() => {
  quickStartManager.removeListener(updateQuickLinks);
});
</script>

<style lang="scss" scoped>
.content {
  padding: 20px 0;
}

.test-steps {
  padding-left: 20px;
  
  li {
    margin-bottom: 8px;
    line-height: 1.6;
  }
}

.quick-links-preview {
  max-height: 300px;
  overflow-y: auto;
  border: 1px solid var(--el-border-color);
  border-radius: 4px;
  padding: 12px;
  
  .link-item {
    display: flex;
    align-items: center;
    padding: 8px 0;
    border-bottom: 1px solid var(--el-border-color-lighter);
    
    &:last-child {
      border-bottom: none;
    }
    
    .link-title {
      flex: 1;
      font-size: 14px;
    }
  }
}
</style>
