<template>
  <view class="app-container">
    <!-- 用户信息卡片 -->
    <view class="user-profile">
      <view class="blur-bg"></view>
      <view class="user-info">
        <view class="avatar-container" @click="navigateToProfile">
          <image
            class="avatar"
            :src="isLogin ? userInfo!.avatar : defaultAvatar"
            mode="aspectFill"
          />
        </view>
        <view class="user-details">
          <block v-if="isLogin">
            <view class="nickname">{{ userInfo!.name || "匿名用户" }}</view>
            <view class="user-id">ID: {{ userInfo?.username || "0000000" }}</view>
          </block>
          <block v-else>
            <view class="login-prompt">立即登录获取更多功能</view>
            <wd-button
              custom-class="btn-login"
              size="small"
              type="primary"
              @click="navigateToLoginPage"
            >
              登录/注册
            </wd-button>
          </block>
        </view>
        <view class="actions">
          <view class="action-btn" @click="navigateToSettings">
            <wd-icon name="setting1" size="22" color="#333" />
          </view>
          <view v-if="isLogin" class="action-btn" @click="navigateToSection('messages')">
            <wd-badge v-if="true" modelValue="99+">
              <wd-icon name="notification" size="22" color="#333" />
            </wd-badge>
          </view>
        </view>
      </view>
    </view>

    <!-- 数据统计 -->
    <view class="stats-card">
      <view class="stats-item" @click="navigateToSection('wallet')">
        <view class="mb-8rpx text-36rpx font-600">0.00</view>
        <view class="text-26rpx text-gray-500">我的余额</view>
      </view>
      <view class="stats-divider"></view>
      <view class="stats-item" @click="navigateToSection('favorites')">
        <view class="mb-8rpx text-36rpx font-600">0</view>
        <view class="text-26rpx text-gray-500">我的收藏</view>
      </view>
      <view class="stats-divider"></view>
      <view class="stats-item" @click="navigateToSection('history')">
        <view class="mb-8rpx text-36rpx font-600">0</view>
        <view class="text-26rpx text-gray-500">浏览历史</view>
      </view>
    </view>

    <!-- 常用工具 -->
    <view class="card-container">
      <view class="card-header">
        <view class="flex-start">
          <wd-icon name="tools" size="18" :color="currentThemeColor" />
          <text class="ml-12rpx text-28rpx font-600">常用工具</text>
        </view>
      </view>
      <view class="flex flex-wrap p-20rpx pt-20rpx pb-10rpx">
        <view class="tool-item" @click="navigateToProfile">
          <view class="tool-icon">
            <wd-icon name="user" size="24" :color="currentThemeColor" />
          </view>
          <view class="text-24rpx">个人资料</view>
        </view>
        <view class="tool-item" @click="navigateToFAQ">
          <view class="tool-icon">
            <wd-icon name="help-circle" size="24" :color="currentThemeColor" />
          </view>
          <view class="text-24rpx">常见问题</view>
        </view>
        <view class="tool-item" @click="handleQuestionFeedback">
          <view class="tool-icon">
            <wd-icon name="check-circle" size="24" :color="currentThemeColor" />
          </view>
          <view class="text-24rpx">问题反馈</view>
        </view>
        <view class="tool-item" @click="navigateToAbout">
          <view class="tool-icon">
            <wd-icon name="info-circle" size="24" :color="currentThemeColor" />
          </view>
          <view class="text-24rpx">关于我们</view>
        </view>
      </view>
    </view>

    <!-- 推荐服务 -->
    <view class="card-container">
      <view class="card-header">
        <view class="flex-start">
          <wd-icon name="star" size="18" :color="currentThemeColor" />
          <text class="ml-12rpx text-28rpx font-600">推荐服务</text>
        </view>
      </view>
      <view>
        <view class="service-item" @click="navigateToSection('services', 'vip')">
          <view class="flex-start">
            <view class="service-icon">
              <wd-icon name="dong" size="22" :color="currentThemeColor" />
            </view>
            <view>
              <view class="text-28rpx font-500">会员中心</view>
              <view class="mt-8rpx text-24rpx text-gray-500">解锁更多特权</view>
            </view>
          </view>
          <wd-icon name="arrow-right" size="14" />
        </view>
        <view class="service-item" @click="navigateToSection('services', 'coupon')">
          <view class="flex-start">
            <view class="service-icon">
              <wd-icon name="discount" size="22" :color="currentThemeColor" />
            </view>
            <view>
              <view class="text-28rpx font-500">优惠券</view>
              <view class="mt-8rpx text-24rpx text-gray-500">查看我的优惠券</view>
            </view>
          </view>
          <wd-icon name="arrow-right" size="14" />
        </view>
        <view
          class="service-item service-item-last"
          @click="navigateToSection('services', 'invite')"
        >
          <view class="flex-start">
            <view class="service-icon">
              <wd-icon name="share" size="22" :color="currentThemeColor" />
            </view>
            <view>
              <view class="text-28rpx font-500">邀请有礼</view>
              <view class="mt-8rpx text-24rpx text-gray-500">邀请好友得奖励</view>
            </view>
          </view>
          <wd-icon name="arrow-right" size="14" />
        </view>
      </view>
    </view>

    <!-- 退出登录按钮 -->
    <view v-if="isLogin" class="p-30rpx">
      <wd-button custom-class="logout-button" plain @click="handleLogout">退出登录</wd-button>
    </view>

    <wd-toast />
  </view>
</template>

<script lang="ts" setup>
import { useToast } from "wot-design-uni";
import { useRouter } from "uni-mini-router";
import { useUserStore, useThemeStore } from "@/store";
import { computed } from "vue";

const toast = useToast();
const userStore = useUserStore();
const themeStore = useThemeStore();
const currentThemeColor = computed(() => themeStore.themeVars.colorTheme);
const userInfo = computed(() => userStore.userInfo);
const isLogin = computed(() => !!userInfo.value);
const defaultAvatar = "/static/images/default-avatar.png";
const isLoading = ref(false);

const router = useRouter();

// 登录
const navigateToLoginPage = () => {
  const pages = getCurrentPages();
  const currentPage = pages[pages.length - 1];
  const currentPagePath = `/${currentPage.route}`;

  router.push({ path: "/pages/login/index", query: { redirect: currentPagePath } });
};

// 退出登录
const handleLogout = () => {
  uni.showModal({
    title: "提示",
    content: "确认退出登录吗？",
    success: function (res) {
      if (res.confirm) {
        userStore.logout();
        toast.show("已退出登录");
      }
    },
  });
};

// 个人信息
const navigateToProfile = () => {
  if (!isLogin.value) {
    navigateToLoginPage();
    return;
  }
  router.push({ path: "/pages/mine/profile/index" });
};

// 常见问题
const navigateToFAQ = () => {
  router.push({ path: "/pages/mine/faq/index" });
};

// 关于我们
const navigateToAbout = () => {
  router.push({ path: "/pages/mine/about/index" });
};

// 设置
const navigateToSettings = () => {
  router.push({ path: "/pages/mine/settings/index" });
};

// 问题反馈
const handleQuestionFeedback = () => {
  router.push({ path: "/pages/mine/feedback/index" });
};

// 导航到各个板块
const navigateToSection = (section: string, subSection?: string) => {
  console.log(`导航到: ${section}${subSection ? ` - ${subSection}` : ""}`);
  // 这里可以根据需要实现具体的导航逻辑
  uni.showToast({
    title: "功能开发中",
    icon: "none",
  });
};

onShow(() => {
  // 确保 tabbar 状态正确
  const pages = getCurrentPages();
  if (pages.length > 0) {
    const currentPage = pages[pages.length - 1];
    if (currentPage.route === "pages/mine/index") {
      // 通过事件通知 tabbar 布局更新状态
      uni.$emit("updateTabbar", "mine");
    }
  }

  // 每次显示页面时都检查并刷新用户信息
  loadUserInfo();
});

// 加载用户信息
const loadUserInfo = async () => {
  if (isLogin.value) {
    isLoading.value = true;
    try {
      await userStore.getInfo();
    } catch (error) {
      console.error("获取用户信息失败", error);
    } finally {
      isLoading.value = false;
    }
  }
};

// 监听用户信息变化，确保数据及时更新
watch(
  () => userInfo.value,
  () => {},
  {
    deep: true,
    immediate: true,
  }
);
</script>

<route lang="json">
{
  "name": "mine",
  "style": { "navigationStyle": "custom" },
  "layout": "tabbar"
}
</route>

<style lang="scss" scoped>
// 用户信息卡片
.user-profile {
  position: relative;
  padding: 30rpx;
  overflow: hidden;

  .blur-bg {
    position: absolute;
    top: 0;
    right: 0;
    left: 0;
    z-index: 0;
    height: 240rpx;
    background: linear-gradient(135deg, var(--wot-color-theme, #165dff) 0%, #667eea 100%);
  }

  .user-info {
    position: relative;
    z-index: 1;
    display: flex;
    align-items: center;

    .avatar-container {
      position: relative;

      .avatar {
        width: 120rpx;
        height: 120rpx;
        border: 4rpx solid rgba(255, 255, 255, 0.8);
        border-radius: 50%;
        box-shadow: 0 6rpx 16rpx rgba(0, 0, 0, 0.1);
      }
    }

    .user-details {
      flex: 1;
      margin-left: 24rpx;

      .nickname {
        margin-bottom: 8rpx;
        font-size: 34rpx;
        font-weight: bold;
      }

      .user-id {
        font-size: 24rpx;
      }

      .login-prompt {
        margin-bottom: 16rpx;
        font-size: 28rpx;
      }
    }

    .actions {
      display: flex;

      .action-btn {
        position: relative;
        display: flex;
        align-items: center;
        justify-content: center;
        width: 70rpx;
        height: 70rpx;
        margin-left: 16rpx;
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 50%;
        box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.05);
      }
    }
  }
}

// 卡片容器
.card-container {
  margin: 24rpx 30rpx;
  overflow: hidden;
  background-color: #fff;
  border-radius: 16rpx;
  box-shadow: 0 1rpx 3rpx rgba(0, 0, 0, 0.1);
}

// 卡片头部
.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20rpx 24rpx;
  border-bottom: 1rpx solid #e5e7eb;
}

// 暗色模式下的卡片样式
:deep(.dark) .card-container {
  background-color: #1f2937;
}

:deep(.dark) .card-header {
  border-bottom-color: #374151;
}

// 工具项
.tool-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 25%;
  margin-bottom: 30rpx;
}

// 工具图标
.tool-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 90rpx;
  height: 90rpx;
  margin-bottom: 12rpx;
  background-color: #f3f4f6;
  border-radius: 18rpx;
  transition: transform 0.15s ease;

  &:active {
    transform: scale(0.95);
  }
}

// 暗色模式下的工具图标样式
:deep(.dark) .tool-icon {
  background-color: #374151;
}

// 数据统计卡片（减少原子类堆叠）
.stats-card {
  display: flex;
  align-items: center;
  padding: 30rpx;
  margin: 20rpx 30rpx;
  background-color: #ffffff;
  border-radius: 16rpx;
  box-shadow: 0 1rpx 3rpx rgba(0, 0, 0, 0.1);
}

:deep(.dark) .stats-card {
  background-color: #1f2937;
}

.stats-item {
  display: flex;
  flex: 1;
  flex-direction: column;
  align-items: center;
}

.stats-divider {
  width: 1px;
  margin: 0 20rpx;
  background-color: #e5e7eb;
}

:deep(.dark) .stats-divider {
  background-color: #374151;
}

// 服务项
.service-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 24rpx;
  border-bottom: 1rpx solid #e5e7eb;
  transition: background-color 0.15s ease;

  &:active {
    background-color: #f3f4f6;
  }

  &.service-item-last {
    border-bottom: none;
  }
}

// 暗色模式下的服务项样式
:deep(.dark) .service-item {
  border-bottom-color: #374151;

  &:active {
    background-color: rgba(255, 255, 255, 0.1);
  }
}

// 服务图标
.service-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 80rpx;
  height: 80rpx;
  margin-right: 20rpx;
  background-color: #f3f4f6;
  border-radius: 16rpx;
}

// 暗色模式下的服务图标样式
:deep(.dark) .service-icon {
  background-color: #374151;
}

// 登录按钮样式
:deep(.btn-login) {
  font-size: 24rpx !important;
  border-radius: 20rpx !important;
}

// 退出登录按钮样式
:deep(.logout-button) {
  width: 100% !important;
  height: 80rpx !important;
  font-size: 32rpx !important;
  font-weight: bold !important;
  border-radius: 40rpx !important;
}
</style>
