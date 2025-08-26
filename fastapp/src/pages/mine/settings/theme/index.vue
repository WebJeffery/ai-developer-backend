<template>
  <view class="app-container dark:text-[var(--wot-dark-color)]">
    <!-- 页面标题 -->
    <view class="page-header">
      <text class="page-title">主题设置</text>
      <text class="page-subtitle">个性化您的应用外观</text>
    </view>

    <!-- 暗黑模式设置 -->
    <wd-card class="setting-section">
      <view class="section-header">
        <wd-icon name="moon" size="20" :color="isDarkMode ? '#FFD700' : '#666'" />
        <text class="section-title">外观模式</text>
      </view>
      <wd-cell title="暗黑模式" :value="isDarkMode ? '已开启' : '已关闭'">
        <wd-switch :model-value="isDarkMode" @change="handleToggleDarkMode" />
      </wd-cell>
    </wd-card>

    <!-- 主题色设置 -->
    <wd-card class="setting-section">
      <view class="section-header">
        <wd-icon name="palette" size="20" color="#666" />
        <text class="section-title">主题色彩</text>
      </view>

      <!-- 预设颜色选择 -->
      <view class="color-section">
        <text class="color-label">预设主题色</text>
        <view class="color-grid">
          <view
            v-for="(color, index) in themeColorOptions"
            :key="index"
            class="color-item"
            :class="{ active: currentThemeColor === color.primary }"
            @click="handleSelectColor(color)"
          >
            <view
              class="color-preview"
              :style="{
                backgroundColor: color.primary,
                border:
                  currentThemeColor === color.primary ? '3px solid #fff' : '1px solid #e0e0e0',
              }"
            >
              <text v-if="currentThemeColor === color.primary" class="check-icon">✓</text>
            </view>
            <text class="color-name">{{ color.name }}</text>
          </view>
        </view>
      </view>

      <!-- 当前主题色显示 -->
      <view class="current-theme-section">
        <view class="current-theme-item">
          <text class="current-theme-label">当前主题色</text>
          <view class="current-theme-value">
            <view
              class="current-color-preview"
              :style="{ backgroundColor: currentThemeColor }"
            ></view>
            <text class="current-color-text">{{ currentThemeColor }}</text>
          </view>
        </view>
      </view>

      <!-- 自定义颜色 -->
      <wd-cell title="自定义颜色" is-link @click="showCustomInput">
        <wd-icon name="edit" size="16" color="#999" />
      </wd-cell>
    </wd-card>

    <wd-divider />

    <!-- 操作按钮 -->
    <wd-card class="action-section">
      <wd-button size="large" block @click="handleResetTheme">重置为默认主题</wd-button>
    </wd-card>

    <!-- 自定义颜色输入弹窗 -->
    <wd-popup v-model="showCustomColorInput" position="bottom" :safe-area-inset-bottom="true">
      <view class="custom-color-popup">
        <view class="popup-header">
          <text class="popup-title">自定义主题色</text>
          <wd-icon name="close" size="20" color="#999" @click="showCustomColorInput = false" />
        </view>

        <wd-divider />

        <view class="color-input-section">
          <view class="input-label">请输入十六进制颜色值</view>
          <view class="input-container">
            <view class="color-preview-small" :style="{ backgroundColor: customColor }"></view>
            <wd-input
              v-model="customColor"
              placeholder="例如: #165DFF"
              :maxlength="7"
              class="color-input"
            />
          </view>
          <view class="input-tip">支持格式：#RGB 或 #RRGGBB</view>
        </view>

        <wd-divider />

        <view class="popup-actions">
          <wd-button type="info" size="large" @click="showCustomColorInput = false">取消</wd-button>
          <wd-button type="primary" size="large" @click="applyCustomColor">应用</wd-button>
        </view>
      </view>
    </wd-popup>
  </view>
</template>

<script lang="ts" setup>
import { useTheme } from "@/composables/useTheme";

// 使用主题组合函数
const { isDark, themeVars, themeColorOptions, toggleTheme, setThemeColor } = useTheme();

// 创建响应式的计算属性
const isDarkMode = computed(() => isDark.value);

// 自定义颜色输入
const customColor = ref("");
const showCustomColorInput = ref(false);

// 当前选中的主题色
const currentThemeColor = computed(() => {
  return themeVars.value.colorTheme || themeColorOptions.value[0].primary;
});

// 选择预设颜色
const handleSelectColor = (color: (typeof themeColorOptions.value)[0]) => {
  setThemeColor(color);
  customColor.value = color.primary;

  // 提示
  uni.showToast({
    title: "主题色已更新",
    icon: "success",
    duration: 1500,
  });
};

// 显示自定义颜色输入
const showCustomInput = () => {
  showCustomColorInput.value = true;
  customColor.value = currentThemeColor.value;
};

// 应用自定义颜色
const applyCustomColor = () => {
  // 验证颜色格式
  const colorRegex = /^#([0-9A-F]{6}|[0-9A-F]{3})$/i;
  if (!colorRegex.test(customColor.value)) {
    uni.showToast({
      title: "请输入有效的颜色值",
      icon: "none",
      duration: 2000,
    });
    return;
  }

  // 转换3位颜色值为6位
  let color = customColor.value;
  if (color.length === 4) {
    color = "#" + color[1] + color[1] + color[2] + color[2] + color[3] + color[3];
  }

  // 创建自定义主题色选项
  const customColorOption = {
    name: "自定义",
    value: "custom",
    primary: color,
  };

  setThemeColor(customColorOption);
  showCustomColorInput.value = false;

  // 提示
  uni.showToast({
    title: "自定义主题色已应用",
    icon: "success",
    duration: 1500,
  });
};

// 重置为默认主题
const handleResetTheme = () => {
  uni.showModal({
    title: "确认重置",
    content: "确定要重置为默认主题吗？",
    success: (res) => {
      if (res.confirm) {
        setThemeColor(themeColorOptions.value[0]);
        customColor.value = themeColorOptions.value[0].primary;

        uni.showToast({
          title: "已重置为默认主题",
          icon: "success",
          duration: 1500,
        });
      }
    },
  });
};

// 切换暗黑模式
const handleToggleDarkMode = () => {
  toggleTheme();
  nextTick(() => {
    uni.showToast({
      title: `已切换到${isDarkMode.value ? "暗黑" : "浅色"}模式`,
      icon: "success",
      duration: 1500,
    });
  });
};

onLoad(() => {
  customColor.value = currentThemeColor.value;
});

onMounted(() => {
  customColor.value = currentThemeColor.value;
});

// 页面显示时确保主题色同步
onShow(() => {
  customColor.value = currentThemeColor.value;
});
</script>

<route lang="json">
{
  "name": "theme",
  "style": {
    "navigationBarTitleText": "主题设置"
  }
}
</route>

<style lang="scss" scoped>
// 基础布局
.page-header {
  padding: 40rpx 20rpx;
  margin-bottom: 30rpx;
  text-align: center;
  background: linear-gradient(135deg, var(--wot-color-theme, #165dff) 0%, #667eea 100%);
  border-radius: 16rpx;

  .page-title {
    display: block;
    margin-bottom: 10rpx;
    font-size: 36rpx;
    font-weight: bold;
    color: #fff;
  }

  .page-subtitle {
    font-size: 26rpx;
    color: rgba(255, 255, 255, 0.8);
  }
}

.setting-section {
  margin-bottom: 30rpx;
}

.section-header {
  display: flex;
  align-items: center;
  padding: 30rpx 30rpx 20rpx;
  border-bottom: 1rpx solid var(--wot-color-border, #f0f0f0);

  .section-title {
    margin-left: 12rpx;
    font-size: 32rpx;
    font-weight: 600;
    color: var(--wot-color-text, #333);
  }
}

// 颜色选择区域
.color-section {
  padding: 30rpx;

  .color-label {
    margin-bottom: 20rpx;
    font-size: 28rpx;
    color: var(--wot-color-text-secondary, #666);
  }

  .color-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 20rpx;
    justify-content: space-between;
  }
}

.color-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: calc(25% - 15rpx);
  padding: 10rpx;
  cursor: pointer;
  transition: all 0.3s ease;

  .color-preview {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 60rpx;
    height: 60rpx;
    margin-bottom: 8rpx;
    border-radius: 12rpx;
    box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;

    .check-icon {
      font-size: 24rpx;
      font-weight: bold;
      color: #fff;
      text-shadow: 0 1rpx 2rpx rgba(0, 0, 0, 0.5);
    }
  }

  .color-name {
    font-size: 22rpx;
    color: var(--wot-color-text-secondary);
    text-align: center;
  }

  &.active .color-preview {
    box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.2);
    transform: scale(1.05);
  }

  &:active .color-preview {
    transform: scale(0.95);
  }
}

// 当前主题色显示
.current-theme-section {
  padding: 30rpx;

  .current-theme-item {
    display: flex;
    align-items: center;
    justify-content: space-between;

    .current-theme-label {
      font-size: 28rpx;
      color: var(--wot-color-text-secondary, #666);
    }

    .current-theme-value {
      display: flex;
      align-items: center;

      .current-color-preview {
        width: 40rpx;
        height: 40rpx;
        border: 2rpx solid var(--wot-color-border, #f0f0f0);
        border-radius: 8rpx;
      }

      .current-color-text {
        margin-left: 10rpx;
        font-size: 28rpx;
        font-weight: 500;
      }
    }
  }
}

.preview-border {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 200rpx;
  height: 60rpx;
  font-size: 26rpx;
  color: var(--wot-color-text-secondary, #666);
  border: 2rpx solid;
  border-radius: 8rpx;
}

// 自定义颜色弹窗
.custom-color-popup {
  padding: 40rpx 30rpx;
  background: var(--wot-popup-bg-color, #fff);
  border-radius: 20rpx 20rpx 0 0;

  .popup-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 30rpx;

    .popup-title {
      font-size: 32rpx;
      font-weight: 600;
      color: var(--wot-color-text, #333);
    }
  }

  .color-input-section {
    margin-bottom: 40rpx;

    .input-label {
      margin-bottom: 20rpx;
      font-size: 28rpx;
      color: var(--wot-color-text-secondary, #666);
    }

    .input-container {
      display: flex;
      gap: 20rpx;
      align-items: center;
      margin-bottom: 10rpx;

      .color-preview-small {
        flex-shrink: 0;
        width: 60rpx;
        height: 60rpx;
        border: 2rpx solid var(--wot-color-border, #f0f0f0);
        border-radius: 8rpx;
      }

      .color-input {
        flex: 1;
      }
    }

    .input-tip {
      margin-left: 80rpx;
      font-size: 24rpx;
      color: var(--wot-color-text-placeholder, #999);
    }
  }

  .popup-actions {
    display: flex;
    gap: 20rpx;
  }
}
</style>
