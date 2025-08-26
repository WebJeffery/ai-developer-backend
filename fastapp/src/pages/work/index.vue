<template>
  <view class="workbench-container">
    <!-- 顶部统计卡片 -->
    <view class="stats-section">
      <view class="stats-grid">
        <view v-for="(stat, index) in statsData" :key="index" class="stat-card">
          <view class="stat-icon" :style="{ backgroundColor: stat.color + '20' }">
            <wd-icon :name="stat.icon" :color="stat.color" size="24" />
          </view>
          <view class="stat-content">
            <text class="stat-number">{{ stat.number }}</text>
            <text class="stat-label">{{ stat.label }}</text>
          </view>
        </view>
      </view>
    </view>

    <!-- 快捷入口 -->
    <view class="quick-actions-section">
      <view class="section-header">
        <text class="section-title">快捷入口</text>
        <text class="section-subtitle">常用功能一键直达</text>
      </view>
      <view class="actions-grid">
        <view class="action-item" v-for="(action, index) in quickActions" :key="index" @tap="handleQuickAction(action)">
          <view class="action-icon" :style="{ backgroundColor: action.color + '15' }">
            <wd-icon :name="action.icon" :color="action.color" size="28" />
          </view>
          <text class="action-name">{{ action.name }}</text>
        </view>
      </view>
    </view>

    <!-- 待办事项 -->
    <view class="todo-section">
      <view class="section-header">
        <text class="section-title">待办事项</text>
        <text class="section-subtitle">{{ pendingTodos.length }} 项待处理</text>
      </view>
      <view class="todo-list">
        <view class="todo-item" v-for="(todo, index) in pendingTodos" :key="index" @tap="handleTodoItem(todo)">
          <view class="todo-priority" :class="'priority-' + todo.priority">
            <view class="priority-dot"></view>
          </view>
          <view class="todo-content">
            <text class="todo-title">{{ todo.title }}</text>
            <text class="todo-time">{{ todo.time }}</text>
          </view>
          <wd-icon name="arrow-right" color="#999" size="16" />
        </view>
      </view>
      <view v-if="pendingTodos.length === 0" class="empty-todos">
        <wd-icon name="smile" color="#999" size="48" />
        <text class="empty-text">暂无待办事项</text>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
// 统计数据
const statsData = ref([
  { icon: "user", number: "1,234", label: "用户总数", color: "#165DFF" },
  { icon: "chart-bar", number: "856", label: "今日活跃", color: "#00B42A" },
  { icon: "calendar", number: "42", label: "待处理订单", color: "#FF7D00" },
  { icon: "warning", number: "8", label: "系统告警", color: "#F53F3F" },
]);

// 快捷入口
const quickActions = ref([
  { name: "用户管理", icon: "user", color: "#165DFF", path: "/pages/work/user/index" },
  { name: "角色管理", icon: "usergroup", color: "#00B42A", path: "/pages/work/role/index" },
  { name: "菜单管理", icon: "app", color: "#FF7D00", path: "/pages/work/menu/index" },
  { name: "部门管理", icon: "fork", color: "#FFC53D", path: "/pages/work/department/index" },
  { name: "岗位管理", icon: "user-avatar", color: "#52C41A", path: "/pages/work/job/index" },
  { name: "日志管理", icon: "link", color: "#13C2C2", path: "/pages/work/log/index" },
  { name: "系统配置", icon: "setting", color: "#722ED1", path: "/pages/work/settings/index" },
  { name: "字典管理", icon: "books", color: "#FA541C", path: "/pages/work/dictionary/index" },
  { name: "任务管理", icon: "clock", color: "#F5222D", path: "/pages/work/task/index" },
  { name: "通知公告", icon: "notification", color: "#FAAD14", path: "/pages/work/notice/index" },
  { name: "帮助中心", icon: "help", color: "#2F54EB", path: "/pages/work/help/index" },
  { name: "系统监控", icon: "dashboard", color: "#B37FEB", path: "/pages/work/monitor/index" },
]);

// 待办事项
const pendingTodos = ref([
  { title: "审核新用户注册申请", time: "2小时前", priority: "high", type: "user" },
  { title: "处理订单退款请求", time: "3小时前", priority: "medium", type: "order" },
  { title: "更新系统权限配置", time: "1天前", priority: "low", type: "config" },
  { title: "回复用户反馈", time: "2天前", priority: "medium", type: "feedback" },
]);

// 处理方法
const handleQuickAction = (action: any) => {
  uni.navigateTo({
    url: action.path,
  });
};

const handleTodoItem = (todo: any) => {
  uni.showToast({
    title: `处理：${todo.title}`,
    icon: "none",
  });
};

// 加载数据
const loadWorkbenchData = async () => {
  // 这里可以添加实际的API调用
  console.log("加载工作台数据...");
};

onMounted(() => {
  loadWorkbenchData();
});
</script>

<route lang="json">
{
  "name": "work",
  "style": {
    "navigationStyle": "custom"
  },
  "layout": "tabbar",
  "meta": {
    "requireAuth": true
  }
}
</route>

<style lang="scss" scoped>
.workbench-container {
  min-height: 100vh;
  padding: 20rpx;
  background-color: #f5f5f5;
}

.stats-section {
  margin-bottom: 30rpx;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20rpx;
}

.stat-card {
  display: flex;
  align-items: center;
  padding: 30rpx;
  background: #fff;
  border-radius: 16rpx;
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.05);
}

.stat-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 60rpx;
  height: 60rpx;
  margin-right: 20rpx;
  border-radius: 12rpx;
}

.stat-content {
  flex: 1;
}

.stat-number {
  display: block;
  margin-bottom: 8rpx;
  font-size: 36rpx;
  font-weight: bold;
}

.stat-label {
  font-size: 24rpx;
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20rpx;
}

.section-title {
  font-size: 32rpx;
  font-weight: bold;
}

.section-subtitle {
  font-size: 24rpx;
}

.quick-actions-section,
.todo-section,
.recent-section {
  padding: 30rpx;
  margin-bottom: 30rpx;
  border-radius: 16rpx;
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.05);
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 30rpx;
}

.action-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20rpx 0;
}

.action-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 80rpx;
  height: 80rpx;
  margin-bottom: 16rpx;
  border-radius: 16rpx;
}

.action-name {
  font-size: 24rpx;
  text-align: center;
}

.todo-list {
  display: flex;
  flex-direction: column;
  gap: 20rpx;
}

.todo-item {
  display: flex;
  align-items: center;
  padding: 30rpx;
  border-radius: 12rpx;
}

.todo-priority {
  margin-right: 20rpx;
}

.priority-dot {
  width: 12rpx;
  height: 12rpx;
  border-radius: 50%;
}

.priority-high .priority-dot {
  background-color: #f53f3f;
}

.priority-medium .priority-dot {
  background-color: #ff7d00;
}

.priority-low .priority-dot {
  background-color: #00b42a;
}

.todo-content {
  flex: 1;
}

.todo-title {
  display: block;
  margin-bottom: 8rpx;
  font-size: 28rpx;
}

.todo-time {
  font-size: 24rpx;
}

.empty-todos {
  padding: 60rpx 0;
  text-align: center;
}

.empty-text {
  display: block;
  margin-top: 20rpx;
  font-size: 28rpx;
}

// 深色模式适配
:deep(.dark) .workbench-container {
  background-color: #1a1a1a;
}

:deep(.dark) .stat-card,
:deep(.dark) .quick-actions-section,
:deep(.dark) .todo-section {
  background-color: #2a2a2a;
}

:deep(.dark) .todo-item {
  background-color: #333;
}
</style>
