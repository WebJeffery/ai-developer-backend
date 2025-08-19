<template>
  <view class="app-container">
    <wd-navbar
      title="关于我们"
      left-arrow
      safe-area-inset-top
      placeholder
      @click-left="handleBack"
    />

    <!-- 顶部品牌区域 -->
    <view class="brand-section">
      <view class="brand-content">
        <wd-img
          :src="webLogo"
          :width="120"
          :height="120"
          round
          custom-class="brand-logo"
          mode="aspectFit"
        />
        <view class="brand-info">
          <view class="brand-title-wrapper">
            <text class="brand-title">{{ webTitle }}</text>
            <wd-tag type="primary" size="small" plain custom-class="version-tag">
              v{{ version }}
            </wd-tag>
          </view>
          <text class="brand-subtitle">{{ webDescription }}</text>
        </view>
      </view>
    </view>

    <!-- 技术栈 -->
    <view class="section">
      <wd-card title="技术栈" custom-style="margin: 20rpx;">
        <view class="tech-stack-container">
          <view class="tech-category">
            <view class="category-title">
              <wd-icon name="computer" size="24" color="#409eff" />
              <text class="category-text">前端技术</text>
            </view>
            <wd-grid :column="4" clickable custom-class="tech-grid">
              <wd-grid-item
                v-for="tech in frontendTechs"
                :key="tech.name"
                :icon="tech.icon"
                :text="tech.name"
              />
            </wd-grid>
          </view>

          <view class="tech-category">
            <view class="category-title">
              <wd-icon name="server" size="24" color="#52c41a" />
              <text class="category-text">后端技术</text>
            </view>
            <wd-grid :column="4" clickable custom-class="tech-grid">
              <wd-grid-item
                v-for="tech in backendTechs"
                :key="tech.name"
                :icon="tech.icon"
                :text="tech.name"
              />
            </wd-grid>
          </view>
        </view>
      </wd-card>
    </view>

    <!-- 资源链接 -->
    <view class="section">
      <wd-card title="资源链接" custom-style="margin: 20rpx;">
        <wd-cell-group>
          <wd-cell title="帮助文档" label="查看完整开发文档" is-link @click="openLink(helpDoc)">
            <template #icon>
              <view class="link-icon-wrapper doc">
                <wd-icon name="document" size="28" color="#409eff" />
              </view>
            </template>
          </wd-cell>
          <wd-cell title="用户协议" label="了解使用条款" is-link @click="openLink(webClause)">
            <template #icon>
              <view class="link-icon-wrapper agreement">
                <wd-icon name="agreement" size="28" color="#52c41a" />
              </view>
            </template>
          </wd-cell>
          <wd-cell title="隐私政策" label="保护您的隐私" is-link @click="openLink(webPrivacy)">
            <template #icon>
              <view class="link-icon-wrapper privacy">
                <wd-icon name="privacy" size="28" color="#faad14" />
              </view>
            </template>
          </wd-cell>
          <wd-cell title="开源代码" label="访问GitHub仓库" is-link @click="openLink(gitCode)">
            <template #icon>
              <view class="link-icon-wrapper github">
                <wd-icon name="github" size="28" color="#333" />
              </view>
            </template>
          </wd-cell>
        </wd-cell-group>
      </wd-card>
    </view>

    <!-- 版权信息 -->
    <view class="copyright-section">
      <wd-divider content-position="center" custom-style="margin: 40rpx 0;">
        <text class="divider-text">版权信息</text>
      </wd-divider>
      <view class="copyright-content">
        <view class="copyright-card">
          <wd-icon name="copyright" size="32" color="#909399" />
          <text class="copyright-text">{{ copyright }}</text>
          <text class="record-text">{{ keepRecord }}</text>
          <view class="copyright-links">
            <text class="copyright-link" @click="openLink(webClause)">用户协议</text>
            <text class="copyright-separator">|</text>
            <text class="copyright-link" @click="openLink(webPrivacy)">隐私政策</text>
          </view>
        </view>
      </view>
    </view>
  </view>
</template>

<script lang="ts" setup>
import { ref } from "vue";

// 系统配置数据
const webTitle = ref("FastAPI Vue3 Admin");
const webDescription = ref("FastAPI Vue3 Admin 是完全开源的权限管理系统");
const version = ref("2.0.0");
const keepRecord = ref("陕ICP备2025069493号-1");
const copyright = ref("Copyright © 2025-2026 service.fastapiadmin.com 版权所有");
const webLogo = ref("http://service.fastapiadmin.com/api/v1/static/image/logo.png");
const helpDoc = ref("http://service.fastapiadmin.com/docs/index.html");
const webClause = ref("https://github.com/1014TaoTao/fastapi_vue3_admin/blob/master/LICENSE");
const webPrivacy = ref("https://github.com/1014TaoTao/fastapi_vue3_admin/blob/master/LICENSE");
const gitCode = ref("https://github.com/1014TaoTao/fastapi_vue3_admin.git");

// 技术栈数据
const frontendTechs = ref([
  { name: "Vue 3", icon: "code", color: "#4fc08d" },
  { name: "TypeScript", icon: "code", color: "#3178c6" },
  { name: "Wot Design", icon: "code", color: "#409eff" },
  { name: "uni-app", icon: "code", color: "#007aff" },
]);

const backendTechs = ref([
  { name: "FastAPI", icon: "link", color: "#009688" },
  { name: "Python", icon: "code", color: "#3776ab" },
  { name: "MySQL", icon: "code", color: "#4479a1" },
  { name: "Redis", icon: "code", color: "#dc382d" },
]);

const handleBack = () => {
  uni.navigateBack();
};

const openLink = (url: string) => {
  // #ifdef H5
  window.open(url, "_blank");
  // #endif

  // #ifdef APP-PLUS
  plus.runtime.openURL(url);
  // #endif

  // #ifdef MP-WEIXIN
  uni.setClipboardData({
    data: url,
    success: () => {
      uni.showToast({
        title: "链接已复制",
        icon: "success",
        duration: 2000,
      });
    },
  });
  // #endif
};
</script>

<style lang="scss" scoped>
.app-container {
  min-height: 100vh;
  padding-bottom: 40rpx;
  background: var(--wot-color-bg-secondary);
}

.brand-section {
  padding: 60rpx 0;
  text-align: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.brand-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.brand-info {
  margin-top: 24rpx;
  text-align: center;
}

.brand-title {
  display: block;
  margin-bottom: 8rpx;
  font-size: 36rpx;
  font-weight: 700;
  color: white;
}

.brand-subtitle {
  display: block;
  margin-bottom: 16rpx;
  font-size: 24rpx;
  color: rgba(255, 255, 255, 0.8);
}

.section {
  margin-top: 40rpx;
}

.copyright-section {
  padding: 0 32rpx;
  margin-top: 60rpx;
  text-align: center;
}

.copyright-content {
  padding: 0 32rpx;
}

.copyright-card {
  padding: 40rpx;
  text-align: center;
  background: var(--wot-color-bg);
  border-radius: 16rpx;
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.04);
}

.copyright-text {
  margin: 20rpx 0 8rpx;
  font-size: 26rpx;
  color: var(--wot-color-text);
}

.record-text {
  margin-bottom: 20rpx;
  font-size: 24rpx;
  color: var(--wot-color-text-secondary);
}

.divider-text {
  font-size: 28rpx;
  font-weight: 600;
  color: var(--wot-color-text);
}

.copyright-links {
  display: flex;
  gap: 16rpx;
  align-items: center;
  justify-content: center;
  margin-top: 20rpx;
}

.copyright-link {
  font-size: 24rpx;
  color: var(--wot-color-primary);
  text-decoration: underline;
}

.copyright-separator {
  font-size: 24rpx;
  color: var(--wot-color-text-third);
}

:deep(.wd-grid-item__content) {
  padding: 0;
}

:deep(.wd-cell__left) {
  display: flex;
  align-items: center;
}

.architecture-detail {
  padding: 0 24rpx;
  margin-top: 32rpx;
}

.detail-item {
  display: flex;
  align-items: flex-start;
  margin-bottom: 16rpx;
  line-height: 1.6;
}

.detail-label {
  flex-shrink: 0;
  margin-right: 16rpx;
  font-weight: 600;
  color: var(--wot-color-text);
}

.detail-value {
  flex: 1;
  color: var(--wot-color-text-secondary);
}

:deep(.architecture-grid) {
  margin: 24rpx;
}

.tech-stack-container {
  padding: 0 24rpx;
}

.tech-category {
  margin-bottom: 32rpx;

  &:last-child {
    margin-bottom: 0;
  }
}

.category-title {
  display: flex;
  align-items: center;
  padding-left: 8rpx;
  margin-bottom: 20rpx;
}

.category-text {
  margin-left: 12rpx;
  font-size: 28rpx;
  font-weight: 600;
  color: var(--wot-color-text);
}

:deep(.tech-grid) {
  margin: 0;
}

:deep(.wd-cell__body) {
  padding: 28rpx 32rpx;
}

:deep(.wd-cell__title) {
  font-size: 30rpx;
  font-weight: 600;
  color: var(--wot-color-text);
}

:deep(.wd-cell__label) {
  margin-top: 8rpx;
  font-size: 26rpx;
  color: var(--wot-color-text-secondary);
}

.link-icon-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48rpx;
  height: 48rpx;
  margin-right: 20rpx;
  border-radius: 12rpx;
}

.link-icon-wrapper.doc {
  background: linear-gradient(135deg, #409eff, #66b1ff);
}

.link-icon-wrapper.agreement {
  background: linear-gradient(135deg, #52c41a, #73d13d);
}

.link-icon-wrapper.privacy {
  background: linear-gradient(135deg, #faad14, #ffc53d);
}

.link-icon-wrapper.github {
  background: linear-gradient(135deg, #333, #666);
}
</style>
