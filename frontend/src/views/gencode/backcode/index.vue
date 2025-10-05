<template>
  <div class="app-container">
    <!-- 搜索区域 -->
    <div class="search-container">
      <el-form ref="queryRef" :model="queryFormData" :inline="true" label-suffix=":">
        <el-form-item label="表名称" prop="table_name">
          <el-input
            v-model="queryFormData.table_name"
            placeholder="请输入表名称"
            clearable
            style="width: 200px"
            @keyup.enter="handleQuery"
          />
        </el-form-item>
        <el-form-item label="表描述" prop="tableComment">
          <el-input
            v-model="queryFormData.table_comment"
            placeholder="请输入表描述"
            clearable
            style="width: 200px"
            @keyup.enter="handleQuery"
          />
        </el-form-item>
        <el-form-item label="创建时间" style="width: 308px">
          <el-date-picker
            v-model="dateRange"
            value-format="YYYY-MM-DD"
            type="daterange"
            range-separator="-"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
          ></el-date-picker>
        </el-form-item>
        <el-form-item>
          <el-button v-hasPerm="['generator:gencode:query']" type="primary" icon="search" @click="handleQuery">查询</el-button>
          <el-button v-hasPerm="['generator:gencode:query']" icon="refresh" @click="handleRefresh">重置</el-button>
        </el-form-item>
      </el-form>
    </div>

    <!-- 内容区域 -->
    <el-card shadow="hover" class="data-table">
      <template #header>
        <div class="card-header">
          <span>
              <el-tooltip content="生成代码">
                <QuestionFilled class="w-4 h-4 mx-1" />
              </el-tooltip>
              生成代码
          </span>
        </div>
      </template>

      <!-- 功能区域 -->
      <div class="data-table__toolbar">
        <div class="data-table__toolbar--actions">
          <el-row :gutter="10">
            <el-col :span="1.5">
              <el-button
                v-hasPerm="['generator:gencode:create']"
                type="primary"
                plain
                icon="Plus"
                @click="openCreateTable"
              >创建</el-button>
            </el-col>
            <el-col :span="1.5">
                <el-button
                v-hasPerm="['generator:gencode:update']"
                type="success"
                plain
                icon="Edit"
                :disabled="single"
                @click="handleEditTable"
                >修改</el-button>
              </el-col>
            <el-col :span="1.5">
              <el-button
                v-hasPerm="['generator:gencode:delete']"
                type="danger"
                plain
                icon="Delete"
                :disabled="multiple"
                @click="handleDelete"
              >删除</el-button>
            </el-col>
            <el-col :span="1.5">
              <el-button
                v-hasPerm="['generator:gencode:import']"
                type="info"
                plain
                icon="Upload"
                @click="openImportTable"
              >导入</el-button>
            </el-col>
            <el-col :span="1.5">
              <el-button
                v-hasPerm="['generator:gencode:code']"
                type="warning"
                plain
                icon="Download"
                :disabled="multiple"
                @click="handleGenTable"
              >生成</el-button>
            </el-col>
          </el-row>
        </div>
        <div class="data-table__toolbar--tools">
          <el-row :gutter="10">
            <el-col :span="1.5">
              <el-tooltip content="刷新">
                <el-button v-hasPerm="['demo:example:refresh']"  type="primary" icon="refresh" circle @click="handleRefresh"/>
              </el-tooltip>
            </el-col>
            <el-col :span="1.5">
              <el-tooltip content="列表筛选">
                <el-dropdown trigger="click">
                  <el-button type="default" icon="operation" circle v-hasPerm="['demo:example:filter']" />
                  <template #dropdown>
                    <el-dropdown-menu>
                      <el-dropdown-item v-for="column in tableColumns" :key="column.prop"
                        :command="column">
                        <el-checkbox v-model="column.show">
                          {{ column.label }}
                        </el-checkbox>
                      </el-dropdown-item>
                    </el-dropdown-menu>
                  </template>
                </el-dropdown>
              </el-tooltip>
            </el-col>
          </el-row>
        </div>
      </div>

      <el-table
        ref="dataTableRef"
        v-loading="loading"
        :data="tableList"
        highlight-current-row
        class="data-table__content"
        height="450"
        border
        stripe
        @selection-change="handleSelectionChange"
      >
        <template #empty>
          <el-empty :image-size="80" description="暂无数据" />
        </template>
        <el-table-column type="selection" align="center" width="55"></el-table-column>
        <el-table-column label="序号" type="index" min-width="55" align="center" fixed>
          <template #default="scope">
            <span>{{(queryFormData.page_no - 1) * queryFormData.page_size + scope.$index + 1}}</span>
          </template>
        </el-table-column>
        <el-table-column
          label="表名称"
          align="center"
          prop="table_name"
          :show-overflow-tooltip="true"
        />
        <el-table-column
          label="表描述"
          align="center"
          prop="tableComment"
          :show-overflow-tooltip="true"
        />
        <el-table-column
          label="实体"
          align="center"
          prop="className"
          :show-overflow-tooltip="true"
        />
        <el-table-column label="创建时间" align="center" prop="createTime" width="160" />
        <el-table-column label="更新时间" align="center" prop="updateTime" width="160" />
        <el-table-column label="操作" align="center" width="330" class-name="small-padding fixed-width">
          <template #default="scope">
            <el-tooltip content="预览" placement="top">
              <el-button v-hasPerm="['generator:gencode:query']" link type="primary" icon="View" @click="handlePreview(scope.row)"></el-button>
            </el-tooltip>
            <el-tooltip content="编辑" placement="top">
              <el-button v-hasPerm="['generator:gencode:update']" link type="primary" icon="Edit" @click="handleEditTable(scope.row)"></el-button>
            </el-tooltip>
            <el-tooltip content="删除" placement="top">
              <el-button v-hasPerm="['generator:gencode:delete']" link type="primary" icon="Delete" @click="handleDelete(scope.row)"></el-button>
            </el-tooltip>
            <el-tooltip content="同步" placement="top">
              <el-button v-hasPerm="['generator:gencode:edit']" link type="primary" icon="Refresh" @click="handleSynchDb(scope.row)"></el-button>
            </el-tooltip>
            <el-tooltip content="生成代码" placement="top">
              <el-button v-hasPerm="['generator:gencode:code']" link type="primary" icon="Download" @click="handleGenTable(scope.row)"></el-button>
            </el-tooltip>
          </template>
        </el-table-column>
      </el-table>
      
      <!-- 分页区域 -->
      <template #footer>
        <pagination 
          v-model:total="total" 
          v-model:page="queryFormData.page_no"
          v-model:limit="queryFormData.page_size" 
          @pagination="loadingData" 
        />
      </template>
    </el-card>

    <!-- 预览界面 -->
    <el-dialog v-model="preview.open" :title="preview.title" width="80%" top="5vh" append-to-body class="scrollbar">
      <el-tabs v-model="preview.activeName">
        <el-tab-pane
          v-for="(value, key) in preview.data"
          :label="key.substring(key.lastIndexOf('/')+1,key.indexOf('.jinja2'))"
          :name="key.substring(key.lastIndexOf('/')+1,key.indexOf('.jinja2'))"
          :key="value"
        >
          <el-link :underline="false" icon="DocumentCopy" @click="() => navigator.clipboard.writeText(value).then(() => copyTextSuccess())" style="float:right">&nbsp;复制</el-link>
          <pre>{{ value }}</pre>
        </el-tab-pane>
      </el-tabs>
    </el-dialog>
    <import-table ref="importRef" @ok="handleQuery" />
    <create-table ref="createRef" @ok="handleQuery" />
  </div>
</template>

<script setup lang="ts">
defineOptions({
    name: "GenCode",
    inheritAttrs: false,
});

import GencodeAPI from "@/api/generator/gencode";
import router from "@/router";
import importTable from "@/views/gencode/backcode/components/importTable.vue";
import createTable from "@/views/gencode/backcode/components/createTable.vue";
import { ElMessage, ElMessageBox } from 'element-plus';

const route = useRoute();
// 创建组件引用
const importRef = ref();
const createRef = ref();

const tableList = ref([]);
const loading = ref(true);
const ids = ref([]);
const single = ref(true);
const multiple = ref(true);
const total = ref(0);
const tableNames = ref([]);
const dateRange = ref([]);
const uniqueId = ref("");


const data = reactive({
  queryFormData: {
    page_no: 1,
    page_size: 10,
    table_name: undefined,
    table_comment: undefined
  },
  preview: {
    open: false,
    title: "代码预览",
    data: {},
    active_name: "model.py",
    activeName: "model.py" // 添加正确的 activeName 属性
  }
});

// 表格列配置
const tableColumns = ref([
    { prop: 'selection', label: '选择框', show: true },
    { prop: 'index', label: '序号', show: true },
    { prop: 'name', label: '名称', show: true },
    { prop: 'status', label: '状态', show: true },
    { prop: 'description', label: '描述', show: true },
    { prop: 'created_at', label: '创建时间', show: true },
    { prop: 'updated_at', label: '更新时间', show: true },
    { prop: 'creator', label: '创建人', show: true },
    { prop: 'operation', label: '操作', show: true }
])

const { queryFormData, preview } = toRefs(data);

onActivated(() => {
  const time = route.query.t;
  if (time != null && time != uniqueId.value) {
    uniqueId.value = time;
    queryFormData.value.page_no = Number(route.query.page_no || 1);
    dateRange.value = [];
    loadingData();
  }
})

/** 查询表集合 */
function loadingData() {
  loading.value = true;
  // 创建包含日期范围的查询参数
  const queryParams = {
    ...queryFormData.value
  };
  
  // 如果有日期范围，添加到查询参数中
  if (dateRange.value && dateRange.value.length === 2) {
    queryParams.start_time = dateRange.value[0];
    queryParams.end_time = dateRange.value[1];
  }
  
  GencodeAPI.listTable(queryParams).then(response => {
    tableList.value = response.rows;
    total.value = response.total;
    loading.value = false;
  });
}

/** 搜索按钮操作 */
function handleQuery() {
  queryFormData.value.page_no = 1;
  loadingData();
}

/** 生成代码操作 */
function handleGenTable(row) {
  const tbNames = row?.table_name || tableNames.value;
  if (!tbNames || (Array.isArray(tbNames) && tbNames.length === 0)) {
    ElMessage.error("请选择要生成的数据");
    return;
  }
  
  if (row?.genType === "1") {
    GencodeAPI.genCodeToPath(row.tableName).then(() => {
      ElMessage.success("成功生成到自定义路径：" + row.genPath);
    });
  } else {
    GencodeAPI.batchGenCode(tbNames).then(response => {
      const blob = new Blob([response], { type: 'application/zip' });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = 'code.zip';
      link.click();
      window.URL.revokeObjectURL(url);
    });
  }
}

/** 同步数据库操作 */
function handleSynchDb(row) {
  const tableName = row.table_name;
  ElMessageBox.confirm(
    '确认要强制同步"' + tableName + '"表结构吗？',
    '确认操作',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(() => {
    return GencodeAPI.syncDb(tableName);
  }).then(() => {
    ElMessage.success("同步成功");
  }).catch(() => {});
}

/** 打开导入表弹窗 */
function openImportTable() {
  if (importRef.value && typeof importRef.value.show === 'function') {
    importRef.value.show();
  }
}

/** 打开创建表弹窗 */
function openCreateTable() {
  if (createRef.value && typeof createRef.value.show === 'function') {
    createRef.value.show();
  }
}

/** 重置按钮操作 */
function handleRefresh() {
  dateRange.value = [];
  // 手动重置表单
  queryFormData.value = {
    page_no: 1,
    page_size: 10,
    table_name: undefined,
    table_comment: undefined
  };
  handleQuery();
}

/** 预览按钮 */
function handlePreview(row) {
  GencodeAPI.previewTable(row.tableId).then(response => {
    preview.value.data = response.data;
    preview.value.open = true;
    preview.value.activeName = "do.py";
  });
}

/** 复制代码成功 */
function copyTextSuccess() {
  ElMessage.success("复制成功");
}

// 多选框选中数据
function handleSelectionChange(selection) {
  ids.value = selection.map(item => item.tableId);
  tableNames.value = selection.map(item => item.table_name);
  single.value = selection.length != 1;
  multiple.value = !selection.length;
}

/** 修改按钮操作 */
function handleEditTable(row) {
  const tableId = row.tableId || ids.value[0];
  router.push({ path: "/tool/gen-edit/index/" + tableId, query: { page_no: queryFormData.value.page_no } });
}

/** 删除按钮操作 */
function handleDelete(row) {
  const tableIds = row?.tableId ? [row.tableId] : ids.value;
  ElMessageBox.confirm(
    '是否确认删除表编号为"' + tableIds + '"的数据项？',
    '删除确认',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(() => {
    return GencodeAPI.deleteTable(tableIds);
  }).then(() => {
    loadingData();
    ElMessage.success("删除成功");
  }).catch(() => {});
}

loadingData();
</script>
