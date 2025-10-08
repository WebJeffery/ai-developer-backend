import request from "@/utils/request";

const API_PATH = "/generator/gencode";

const GencodeAPI = {
  // 查询生成表数据
  listTable(query: TablePageQuery) {
    return request<ApiResponse<PageResult<GenTableOutVO[]>>>({
      url: `${API_PATH}/list`,
      method: 'get',
      params: query
    })
  },

  // 查询db数据库列表
  listDbTable(query: TablePageQuery) {
    return request<ApiResponse<PageResult<TablePageVO[]>>>({
      url: `${API_PATH}/db/list`,
      method: 'get',
      params: query
    })
  },

  // 导入表 - 将数组转换为适合FastAPI解析的格式
  importTable(table_names: string[]) {
    // 构建符合FastAPI期望的查询字符串
    let queryString = '';
    table_names.forEach((name, index) => {
      queryString += `${index === 0 ? '?' : '&'}table_names=${encodeURIComponent(name)}`;
    });
    
    return request<ApiResponse>({
      url: `${API_PATH}/import${queryString}`,
      method: 'post'
    })
  },

  // 查询表详细信息
  getGenTableDetail(table_id: number) {
    return request<ApiResponse<GenTableDetailResult>>({
      url: `${API_PATH}/detail/${table_id}`,
      method: 'get'
    })
  },

  // 创建表
  createTable(sql: string) {
    return request<ApiResponse>({
      url: `${API_PATH}/create`,
      method: 'post',
      params: { sql }
    })
  },

  // 修改代码生成信息
  updateGenTable(table_id: number, body: GenTableSchema) {
    return request<ApiResponse>({
      url: `${API_PATH}/update/${table_id}`,
      method: 'put',
      data: body,
    })
  },

  // 删除表数据
  deleteTable(data: GenTableDeleteSchema) {
    return request<ApiResponse>({
      url: `${API_PATH}/delete`,
      method: 'delete',
      data
    })
  },

  // 批量生成代码
  batchGenCode(table_names: string[]) {
    return request<Blob>({
      url: `${API_PATH}/batch/output`,
      method: 'patch',
      params: { table_names },
      responseType: 'blob'
    })
  },

  // 生成代码到指定路径
  genCodeToPath(table_name: string) {
    return request<ApiResponse>({
      url: `${API_PATH}/output/${table_name}`,
      method: 'post'
    })
  },

  // 预览生成代码
  previewTable(table_id: number) {
    return request<ApiResponse<GeneratorPreviewVO[]>>({
      url: `${API_PATH}/preview/${table_id}`,
      method: 'get'
    })
  },

  // 同步数据库
  syncDb(table_name: string) {
    return request<ApiResponse>({
      url: `${API_PATH}/synch_db/${table_name}`,
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
  file_name: string;
  /** 文件内容 */
  content: string;
}

/**  数据表分页查询参数 */
export interface TablePageQuery extends PageQuery {
  /** 表名称 */
  table_name?: string;
  /** 表描述 */
  table_comment?: string;
}

/** 数据表分页对象 */
export interface TablePageVO {
  /** 表名称 */
  table_name: string;

  /** 表描述 */
  table_comment: string;

  /** 数据库名称 */
  database_name: string;

  /** 表单类型 */
  table_type: string;

}

/** 代码生成表输出对象 */
export interface GenTableOutVO {
  /** 主键 */
  id?: number;
  /** 表名称 */
  table_name: string;
  /** 表描述 */
  table_comment: string;
  /** 关联子表的表名 */
  sub_table_name?: string;
  /** 子表关联的外键名 */
  sub_table_fk_name: string;
  /** 实体类名称 */
  class_name: string;
  /** 使用的模板（crud单表操作 tree树表操作） */
  tpl_category?: string;
  /** 前端模板类型（element-ui模版 element-plus模版） */
  tpl_web_type?: string;
  /** 生成包路径 */
  package_name: string;
  /** 生成模块名 */
  module_name: string;
  /** 生成业务名 */
  business_name: string;
  /** 生成功能名 */
  function_name: string;
  /** 生成功能作者 */
  function_author?: string;
  /** 生成代码方式（0zip压缩包 1自定义路径） */
  gen_type?: string;
  /** 生成路径（不填默认项目路径） */
  gen_path?: string;
  /** 其它生成选项 */
  options?: string;
  /** 树编码字段 */
  tree_code?: string;
  /** 树父编码字段 */
  tree_parent_code?: string;
  /** 树名称字段 */
  tree_name?: string;
  /** 上级菜单ID字段 */
  parent_menu_id?: number;
  /** 上级菜单名称字段 */
  parent_menu_name?: string;
  /** 是否为子表 */
  sub?: boolean;
  /** 是否为树表 */
  tree?: boolean;
  /** 是否为单表 */
  crud?: boolean;
}

/** 代码生成业务表模型 */
export interface GenTableSchema extends GenTableOutVO {
  /** 主键信息 */
  pk_column?: GenTableColumnOutSchema;
  /** 子表信息 */
  sub_table?: GenTableSchema;
  /** 表列信息 */
  columns: GenTableColumnOutSchema[];
}

/** 代码生成业务表列模型 */
export interface GenTableColumnSchema {
  /** 主键 */
  id?: number;
  /** 归属表编号 */
  table_id?: number;
  /** 列名称 */
  column_name: string;
  /** 列描述 */
  column_comment?: string;
  /** 列类型 */
  column_type: string;
  /** PYTHON类型 */
  python_type?: string;
  /** PYTHON字段名 */
  python_field: string;
  /** 是否主键（1是） */
  is_pk?: string;
  /** 是否自增（1是） */
  is_increment?: string;
  /** 是否必填（1是） */
  is_required?: string;
  /** 是否唯一（1是） */
  is_unique?: string;
  /** 是否为插入字段（1是） */
  is_insert?: string;
  /** 是否编辑字段（1是） */
  is_edit?: string;
  /** 是否列表字段（1是） */
  is_list?: string;
  /** 是否查询字段（1是） */
  is_query?: string;
  /** 查询方式（等于、不等于、大于、小于、范围） */
  query_type?: string;
  /** 显示类型（文本框、文本域、下拉框、复选框、单选框、日期控件） */
  html_type: string;
  /** 字典类型 */
  dict_type: string;
  /** 排序 */
  sort?: number;
  /** 功能描述 */
  description?: string;
}

/** 代码生成业务表列输出模型 */
export interface GenTableColumnOutSchema extends GenTableColumnSchema {
  /** 字段大写形式 */
  cap_python_field?: string;
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
  super_column?: boolean;
  /** 是否为基类字段白名单 */
  usable_column?: boolean;
}

/** 删除代码生成业务表模型 */
export interface GenTableDeleteSchema {
  /** 需要删除的代码生成业务表ID列表 */
  table_ids: number[];
}

/** 表详情查询结果 */
export interface GenTableDetailResult {
  /** 表信息 */
  info: GenTableOutVO;
  /** 表列信息 */
  rows: GenTableColumnOutSchema[];
  /** 所有表信息 */
  tables: GenTableOutVO[];
}
