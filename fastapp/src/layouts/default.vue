<script lang="ts" setup>
import { useThemeStore } from "@/store/modules/theme.store";
import { onMounted, onUnmounted, computed } from "vue";

const themeStore = useThemeStore();
const theme = computed(() => themeStore.theme);
const themeVars = computed(() => themeStore.themeVars);

// 监听主题变化事件
const handleThemeChange = (newTheme: string) => {
  // 当主题变化时强制更新组件
  // 这里可以添加一些更新逻辑
};

onMounted(() => {
  // 监听主题变化事件
  uni.$on("theme-change", handleThemeChange);
});

onUnmounted(() => {
  // 移除事件监听
  uni.$off("theme-change", handleThemeChange);
});
</script>

<template>
  <wd-config-provider :theme-vars="themeVars" :theme="theme" :custom-class="`page-wrapper theme-adaptive ${theme}`">
    <slot />
    <wd-notify />
    <wd-toast />
    <wd-message-box />
  </wd-config-provider>
</template>

<style lang="scss" scoped>
.page-wrapper {
  box-sizing: border-box;
  min-height: calc(100vh - var(--window-top));
  background-color: var(--bg-color-2);
  transition: background-color 0.3s ease;
}

.wot-theme-dark.page-wrapper {
  background-color: var(--bg-color);
}
</style>