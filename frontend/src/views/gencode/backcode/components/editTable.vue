<template>
  <el-card>
    <el-tabs v-model="activeName">
      <el-tab-pane label="基本信息" name="basic">
        <basic-info-form ref="basicInfo" :info="info" />
      </el-tab-pane>
      <el-tab-pane label="字段信息" name="columnInfo">
        <el-table ref="dragTable" :data="columns" row-key="columnId" :max-height="tableHeight">
          <el-table-column label="序号" type="index" min-width="5%"/>
          <el-table-column
            label="字段列名"
            prop="columnName"
            min-width="10%"
            :show-overflow-tooltip="true"
          />
          <el-table-column label="字段描述" min-width="10%">
            <template #default="scope">
              <el-input v-model="scope.row.columnComment"></el-input>
            </template>
          </el-table-column>
          <el-table-column
            label="物理类型"
            prop="columnType"
            min-width="10%"
            :show-overflow-tooltip="true"
          />
          <el-table-column label="Python类型" min-width="11%">
            <template #default="scope">
              <el-select v-model="scope.row.pythonType">
                <el-option label="str" value="str" />
                <el-option label="int" value="int" />
                <el-option label="float" value="float" />
                <el-option label="Decimal" value="Decimal" />
                <el-option label="date" value="date" />
                <el-option label="time" value="time" />
                <el-option label="datetime" value="datetime" />
                <el-option label="bytes" value="bytes" />
                <el-option label="dict" value="dict" />
                <el-option label="list" value="list" />
              </el-select>
            </template>
          </el-table-column>
          <el-table-column label="Python属性" min-width="10%">
            <template #default="scope">
              <el-input v-model="scope.row.pythonField"></el-input>
            </template>
          </el-table-column>

          <el-table-column label="插入" min-width="5%">
            <template #default="scope">
              <el-checkbox v-model="scope.row.isInsert" true-label="1" false-label="0"></el-checkbox>
            </template>
          </el-table-column>
          <el-table-column label="编辑" min-width="5%">
            <template #default="scope">
              <el-checkbox v-model="scope.row.isEdit" true-label="1" false-label="0"></el-checkbox>
            </template>
          </el-table-column>
          <el-table-column label="列表" min-width="5%">
            <template #default="scope">
              <el-checkbox v-model="scope.row.isList" true-label="1" false-label="0"></el-checkbox>
            </template>
          </el-table-column>
          <el-table-column label="查询" min-width="5%">
            <template #default="scope">
              <el-checkbox v-model="scope.row.isQuery" true-label="1" false-label="0"></el-checkbox>
            </template>
          </el-table-column>
          <el-table-column label="查询方式" min-width="10%">
            <template #default="scope">
              <el-select v-model="scope.row.queryType">
                <el-option label="=" value="EQ" />
                <el-option label="!=" value="NE" />
                <el-option label=">" value="GT" />
                <el-option label=">=" value="GTE" />
                <el-option label="<" value="LT" />
                <el-option label="<=" value="LTE" />
                <el-option label="LIKE" value="LIKE" />
                <el-option label="BETWEEN" value="BETWEEN" />
              </el-select>
            </template>
          </el-table-column>
          <el-table-column label="必填" min-width="5%">
            <template #default="scope">
              <el-checkbox v-model="scope.row.isRequired" true-label="1" false-label="0"></el-checkbox>
            </template>
          </el-table-column>
          <el-table-column label="唯一" min-width="5%">
            <template #default="scope">
              <el-checkbox v-model="scope.row.isUnique" true-label="1" false-label="0"></el-checkbox>
            </template>
          </el-table-column>
          <el-table-column label="显示类型" min-width="12%">
            <template #default="scope">
              <el-select v-model="scope.row.htmlType">
                <el-option label="文本框" value="input" />
                <el-option label="文本域" value="textarea" />
                <el-option label="下拉框" value="select" />
                <el-option label="单选框" value="radio" />
                <el-option label="复选框" value="checkbox" />
                <el-option label="日期控件" value="datetime" />
                <el-option label="图片上传" value="imageUpload" />
                <el-option label="文件上传" value="fileUpload" />
                <el-option label="富文本控件" value="editor" />
              </el-select>
            </template>
          </el-table-column>
          <el-table-column label="字典类型" min-width="12%">
            <template #default="scope">
              <el-select v-model="scope.row.dictType" clearable filterable placeholder="请选择">
                <el-option
                  v-for="dict in dictOptions"
                  :key="dict.dictType"
                  :label="dict.dictName"
                  :value="dict.dictType">
                  <span style="float: left">{{ dict.dictName }}</span>
                  <span style="float: right; color: #8492a6; font-size: 13px">{{ dict.dictType }}</span>
              </el-option>
              </el-select>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>
      <el-tab-pane label="生成信息" name="genInfo">
        <!-- 将GenTableSchema类型转换为GenInfo类型 -->
          <gen-info-form 
            ref="genInfo" 
            :info="convertToGenInfo(info)" 
            :tables="tables" 
          />
      </el-tab-pane>
    </el-tabs>
    <el-form label-width="100px">
      <div style="text-align: center;margin-left:-100px;margin-top:10px;">
        <el-button type="primary" @click="submitForm()">提交</el-button>
        <el-button @click="close()">返回</el-button>
      </div>
    </el-form>
  </el-card>
</template>

<script setup lang="ts" name="GenEdit">
import GencodeAPI from "@/api/generator/gencode";
import DictAPI from "@/api/system/dict";
import { ElMessage } from 'element-plus';
import router from '@/router';
import type { GenTableSchema, GenTableDetailResult } from '@/api/generator/gencode';

const route = useRoute();
const basicInfoRef = ref();
const genInfoRef = ref();

const activeName = ref("columnInfo");
const tableHeight = ref(document.documentElement.scrollHeight - 245 + "px");
const tables = ref<Array<any>>([]);
const columns = ref<Array<any>>([]);
const dictOptions = ref<Array<any>>([]);
const info = ref<GenTableSchema>({} as GenTableSchema);

/**
 * 将对象转换为GenInfo类型
 */
function convertToGenInfo(tableSchema: any): any {
  if (!tableSchema) {
    return {};
  }
  return {
    tplCategory: tableSchema.tpl_category,
    tplWebType: tableSchema.tpl_web_type,
    packageName: tableSchema.package_name,
    moduleName: tableSchema.module_name,
    businessName: tableSchema.business_name,
    functionName: tableSchema.function_name,
    genType: tableSchema.gen_type,
    parentMenuId: tableSchema.parent_menu_id,
    genPath: tableSchema.gen_path,
    subTableName: tableSchema.sub_table_name,
    subTableFkName: tableSchema.sub_table_fk_name,
    treeCode: tableSchema.tree_code,
    treeParentCode: tableSchema.tree_parent_code,
    treeName: tableSchema.tree_name
  };
}

/** 提交按钮 */
function submitForm() {
  // 简化表单验证逻辑
  const genTable = Object.assign({}, info.value);
  genTable.columns = columns.value;
  genTable.tree_code = info.value.tree_code;
  genTable.tree_name = info.value.tree_name;
  genTable.tree_parent_code = info.value.tree_parent_code;
  genTable.parent_menu_id = info.value.parent_menu_id;
  
  // 确保id存在且为number类型
  if (info.value && info.value.id !== undefined) {
    GencodeAPI.updateGenTable(Number(info.value.id), genTable).then((res: any) => {
      ElMessage.success(res.data.message || "更新成功");
      if (res.data.code === 200) {
        close();
      }
    });
  } else {
    ElMessage.error("表ID不存在，无法更新");
  }
}

function close() {
  const pageNum = route.query.page_no || route.query.pageNum;
  router.push({ path: "/tool/gen", query: { t: Date.now(), page_no: pageNum } });
}

(() => {
  const tableId = route.params && route.params.tableId;
  if (tableId) {
    // 获取表详细信息
    GencodeAPI.getGenTableDetail(Number(tableId)).then(res => {
      if (res.data && res.data.data) {
        columns.value = res.data.data.rows || [];
        // 确保info包含所有必要的字段，特别是columns
        const tableInfo = res.data.data.info || {};
        info.value = {
          ...tableInfo,
          columns: columns.value
        };
        tables.value = res.data.data.tables || [];
      }
    });
    /** 查询字典下拉列表 */
    DictAPI.getDictTypeOptionselect().then((response: any) => {
      dictOptions.value = response.data.data || [];
    });
  }
})();
</script>
