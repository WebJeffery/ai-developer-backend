import request from "@/utils/request";

const ExampleAPI = {
  getExampleList(query: ExamplePageQuery) {
    return request<ApiResponse<PageResult<ExampleTable[]>>>({
      url: `/example/demo/list`,
      method: "get",
      params: query,
    });
  },

  getExampleDetail(query: number) {
    return request<ApiResponse<ExampleTable>>({ 
      url: `/example/demo/detail/${query}`,
      method: "get",
    });
  },

  createExample(body: ExampleForm) {
    return request<ApiResponse>({
      url: `/example/demo/create`,
      method: "post",
      data: body,
    });
  },

  updateExample(id: number, body: ExampleForm) {
    return request<ApiResponse>({
      url: `/example/demo/update/${id}`,
      method: "put",
      data: body,
    });
  },

  deleteExample(body: number[]) {
    return request<ApiResponse>({
      url: `/example/demo/delete`,
      method: "delete",
      data: body,
    });
  },

  batchAvailableExample(body: BatchType) {
    return request<ApiResponse>({
      url: `/example/demo/available/setting`,
      method: "patch",
      data: body,
    });
  },

  exportExample(body: ExamplePageQuery) {
    return request<Blob>({
      url: `/example/demo/export`,
      method: "post",
      data: body,
      responseType: "blob",
    });
  },

  downloadTemplate() {
    return request<ApiResponse>({
      url: `/example/demo/download/template`,
      method: "post",
      responseType: "blob",
    });
  },

  importExample(body: any) {
    return request<ApiResponse>({
      url: `/example/demo/import`,
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
