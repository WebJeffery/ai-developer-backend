import request from "@/utils/request";

const GENERATOR_BASE_URL = "/gencode";

const GencodeAPI = {
  
  // 查询生成表数据
  listTable(query: TablePageQuery) {
    return request<PageResult<GenTableOutVO>>({
      url: `${GENERATOR_BASE_URL}/list`,
      method: 'get',
      params: query
    })
  },

  // 查询db数据库列表
  listDbTable(query: TablePageQuery) {
    return request<PageResult<TablePageVO>>({
      url: `${GENERATOR_BASE_URL}/db/list`,
      method: 'get',
      params: query
    })
  },

  // 查询表详细信息
  getGenTableDetail(tableId: number) {
    return request<GenTableDetailResult>({
      url: `${GENERATOR_BASE_URL}/detail/${tableId}`,
      method: 'get'
    })
  },

  // 创建表
  createTable(sql: string) {
    return request({
      url: `${GENERATOR_BASE_URL}/create`,
      method: 'post',
      params: { sql }
    })
  },

  // 修改代码生成信息
  updateGenTable(data: GenTableUpdateSchema) {
    return request({
      url: `${GENERATOR_BASE_URL}/update`,
      method: 'put',
      data
    })
  },

  // 导入表
  importTable(tables: string[]) {
    return request({
      url: `${GENERATOR_BASE_URL}/import`,
      method: 'post',
      data: { tables }
    })
  },


  // 预览生成代码
  previewTable(tableId: number) {
    return request<GeneratorPreviewVO[]>({
      url: `${GENERATOR_BASE_URL}/preview/${tableId}`,
      method: 'get'
    })
  },

  // 删除表数据
  deleteTable(tableIds: number[]) {
    return request({
      url: `${GENERATOR_BASE_URL}/delete`,
      method: 'delete',
      data: tableIds
    })
  },

  // 批量生成代码
  batchGenCode(tables: string) {
    return request<Blob>({
      url: `${GENERATOR_BASE_URL}/batch/out`,
      method: 'patch',
      params: { tables },
      responseType: 'blob'
    })
  },

  // 生成代码到指定路径
  genCodeToPath(tableName: string) {
    return request({
      url: `${GENERATOR_BASE_URL}/out/path/${tableName}`,
      method: 'post'
    })
  },

  // 同步数据库
  syncDb(tableName: string) {
    return request({
      url: `${GENERATOR_BASE_URL}/sync/db/${tableName}`,
      method: 'post'
    })
  }
};

export default GencodeAPI;

/** 代码生成预览对象 */
export interface GeneratorPreviewVO {
  /** 文件生成路径 */
  path: string;
  /** 文件名称 */
  fileName: string;
  /** 文件内容 */
  content: string;
}

/**  数据表分页查询参数 */
export interface TablePageQuery extends PageQuery {
  /** 关键字(表名) */
  keywords?: string;
}

/** 数据表分页对象 */
export interface TablePageVO {
  /** 表名称 */
  tableName: string;

  /** 表描述 */
  tableComment: string;

  /** 存储引擎 */
  engine: string;

  /** 字符集排序规则 */
  tableCollation: string;

  /** 创建时间 */
  createTime: string;
}

/** 代码生成表输出对象 */
export interface GenTableOutVO {
  /** 主键 */
  id?: number;
  /** 表名称 */
  tableName: string;
  /** 表描述 */
  tableComment: string;
  /** 关联子表的表名 */
  subTableName?: string;
  /** 子表关联的外键名 */
  subTableFkName: string;
  /** 实体类名称 */
  className: string;
  /** 使用的模板（crud单表操作 tree树表操作） */
  tplCategory?: string;
  /** 前端模板类型（element-ui模版 element-plus模版） */
  tplWebType?: string;
  /** 生成包路径 */
  packageName: string;
  /** 生成模块名 */
  moduleName: string;
  /** 生成业务名 */
  businessName: string;
  /** 生成功能名 */
  functionName: string;
  /** 生成功能作者 */
  functionAuthor?: string;
  /** 生成代码方式（0zip压缩包 1自定义路径） */
  genType?: string;
  /** 生成路径（不填默认项目路径） */
  genPath?: string;
  /** 其它生成选项 */
  options?: string;
  /** 树编码字段 */
  treeCode?: string;
  /** 树父编码字段 */
  treeParentCode?: string;
  /** 树名称字段 */
  treeName?: string;
  /** 上级菜单ID字段 */
  parentMenuId?: number;
  /** 上级菜单名称字段 */
  parentMenuName?: string;
  /** 是否为子表 */
  sub?: boolean;
  /** 是否为树表 */
  tree?: boolean;
  /** 是否为单表 */
  crud?: boolean;
}

/** 代码生成表更新模型 */
export interface GenTableUpdateSchema extends GenTableOutVO {
  /** 主键信息 */
  pkColumn?: GenTableColumnUpdateSchema;
  /** 子表信息 */
  subTable?: GenTableUpdateSchema;
  /** 表列信息 */
  columns: GenTableColumnUpdateSchema[];
}

/** 代码生成表列更新模型 */
export interface GenTableColumnUpdateSchema {
  /** 主键 */
  id?: number;
  /** 归属表编号 */
  tableId?: number;
  /** 列名称 */
  columnName: string;
  /** 列描述 */
  columnComment?: string;
  /** 列类型 */
  columnType: string;
  /** PYTHON类型 */
  pythonType?: string;
  /** PYTHON字段名 */
  pythonField: string;
  /** 是否主键（1是） */
  isPk?: string;
  /** 是否自增（1是） */
  isIncrement?: string;
  /** 是否必填（1是） */
  isRequired?: string;
  /** 是否唯一（1是） */
  isUnique?: string;
  /** 是否为插入字段（1是） */
  isInsert?: string;
  /** 是否编辑字段（1是） */
  isEdit?: string;
  /** 是否列表字段（1是） */
  isList?: string;
  /** 是否查询字段（1是） */
  isQuery?: string;
  /** 查询方式（等于、不等于、大于、小于、范围） */
  queryType?: string;
  /** 显示类型（文本框、文本域、下拉框、复选框、单选框、日期控件） */
  htmlType: string;
  /** 字典类型 */
  dictType: string;
  /** 排序 */
  sort?: number;
  /** 字段大写形式 */
  capPythonField?: string;
  /** 是否主键 */
  pk?: boolean;
  /** 是否自增 */
  increment?: boolean;
  /** 是否必填 */
  required?: boolean;
  /** 是否唯一 */
  unique?: boolean;
  /** 是否为插入字段 */
  insert?: boolean;
  /** 是否编辑字段 */
  edit?: boolean;
  /** 是否列表字段 */
  list?: boolean;
  /** 是否查询字段 */
  query?: boolean;
  /** 是否为基类字段 */
  superColumn?: boolean;
  /** 是否为基类字段白名单 */
  usableColumn?: boolean;
}

/** 表详情查询结果 */
export interface GenTableDetailResult {
  /** 表信息 */
  info: GenTableOutVO;
  /** 表列信息 */
  rows: GenTableColumnUpdateSchema[];
  /** 所有表信息 */
  tables: GenTableOutVO[];
}
