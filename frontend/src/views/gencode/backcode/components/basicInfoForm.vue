<template>
  <el-form ref="basicInfoForm" :model="info" :rules="rules" label-width="150px">
    <el-row>
      <el-col :span="12">
        <el-form-item label="表名称" prop="tableName">
          <el-input v-model="info.table_name" placeholder="请输入仓库名称"/>
        </el-form-item>
      </el-col>
      <el-col :span="12">
        <el-form-item label="表描述" prop="tableComment">
          <el-input v-model="info.table_comment" placeholder="请输入"/>
        </el-form-item>
      </el-col>
      <el-col :span="12">
        <el-form-item label="实体类名称" prop="className">
          <el-input v-model="info.class_name" placeholder="请输入"/>
        </el-form-item>
      </el-col>
      <el-col :span="12">
        <el-form-item label="作者" prop="functionAuthor">
          <el-input v-model="info.function_author" placeholder="请输入"/>
        </el-form-item>
      </el-col>
      <el-col :span="24">
        <el-form-item label="备注" prop="remark">
          <el-input v-model="info.remark" type="textarea" :rows="3"></el-input>
        </el-form-item>
      </el-col>
    </el-row>
  </el-form>
</template>

<script setup lang="ts">
defineProps({
  info: {
    type: Object,
    default: null
  }
});

// 表单校验
const rules = ref({
  table_name: [{ required: true, message: "请输入表名称", trigger: "blur" }],
  table_comment: [{ required: true, message: "请输入表描述", trigger: "blur" }],
  class_name: [{ required: true, message: "请输入实体类名称", trigger: "blur" }],
  function_author: [{ required: true, message: "请输入作者", trigger: "blur" }]
});
</script>
