import request from "@/utils/request";

const JobAPI = {
  getJobList(query: JobPageQuery) {
    return request<ApiResponse<PageResult<JobTable[]>>>({
      url: `/monitor/job/list`,
      method: "get",
      params: query,
    });
  },

  getJobDetail(query: number) {
    return request<ApiResponse<JobTable>>({
      url: `/monitor/job/detail/${query}`,
      method: "get",
    });
  },

  createJob(body: JobForm) {
    return request<ApiResponse>({
      url: `/monitor/job/create`,
      method: "post",
      data: body,
    });
  },

  updateJob(id: number, body: JobForm) {
    return request<ApiResponse>({
      url: `/monitor/job/update/${id}`,
      method: "put",
      data: body,
    });
  },

  deleteJob(body: number[]) {
    return request<ApiResponse>({
      url: `/monitor/job/delete`,
      method: "delete",
      data: body,
    });
  },

  exportJob(body: JobPageQuery) {
    return request<Blob>({
      url: `/monitor/job/export`,
      method: "post",
      data: body,
      responseType: "blob",
    });
  },

  clearJob() {
    return request<ApiResponse>({
      url: `/monitor/job/clear`,
      method: "delete",
    });
  },

  OptionJob(params: JobOptionData) {
    return request<ApiResponse>({
      url: `/monitor/job/option`,
      method: "put",
      data: params,
    });
  },

  // 获取定时任务运行日志（实时状态）
  getJobRunLog() {
    return request<ApiResponse<JobRunLog[]>>({
      url: `/monitor/job/log`,
      method: "get",
    });
  },

  // 获取定时任务日志详情
  getJobLogDetail(id: number) {
    return request<ApiResponse<JobLogDetail>>({
      url: `/monitor/job/log/detail/${id}`,
      method: "get",
    });
  },

  // 查询定时任务日志列表
  getJobLogList(query: JobLogPageQuery) {
    return request<ApiResponse<PageResult<JobLogTable[]>>>({
      url: `/monitor/job/log/list`,
      method: "get",
      params: query,
    });
  },

  // 删除定时任务日志
  deleteJobLog(ids: number[]) {
    return request<ApiResponse>({
      url: `/monitor/job/log/delete`,
      method: "delete",
      data: ids,
    });
  },

  // 清空定时任务日志
  clearJobLog() {
    return request<ApiResponse>({
      url: `/monitor/job/log/clear`,
      method: "delete",
    });
  },

  // 导出定时任务日志
  exportJobLog(query: JobLogPageQuery) {
    return request<Blob>({
      url: `/monitor/job/log/export`,
      method: "post",
      data: query,
      responseType: "blob",
    });
  },

};

export default JobAPI;

export interface JobPageQuery extends PageQuery {
  name?: string;
  status?: boolean;
  /** 开始时间 */
  start_time?: string;
  /** 结束时间 */
  end_time?: string;
}

export interface JobLogPageQuery extends PageQuery {
  status?: boolean;
  /** 开始时间 */
  start_time?: string;
  /** 结束时间 */
  end_time?: string;
}

export interface JobOptionData {
  id?: number;
  option?: number; //操作类型 1: 暂停 2: 恢复 3: 重启
}

export interface JobTable {
  index?: number;
  id: number;
  name: string;
  func?: string;
  trigger?: string;
  args?: string;
  kwargs?: string;
  coalesce?: boolean;
  max_instances?: number;
  jobstore?: string;
  executor?: string;
  trigger_args?: string;
  start_date?: string;
  end_date?: string;
  status?: boolean;
  description?: string;
  created_at?: string;
  updated_at?: string;
  creator?: creatorType;
}

export interface JobForm {
  id?: number;
  name?: string;
  func?: string;
  trigger?: string;
  args?: string;
  kwargs?: string;
  coalesce?: boolean;
  max_instances?: number;
  jobstore?: string;
  executor?: string;
  trigger_args?: string;
  start_date?: string;
  end_date?: string;
  status?: boolean;
  description?: string;
}

// 定时任务运行日志接口（对应Scheduler实时状态）
export interface JobRunLog {
  id: string;
  name: string;
  trigger: string;
  executor: string;
  func: string;
  func_ref: string;
  args: any[];
  kwargs: any;
  misfire_grace_time: number;
  coalesce: boolean;
  max_instances: number;
  next_run_time: string;
  state: string;
}

// 定时任务日志详情接口（对应数据库日志表）
export interface JobLogDetail {
  id: number;
  job_name: string;
  job_group: string;
  job_executor: string;
  invoke_target: string;
  job_args?: string;
  job_kwargs?: string;
  job_trigger?: string;
  job_message?: string;
  status: boolean;
  exception_info?: string;
  create_time: string;
}

// 定时任务日志列表接口（对应数据库日志表）
export interface JobLogTable {
  index?: number;
  id: number;
  job_name: string;
  job_group: string;
  job_executor: string;
  invoke_target: string;
  job_args?: string;
  job_kwargs?: string;
  job_trigger?: string;
  job_message?: string;
  status: boolean;
  exception_info?: string;
  create_time: string;
}
