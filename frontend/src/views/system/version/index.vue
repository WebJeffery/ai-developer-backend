<!-- 版本管理 -->
<template>
  <div class="app-container">
    <!-- 搜索区域 -->
    <div class="search-container">
      <el-form ref="queryFormRef" :model="queryFormData" :inline="true" label-suffix=":">
        <el-form-item prop="title" label="版本标题">
          <el-input v-model="queryFormData.title" placeholder="请输入版本标题" clearable />
        </el-form-item>
        <el-form-item prop="status" label="状态">
          <el-select v-model="queryFormData.status" placeholder="请选择状态" style="width: 167.5px" clearable>
            <el-option value="draft" label="草稿" />
            <el-option value="released" label="已发布" />
            <el-option value="archived" label="已归档" />
          </el-select>
        </el-form-item>
        <!-- 时间范围，收起状态下隐藏 -->
        <el-form-item v-if="isExpand" prop="start_time" label="创建时间">
          <DatePicker v-model="dateRange" @update:model-value="handleDateRangeChange" />
        </el-form-item>
        <!-- 查询、重置、展开/收起按钮 -->
        <el-form-item class="search-buttons">
          <el-button type="primary" icon="search" @click="handleQuery">
            查询
          </el-button>
          <el-button icon="refresh" @click="handleResetQuery">
            重置
          </el-button>
          <!-- 展开/收起 -->
          <template v-if="isExpandable">
            <el-link class="ml-3" type="primary" underline="never" @click="isExpand = !isExpand">
              {{ isExpand ? "收起" : "展开" }}
              <el-icon>
                <template v-if="isExpand">
                  <ArrowUp />
                </template>
                <template v-else>
                  <ArrowDown />
                </template>
              </el-icon>
            </el-link>
          </template>
        </el-form-item>
      </el-form>
    </div>

    <!-- 内容区域 -->
    <el-card shadow="hover" class="data-table">
      <template #header>
        <div class="card-header">
          <span>
            <el-tooltip content="版本管理维护系统的版本信息。">
              <QuestionFilled class="w-4 h-4 mx-1" />
            </el-tooltip>
            版本列表
          </span>
        </div>
      </template>

      <!-- 功能区域 -->
      <div class="data-table__toolbar">
        <div class="data-table__toolbar--actions">
          <el-button type="success" icon="plus" @click="handleOpenDialog('create')">新增</el-button>
          <el-button type="danger" icon="delete" :disabled="selectIds.length === 0" @click="handleDelete(selectIds)">批量删除</el-button>
        </div>
        <div class="data-table__toolbar--tools">
          <el-tooltip content="刷新">
            <el-button type="primary" icon="refresh" circle @click="handleRefresh" />
          </el-tooltip>
          <el-tooltip content="列表筛选">
            <el-dropdown trigger="click">
              <el-button type="default" icon="operation" circle />
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item v-for="column in tableColumns" :key="column.prop" :command="column">
                    <el-checkbox v-model="column.show">
                      {{ column.label }}
                    </el-checkbox>
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </el-tooltip>
        </div>
      </div>

      <!-- 表格区域：版本列表 -->
      <el-table ref="dataTableRef" v-loading="loading" :data="pageTableData" highlight-current-row class="data-table__content" height="450" border stripe @selection-change="handleSelectionChange">
        <template #empty>
          <el-empty :image-size="80" description="暂无数据" />
        </template>
        <el-table-column v-if="tableColumns.find(col => col.prop === 'selection')?.show" type="selection" min-width="55" align="center" />
        <el-table-column v-if="tableColumns.find(col => col.prop === 'index')?.show" fixed label="序号" min-width="60">
          <template #default="scope">
            {{ (queryFormData.page_no - 1) * queryFormData.page_size + scope.$index + 1 }}
          </template>
        </el-table-column>
        <el-table-column v-if="tableColumns.find(col => col.prop === 'version_number')?.show" label="版本号" prop="version_number" min-width="100" />
        <el-table-column v-if="tableColumns.find(col => col.prop === 'title')?.show" label="版本标题" prop="title" min-width="140" />
        <el-table-column v-if="tableColumns.find(col => col.prop === 'status')?.show" label="状态" prop="status" min-width="100">
          <template #default="scope">
            <el-tag :type="getStatusTagType(scope.row.status)">
              {{ getStatusLabel(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column v-if="tableColumns.find(col => col.prop === 'project')?.show" label="所属项目" prop="project" min-width="120" />
        <el-table-column v-if="tableColumns.find(col => col.prop === 'release_notes')?.show" label="发布说明" prop="release_notes" min-width="200" show-overflow-tooltip />
        <el-table-column v-if="tableColumns.find(col => col.prop === 'released_at')?.show" label="发布时间" prop="released_at" min-width="180" sortable />
        <el-table-column v-if="tableColumns.find(col => col.prop === 'created_at')?.show" label="创建时间" prop="created_at" min-width="180" sortable />
        <el-table-column v-if="tableColumns.find(col => col.prop === 'updated_at')?.show" label="更新时间" prop="updated_at" min-width="180" sortable />
        <el-table-column v-if="tableColumns.find(col => col.prop === 'creator')?.show" key="creator" label="创建人" min-width="100">
          <template #default="scope">
            {{ scope.row.creator?.name }}
          </template>
        </el-table-column>

        <el-table-column v-if="tableColumns.find(col => col.prop === 'operation')?.show" fixed="right" label="操作" align="center" min-width="200">
          <template #default="scope">
            <el-button type="info" size="small" link icon="document" @click="handleOpenDialog('detail', scope.row.id)">详情</el-button>
            <el-button type="primary" size="small" link icon="edit" @click="handleOpenDialog('update', scope.row.id)">编辑</el-button>
            <el-button type="danger" size="small" link icon="delete" @click="handleDelete([scope.row.id])">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页区域 -->
      <template #footer>
        <pagination v-model:total="total" v-model:page="queryFormData.page_no" v-model:limit="queryFormData.page_size" @pagination="loadingData" />
      </template>
    </el-card>

    <!-- 弹窗区域 -->
    <el-dialog v-model="dialogVisible.visible" :title="dialogVisible.title" @close="handleCloseDialog">
      <!-- 详情 -->
      <template v-if="dialogVisible.type === 'detail'">
        <el-descriptions :column="4" border>
          <el-descriptions-item label="版本号" :span="2">
            {{ detailFormData.version_number }}
          </el-descriptions-item>
          <el-descriptions-item label="版本标题" :span="2">
            {{ detailFormData.title }}
          </el-descriptions-item>
          <el-descriptions-item label="状态" :span="2">
            <el-tag :type="getStatusTagType(detailFormData.status)">
              {{ getStatusLabel(detailFormData.status) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="所属项目" :span="2">
            {{ detailFormData.project }}
          </el-descriptions-item>
          <el-descriptions-item label="发布说明" :span="4">
            {{ detailFormData.release_notes }}
          </el-descriptions-item>
          <el-descriptions-item label="发布时间" :span="2">
            {{ detailFormData.released_at }}
          </el-descriptions-item>
          <el-descriptions-item label="描述" :span="2">
            {{ detailFormData.description }}
          </el-descriptions-item>
          <el-descriptions-item label="创建人" :span="2">
            {{ detailFormData.creator?.name }}
          </el-descriptions-item>
          <el-descriptions-item label="创建时间" :span="2">
            {{ detailFormData.created_at }}
          </el-descriptions-item>
          <el-descriptions-item label="更新时间" :span="2">
            {{ detailFormData.updated_at }}
          </el-descriptions-item>
        </el-descriptions>
      </template>
      <!-- 新增、编辑表单 -->
      <template v-else>
        <el-form ref="dataFormRef" :model="formData" :rules="rules" label-suffix=":" label-width="auto" label-position="right">
          <el-form-item label="版本号" prop="version_number">
            <el-input v-model="formData.version_number" placeholder="请输入版本号" :maxlength="50" />
          </el-form-item>
          <el-form-item label="版本标题" prop="title">
            <el-input v-model="formData.title" placeholder="请输入版本标题" :maxlength="255" />
          </el-form-item>
          <el-form-item label="状态" prop="status">
            <el-select v-model="formData.status" placeholder="请选择状态">
              <el-option value="draft" label="草稿" />
              <el-option value="released" label="已发布" />
              <el-option value="archived" label="已归档" />
            </el-select>
          </el-form-item>
          <el-form-item label="所属项目" prop="project">
            <el-input v-model="formData.project" placeholder="请输入所属项目" :maxlength="100" />
          </el-form-item>
          <el-form-item label="发布说明" prop="release_notes">
            <el-input v-model="formData.release_notes" :rows="4" type="textarea" placeholder="请输入发布说明" />
          </el-form-item>
          <el-form-item label="发布时间" prop="released_at">
            <el-date-picker v-model="formData.released_at" type="datetime" placeholder="请选择发布时间" format="YYYY-MM-DD HH:mm:ss" value-format="YYYY-MM-DD HH:mm:ss" />
          </el-form-item>
          <el-form-item label="描述" prop="description">
            <el-input v-model="formData.description" :rows="4" :maxlength="500" show-word-limit type="textarea" placeholder="请输入描述" />
          </el-form-item>
        </el-form>
      </template>

      <template #footer>
        <div class="dialog-footer">
          <!-- 详情弹窗不需要确定按钮的提交逻辑 -->
          <el-button @click="handleCloseDialog">取消</el-button>
          <el-button v-if="dialogVisible.type !== 'detail'" type="primary" @click="handleSubmit">确定</el-button>
          <el-button v-else type="primary" @click="handleCloseDialog">确定</el-button>
        </div>
      </template>
    </el-dialog>

  </div>
</template>

<script setup lang="ts">
defineOptions({
  name: "Version",
  inheritAttrs: false,
});

import VersionAPI, { VersionTable, VersionForm, VersionPageQuery } from "@/api/system/version";
import { ElMessageBox } from "element-plus";

const queryFormRef = ref();
const dataFormRef = ref();
const total = ref(0);
const selectIds = ref<number[]>([]);
const loading = ref(false);
const isExpand = ref(false);
const isExpandable = ref(true);

// 分页表单
const pageTableData = ref<VersionTable[]>([]);

// 表格列配置
const tableColumns = ref([
  { prop: 'selection', label: '选择框', show: true },
  { prop: 'index', label: '序号', show: true },
  { prop: 'version_number', label: '版本号', show: true },
  { prop: 'title', label: '版本标题', show: true },
  { prop: 'status', label: '状态', show: true },
  { prop: 'project', label: '所属项目', show: true },
  { prop: 'release_notes', label: '发布说明', show: true },
  { prop: 'released_at', label: '发布时间', show: true },
  { prop: 'created_at', label: '创建时间', show: true },
  { prop: 'updated_at', label: '更新时间', show: true },
  { prop: 'creator', label: '创建人', show: true },
  { prop: 'operation', label: '操作', show: true }
])

// 详情表单
const detailFormData = ref<VersionTable>({});

// 分页查询参数
const queryFormData = reactive<VersionPageQuery>({
  page_no: 1,
  page_size: 10,
  title: undefined,
  status: undefined,
  start_time: undefined,
  end_time: undefined,
});

// 编辑表单
const formData = reactive<VersionForm>({
  id: undefined,
  version_number: '',
  title: '',
  release_notes: undefined,
  project: undefined,
  status: 'draft',
  released_at: undefined,
  description: undefined,
})

// 弹窗状态
const dialogVisible = reactive({
  title: "",
  visible: false,
  type: 'create' as 'create' | 'update' | 'detail',
});

// 表单验证规则
const rules = reactive({
  version_number: [{ required: true, message: "请输入版本号", trigger: "blur" }],
  title: [{ required: true, message: "请输入版本标题", trigger: "blur" }],
  // status字段在后端有默认值'draft'，因此不是必填项
});

// 日期范围临时变量
const dateRange = ref<[Date, Date] | []>([]);

// 处理日期范围变化
function handleDateRangeChange(range: [Date, Date]) {
  dateRange.value = range;
  if (range && range.length === 2) {
    queryFormData.start_time = range[0]?.toISOString();
    queryFormData.end_time = range[1]?.toISOString();
  } else {
    queryFormData.start_time = undefined;
    queryFormData.end_time = undefined;
  }
}

// 获取状态标签类型
function getStatusTagType(status: string | undefined) {
  switch (status) {
    case 'draft': return 'info';
    case 'released': return 'success';
    case 'archived': return 'warning';
    default: return 'info';
  }
}

// 获取状态标签文本
function getStatusLabel(status: string | undefined) {
  switch (status) {
    case 'draft': return '草稿';
    case 'released': return '已发布';
    case 'archived': return '已归档';
    default: return status || '';
  }
}

// 列表刷新
async function handleRefresh() {
  await loadingData();
};

// 加载表格数据
async function loadingData() {
  loading.value = true;
  try {
    const response = await VersionAPI.getVersionList(queryFormData);
    pageTableData.value = response.data.data.items;
    total.value = response.data.data.total;
  }
  catch (error: any) {
    console.error(error);
  }
  finally {
    loading.value = false;
  }
}

// 查询（重置页码后获取数据）
async function handleQuery() {
  queryFormData.page_no = 1;
  loadingData();
}

// 重置查询
async function handleResetQuery() {
  queryFormRef.value.resetFields();
  queryFormData.page_no = 1;
  dateRange.value = [];
  queryFormData.start_time = undefined;
  queryFormData.end_time = undefined;
  loadingData();
}

// 定义初始表单数据常量
const initialFormData: VersionForm = {
  id: undefined,
  version_number: '',
  title: '',
  release_notes: undefined,
  project: undefined,
  status: 'draft',
  released_at: undefined,
  description: undefined,
}

// 重置表单
async function resetForm() {
  if (dataFormRef.value) {
    dataFormRef.value.resetFields();
    dataFormRef.value.clearValidate();
  }
  // 完全重置 formData 为初始状态
  Object.assign(formData, initialFormData);
}

// 行复选框选中项变化
async function handleSelectionChange(selection: any) {
  selectIds.value = selection.map((item: any) => item.id);
}

// 关闭弹窗
async function handleCloseDialog() {
  dialogVisible.visible = false;
  resetForm();
}

// 打开弹窗
async function handleOpenDialog(type: 'create' | 'update' | 'detail', id?: number) {
  dialogVisible.type = type;
  if (id) {
    const response = await VersionAPI.getVersionDetail(id);
    if (type === 'detail') {
      dialogVisible.title = "版本详情";
      Object.assign(detailFormData.value, response.data.data);
    } else if (type === 'update') {
      dialogVisible.title = "修改版本";
      Object.assign(formData, response.data.data);
    }
  } else {
    dialogVisible.title = "新增版本";
    formData.id = undefined;
  }
  dialogVisible.visible = true;
}

// 提交表单（防抖）
async function handleSubmit() {
  // 表单校验
  dataFormRef.value.validate(async (valid: any) => {
    if (valid) {
      loading.value = true;
      // 根据弹窗传入的参数(detail\create\update)判断走什么逻辑
      const id = formData.id;
      if (id) {
        try {
          await VersionAPI.updateVersion(id, { id, ...formData })
          dialogVisible.visible = false;
          resetForm();
          handleCloseDialog();
          handleResetQuery();
        } catch (error: any) {
          console.error(error);
        } finally {
          loading.value = false;
        }
      } else {
        try {
          await VersionAPI.createVersion(formData)
          dialogVisible.visible = false;
          resetForm();
          handleCloseDialog();
          handleResetQuery();
        } catch (error: any) {
          console.error(error);
        } finally {
          loading.value = false;
        }
      }
    }
  });
}

// 删除、批量删除
async function handleDelete(ids: number[]) {
  ElMessageBox.confirm("确认删除该项数据?", "警告", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  }).then(async () => {
    try {
      loading.value = true;
      await VersionAPI.deleteVersion(ids);
      handleResetQuery();
    } catch (error: any) {
      console.error(error);
    } finally {
      loading.value = false;
    }
  }).catch(() => {
    ElMessageBox.close();
  });
}


onMounted(async () => {
  // 加载表格数据
  loadingData();
});
</script>

<style lang="scss" scoped></style>
