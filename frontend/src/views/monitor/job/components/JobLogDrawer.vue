<!-- 字典数据 -->
<template>
  <el-drawer v-model="drawerVisible" :title="'【' + props.dictLabel + '】日志数据'" :size="drawerSize">
    <!-- 搜索区域 -->
    <div class="search-container">
      <!-- 开发中 -->
    </div>
  </el-drawer>
</template>

<script setup lang="ts">
// 处理可以参考字典数据抽屉
// 添加 props 来接收 dictType
const props = defineProps({
  dictType: {
    type: String,
    required: true
  },
  dictLabel: {
    type: String,
    required: true
  }
})

import { useAppStore } from "@/store/modules/app.store";
import { DeviceEnum } from "@/enums/settings/device.enum";

const appStore = useAppStore();
const drawerSize = computed(() => (appStore.device === DeviceEnum.DESKTOP ? "80%" : "60%"));
const drawerVisible = ref<boolean>(false);

</script>
