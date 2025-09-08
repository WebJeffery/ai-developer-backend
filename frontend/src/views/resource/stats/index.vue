<template>
  <div class="app-container">
    <!-- 存储空间信息 -->
    <el-row :gutter="16" class="mb-4">
      <el-col :span="24">
        <el-card :loading="statsLoading" shadow="hover">
          <template #header>
            <div class="flex items-center gap-2">
              <el-icon><Monitor /></el-icon>
              <span class="font-medium">存储空间信息</span>
              <el-tooltip content="存储空间使用详情">
                <el-icon><QuestionFilled /></el-icon>
              </el-tooltip>
            </div>
          </template>
          <el-descriptions :column="2" border>
            <el-descriptions-item label="挂载点">{{ stats?.mount_point || '-' }}</el-descriptions-item>
            <el-descriptions-item label="总空间">{{ formatFileSize(stats?.total_space) }}</el-descriptions-item>
            <el-descriptions-item label="已使用">{{ formatFileSize(stats?.used_space) }}</el-descriptions-item>
            <el-descriptions-item label="可用空间">{{ formatFileSize(stats?.free_space) }}</el-descriptions-item>
          </el-descriptions>
          <div class="mt-4">
            <div class="mb-2">
              <span>使用率</span>
            </div>
            <el-progress 
              :percentage="Math.round(((stats?.used_space || 0) / (stats?.total_space || 1)) * 100)"
              :status="getStorageStatus(Math.round(((stats?.used_space || 0) / (stats?.total_space || 1)) * 100))"
              :text-inside="true"
              :stroke-width="16"
            />
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 基础统计信息表格 -->
    <el-row :gutter="16" class="mb-4">
      <el-col :span="24">
        <el-card :loading="statsLoading" shadow="hover">
          <template #header>
            <div class="flex items-center gap-2">
              <el-icon><DataAnalysis /></el-icon>
              <span class="font-medium">基础统计信息</span>
              <el-tooltip content="文件系统基础统计信息">
                <el-icon><QuestionFilled /></el-icon>
              </el-tooltip>
            </div>
          </template>
          <el-table :data="getBasicStatsData()" border>
            <template #empty>
              <el-empty :image-size="80" description="暂无数据" />
            </template>
            <el-table-column label="文件总数" prop="total_files" align="center" />
            <el-table-column label="文件夹数" prop="total_dirs" align="center" />
            <el-table-column label="总大小" prop="total_size" align="center" />
            <el-table-column label="已使用空间" prop="used_space" align="center" />
          </el-table>
        </el-card>
      </el-col>
    </el-row>

    <!-- 文件类型和扩展名统计 -->
    <el-row :gutter="16" class="mb-4">
      <!-- 文件类型统计 -->
      <el-col :span="12">
        <el-card :loading="statsLoading" shadow="hover">
          <template #header>
            <div class="flex items-center gap-2">
              <el-icon><DataAnalysis /></el-icon>
              <span class="font-medium">文件类型统计</span>
              <el-tooltip content="按文件类型统计文件数量">
                <el-icon><QuestionFilled /></el-icon>
              </el-tooltip>
            </div>
          </template>
          <el-table :data="getTypeStatsData()" border>
            <template #empty>
              <el-empty :image-size="80" description="暂无数据" />
            </template>
            <el-table-column label="文件类型" prop="type" />
            <el-table-column label="数量" prop="count" align="center" width="100" />
          </el-table>
        </el-card>
      </el-col>

      <!-- 文件扩展名统计 -->
      <el-col :span="12">
        <el-card :loading="statsLoading" shadow="hover">
          <template #header>
            <div class="flex items-center gap-2">
              <el-icon><PieChart /></el-icon>
              <span class="font-medium">文件扩展名统计</span>
              <el-tooltip content="按文件扩展名统计文件数量">
                <el-icon><QuestionFilled /></el-icon>
              </el-tooltip>
            </div>
          </template>
          <el-table :data="getExtensionStatsData()" border>
            <template #empty>
              <el-empty :image-size="80" description="暂无数据" />
            </template>
            <el-table-column label="扩展名" prop="extension" />
            <el-table-column label="数量" prop="count" align="center" width="100" />
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import {
  Document,
  Folder,
  DataAnalysis,
  PieChart,
  Monitor,
  QuestionFilled
} from '@element-plus/icons-vue'
import { ResourceAPI, type ResourceStats } from '@/api/resource/resource'

// 响应式数据
const stats = ref<ResourceStats | null>(null)
const statsLoading = ref(false)

// 方法
const loadStats = async () => {
  try {
    statsLoading.value = true
    const response = await ResourceAPI.getResourceStats()
    stats.value = response.data.data
  } catch (error) {
    ElMessage.error('获取统计信息失败')
    console.error('Load stats error:', error)
  } finally {
    statsLoading.value = false
  }
}

// 数据处理函数
const getBasicStatsData = () => {
  if (!stats.value) return []
  return [
    {
      total_files: stats.value.total_files || 0,
      total_dirs: stats.value.total_dirs || 0,
      total_size: formatFileSize(stats.value.total_size),
      used_space: formatFileSize(stats.value.used_space)
    }
  ]
}

const getTypeStatsData = () => {
  if (!stats.value?.type_stats) return []
  return Object.entries(stats.value.type_stats).map(([type, count]) => ({
    type,
    count
  }))
}

const getExtensionStatsData = () => {
  if (!stats.value?.extension_stats) return []
  return Object.entries(stats.value.extension_stats).map(([extension, count]) => ({
    extension,
    count
  }))
}

// 工具函数
const formatFileSize = (size?: number | null) => {
  if (!size || size === null) return '-'
  const units = ['B', 'KB', 'MB', 'GB', 'TB']
  let unitIndex = 0
  let fileSize = size

  while (fileSize >= 1024 && unitIndex < units.length - 1) {
    fileSize /= 1024
    unitIndex++
  }

  return `${fileSize.toFixed(1)} ${units[unitIndex]}`
}

// 存储空间使用率状态计算
const getStorageStatus = (percentage: number) => {
  if (percentage > 80) return 'exception'
  if (percentage > 60) return 'warning'
  return 'success'
}

// 生命周期
onMounted(() => {
  loadStats()
})
</script>

<style lang="scss" scoped></style>
