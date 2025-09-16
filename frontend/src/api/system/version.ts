import request from "@/utils/request";

const VersionAPI = {
  getVersionList(query: VersionPageQuery) {
    return request<ApiResponse<PageResult<VersionTable[]>>>({
      url: `/system/version/list`,
      method: "get",
      params: query,
    });
  },

  getVersionDetail(query: number) {
    return request<ApiResponse<VersionTable>>({
      url: `/system/version/detail/${query}`,
      method: "get",
    });
  },

  createVersion(body: VersionForm) {
    return request<ApiResponse>({
      url: `/system/version/create`,
      method: "post",
      data: body,
    });
  },

  updateVersion(id: number, body: VersionForm) {
    return request<ApiResponse>({
      url: `/system/version/update/${id}`,
      method: "put",
      data: body,
    });
  },

  deleteVersion(body: number[]) {
    return request<ApiResponse>({
      url: `/system/version/delete`,
      method: "delete",
      data: body,
    });
  },

};

export default VersionAPI;

export interface VersionPageQuery extends PageQuery {
  title?: string;
  status?: string;
  start_time?: string;
  end_time?: string;
}

export interface VersionTable {
  index?: number;
  id?: number;
  version_number?: string;
  title?: string;
  release_notes?: string;
  project?: string;
  status?: string;
  released_at?: string;
  description?: string;
  created_at?: string;
  updated_at?: string;
  creator?: creatorType;
}

export interface VersionForm {
  id?: number;
  version_number: string;
  title: string;
  release_notes?: string;
  project?: string;
  status?: string;
  released_at?: string;
  description?: string;
}
