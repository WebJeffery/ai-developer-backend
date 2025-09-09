<template>
  <div class="app-container">
    <!-- 搜索区域 -->
    <div class="search-container">
      <el-form ref="queryFormRef" :model="queryFormData" :inline="true" label-suffix=":">
        <el-form-item prop="keyword" label="关键词">
          <el-input v-model="queryFormData.keyword" placeholder="请输入文件名或关键词" clearable />
        </el-form-item>
        <el-form-item prop="file_type" label="文件类型">
          <el-select v-model="queryFormData.file_type" placeholder="请选择" style="width: 167.5px" clearable>
            <el-option label="图片" value="image" />
            <el-option label="文档" value="document" />
            <el-option label="视频" value="video" />
            <el-option label="音频" value="audio" />
            <el-option label="其他" value="other" />
          </el-select>
        </el-form-item>
        <el-form-item prop="min_size" label="文件大小">
          <el-input-number
            v-model="queryFormData.min_size"
            placeholder="最小"
            :min="0"
            controls-position="right"
            style="width: 120px"
          />
          <span style="margin: 0 8px">-</span>
          <el-input-number
            v-model="queryFormData.max_size"
            placeholder="最大"
            :min="0"
            controls-position="right"
            style="width: 120px"
          />
        </el-form-item>
        <el-form-item class="search-buttons">
          <el-button type="primary" icon="search" @click="handleQuery">查询</el-button>
          <el-button icon="refresh" @click="handleResetQuery">重置</el-button>
        </el-form-item>
      </el-form>
    </div>

    <!-- 内容区域 -->
    <el-card shadow="hover" class="data-table">
      <template #header>
        <div class="card-header">
          <span>
            <el-tooltip content="资源文件管理系统">
              <QuestionFilled class="w-4 h-4 mx-1" />
            </el-tooltip>
            文件列表
          </span>
        </div>
      </template>

      <!-- 功能区域 -->
      <div class="data-table__toolbar">
        <div class="data-table__toolbar--actions">
          <el-button type="success" icon="plus" @click="handleUpload">上传文件</el-button>
          <el-button type="primary" icon="folder-add" @click="handleCreateDir">新建文件夹</el-button>
          <el-button type="danger" icon="delete" :disabled="selectedItems.length === 0" @click="handleBatchDelete">批量删除</el-button>
        </div>
        <div class="data-table__toolbar--tools">
          <el-checkbox v-model="showHiddenFiles" @change="handleShowHiddenChange">
          显示隐藏文件
        </el-checkbox>
        <el-button-group>
          <el-button
            :type="viewMode === 'list' ? 'primary' : ''"
            @click="viewMode = 'list'"
          >
            <el-icon><List /></el-icon>
          </el-button>
          <el-button
            :type="viewMode === 'grid' ? 'primary' : ''"
            @click="viewMode = 'grid'"
          >
            <el-icon><Grid /></el-icon>
          </el-button>
        </el-button-group>
          <el-tooltip content="刷新">
            <el-button type="primary" icon="refresh" circle @click="handleRefresh" />
          </el-tooltip>
        </div>
      </div>

      <!-- 资源路径 -->
      <div class="breadcrumb-section">
        <div class="breadcrumb-container">
          <div class="breadcrumb-header">
            <el-tooltip content="点击路径可以快速返回上级目录">
              <el-icon class="breadcrumb-icon"><QuestionFilled /></el-icon>
            </el-tooltip>
            <span class="breadcrumb-label">当前路径：</span>
          </div>
          <el-breadcrumb separator="/">
            <el-breadcrumb-item
              v-for="(item, index) in breadcrumbList"
              :key="index"
              @click="handleBreadcrumbClick(item, index)"
              :class="{ 'is-link': index < breadcrumbList.length - 1 }"
            >
              {{ item.name }}
            </el-breadcrumb-item>
          </el-breadcrumb>
      </div>
    </div>

      <!-- 表格区域 -->
      <el-table
        v-if="viewMode === 'list'"
        ref="dataTableRef"
        v-loading="loading"
        :data="fileList"
        row-key="path"
        class="data-table__content"
        height="540"
        border
        stripe
        @selection-change="handleSelectionChange"
      >
        <template #empty>
          <el-empty :image-size="80" description="暂无数据" />
        </template>
        <el-table-column type="selection" min-width="55" align="center" />
        <el-table-column type="index" fixed label="序号" min-width="60" />
        <el-table-column label="名称" prop="name" min-width="200">
          <template #default="{ row }">
            <div class="file-name">
              <el-icon class="file-icon">
                <Folder v-if="row.is_dir" />
                <Document v-else />
              </el-icon>
              <span 
                :class="{ 'file-name-clickable': !row.is_dir }"
                @click="handleFileNameClick(row)"
              >
                {{ row.name }}
              </span>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="大小" prop="size" min-width="120" align="center">
          <template #default="{ row }">
            <span v-if="!row.is_dir">{{ formatFileSize(row.size) }}</span>
          </template>
        </el-table-column>
        <el-table-column label="类型" prop="file_type" min-width="100" align="center">
          <template #default="{ row }">
            <el-tag v-if="row.file_type" size="small">{{ row.file_type }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="修改时间" prop="modified_time" min-width="180" sortable />
        <el-table-column fixed="right" label="操作" align="center" min-width="200">
          <template #default="{ row }">
            <el-button
              v-if="!row.is_dir"
              type="success"
              size="small"
              link
              icon="download"
              @click="handleDownload(row)"
            >
              下载
            </el-button>
            <el-button type="primary" size="small" link icon="edit" @click="handleRename(row)">
              重命名
            </el-button>
            <el-button type="danger" size="small" link icon="delete" @click="handleDelete(row)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 网格视图 -->
      <div v-else class="grid-view">
        <div
          v-for="item in fileList"
          :key="item.path"
          class="grid-item"
          @click="handleItemClick(item)"
        >
          <div class="item-icon">
            <el-icon v-if="item.is_dir" size="48">
              <Folder />
            </el-icon>
            <el-icon v-else size="48">
              <Document />
            </el-icon>
          </div>
          <div class="item-name">{{ item.name }}</div>
          <div class="item-size" v-if="!item.is_dir">
            {{ formatFileSize(item.size) }}
        </div>
      </div>
    </div>

      <!-- 分页区域 -->
      <template #footer>
        <pagination
          v-model:total="total"
          v-model:page="pagination.page_no"
          v-model:limit="pagination.page_size"
          @pagination="handlePagination"
        />
      </template>
    </el-card>

    <!-- 上传对话框 -->
    <el-dialog
      v-model="uploadDialogVisible"
      title="上传文件"
      width="500px"
      :before-close="handleUploadClose"
    >
      <el-upload
        ref="uploadRef"
        :auto-upload="false"
        :multiple="true"
        :file-list="uploadFileList"
        @change="handleUploadChange"
        drag
      >
        <el-icon class="el-icon--upload"><upload-filled /></el-icon>
        <div class="el-upload__text">
          将文件拖到此处，或<em>点击上传</em>
        </div>
        <template #tip>
          <div class="el-upload__tip">
            支持多文件上传，单个文件不超过100MB
          </div>
        </template>
      </el-upload>
      <template #footer>
        <el-button @click="uploadDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleUploadConfirm" :loading="uploading">
          确定上传
        </el-button>
      </template>
    </el-dialog>

    <!-- 新建文件夹对话框 -->
    <el-dialog
      v-model="createDirDialogVisible"
      title="新建文件夹"
      width="400px"
    >
      <el-form :model="createDirForm" label-width="80px">
        <el-form-item label="文件夹名" required>
          <el-input
            v-model="createDirForm.dir_name"
            placeholder="请输入文件夹名称"
            @keyup.enter="handleCreateDirConfirm"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="createDirDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleCreateDirConfirm">确定</el-button>
      </template>
    </el-dialog>

    <!-- 重命名对话框 -->
    <el-dialog
      v-model="renameDialogVisible"
      title="重命名"
      width="400px"
    >
      <el-form :model="renameForm" label-width="80px">
        <el-form-item label="新名称" required>
          <el-input
            v-model="renameForm.new_name"
            placeholder="请输入新名称"
            @keyup.enter="handleRenameConfirm"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="renameDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleRenameConfirm">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Upload,
  FolderAdd,
  Refresh,
  Search,
  RefreshLeft,
  List,
  Grid,
  Folder,
  Document,
  UploadFilled,
  QuestionFilled
} from '@element-plus/icons-vue'
import Pagination from '@/components/Pagination/index.vue'
import { ResourceAPI, type ResourceItem, type ResourceListQuery, type ResourceSearchQuery, type ResourceListResponse } from '@/api/resource/resource'
import { RESOURCE_ROOT_PATH } from '@/constants'

// 响应式数据
const loading = ref(false)
const fileList = ref<ResourceItem[]>([])
const selectedItems = ref<ResourceItem[]>([])
const currentPath = ref(RESOURCE_ROOT_PATH)
const breadcrumbList = ref([{ name: '资源根目录', path: RESOURCE_ROOT_PATH }])
const showHiddenFiles = ref(false)
const viewMode = ref<'list' | 'grid'>('list')
const total = ref(0)

// 分页
const pagination = reactive({
  page_no: 1,
  page_size: 20
})

// 搜索表单
const queryFormData = reactive<ResourceSearchQuery>({
  keyword: '',
  file_type: '',
  min_size: undefined,
  max_size: undefined
})

// 对话框状态
const uploadDialogVisible = ref(false)
const createDirDialogVisible = ref(false)
const renameDialogVisible = ref(false)
const uploading = ref(false)

// 上传相关
const uploadRef = ref()
const uploadFileList = ref<any[]>([])

// 表单数据
const createDirForm = reactive({
  dir_name: ''
})

const renameForm = reactive({
  new_name: '',
  old_path: ''
})

// 工具函数：处理路径转换
const ensureRootPath = (path: string) => {
  // 如果是HTTP URL，提取相对路径部分
  if (path.startsWith('http')) {
    const url = new URL(path)
    return url.pathname.replace('/api/v1/static', '/home/static')
  }
  
  if (path.startsWith(RESOURCE_ROOT_PATH)) {
    return path
  }
  return RESOURCE_ROOT_PATH + '/' + path.replace(/^\/+/, '')
}

// 计算属性
const currentQuery = computed(() => ({
  path: currentPath.value,
  include_hidden: showHiddenFiles.value
}))

// 方法
const loadFileList = async () => {
  try {
    loading.value = true
    const response = await ResourceAPI.getResourceList(currentQuery.value)
    
    // 根据新的 API 响应结构获取数据
    const data = response.data?.data?.items || response.data?.data
    
    if (Array.isArray(data)) {
      // 直接使用后端返回的数据结构，无需转换
      fileList.value = data.map(item => ({
        ...item,
        is_hidden: item.name.startsWith('.')
      }))
      total.value = response.data?.data?.total_files + response.data?.data?.total_dirs || fileList.value.length
    } else {
      fileList.value = []
      total.value = 0
    }
  } catch (error) {
    ElMessage.error('加载文件列表失败')
    console.error('Load file list error:', error)
    fileList.value = []
    total.value = 0
  } finally {
    loading.value = false
  }
}

const handleBreadcrumbClick = (item: any, index: number) => {
  if (index < breadcrumbList.value.length - 1) {
    currentPath.value = ensureRootPath(item.path)
    updateBreadcrumb()
    loadFileList()
  }
}

const updateBreadcrumb = () => {
  const rootPath = RESOURCE_ROOT_PATH
  let relativePath = currentPath.value
  
  // 处理HTTP URL格式的路径
  if (currentPath.value.startsWith('http')) {
    const url = new URL(currentPath.value)
    relativePath = url.pathname.replace('/api/v1/static', '/home/static')
  }
  
  relativePath = relativePath.replace(rootPath, '').replace(/^\/+/, '')
  const pathParts = relativePath ? relativePath.split('/').filter(Boolean) : []
  
  breadcrumbList.value = [
    { name: '资源根目录', path: rootPath },
    ...pathParts.map((part, index) => ({
      name: part,
      path: rootPath + '/' + pathParts.slice(0, index + 1).join('/')
    }))
  ]
}

const handleFileNameClick = (row: ResourceItem) => {
  if (row.is_dir) {
    currentPath.value = ensureRootPath(row.path)
    updateBreadcrumb()
    loadFileList()
  } else {
    // 文件预览
    handleFilePreview(row)
  }
}

const handleItemClick = (item: ResourceItem) => {
  if (item.is_dir) {
    currentPath.value = ensureRootPath(item.path)
    updateBreadcrumb()
    loadFileList()
  } else {
    // 文件预览
    handleFilePreview(item)
  }
}

// 文件预览
const handleFilePreview = (file: ResourceItem) => {
  // 使用后端返回的完整URL路径进行预览
  const previewUrl = file.path
  
  // 根据文件类型决定预览方式
  const fileExtension = file.file_extension?.toLowerCase() || ''
  
  if (['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg'].includes(fileExtension)) {
    // 图片预览
    window.open(previewUrl, '_blank')
  } else if (['.pdf'].includes(fileExtension)) {
    // PDF预览
    window.open(previewUrl, '_blank')
  } else if (['.txt', '.md', '.json', '.xml', '.html', '.css', '.js', '.ts', '.vue'].includes(fileExtension)) {
    // 文本文件预览
    window.open(previewUrl, '_blank')
  } else {
    // 其他文件直接下载
    window.open(previewUrl, '_blank')
  }
}

const handleSelectionChange = (selection: ResourceItem[]) => {
  selectedItems.value = selection
}

const handleUpload = () => {
  uploadDialogVisible.value = true
  uploadFileList.value = []
}

const handleUploadChange = (file: any, fileList: any[]) => {
  uploadFileList.value = fileList
}

const handleUploadConfirm = async () => {
  if (uploadFileList.value.length === 0) {
    ElMessage.warning('请选择要上传的文件')
    return
  }

  try {
    uploading.value = true
    const formData = new FormData()
    uploadFileList.value.forEach((file: any) => {
      formData.append('file', file.raw)
    })
    formData.append('target_path', ensureRootPath(currentPath.value))

    await ResourceAPI.uploadFile(formData)
    ElMessage.success('上传成功')
    uploadDialogVisible.value = false
    loadFileList()
  } catch (error) {
    ElMessage.error('上传失败')
    console.error('Upload error:', error)
  } finally {
    uploading.value = false
  }
}

const handleUploadClose = () => {
  uploadDialogVisible.value = false
  uploadFileList.value = []
}

const handleCreateDir = () => {
  createDirForm.dir_name = ''
  createDirDialogVisible.value = true
}

const handleCreateDirConfirm = async () => {
  if (!createDirForm.dir_name.trim()) {
    ElMessage.warning('请输入文件夹名称')
    return
  }

  try {
    await ResourceAPI.createDirectory({
      parent_path: ensureRootPath(currentPath.value),
      dir_name: createDirForm.dir_name.trim()
    })
    ElMessage.success('创建成功')
    createDirDialogVisible.value = false
    loadFileList()
  } catch (error) {
    ElMessage.error('创建失败')
    console.error('Create directory error:', error)
  }
}

const handleRefresh = () => {
  loadFileList()
}

const handleQuery = async () => {
  try {
    loading.value = true
    const response = await ResourceAPI.searchResource(queryFormData)
    
    // 根据新的 API 响应结构获取数据
    const data = response.data?.data?.items || response.data?.data
    if (Array.isArray(data)) {
      // 直接使用后端返回的数据结构，无需转换
      fileList.value = data.map(item => ({
        ...item,
        is_hidden: item.name.startsWith('.')
      }))
      total.value = response.data?.data?.total_files + response.data?.data?.total_dirs || fileList.value.length
    } else {
      console.warn('搜索 API 返回的数据不是数组类型:', data)
      fileList.value = []
      total.value = 0
    }
  } catch (error) {
    ElMessage.error('搜索失败')
    console.error('Search error:', error)
    fileList.value = []
    total.value = 0
  } finally {
    loading.value = false
  }
}

const handleResetQuery = () => {
  Object.assign(queryFormData, {
    keyword: '',
    file_type: '',
    min_size: undefined,
    max_size: undefined
  })
  loadFileList()
}

const handleShowHiddenChange = () => {
  loadFileList()
}

const handleDownload = async (item: ResourceItem) => {
  try {
    const filePath = ensureRootPath(item.path)
    const response = await ResourceAPI.downloadFile(filePath)
    const blob = response.data
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = item.name
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    window.URL.revokeObjectURL(url)
  } catch (error) {
    ElMessage.error('下载失败')
    console.error('Download error:', error)
  }
}

const handleRename = (item: ResourceItem) => {
  renameForm.old_path = ensureRootPath(item.path)
  renameForm.new_name = item.name
  renameDialogVisible.value = true
}

const handleRenameConfirm = async () => {
  if (!renameForm.new_name.trim()) {
    ElMessage.warning('请输入新名称')
    return
  }

  try {
    await ResourceAPI.renameResource({
      old_path: renameForm.old_path,
      new_name: renameForm.new_name.trim()
    })
    ElMessage.success('重命名成功')
    renameDialogVisible.value = false
    loadFileList()
  } catch (error) {
    ElMessage.error('重命名失败')
    console.error('Rename error:', error)
  }
}

const handleMove = (item: ResourceItem) => {
  // TODO: 实现移动功能
  ElMessage.info('移动功能待实现')
}


const handleDelete = async (item: ResourceItem) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除 ${item.name} 吗？`,
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    const filePath = ensureRootPath(item.path)
    await ResourceAPI.deleteResource([filePath])
    ElMessage.success('删除成功')
    loadFileList()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
      console.error('Delete error:', error)
    }
  }
}

const handleSizeChange = (size: number) => {
  pagination.page_size = size
  loadFileList()
}

const handleCurrentChange = (page: number) => {
  pagination.page_no = page
  loadFileList()
}

const handlePagination = (params: { page: number; limit: number }) => {
  pagination.page_no = params.page
  pagination.page_size = params.limit
  loadFileList()
}

const handleBatchDelete = async () => {
  if (selectedItems.value.length === 0) {
    ElMessage.warning('请选择要删除的文件')
    return
  }

  try {
    await ElMessageBox.confirm(
      `确定要删除选中的 ${selectedItems.value.length} 个文件吗？`,
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    const paths = selectedItems.value.map(item => ensureRootPath(item.path))
    await ResourceAPI.deleteResource(paths)
    ElMessage.success('删除成功')
    loadFileList()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
      console.error('Batch delete error:', error)
    }
  }
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

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleString()
}

// 生命周期
onMounted(() => {
  loadFileList()
})
</script>

<style lang="scss" scoped>
.app-container {
  .search-container {
    margin-bottom: 16px;
    padding: 20px;
    border-radius: 8px;
    // 使用系统主题颜色

    .search-buttons {
      margin-left: 16px;
    }
  }

  .data-table {
    .card-header {
      display: flex;
      align-items: center;
    }

    .breadcrumb-section {
      margin: 16px 0;
      padding: 12px 0;
      // 使用系统主题颜色

      .breadcrumb-container {
        display: flex;
        align-items: center;
        gap: 12px;

        .breadcrumb-header {
          display: flex;
          align-items: center;
          gap: 6px;
          flex-shrink: 0;

          .breadcrumb-icon {
            font-size: 14px;
          }

          .breadcrumb-label {
            font-size: 14px;
            font-weight: 500;
          }
        }
      }
    }

    .data-table__toolbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
      margin-bottom: 16px;

      .data-table__toolbar--actions {
        display: flex;
        gap: 8px;
      }

      .data-table__toolbar--tools {
      display: flex;
        align-items: center;
        gap: 16px;
      }
    }

     .data-table__content {
     .file-name {
       display: flex;
       align-items: center;
       gap: 8px;

       .file-name-clickable {
         cursor: pointer;
         color: var(--el-color-primary);
         
         &:hover {
           color: var(--el-color-primary-light-3);
           text-decoration: underline;
         }
       }
     }
   }

    .grid-view {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
      gap: 20px;
      padding: 20px;

      .grid-item {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 15px;
        // 使用系统主题颜色
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.3s;

        .item-icon {
          margin-bottom: 10px;
        }

        .item-name {
          font-size: 14px;
          text-align: center;
          word-break: break-all;
          margin-bottom: 5px;
        }

        .item-size {
          font-size: 12px;
        }
      }
    }
  }

}

:deep(.el-breadcrumb__item) {
  &.is-link {
    cursor: pointer;
    color: var(--el-color-primary);
    
    &:hover {
      color: var(--el-color-primary-light-3);
    }
  }
}
</style>
