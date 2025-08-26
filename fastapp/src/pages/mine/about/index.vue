<template>
  <view class="app-container dark:text-[var(--wot-dark-color)]">
    <wd-card custom-style="margin-top: 20rpx">
      <view class="about-header">
        <wd-img
          width="120rpx"
          height="120rpx"
          src="/static/logo.png"
          mode="aspectFit"
          class="about-logo"
        />
        <view class="about-meta">
          <text class="app-title">{{ webTitle }}</text>
          <text class="app-version">版本 {{ version }}</text>
        </view>
      </view>
    </wd-card>

    <!-- 公司信息区域 -->
    <wd-card title="项目概述" custom-style="margin-top: 20rpx">
      <view class="company-section">
        <view class="section-title">
          <wd-icon name="home" size="18" />
          <text>{{ webTitle }}</text>
        </view>
        <text class="section-subtitle">{{ webDescription }}</text>
      </view>
    </wd-card>

    <!-- 项目列表 -->
    <wd-card title="技术站" custom-style="margin-top: 20rpx">
      <wd-cell-group border>
        <wd-cell title="后台" icon="desktop">
          <view slot="label" class="project-desc">
            基于 FastAPI + Uvicorn + SQLAlchemy 构建的RBAC管理系统
          </view>
        </wd-cell>

        <wd-cell title="web前端" icon="mobile">
          <view slot="label" class="project-desc">
            基于 Vue3 + Vite6 + TypeScript + Element-Plus + Pinia 构建的中后台管理模板
          </view>
        </wd-cell>

        <wd-cell title="移动端" icon="server" label="">
          <view slot="label" class="project-desc">
            基于 uni-app + Vite6 + Vue 3 + TypeScript + Wot Design Uni + Pinia 构建的移动端应用模板
          </view>
        </wd-cell>
      </wd-cell-group>
    </wd-card>

    <!-- 联系方式 -->
    <wd-card title="联系我们" custom-style="margin-top: 20rpx">
      <wd-cell-group border>
        <wd-cell title="联系邮箱" value="948080782@qq.com" icon="mail" ellipsis />
        <wd-cell title="官方网站" :value="helpDoc" is-link :to="helpDoc" icon="link" ellipsis />
        <wd-cell title="源码地址" :value="gitCode" is-link :to="gitCode" icon="github" ellipsis />
      </wd-cell-group>
    </wd-card>

    <!-- 底部版权信息 -->
    <view class="about-footer">
      <text class="copyright">{{ copyright }}</text>
      <text class="copyright copyright-sub">{{ keepRecord }}</text>
    </view>
  </view>
</template>

<script lang="ts" setup>
// 系统配置数据
const webTitle = ref("FastAPI Vue3 Admin");
const webDescription = ref("FastAPI Vue3 Admin 是完全开源的权限管理系统");
const version = ref("2.0.0");
const keepRecord = ref("陕ICP备2025069493号-1");
const copyright = ref("Copyright © 2025-2026 service.fastapiadmin.com 版权所有");
const helpDoc = ref("http://service.fastapiadmin.com");
const gitCode = ref("https://github.com/1014TaoTao/fastapi_vue3_admin.git");

onMounted(() => {
  // #ifdef MP-WEIXIN
  version.value = uni.getSystemInfoSync().appVersion;
  // #endif
});
</script>

<route lang="json">
{
  "name": "about",
  "style": {
    "navigationBarTitleText": "关于我们"
  }
}
</route>

<style lang="scss" scoped>
.about-header {
  display: flex;
  align-items: center;
  padding: 20rpx;
}

.about-logo {
  margin-right: 16rpx;
}

.about-meta {
  flex: 1;
}

.app-title {
  display: block;
  margin-bottom: 8rpx;
  font-size: 32rpx;
  font-weight: 700;
}

.app-version {
  font-size: 24rpx;
  color: #6b7280;
}

.company-section {
  padding: 24rpx;
}

.section-title {
  display: flex;
  align-items: center;
  margin-bottom: 12rpx;
  font-size: 28rpx;
  font-weight: 500;

  :deep(.wd-icon) {
    margin-right: 12rpx;
  }
}

.section-subtitle {
  display: block;
  padding-left: 32rpx;
  font-size: 24rpx;
  color: #6b7280;
}

.project-desc {
  margin-top: 8rpx;
  font-size: 24rpx;
  color: #6b7280;
}

.about-footer {
  padding: 32rpx 0;
  text-align: center;
}

.copyright {
  display: block;
  font-size: 24rpx;
  color: #9ca3af;
}

.copyright-sub {
  margin-top: 8rpx;
}
</style>
