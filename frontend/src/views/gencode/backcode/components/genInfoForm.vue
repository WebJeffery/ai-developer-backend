<template>
  <el-form ref="genInfoForm" :model="info" :rules="rules" label-width="150px">
    <el-row>
      <el-col :span="12">
        <el-form-item prop="tplCategory">
          <template #label>生成模板</template>
          <el-select v-model="info.tplCategory" @change="tplSelectChange">
            <el-option label="单表（增删改查）" value="crud" />
            <el-option label="树表（增删改查）" value="tree" />
            <el-option label="主子表（增删改查）" value="sub" />
          </el-select>
        </el-form-item>
      </el-col>

      <el-col :span="12">
        <el-form-item prop="tplWebType">
          <template #label>前端类型</template>
          <el-select v-model="info.tplWebType">
            <el-option label="Vue2 Element UI 模版" value="element-ui" />
            <el-option label="Vue3 Element Plus 模版" value="element-plus" />
          </el-select>
        </el-form-item>
      </el-col>

      <el-col :span="12">
        <el-form-item prop="packageName">
          <template #label>
            生成包路径
            <el-tooltip content="生成在哪个java包下，例如 com.ruoyi.system" placement="top">
              <el-icon><question-filled /></el-icon>
            </el-tooltip>
          </template>
          <el-input v-model="info.packageName" />
        </el-form-item>
      </el-col>

      <el-col :span="12">
        <el-form-item prop="moduleName">
          <template #label>
            生成模块名
            <el-tooltip content="可理解为子系统名，例如 system" placement="top">
              <el-icon><question-filled /></el-icon>
            </el-tooltip>
          </template>
          <el-input v-model="info.moduleName" />
        </el-form-item>
      </el-col>

      <el-col :span="12">
        <el-form-item prop="businessName">
          <template #label>
            生成业务名
            <el-tooltip content="可理解为功能英文名，例如 user" placement="top">
              <el-icon><question-filled /></el-icon>
            </el-tooltip>
          </template>
          <el-input v-model="info.businessName" />
        </el-form-item>
      </el-col>

      <el-col :span="12">
        <el-form-item prop="functionName">
          <template #label>
            生成功能名
            <el-tooltip content="用作类描述，例如 用户" placement="top">
              <el-icon><question-filled /></el-icon>
            </el-tooltip>
          </template>
          <el-input v-model="info.functionName" />
        </el-form-item>
      </el-col>

      <el-col :span="12">
        <el-form-item prop="genType">
          <template #label>
            生成代码方式
            <el-tooltip content="默认为zip压缩包下载，也可以自定义生成路径" placement="top">
              <el-icon><question-filled /></el-icon>
            </el-tooltip>
          </template>
          <el-radio v-model="info.genType" value="0">zip压缩包</el-radio>
          <el-radio v-model="info.genType" value="1">自定义路径</el-radio>
        </el-form-item>
      </el-col>

      <el-col :span="12">
        <el-form-item>
          <template #label>
            上级菜单
            <el-tooltip content="分配到指定菜单下，例如 系统管理" placement="top">
              <el-icon><question-filled /></el-icon>
            </el-tooltip>
          </template>
          <el-tree-select
            v-model="info.parentMenuId"
            :data="menuOptions"
            :props="{ value: 'menuId', label: 'menuName', children: 'children' }"
            value-key="menuId"
            placeholder="请选择系统菜单"
            check-strictly
          />
        </el-form-item>
      </el-col>

      <el-col v-if="info.genType == '1'" :span="24">
        <el-form-item prop="genPath">
          <template #label>
            自定义路径
            <el-tooltip content="填写磁盘绝对路径，若不填写，则生成到当前Web项目下" placement="top">
              <el-icon><question-filled /></el-icon>
            </el-tooltip>
          </template>
          <el-input v-model="info.genPath">
            <template #append>
              <el-dropdown>
                <el-button type="primary">
                  最近路径快速选择
                  <i class="el-icon-arrow-down el-icon--right"></i>
                </el-button>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item @click="handleResetGenPath">恢复默认的生成基础路径</el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
            </template>
          </el-input>
        </el-form-item>
      </el-col>
    </el-row>
    
    <template v-if="info.tplCategory == 'tree'">
      <h4 class="form-header">其他信息</h4>
      <el-row v-show="info.tplCategory == 'tree'">
        <el-col :span="12">
          <el-form-item>
            <template #label>
              树编码字段
              <el-tooltip content="树显示的编码字段名， 如：dept_id" placement="top">
                <el-icon><question-filled /></el-icon>
              </el-tooltip>
            </template>
            <el-select v-model="info.treeCode" placeholder="请选择">
              <el-option
                v-for="(column, index) in info.columns || []"
                :key="index"
                :label="column.columnName + '：' + column.columnComment"
                :value="column.columnName"
              ></el-option>
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item>
            <template #label>
              树父编码字段
              <el-tooltip content="树显示的父编码字段名， 如：parent_Id" placement="top">
                <el-icon><question-filled /></el-icon>
              </el-tooltip>
            </template>
            <el-select v-model="info.treeParentCode" placeholder="请选择">
              <el-option
                v-for="(column, index) in info.columns || []"
                :key="index"
                :label="column.columnName + '：' + column.columnComment"
                :value="column.columnName"
              ></el-option>
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item>
            <template #label>
              树名称字段
              <el-tooltip content="树节点的显示名称字段名， 如：dept_name" placement="top">
                <el-icon><question-filled /></el-icon>
              </el-tooltip>
            </template>
            <el-select v-model="info.treeName" placeholder="请选择">
              <el-option
                v-for="(column, index) in info.columns || []"
                :key="index"
                :label="column.columnName + '：' + column.columnComment"
                :value="column.columnName"
              ></el-option>
            </el-select>
          </el-form-item>
        </el-col>
      </el-row>
    </template>

    <template v-if="info.tplCategory == 'sub'">
      <h4 class="form-header">关联信息</h4>
      <el-row>
        <el-col :span="12">
          <el-form-item>
            <template #label>
              关联子表的表名
              <el-tooltip content="关联子表的表名， 如：sys_user" placement="top">
                <el-icon><question-filled /></el-icon>
              </el-tooltip>
            </template>
            <el-select v-model="info.subTableName" placeholder="请选择" @change="subSelectChange">
              <el-option
                v-for="(table, index) in tables || []"
                :key="index"
                :label="(table.tableName || '') + '：' + (table.tableComment || '')"
                :value="table.tableName || ''"
                :disabled="!table.tableName"
              ></el-option>
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item>
            <template #label>
              子表关联的外键名
              <el-tooltip content="子表关联的外键名， 如：user_id" placement="top">
                <el-icon><question-filled /></el-icon>
              </el-tooltip>
            </template>
            <el-select v-model="info.subTableFkName" placeholder="请选择">
              <el-option
                v-for="(column, index) in subColumns"
                :key="index"
                :label="column.columnName + '：' + column.columnComment"
                :value="column.columnName"
              ></el-option>
            </el-select>
          </el-form-item>
        </el-col>
      </el-row>
    </template>

  </el-form>
</template>

<script setup lang="ts">
import MenuAPI from "@/api/system/menu";
import { ref, computed, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';

const subColumns = ref<Array<{ columnName: string; columnComment: string }>>([]);
const menuOptions = ref<Array<{ id: number; menuId: number; menuName: string; parent_id: number; children: Array<any> }>>([]);
const router = useRouter();

// 定义类型接口
interface TableColumn {
  columnName: string;
  columnComment: string;
}

interface TableInfo {
  tableName?: string;
  tableComment?: string;
  columns?: TableColumn[];
}

interface GenInfo {
  tplCategory?: string;
  tplWebType?: string;
  packageName?: string;
  moduleName?: string;
  businessName?: string;
  functionName?: string;
  genType?: string;
  parentMenuId?: number;
  genPath?: string;
  subTableName?: string;
  subTableFkName?: string;
  columns?: TableColumn[];
  treeCode?: string;
  treeParentCode?: string;
  treeName?: string;
}

const props = defineProps<{
  info?: GenInfo;
  tables?: TableInfo[];
}>();

const emit = defineEmits<{
  (e: 'update:info', value: GenInfo): void;
}>();

// 使用computed创建一个安全的info对象，确保所有属性都有默认值
const info = computed<GenInfo>({
  get() {
    return {
      tplCategory: '',
      tplWebType: 'element-plus',
      packageName: '',
      moduleName: '',
      businessName: '',
      functionName: '',
      genType: '0',
      parentMenuId: undefined,
      genPath: '',
      subTableName: '',
      subTableFkName: '',
      columns: [],
      treeCode: '',
      treeParentCode: '',
      treeName: '',
      ...props.info
    };
  },
  set(newValue: GenInfo) {
    emit('update:info', newValue);
  }
});

// 表单校验
const rules = ref({
  tplCategory: [{ required: true, message: "请选择生成模板", trigger: "blur" }],
  packageName: [{ required: true, message: "请输入生成包路径", trigger: "blur" }],
  moduleName: [{ required: true, message: "请输入生成模块名", trigger: "blur" }],
  businessName: [{ required: true, message: "请输入生成业务名", trigger: "blur" }],
  functionName: [{ required: true, message: "请输入生成功能名", trigger: "blur" }]
});

function subSelectChange() {
  emit('update:info', {
    ...info.value,
    subTableFkName: ""
  });
}

function tplSelectChange(value: string) {
  if (value !== "sub") {
    emit('update:info', {
      ...info.value,
      subTableName: "",
      subTableFkName: ""
    });
  }
}

function setSubTableColumns(value?: string) {
  if (!value || !props.tables) {
    subColumns.value = [];
    return;
  }
  
  for (const item of props.tables) {
    if (item.tableName === value && item.columns) {
      subColumns.value = item.columns;
      break;
    }
  }
}

// 恢复默认生成路径的方法
function handleResetGenPath() {
  emit('update:info', {
    ...info.value,
    genPath: '/'
  });
}

/** 查询菜单下拉树结构 */
function getMenuTreeselect() {
  MenuAPI.getMenuList().then((response: any) => {
    // 简单的树形结构处理逻辑
    function buildTree(data: any[], idField: string): any[] {
      const result: any[] = [];
      const map: Record<string, any> = {};
      
      // 构建id映射
      data.forEach(item => {
        map[item[idField]] = item;
        item.children = [];
        // 转换属性名以匹配tree-select的期望格式
        if (item.id !== undefined) {
          item.menuId = item.id;
        }
        if (item.menu_name !== undefined) {
          item.menuName = item.menu_name;
        }
      });
      
      // 构建树
      data.forEach(item => {
        if (item.parent_id === 0 || !map[item.parent_id]) {
          result.push(item);
        } else {
          map[item.parent_id].children.push(item);
        }
      });
      
      return result;
    }
    
    if (response && response.data && response.data.data) {
      menuOptions.value = buildTree(response.data.data, "id");
    }
  });
}

onMounted(() => {
  getMenuTreeselect();
  // 初始化时检查tplWebType是否为空
  if (!props.info?.tplWebType) {
    emit('update:info', {
      ...info.value,
      tplWebType: "element-plus"
    });
  }
});

watch(() => props.info?.subTableName, (val) => {
  setSubTableColumns(val);
});

watch(() => props.info?.tplWebType, (val) => {
  if (val === '' || val === undefined) {
    emit('update:info', {
      ...info.value,
      tplWebType: "element-plus"
    });
  }
});

</script>
