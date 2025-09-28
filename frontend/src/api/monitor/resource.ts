import request from "@/utils/request";

export const ResourceAPI = {
  /**
   * 获取目录列表
   * @param query 查询参数
   */
  getResourceList(query: ResourcePageQuery) {
    return request<ApiResponse<PageResult<ResourceItem[]>>>({
      url: `/monitor/resource/list`,
      method: "get",
      params: query,
    });
  },


  /**
   * 上传文件
   * @param formData 文件数据
   */
  uploadFile(formData: FormData) {
    return request<ApiResponse<ResourceUploadSchema>>({
      url: `/monitor/resource/upload`,
      method: "post",
      data: formData,
      headers: { "Content-Type": "multipart/form-data" },
    });
  },

  /**
   * 下载文件
   * @param path 文件路径
   */
  downloadFile(path: string) {
    return request<Blob>({
      url: `/monitor/resource/download`,
      method: "get",
      params: { path },
      responseType: "blob",
    });
  },

  /**
   * 删除文件或目录
   * @param body 文件路径数组
   */
  deleteResource(body: string[]) {
    return request<ApiResponse>({
      url: `/monitor/resource/delete`,
      method: "delete",
      data: body,
    });
  },

  /**
   * 移动文件或目录
   * @param body 移动参数
   */
  moveResource(body: ResourceMoveQuery) {
    return request<ApiResponse>({
      url: `/monitor/resource/move`,
      method: "post",
      data: body,
    });
  },

  /**
   * 复制文件或目录
   * @param body 复制参数
   */
  copyResource(body: ResourceCopyQuery) {
    return request<ApiResponse>({
      url: `/monitor/resource/copy`,
      method: "post",
      data: body,
    });
  },

  /**
   * 重命名文件或目录
   * @param body 重命名参数
   */
  renameResource(body: ResourceRenameQuery) {
    return request<ApiResponse>({
      url: `/monitor/resource/rename`,
      method: "post",
      data: body,
    });
  },

  /**
   * 创建目录
   * @param body 创建目录参数
   */
  createDirectory(body: ResourceCreateDirQuery) {
    return request<ApiResponse>({
      url: `/monitor/resource/create-dir`,
      method: "post",
      data: body,
    });
  },

  /**
   * 导出资源列表
   * @param body 导出条件
   */
  exportResource(body: ResourcePageQuery) {
    return request<Blob>({
      url: `/monitor/resource/export`,
      method: "post",
      data: body,
      responseType: "blob",
    });
  },
};

export default ResourceAPI;



/**
 * 资源列表查询参数
 */
export interface ResourceListQuery {
  /** 目录路径 */
  path?: string;
  /** 包含隐藏文件 */
  include_hidden?: boolean;
}

/**
 * 资源目录模型
 */
export interface ResourceDirectorySchema {
  /** 目录路径 */
  path: string;
  /** 目录名称 */
  name: string;
  /** 目录项 */
  items: ResourceItem[];
  /** 文件总数 */
  total_files: number;
  /** 目录总数 */
  total_dirs: number;
  /** 总大小 */
  total_size: number;
}

/**
 * 资源搜索查询参数
 */
export interface ResourceSearchQuery {
  /** 关键词 */
  name?: string;
}

/**
 * 资源分页查询参数
 */
export interface ResourcePageQuery extends PageQuery {
  /** 关键词 */
  name?: string;
  /** 目录路径 */
  path?: string;
  /** 包含隐藏文件 */
  include_hidden?: boolean;
}

/**
 * 资源上传响应模型
 */
export interface ResourceUploadSchema {
  /** 文件名 */
  filename: string;
  /** 访问URL */
  file_url: string;
  /** 文件大小 */
  file_size: number;
  /** 上传时间 */
  upload_time: string;
}

/**
 * 资源项信息
 */
export interface ResourceItem {
  /** 文件/目录名称 */
  name: string;
  /** 文件URL路径 */
  file_url: string;
  /** 相对路径 */
  relative_path?: string;
  /** 是否为文件 */
  is_file?: boolean;
  /** 是否为目录 */
  is_dir?: boolean;
  /** 文件大小（字节） */
  size?: number | null;
  /** 创建时间 */
  created_time: string;
  /** 修改时间 */
  modified_time: string;
  /** 是否为隐藏文件 */
  is_hidden?: boolean;
}

/**
 * 资源移动参数
 */
export interface ResourceMoveQuery {
  /** 源路径 */
  source_path: string;
  /** 目标路径 */
  target_path: string;
  /** 是否覆盖 */
  overwrite?: boolean;
}

/**
 * 资源复制参数
 */
export interface ResourceCopyQuery {
  /** 源路径 */
  source_path: string;
  /** 目标路径 */
  target_path: string;
  /** 是否覆盖 */
  overwrite?: boolean;
}

/**
 * 资源重命名参数
 */
export interface ResourceRenameQuery {
  /** 原路径 */
  old_path: string;
  /** 新名称 */
  new_name: string;
}

/**
 * 创建目录参数
 */
export interface ResourceCreateDirQuery {
  /** 父目录路径 */
  parent_path: string;
  /** 目录名称 */
  dir_name: string;
}
