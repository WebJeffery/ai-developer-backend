<template>
  <view class="faq-container">
    <scroll-view class="content-scroll" scroll-y :scroll-top="scrollTop" @scroll="handleScroll">
      <view class="content-wrapper">
        <!-- 技术支持卡片 -->
        <view class="support-card">
          <view class="card-header">
            <wd-icon name="service" size="48rpx" color="#0083f0" />
            <text class="card-title">技术支持</text>
          </view>
          <view class="card-body">
            <text class="card-desc">专业的技术团队为您提供7×24小时服务支持</text>
            <view class="support-grid">
              <view class="support-item" @tap="handleContact('email')">
                <view class="support-icon">
                  <wd-icon name="mail" size="40rpx" color="#0083f0" />
                </view>
                <view class="support-info">
                  <text class="support-label">邮箱支持</text>
                  <text class="support-value" user-select>support@example.com</text>
                </view>
              </view>
              <view class="support-item" @tap="handleContact('phone')">
                <view class="support-icon">
                  <wd-icon name="phone" size="40rpx" color="#0083f0" />
                </view>
                <view class="support-info">
                  <text class="support-label">客服热线</text>
                  <text class="support-value">400-123-4567</text>
                </view>
              </view>
              <view class="support-item">
                <view class="support-icon">
                  <wd-icon name="clock" size="40rpx" color="#0083f0" />
                </view>
                <view class="support-info">
                  <text class="support-label">服务时间</text>
                  <text class="support-value">工作日 9:00-18:00</text>
                </view>
              </view>
            </view>
          </view>
        </view>

        <!-- FAQ内容区域 -->
        <view class="faq-section">
          <wd-collapse v-model="activeNames" accordion>
            <wd-collapse-item title="常见问题" name="faq">
              <view class="faq-list">
                <view
                  v-for="(item, index) in faqList"
                  :key="index"
                  class="faq-item"
                  :class="{ active: currentFaq === index }"
                  @tap="toggleFaq(index)"
                >
                  <view class="faq-header">
                    <view class="faq-question">
                      <wd-icon name="question-filled" size="28rpx" color="#ff9500" />
                      <text class="question-text">{{ item.question }}</text>
                    </view>
                    <wd-icon
                      name="arrow-down-bold"
                      size="24rpx"
                      color="#999"
                      :custom-class="currentFaq === index ? 'rotate-180' : ''"
                    />
                  </view>
                  <view v-if="currentFaq === index" class="faq-answer">
                    <text class="answer-text">{{ item.answer }}</text>
                  </view>
                </view>
              </view>
            </wd-collapse-item>

            <wd-collapse-item title="系统功能" name="features">
              <view class="feature-list">
                <view v-for="(feature, index) in featureList" :key="index" class="feature-item">
                  <view class="feature-icon">
                    <wd-icon :name="feature.icon" size="48rpx" :color="feature.color" />
                  </view>
                  <view class="feature-content">
                    <text class="feature-name">{{ feature.name }}</text>
                    <text class="feature-desc">{{ feature.desc }}</text>
                  </view>
                </view>
              </view>
            </wd-collapse-item>

            <wd-collapse-item title="使用指南" name="guide">
              <view class="guide-section">
                <view class="guide-header">
                  <wd-icon name="light" size="44rpx" color="#ff9500" />
                  <text class="guide-title">快速开始</text>
                </view>
                <view class="guide-steps">
                  <view v-for="(step, index) in guideSteps" :key="index" class="guide-step">
                    <view class="step-indicator">
                      <view class="step-number">{{ index + 1 }}</view>
                      <view v-if="index < guideSteps.length - 1" class="step-line"></view>
                    </view>
                    <view class="step-content">
                      <text class="step-title">{{ step.title }}</text>
                      <text v-if="step.desc" class="step-desc">{{ step.desc }}</text>
                    </view>
                  </view>
                </view>
                <view class="guide-footer">
                  <wd-icon name="tips" size="28rpx" color="#999" />
                  <text class="footer-text">详细操作手册请查看帮助文档或联系客服获取</text>
                </view>
              </view>
            </wd-collapse-item>
          </wd-collapse>
        </view>
      </view>
    </scroll-view>
  </view>
</template>

<script lang="ts" setup>
import { ref } from "vue";

// 响应式数据
const activeNames = ref<string[]>(["faq"]);
const currentFaq = ref<number | null>(null);
const scrollTop = ref<number>(0);

// FAQ数据
const faqList = ref([
  {
    question: "如何重置密码？",
    answer:
      "在登录页面点击 '忘记密码'，按照提示操作即可重置密码。如果无法收到验证码，请检查邮箱或手机号是否正确，或联系客服协助处理。",
  },
  {
    question: "数据如何备份？",
    answer:
      "系统会自动定期备份数据，您也可以在'系统设置-数据管理'中手动导出数据。建议每月进行一次完整数据备份，确保数据安全。",
  },
  {
    question: "支持哪些浏览器？",
    answer:
      "推荐使用Chrome 90+、Firefox 88+、Safari 14+、Edge 90+等现代浏览器。IE浏览器仅支持IE11及以上版本。",
  },
  {
    question: "如何联系客服？",
    answer:
      "您可以通过以下方式联系客服：1. 客服热线 400-123-4567（工作日9:00-18:00）；2. 邮箱 support@example.com（7×24小时）；3. 在线客服（工作日9:00-18:00）。",
  },
]);

// 系统功能数据
const featureList = ref([
  {
    name: "用户管理",
    desc: "支持用户注册、登录、权限管理等功能",
    icon: "user",
    color: "#0083f0",
  },
  {
    name: "数据统计",
    desc: "提供实时数据分析和可视化报表",
    icon: "chart",
    color: "#00c250",
  },
  {
    name: "文件管理",
    desc: "支持文件上传、下载、分类管理",
    icon: "folder",
    color: "#ff9500",
  },
  {
    name: "消息通知",
    desc: "实时消息推送和系统通知",
    icon: "notification",
    color: "#ff3b30",
  },
]);

// 使用指南数据
const guideSteps = ref([
  {
    title: "注册账号并登录系统",
    desc: "使用手机号或邮箱注册账号，完成实名认证",
  },
  {
    title: "完善个人或企业信息",
    desc: "填写基本信息，设置安全问题和密保邮箱",
  },
  {
    title: "根据需求配置功能模块",
    desc: "选择需要的功能模块，设置相关参数",
  },
  {
    title: "开始使用各项功能",
    desc: "完成初始化设置，开始使用系统各项功能",
  },
]);

const handleScroll = (e: any) => {
  scrollTop.value = e.detail.scrollTop;
};

const toggleFaq = (index: number) => {
  currentFaq.value = currentFaq.value === index ? null : index;
};

const handleContact = (type: "email" | "phone") => {
  if (type === "email") {
    // #ifdef H5
    window.location.href = "mailto:support@example.com";
    // #endif
    // #ifndef H5
    uni.setClipboardData({
      data: "support@example.com",
      success: () => {
        uni.showToast({
          title: "邮箱已复制",
          icon: "success",
        });
      },
    });
    // #endif
  } else if (type === "phone") {
    // #ifdef H5
    window.location.href = "tel:400-123-4567";
    // #endif
    // #ifndef H5
    uni.makePhoneCall({
      phoneNumber: "400-123-4567",
    });
    // #endif
  }
};

// 生命周期
onMounted(() => {
  // 可以在这里添加页面埋点或初始化逻辑
});
</script>
<route lang="json">
{
  "name": "faq",
  "style": {
    "navigationBarTitleText": "常见问题"
  }
}
</route>
<style lang="scss" scoped>
.faq-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  background: var(--wot-color-bg);

  .content-scroll {
    flex: 1;
    height: 100%;
  }

  .content-wrapper {
    padding: 24rpx;
  }

  // 技术支持卡片样式
  .support-card {
    margin-bottom: 24rpx;
    overflow: hidden;
    background: #fff;
    border-radius: 24rpx;
    box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.04);

    .card-header {
      display: flex;
      align-items: center;
      padding: 32rpx 32rpx 24rpx;
      border-bottom: 1rpx solid var(--wot-color-border);

      .card-title {
        margin-left: 16rpx;
        font-size: 32rpx;
        font-weight: 600;
        color: var(--wot-color-text);
      }
    }

    .card-body {
      padding: 32rpx;

      .card-desc {
        display: block;
        margin-bottom: 32rpx;
        font-size: 28rpx;
        line-height: 1.5;
        color: var(--wot-color-text-light);
        text-align: center;
      }

      .support-grid {
        display: grid;
        grid-template-columns: 1fr;
        gap: 24rpx;

        .support-item {
          display: flex;
          align-items: center;
          padding: 32rpx;
          background: var(--wot-color-bg);
          border-radius: 16rpx;
          transition: all 0.3s ease;

          &:active {
            opacity: 0.8;
            transform: scale(0.98);
          }

          .support-icon {
            flex-shrink: 0;
            margin-right: 24rpx;
          }

          .support-info {
            flex: 1;

            .support-label {
              display: block;
              margin-bottom: 8rpx;
              font-size: 28rpx;
              font-weight: 600;
              color: var(--wot-color-text);
            }

            .support-value {
              display: block;
              font-size: 26rpx;
              color: var(--wot-color-text-light);
            }
          }
        }
      }
    }
  }

  // FAQ区域样式
  .faq-section {
    :deep(.wd-collapse-item__title) {
      font-size: 32rpx;
      font-weight: 600;
    }

    :deep(.wd-collapse-item__content) {
      padding: 0;
    }

    .faq-list {
      .faq-item {
        border-bottom: 1rpx solid var(--wot-color-border);
        transition: all 0.3s ease;

        &:last-child {
          border-bottom: none;
        }

        &.active {
          background: rgba(0, 131, 240, 0.02);
        }

        .faq-header {
          display: flex;
          align-items: center;
          justify-content: space-between;
          padding: 32rpx;

          .faq-question {
            display: flex;
            flex: 1;
            align-items: center;
            margin-right: 24rpx;

            .question-text {
              margin-left: 16rpx;
              font-size: 30rpx;
              color: var(--wot-color-text);
            }
          }

          .wd-icon {
            transition: transform 0.3s ease;

            &.rotate-180 {
              transform: rotate(180deg);
            }
          }
        }

        .faq-answer {
          padding: 0 32rpx 32rpx 32rpx;
          border-top: 1rpx solid var(--wot-color-border);

          .answer-text {
            display: block;
            padding: 24rpx 0;
            font-size: 28rpx;
            line-height: 1.6;
            color: var(--wot-color-text-light);
          }
        }
      }
    }

    .feature-list {
      .feature-item {
        display: flex;
        align-items: center;
        padding: 32rpx;
        border-bottom: 1rpx solid var(--wot-color-border);

        &:last-child {
          border-bottom: none;
        }

        .feature-icon {
          flex-shrink: 0;
          margin-right: 24rpx;
        }

        .feature-content {
          flex: 1;

          .feature-name {
            display: block;
            margin-bottom: 8rpx;
            font-size: 30rpx;
            font-weight: 600;
            color: var(--wot-color-text);
          }

          .feature-desc {
            display: block;
            font-size: 26rpx;
            line-height: 1.4;
            color: var(--wot-color-text-light);
          }
        }
      }
    }

    .guide-section {
      padding: 32rpx;

      .guide-header {
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 48rpx;

        .guide-title {
          margin-left: 16rpx;
          font-size: 32rpx;
          font-weight: 600;
          color: var(--wot-color-text);
        }
      }

      .guide-steps {
        .guide-step {
          display: flex;
          margin-bottom: 48rpx;

          &:last-child {
            margin-bottom: 0;
          }

          .step-indicator {
            position: relative;
            flex-shrink: 0;
            margin-right: 24rpx;

            .step-number {
              display: flex;
              align-items: center;
              justify-content: center;
              width: 48rpx;
              height: 48rpx;
              font-size: 24rpx;
              font-weight: 600;
              color: #fff;
              background: var(--wot-color-theme);
              border-radius: 50%;
            }

            .step-line {
              position: absolute;
              top: 48rpx;
              left: 50%;
              width: 2rpx;
              height: 48rpx;
              background: var(--wot-color-border);
              transform: translateX(-50%);
            }
          }

          .step-content {
            flex: 1;
            padding-top: 8rpx;

            .step-title {
              display: block;
              margin-bottom: 8rpx;
              font-size: 30rpx;
              font-weight: 600;
              color: var(--wot-color-text);
            }

            .step-desc {
              display: block;
              font-size: 26rpx;
              line-height: 1.4;
              color: var(--wot-color-text-light);
            }
          }
        }
      }

      .guide-footer {
        display: flex;
        align-items: center;
        padding: 32rpx;
        margin-top: 48rpx;
        background: var(--wot-color-bg);
        border-radius: 16rpx;

        .footer-text {
          margin-left: 16rpx;
          font-size: 26rpx;
          color: var(--wot-color-text-light);
        }
      }
    }
  }
}

// 响应式设计
@media screen and (min-width: 768px) {
  .faq-container {
    .content-wrapper {
      max-width: 750rpx;
      margin: 0 auto;
    }

    .support-card {
      .support-grid {
        grid-template-columns: repeat(3, 1fr);
      }
    }
  }
}

// 暗黑模式适配
@media (prefers-color-scheme: dark) {
  .faq-container {
    --wot-color-text: #f5f5f5;
    --wot-color-text-light: #969799;
    --wot-color-border: #3a3a3c;
    --wot-color-bg: #1c1c1e;

    .support-card,
    .faq-section :deep(.wd-collapse) {
      color: var(--wot-color-text);
      background: #2c2c2e;
    }
  }
}
</style>
