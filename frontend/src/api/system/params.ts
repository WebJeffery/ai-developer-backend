import request from "@/utils/request";

const ParamsAPI = {
  uploadFile(body: any) {
    return request<ApiResponse<UploadFilePath>>({
      url: `/system/param/upload`,
      method: "post",
      data: body,
      headers: { "Content-Type": "multipart/form-data" },
    });
  },

  getInitConfig() {
    return request<ApiResponse<ConfigTable[]>>({
      url: `/system/param/info`,
      method: "get",
    });
  },

  getConfigList(query: ConfigPageQuery) {
    return request<ApiResponse<PageResult<ConfigTable[]>>>({
      url: `/system/param/list`,
      method: "get",
      params: query,
    });
  },

  getConfigDetail(query: number) {
    return request<ApiResponse<ConfigTable>>({
      url: `/system/param/detail/${query}`,
      method: "get",
    });
  },

  createConfig(body: ConfigForm) {
    return request<ApiResponse>({
      url: `/system/param/create`,
      method: "post",
      data: body,
    });
  },

  updateConfig(id: number, body: ConfigForm) {
    return request<ApiResponse>({
      url: `/system/param/update/${id}`,
      method: "put",
      data: body,
    });
  },

  deleteConfig(body: number[]) {
    return request<ApiResponse>({
      url: `/system/param/delete`,
      method: "delete",
      data: body,
    });
  },

  exportConfig(body: ConfigPageQuery) {
    return request<Blob>({
      url: `/system/param/export`,
      method: "post",
      data: body,
      responseType: "blob",
    });
  },
};

export default ParamsAPI;

export interface ConfigPageQuery extends PageQuery {
  /** 配置名称 */
  config_name?: string;
  /** 配置键 */
  config_key?: string;
  /** 配置类型 */
  config_type?: boolean;
  /** 开始时间 */
  start_time?: string;
  /** 结束时间 */
  end_time?: string;
}

export interface ConfigTable {
  id?: number;
  config_name?: string;
  config_key?: string;
  config_value?: string;
  config_type?: boolean;
  description?: string;
  created_at?: string;
  updated_at?: string;
  creator?: creatorType;
}

export interface ConfigForm {
  id?: number;
  config_name?: string;
  config_key?: string;
  config_value?: string;
  config_type?: boolean;
  description?: string;
}
