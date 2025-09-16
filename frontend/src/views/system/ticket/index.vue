<!-- 工单管理 -->
<template>
  <div class="app-container">
    <!-- 搜索区域 -->
    <div class="search-container">
      <el-form ref="queryFormRef" :model="queryFormData" :inline="true"  label-suffix=":">
        <el-form-item prop="title" label="工单标题">
          <el-input v-model="queryFormData.title" placeholder="请输入工单标题" clearable />
        </el-form-item>
        <el-form-item prop="priority" label="优先级">
          <el-select v-model="queryFormData.priority" placeholder="请选择优先级" style="width: 167.5px" clearable>
            <el-option value="low" label="低" />
            <el-option value="medium" label="中" />
            <el-option value="high" label="高" />
            <el-option value="urgent" label="紧急" />
          </el-select>
        </el-form-item>
        <el-form-item prop="status" label="状态">
          <el-select v-model="queryFormData.status" placeholder="请选择状态" style="width: 167.5px" clearable>
            <el-option value="pending" label="待处理" />
            <el-option value="progress" label="处理中" />
            <el-option value="resolved" label="已解决" />
            <el-option value="closed" label="已关闭" />
          </el-select>
        </el-form-item>
        <!-- 时间范围，收起状态下隐藏 -->
        <el-form-item v-if="isExpand" prop="start_time" label="创建时间">
          <DatePicker
            v-model="dateRange"
            @update:model-value="handleDateRangeChange"
          />
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
            <el-tooltip content="工单管理维护系统。">
              <QuestionFilled class="w-4 h-4 mx-1" />
            </el-tooltip>
            工单列表
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

      <!-- 表格区域：工单列表 -->
      <el-table ref="dataTableRef" v-loading="loading" :data="pageTableData" highlight-current-row class="data-table__content" height="450" border stripe @selection-change="handleSelectionChange">
        <template #empty>
          <el-empty :image-size="80" description="暂无数据" />
        </template>
        <el-table-column v-if="tableColumns.find(col => col.prop === 'selection')?.show" type="selection" min-width="55" align="center" />
        <el-table-column v-if="tableColumns.find(col => col.prop === 'index')?.show" fixed label="序号" min-width="60" >
          <template #default="scope">
            {{ (queryFormData.page_no - 1) * queryFormData.page_size + scope.$index + 1 }}
          </template>
        </el-table-column>
        <el-table-column v-if="tableColumns.find(col => col.prop === 'title')?.show" label="工单标题" prop="title" min-width="140" />
        <el-table-column v-if="tableColumns.find(col => col.prop === 'status')?.show" label="状态" prop="status" min-width="100">
          <template #default="scope">
            <el-tag :type="getStatusTagType(scope.row.status)">
              {{ getStatusLabel(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column v-if="tableColumns.find(col => col.prop === 'priority')?.show" label="优先级" prop="priority" min-width="80">
          <template #default="scope">
            <el-tag :type="getPriorityTagType(scope.row.priority)">
              {{ getPriorityLabel(scope.row.priority) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column v-if="tableColumns.find(col => col.prop === 'type')?.show" label="类型" prop="type" min-width="80">
          <template #default="scope">
            {{ getTypeLabel(scope.row.type) }}
          </template>
        </el-table-column>
        <el-table-column v-if="tableColumns.find(col => col.prop === 'project')?.show" label="项目" prop="project" min-width="100" />
        <el-table-column v-if="tableColumns.find(col => col.prop === 'version')?.show" label="版本" prop="version" min-width="80" />
        <el-table-column v-if="tableColumns.find(col => col.prop === 'assignee')?.show" label="指派给" prop="assignee" min-width="100">
          <template #default="scope">
            {{ scope.row.assignee?.name }}
          </template>
        </el-table-column>
        <el-table-column v-if="tableColumns.find(col => col.prop === 'reporter')?.show" label="报告人" prop="reporter" min-width="100">
          <template #default="scope">
            {{ scope.row.reporter?.name }}
          </template>
        </el-table-column>
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
          <el-descriptions-item label="工单标题" :span="2">
            {{ detailFormData.title }}
          </el-descriptions-item>
          <el-descriptions-item label="状态" :span="2">
            <el-tag :type="getStatusTagType(detailFormData.status)">
              {{ getStatusLabel(detailFormData.status) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="优先级" :span="2">
            <el-tag :type="getPriorityTagType(detailFormData.priority)">
              {{ getPriorityLabel(detailFormData.priority) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="类型" :span="2">
            {{ getTypeLabel(detailFormData.type) }}
          </el-descriptions-item>
          <el-descriptions-item label="项目" :span="2">
            {{ detailFormData.project }}
          </el-descriptions-item>
          <el-descriptions-item label="版本" :span="2">
            {{ detailFormData.version }}
          </el-descriptions-item>
          <el-descriptions-item label="指派给" :span="2">
            {{ detailFormData.assignee?.name }}
          </el-descriptions-item>
          <el-descriptions-item label="报告人" :span="2">
            {{ detailFormData.reporter?.name }}
          </el-descriptions-item>
          <el-descriptions-item label="描述" :span="4">
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
          <el-form-item label="工单标题" prop="title">
            <el-input v-model="formData.title" placeholder="请输入工单标题" :maxlength="255" />
          </el-form-item>
          <el-form-item label="优先级" prop="priority">
            <el-select v-model="formData.priority" placeholder="请选择优先级" clearable>
              <el-option value="low" label="低" />
              <el-option value="medium" label="中" />
              <el-option value="high" label="高" />
              <el-option value="urgent" label="紧急" />
            </el-select>
          </el-form-item>
          <el-form-item label="类型" prop="type">
            <el-select v-model="formData.type" placeholder="请选择类型" clearable>
              <el-option value="bug" label="缺陷" />
              <el-option value="feature" label="功能" />
              <el-option value="task" label="任务" />
            </el-select>
          </el-form-item>
          <el-form-item label="状态" prop="status">
            <el-select v-model="formData.status" placeholder="请选择状态">
              <el-option value="pending" label="待处理" />
              <el-option value="progress" label="处理中" />
              <el-option value="resolved" label="已解决" />
              <el-option value="closed" label="已关闭" />
            </el-select>
          </el-form-item>
          <el-form-item label="项目" prop="project">
            <el-input v-model="formData.project" placeholder="请输入项目名称" :maxlength="100" />
          </el-form-item>
          <el-form-item label="版本" prop="version">
            <el-input v-model="formData.version" placeholder="请输入版本号" :maxlength="50" />
          </el-form-item>
          <el-form-item label="指派给" prop="assignee_id">
            <!-- 这里应该是一个用户选择器，暂时用输入框代替 -->
            <el-input v-model.number="formData.assignee_id" placeholder="请输入指派用户ID" type="number" />
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
  name: "Ticket",
  inheritAttrs: false,
});

import TicketAPI, { TicketTable, TicketForm, TicketPageQuery } from "@/api/system/ticket";
import { ElMessageBox } from "element-plus";

const queryFormRef = ref();
const dataFormRef = ref();
const total = ref(0);
const selectIds = ref<number[]>([]);
const loading = ref(false);
const isExpand = ref(false);
const isExpandable = ref(true);

// 分页表单
const pageTableData = ref<TicketTable[]>([]);

// 表格列配置
const tableColumns = ref([
  { prop: 'selection', label: '选择框', show: true },
  { prop: 'index', label: '序号', show: true },
  { prop: 'title', label: '工单标题', show: true },
  { prop: 'status', label: '状态', show: true },
  { prop: 'priority', label: '优先级', show: true },
  { prop: 'type', label: '类型', show: true },
  { prop: 'project', label: '项目', show: true },
  { prop: 'version', label: '版本', show: true },
  { prop: 'assignee', label: '指派给', show: true },
  { prop: 'reporter', label: '报告人', show: true },
  { prop: 'created_at', label: '创建时间', show: true },
  { prop: 'updated_at', label: '更新时间', show: true },
  { prop: 'creator', label: '创建人', show: true },
  { prop: 'operation', label: '操作', show: true }
])

// 详情表单
const detailFormData = ref<TicketTable>({});

// 分页查询参数
const queryFormData = reactive<TicketPageQuery>({
  page_no: 1,
  page_size: 10,
  title: undefined,
  priority: undefined,
  status: undefined,
  start_time: undefined,
  end_time: undefined,
});

// 编辑表单
const formData = reactive<TicketForm>({
  id: undefined,
  title: '',
  priority: 'medium',
  type: 'bug',
  status: 'pending',
  description: undefined,
  assignee_id: undefined,
  reporter_id: 1, // 默认当前用户ID，实际应该从认证信息中获取
  project: undefined,
  version: undefined
})

// 弹窗状态
const dialogVisible = reactive({
  title: "",
  visible: false,
  type: 'create' as 'create' | 'update' | 'detail',
});

// 表单验证规则
const rules = reactive({
  title: [{ required: true, message: "请输入工单标题", trigger: "blur" }],
  priority: [{ required: false, message: "请选择优先级", trigger: "blur" }],
  type: [{ required: false, message: "请选择类型", trigger: "blur" }],
  status: [{ required: true, message: "请选择状态", trigger: "blur" }],
  project: [{ required: false, message: "请输入项目名称", trigger: "blur" }],
  version: [{ required: false, message: "请输入版本号", trigger: "blur" }],
});

// 日期范围临时变量
const dateRange = ref<[Date, Date] | []>([]);

// 处理日期范围变化
function handleDateRangeChange(range: [Date, Date]) {
  dateRange.value = range;
  if (range && range.length === 2) {
    queryFormData.start_time = range[0].toISOString();
    queryFormData.end_time = range[1].toISOString();
  } else {
    queryFormData.start_time = undefined;
    queryFormData.end_time = undefined;
  }
}

// 获取状态标签类型
function getStatusTagType(status: string) {
  switch (status) {
    case 'pending': return 'info';
    case 'progress': return 'warning';
    case 'resolved': return 'success';
    case 'closed': return 'danger';
    default: return 'info';
  }
}

// 获取状态标签文本
function getStatusLabel(status: string) {
  switch (status) {
    case 'pending': return '待处理';
    case 'progress': return '处理中';
    case 'resolved': return '已解决';
    case 'closed': return '已关闭';
    default: return status;
  }
}

// 获取优先级标签类型
function getPriorityTagType(priority: string) {
  switch (priority) {
    case 'low': return '';
    case 'medium': return 'warning';
    case 'high': return 'danger';
    case 'urgent': return 'danger';
    default: return '';
  }
}

// 获取优先级标签文本
function getPriorityLabel(priority: string) {
  switch (priority) {
    case 'low': return '低';
    case 'medium': return '中';
    case 'high': return '高';
    case 'urgent': return '紧急';
    default: return priority;
  }
}

// 获取类型标签文本
function getTypeLabel(type: string) {
  switch (type) {
    case 'bug': return '缺陷';
    case 'feature': return '功能';
    case 'task': return '任务';
    default: return type;
  }
}

// 列表刷新
async function handleRefresh () {
  await loadingData();
};

// 加载表格数据
async function loadingData() {
  loading.value = true;
  try {
    const response = await TicketAPI.getTicketList(queryFormData);
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
const initialFormData: TicketForm = {
  id: undefined,
  title: '',
  priority: 'medium',
  type: 'bug',
  status: 'pending',
  description: undefined,
  assignee_id: undefined,
  reporter_id: 1, // 默认当前用户ID，实际应该从认证信息中获取
  project: undefined,
  version: undefined
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
    const response = await TicketAPI.getTicketDetail(id);
    if (type === 'detail') {
      dialogVisible.title = "工单详情";
      Object.assign(detailFormData.value, response.data.data);
    } else if (type === 'update') {
      dialogVisible.title = "修改工单";
      Object.assign(formData, response.data.data);
    }
  } else {
    dialogVisible.title = "新增工单";
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
      // 根据弹窗传入的参数(deatil\create\update)判断走什么逻辑
      const id = formData.id;
      if (id) {
        try {
          await TicketAPI.updateTicket(id, { id, ...formData })
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
          await TicketAPI.createTicket(formData)
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
      await TicketAPI.deleteTicket(ids);
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
