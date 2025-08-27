<script lang="ts" setup>
import { onLoad } from "@dcloudio/uni-app";
import { useThemeStore } from "@/store/modules/theme.store";

const useTheme = useThemeStore();

let theme = useTheme.theme;
let themeVars = useTheme.themeVars;

onLoad(() => {
  theme = useTheme.theme;
  themeVars = useTheme.themeVars;
});
</script>

<script lang="ts">
export default {
  options: {
    addGlobalClass: true,
    virtualHost: true,
    styleIsolation: "shared",
  },
};
</script>

<template>
  <wd-config-provider :theme-vars="themeVars" :theme="theme" :custom-class="`page-wraper ${theme}`">
    <slot />
    <wd-notify />
    <wd-toast />
    <wd-message-box />
  </wd-config-provider>
</template>

<style lang="scss" scoped>
.page-wraper {
  box-sizing: border-box;
  min-height: calc(100vh - var(--window-top));
  background: #f9f9f9;
}

.wot-theme-dark.page-wraper {
  background: #222;
}
</style>
