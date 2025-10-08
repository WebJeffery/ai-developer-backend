<template>
  <!-- 导入表 -->
  <el-dialog v-model="visible" title="导入表"  width="800px" top="5vh" append-to-body>
    <el-form ref="queryRef" :model="queryFormData" :inline="true">
      <el-form-item label="表名称" prop="tableName">
        <el-input
          v-model="queryFormData.table_name"
          placeholder="请输入表名称"
          clearable
          style="width: 180px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="表描述" prop="tableComment">
        <el-input
          v-model="queryFormData.table_comment"
          placeholder="请输入表描述"
          clearable
          style="width: 180px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="Search" @click="handleQuery">搜索</el-button>
        <el-button icon="Refresh" @click="resetQuery">重置</el-button>
      </el-form-item>
    </el-form>
    <el-row>
      <el-table  ref="table" :data="dbTableList" height="300px" @row-click="clickRow" @selection-change="handleSelectionChange">
        <template #empty>
          <el-empty :image-size="80" description="暂无数据" />
        </template>
        <el-table-column type="selection" width="55"></el-table-column>
        <el-table-column label="序号" type="index" min-width="55" align="center" fixed>
          <template #default="scope">
            <span>{{(queryFormData.page_no - 1) * queryFormData.page_size + scope.$index + 1}}</span>
          </template>
        </el-table-column>
        <el-table-column prop="database_name" label="数据库名称" :show-overflow-tooltip="true"></el-table-column>
        <el-table-column prop="table_name" label="表名称" :show-overflow-tooltip="true"></el-table-column>
        <el-table-column prop="table_comment" label="表描述" :show-overflow-tooltip="true"></el-table-column>
        <el-table-column prop="table_type" label="表类型"></el-table-column>
      </el-table>
      <pagination
        v-model:page="queryFormData.page_no"
        v-model:limit="queryFormData.page_size"
        :total="total"
        @pagination="getList"
      />
    </el-row>
    <template #footer>
      <div class="dialog-footer">
        <el-button type="primary" @click="handleImportTable">确 定</el-button>
        <el-button @click="visible = false">取 消</el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import GencodeAPI from "@/api/generator/gencode";
import { ElMessage } from 'element-plus';

const total = ref(0);
const visible = ref(false);
const tables = ref<Array<string>>([]);
const dbTableList = ref<Array<any>>([]);
const queryRef = ref();
const table = ref();

const queryFormData = reactive({
  page_no: 1,
  page_size: 10,
  table_name: undefined,
  table_comment: undefined
});

const emit = defineEmits(["ok"]);

/** 查询参数列表 */
function show() {
  getList();
  visible.value = true;
}

/** 单击选择行 */
function clickRow(row: any) {
  table.value?.toggleRowSelection(row);
}

/** 多选框选中数据 */
function handleSelectionChange(selection: Array<any>) {
  tables.value = selection.map(item => item.table_name);
}

/** 查询表数据 */
function getList() {
  GencodeAPI.listDbTable(queryFormData).then(res => {
    console.log(res.data);
    dbTableList.value = res.data.data.items;
    total.value = res.data.data.total;
  });
}

/** 搜索按钮操作 */
function handleQuery() {
  queryFormData.page_no = 1;
  getList();
}

/** 重置按钮操作 */
function resetQuery() {
  if (queryRef.value) {
    queryRef.value.resetFields();
  }
  handleQuery();
}

/** 导入按钮操作 */
function handleImportTable() {
  const tableNames = tables.value.join(",");
  if (tableNames == "") {
    ElMessage.error("请选择要导入的表");
    return;
  }
  // 传递逗号分隔的字符串格式
  GencodeAPI.importTable(tableNames.split(",")).then((res: any) => {
    ElMessage.success(res.data.message);
    if (res.data.code === 200) {
      visible.value = false;
      emit("ok");
    }
  });
}

defineExpose({
  show,
});
</script>
