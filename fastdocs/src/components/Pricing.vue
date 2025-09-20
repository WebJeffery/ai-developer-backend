<template>
    <div class="pricing-container">
        <div class="pricing-header">
            <h1 class="pricing-title">订阅支持</h1>
            <p class="pricing-subtitle">
                ✨此架构无需商业授权，任何个人或企业均可自由使用✨<br>
                <span style="color: var(--vp-c-text-2)">
                    以下付费版本仅用于赞助支持，非必须购买
                </span>
            </p>
        </div>

        <div class="pricing-toggle">
            <span class="billing-period">月付</span>
            <label class="toggle-switch">
                <input type="checkbox" v-model="isAnnual" @change="toggleBillingPeriod">
                <span class="slider"></span>
            </label>
            <span class="billing-period">年付</span>
            <span class="discount-badge" v-if="isAnnual">省20%</span>
        </div>

        <div class="pricing-cards">
            <div class="pricing-card">
                <div class="card-content">
                    <div class="card-header">
                        <h2>{{ plans.openSource.title }}</h2>
                        <p class="card-description">{{ plans.openSource.description }}</p>
                    </div>
                    <div class="price-section">
                        <div class="current-price">免费</div>
                    </div>
                    <ul class="features-list">
                        <li v-for="(feature, index) in plans.openSource.features" :key="index">
                            <span class="feature-icon"><svg width="16" height="16" viewBox="0 0 16 16" fill="none"
                                    xmlns="http://www.w3.org/2000/svg">
                                    <path d="M12.6667 4.66667L6 11.3333L3.33333 8.66667" stroke="currentColor"
                                        stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
                                </svg></span>
                            {{ feature }}
                        </li>
                    </ul>
                </div>
                <button class="cta-button" @click="handleSubscribe('openSource')">
                    立即使用
                </button>
            </div>

            <div class="pricing-card highlighted">
                <div class="popular-tag">最受欢迎</div>
                <div class="card-content">
                    <div class="card-header">
                        <h2>{{ plans.professional.title }}</h2>
                        <p class="card-description">{{ plans.professional.description }}</p>
                    </div>
                    <div class="price-section">
                        <div class="current-price">
                            {{ isAnnual ? plans.professional.price.annual : plans.professional.price.monthly }}
                            <span class="billing-cycle">{{ isAnnual ? '/ 年' : '/ 月' }}</span>
                        </div>
                        <div v-if="isAnnual" class="original-price">
                            <del>原价: {{ '￥' + (parseInt(plans.professional.price.monthly.replace('￥', '')) * 12)
                                }}</del>
                        </div>
                    </div>
                    <ul class="features-list">
                        <li v-for="(feature, index) in plans.professional.features" :key="index">
                            <span class="feature-icon"><svg width="16" height="16" viewBox="0 0 16 16" fill="none"
                                    xmlns="http://www.w3.org/2000/svg">
                                    <path d="M12.6667 4.66667L6 11.3333L3.33333 8.66667" stroke="currentColor"
                                        stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
                                </svg></span>
                            {{ feature }}
                        </li>
                    </ul>
                </div>
                <button class="cta-button primary" @click="handleSubscribe('professional')">
                    立即订阅
                </button>
            </div>

            <div class="pricing-card">
                <div class="card-content">
                    <div class="card-header">
                        <h2>{{ plans.enterprise.title }}</h2>
                        <p class="card-description">{{ plans.enterprise.description }}</p>
                    </div>
                    <div class="price-section">
                        <div class="current-price">
                            {{ plans.enterprise.price.custom }}
                        </div>
                    </div>
                    <ul class="features-list">
                        <li v-for="(feature, index) in plans.enterprise.features" :key="index">
                            <span class="feature-icon">
                                <svg width="16" height="16" viewBox="0 0 16 16" fill="none"
                                    xmlns="http://www.w3.org/2000/svg">
                                    <path d="M12.6667 4.66667L6 11.3333L3.33333 8.66667" stroke="currentColor"
                                        stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
                                </svg>
                            </span>
                            {{ feature }}
                        </li>
                    </ul>
                </div>
                <button class="cta-button" @click="handleSubscribe('enterprise')">
                    联系我们
                </button>
            </div>
        </div>

        <!-- 订阅成功弹窗 -->
        <div v-if="showSuccessModal" class="modal-overlay" @click="showSuccessModal = false">
            <div class="modal-content" @click.stop>
                <div class="modal-header">
                    <h3>订阅成功！</h3>
                    <button class="close-btn" @click="showSuccessModal = false">
                        <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M12 4L4 12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"
                                stroke-linejoin="round" />
                            <path d="M4 4L12 12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"
                                stroke-linejoin="round" />
                        </svg>
                    </button>
                </div>
                <div class="modal-body">
                    <p>感谢您的支持！我们会尽快与您联系。</p>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const isAnnual = ref(false);
const showSuccessModal = ref(false);

const plans = {
    openSource: {
        title: '开源版',
        description: '个人开发者与独立项目之选',
        features: [
            '全部基础功能',
            '全量架构源码',
            'MIT 许可证',
            'GitHub 社区支持',
            '自由使用',
            '自主部署',
            '无需保留版权',
            '无需保留许可声明',
            '部分文档访问',
            '部分插件源码'
        ]
    },
    professional: {
        title: '专业版',
        description: '专业开发者的得力助手',
        price: {
            monthly: '￥199',
            annual: '￥1599',
            original: '￥2388'
        },
        features: [
            '所有开源版功能',
            '所有文档访问',
            '所有官方插件源码',
            'Discord 身份标签',
            'Discord 专属频道',
            '优先技术支持',
            '部署指导',
            '专属客服',
            '月度项目更新',
            '企业级安全保障'
        ]
    },
    enterprise: {
        title: '企业版',
        description: '为团队与大规模项目而生',
        price: {
            custom: '定制化'
        },
        features: [
            '所有专业版功能',
            '专属企业群组',
            '远程技术支持',
            '定制化开发服务',
            '专属项目经理',
            '性能优化方案',
            '企业级培训',
            '专属部署环境',
            '7x24小时紧急支持',
            '源码定制许可'
        ]
    }
};

function toggleBillingPeriod() {
    isAnnual.value = !isAnnual.value;
}

function handleSubscribe(planType) {
    // 这里可以添加实际的订阅逻辑
    console.log(`订阅 ${planType} 计划`, isAnnual.value ? '年付' : '月付');

    // 显示成功弹窗
    showSuccessModal.value = true;

}
</script>

<style scoped>
.pricing-container {
    margin: 0 auto;
    padding: 2rem 0 4rem;
    max-width: 1200px;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.pricing-header {
    text-align: center;
    margin-bottom: 2rem;
}

.pricing-title {
    color: var(--vp-c-text-1);
    margin: 2rem 0 1rem;
    font-size: 2.5rem;
}

.pricing-subtitle {
    color: var(--vp-c-text-2);
    margin-bottom: 2rem;
    font-size: 1.1rem;
}

.pricing-toggle {
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 3rem;
    gap: 1rem;
}

.billing-period {
    color: var(--vp-c-text-2);
    font-size: 1rem;
}

.discount-badge {
    background-color: var(--vp-c-success-soft);
    color: var(--vp-c-success);
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: bold;
}

.toggle-switch {
    position: relative;
    display: inline-block;
    width: 50px;
    height: 24px;
}

.toggle-switch input {
    opacity: 0;
    width: 0;
    height: 0;
}

.slider {
    position: absolute;
    cursor: pointer;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: var(--vp-c-border);
    transition: .4s;
    border-radius: 24px;
}

.slider:before {
    position: absolute;
    content: "";
    height: 18px;
    width: 18px;
    left: 3px;
    bottom: 3px;
    background-color: white;
    transition: .4s;
    border-radius: 50%;
}

input:checked+.slider {
    background-color: var(--vp-c-brand-1);
}

input:checked+.slider:before {
    transform: translateX(26px);
}

.pricing-cards {
    display: flex;
    flex-wrap: nowrap;
    justify-content: center;
    gap: 2rem;
    padding: 0 1rem;
}

.pricing-card {
    position: relative;
    border: 1px solid var(--vp-c-border);
    border-radius: 12px;
    padding: 1rem;
    display: flex;
    flex-direction: column;
    transition: all 0.3s ease;
    background-color: var(--vp-c-background);
}

.pricing-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05);
}

.pricing-card.highlighted {
    border: 2px solid var(--vp-c-brand-1);
    background-color: var(--vp-c-brand-soft);
}

.popular-tag {
    position: absolute;
    top: -18px;
    left: 50%;
    transform: translateX(-50%);
    background-color: var(--vp-c-brand-1);
    color: white;
    padding: 0.25rem 1rem;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: bold;
}

.card-content {
    flex: 1;
}

.card-header {
    margin: -1rem 0 1.5rem;
    text-align: center;
}

.card-description {
    font-size: 0.9rem;
    color: var(--vp-c-text-2);
}

.price-section {
    text-align: center;
    margin-bottom: 2rem;
    padding: 1rem 0;
}

.current-price {
    font-size: 2.5rem;
    font-weight: bold;
    color: var(--vp-c-brand-1);
    margin-bottom: 0.5rem;
}

.billing-cycle {
    font-size: 1rem;
    color: var(--vp-c-text-3);
}

.original-price {
    color: var(--vp-c-text-3);
    font-size: 1rem;
    margin-top: 0.5rem;
}

.features-list {
    list-style: none;
    padding: 0;
    margin-bottom: 2rem;
}

.features-list li {
    padding: 0.75rem 0;
    display: flex;
    align-items: flex-start;
    font-size: 0.95rem;
    border-bottom: 1px solid var(--vp-c-border);
}

.features-list li:last-child {
    border-bottom: none;
}

.feature-icon {
    color: var(--vp-c-brand-1);
    margin-right: 0.75rem;
    margin-top: 2px;
    flex-shrink: 0;
}

.cta-button {
    width: 100%;
    padding: 0.85rem;
    border: 2px solid var(--vp-c-brand-1);
    border-radius: 8px;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.2s ease;
    font-size: 1rem;
    background-color: transparent;
    color: var(--vp-c-brand-1);
}

.cta-button:hover {
    background-color: var(--vp-c-brand-1);
    color: white;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(125, 71, 229, 0.2);
}

.cta-button.primary {
    background-color: var(--vp-c-brand-1);
    color: white;
}

.cta-button.primary:hover {
    background-color: var(--vp-c-brand-2);
    border-color: var(--vp-c-brand-2);
}

/* 弹窗样式 */
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
}

.modal-content {
    background-color: white;
    border-radius: 8px;
    padding: 2rem;
    max-width: 400px;
    width: 90%;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid var(--vp-c-border);
}

.modal-header h3 {
    margin: 0;
    color: var(--vp-c-text-1);
}

.modal-body p {
    color: var(--vp-c-text-2);
    margin: 0;
    text-align: center;
}

.modal-close {
    background: none;
    border: none;
    cursor: pointer;
    color: var(--vp-c-text-3);
    padding: 0;
}

@media (max-width: 1200px) {
    .pricing-cards {
        overflow-x: auto;
        justify-content: flex-start;
        padding-bottom: 1rem;
    }

    .pricing-cards::-webkit-scrollbar {
        height: 6px;
    }

    .pricing-cards::-webkit-scrollbar-track {
        background: var(--vp-c-border);
        border-radius: 3px;
    }

    .pricing-cards::-webkit-scrollbar-thumb {
        background: var(--vp-c-text-3);
        border-radius: 3px;
    }

    .pricing-cards::-webkit-scrollbar-thumb:hover {
        background: var(--vp-c-text-2);
    }
}

@media (max-width: 767px) {
    .pricing-card {
        padding: 1.5rem;
        min-width: 280px;
    }

    .pricing-title {
        font-size: 2rem;
        margin: 1.5rem 0 0.75rem;
    }

    .pricing-subtitle {
        margin-bottom: 1.5rem;
        font-size: 1rem;
    }

    .current-price {
        font-size: 2rem;
    }
}

@media (min-width: 768px) {
    .pricing-cards {
        justify-content: center;
    }
}
</style>