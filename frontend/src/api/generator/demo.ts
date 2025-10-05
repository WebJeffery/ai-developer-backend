import request from "@/utils/request";

const API_PATH = "/generator/demo";

const ExampleAPI = {
  getExampleList(query: ExamplePageQuery) {
    return request<ApiResponse<PageResult<ExampleTable[]>>>({
      url: `${API_PATH}/list`,
      method: "get",
      params: query,
    });
  },

  getExampleDetail(query: number) {
    return request<ApiResponse<ExampleTable>>({ 
      url: `${API_PATH}/detail/${query}`,
      method: "get",
    });
  },

  createExample(body: ExampleForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/create`,
      method: "post",
      data: body,
    });
  },

  updateExample(id: number, body: ExampleForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/update/${id}`,
      method: "put",
      data: body,
    });
  },

  deleteExample(body: number[]) {
    return request<ApiResponse>({
      url: `${API_PATH}/delete`,
      method: "delete",
      data: body,
    });
  },

  batchAvailableExample(body: BatchType) {
    return request<ApiResponse>({
      url: `${API_PATH}/available/setting`,
      method: "patch",
      data: body,
    });
  },

  exportExample(body: ExamplePageQuery) {
    return request<Blob>({
      url: `${API_PATH}/export`,
      method: "post",
      data: body,
      responseType: "blob",
    });
  },

  downloadTemplate() {
    return request<ApiResponse>({
      url: `${API_PATH}/download/template`,
      method: "post",
      responseType: "blob",
    });
  },

  importExample(body: any) {
    return request<ApiResponse>({
      url: `${API_PATH}/import`,
      method: "post",
      data: body,
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
  },
};

export default ExampleAPI;

export interface ExamplePageQuery extends PageQuery {
  /** 示例标题 */
  name?: string;
  /** 示例状态 */
  status?: boolean;
  /** 开始时间 */
  start_time?: string;
  /** 结束时间 */
  end_time?: string;
}

export interface ExampleTable {
  index?: number;
  id?: number;
  name?: string;
  status?: boolean;
  description?: string;
  created_at?: string;
  updated_at?: string;
  creator?: creatorType;
}

export interface ExampleForm {
  id?: number;
  name?: string;
  status?: boolean;
  description?: string;
}
