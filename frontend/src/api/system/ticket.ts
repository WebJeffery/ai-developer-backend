import request from "@/utils/request";

const TicketAPI = {
  getTicketList(query: TicketPageQuery) {
    return request<ApiResponse<PageResult<TicketTable[]>>>({
      url: `/system/ticket/list`,
      method: "get",
      params: query,
    });
  },

  getTicketDetail(query: number) {
    return request<ApiResponse<TicketTable>>({
      url: `/system/ticket/detail/${query}`,
      method: "get",
    });
  },

  createTicket(body: TicketForm) {
    return request<ApiResponse>({
      url: `/system/ticket/create`,
      method: "post",
      data: body,
    });
  },

  updateTicket(id: number, body: TicketForm) {
    return request<ApiResponse>({
      url: `/system/ticket/update/${id}`,
      method: "put",
      data: body,
    });
  },

  deleteTicket(body: number[]) {
    return request<ApiResponse>({
      url: `/system/ticket/delete`,
      method: "delete",
      data: body,
    });
  },

};

export default TicketAPI;

export interface TicketPageQuery extends PageQuery {
  title?: string;
  status?: string;
  priority?: string;
  start_time?: string;
  end_time?: string;
}

export interface TicketTable {
  index?: number;
  id?: number;
  title?: string;
  priority?: string;
  type?: string;
  status?: string;
  description?: string;
  assignee?: creatorType;
  reporter?: creatorType;
  project?: string;
  version?: string;
  created_at?: string;
  updated_at?: string;
  creator?: creatorType;
}

export interface TicketForm {
  id?: number;
  title: string;
  priority?: string;
  type?: string;
  status?: string;
  description?: string;
  assignee_id?: number;
  reporter_id: number;
  project?: string;
  version?: string;
}