--
-- PostgreSQL database dump
--

-- Dumped from database version 17.5 (ServBay)
-- Dumped by pg_dump version 17.5 (ServBay)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: ai_mcp; Type: TABLE; Schema: public; Owner: tao
--

CREATE TABLE public.ai_mcp (
    name character varying(50) NOT NULL,
    type integer NOT NULL,
    url character varying(255),
    command character varying(255),
    args character varying(255),
    env json,
    creator_id integer,
    id integer NOT NULL,
    description text,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


ALTER TABLE public.ai_mcp OWNER TO tao;

--
-- Name: TABLE ai_mcp; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON TABLE public.ai_mcp IS 'MCP 服务器表';


--
-- Name: COLUMN ai_mcp.name; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.ai_mcp.name IS 'MCP 名称';


--
-- Name: COLUMN ai_mcp.type; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.ai_mcp.type IS 'MCP 类型（0:stdio 1:sse）';


--
-- Name: COLUMN ai_mcp.url; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.ai_mcp.url IS '远程 SSE 地址';


--
-- Name: COLUMN ai_mcp.command; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.ai_mcp.command IS 'MCP 命令';


--
-- Name: COLUMN ai_mcp.args; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.ai_mcp.args IS 'MCP 命令参数';


--
-- Name: COLUMN ai_mcp.env; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.ai_mcp.env IS 'MCP 环境变量';


--
-- Name: COLUMN ai_mcp.creator_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.ai_mcp.creator_id IS '创建人ID';


--
-- Name: COLUMN ai_mcp.id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.ai_mcp.id IS '主键ID';


--
-- Name: COLUMN ai_mcp.description; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.ai_mcp.description IS '备注/描述';


--
-- Name: COLUMN ai_mcp.created_at; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.ai_mcp.created_at IS '创建时间';


--
-- Name: COLUMN ai_mcp.updated_at; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.ai_mcp.updated_at IS '更新时间';


--
-- Name: ai_mcp_id_seq; Type: SEQUENCE; Schema: public; Owner: tao
--

CREATE SEQUENCE public.ai_mcp_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.ai_mcp_id_seq OWNER TO tao;

--
-- Name: ai_mcp_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tao
--

ALTER SEQUENCE public.ai_mcp_id_seq OWNED BY public.ai_mcp.id;


--
-- Name: application_myapp; Type: TABLE; Schema: public; Owner: tao
--

CREATE TABLE public.application_myapp (
    name character varying(64) NOT NULL,
    status boolean NOT NULL,
    access_url character varying(500) NOT NULL,
    icon_url character varying(300),
    creator_id integer,
    id integer NOT NULL,
    description text,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


ALTER TABLE public.application_myapp OWNER TO tao;

--
-- Name: TABLE application_myapp; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON TABLE public.application_myapp IS '应用系统表';


--
-- Name: COLUMN application_myapp.name; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.application_myapp.name IS '应用名称';


--
-- Name: COLUMN application_myapp.status; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.application_myapp.status IS '是否启用(True:启用 False:禁用)';


--
-- Name: COLUMN application_myapp.access_url; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.application_myapp.access_url IS '访问地址';


--
-- Name: COLUMN application_myapp.icon_url; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.application_myapp.icon_url IS '应用图标URL';


--
-- Name: COLUMN application_myapp.creator_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.application_myapp.creator_id IS '创建人ID';


--
-- Name: COLUMN application_myapp.id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.application_myapp.id IS '主键ID';


--
-- Name: COLUMN application_myapp.description; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.application_myapp.description IS '备注/描述';


--
-- Name: COLUMN application_myapp.created_at; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.application_myapp.created_at IS '创建时间';


--
-- Name: COLUMN application_myapp.updated_at; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.application_myapp.updated_at IS '更新时间';


--
-- Name: application_myapp_id_seq; Type: SEQUENCE; Schema: public; Owner: tao
--

CREATE SEQUENCE public.application_myapp_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.application_myapp_id_seq OWNER TO tao;

--
-- Name: application_myapp_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tao
--

ALTER SEQUENCE public.application_myapp_id_seq OWNED BY public.application_myapp.id;


--
-- Name: example_demo; Type: TABLE; Schema: public; Owner: tao
--

CREATE TABLE public.example_demo (
    name character varying(64),
    status boolean NOT NULL,
    creator_id integer,
    id integer NOT NULL,
    description text,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


ALTER TABLE public.example_demo OWNER TO tao;

--
-- Name: TABLE example_demo; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON TABLE public.example_demo IS '示例表';


--
-- Name: COLUMN example_demo.name; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.example_demo.name IS '名称';


--
-- Name: COLUMN example_demo.status; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.example_demo.status IS '是否启用(True:启用 False:禁用)';


--
-- Name: COLUMN example_demo.creator_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.example_demo.creator_id IS '创建人ID';


--
-- Name: COLUMN example_demo.id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.example_demo.id IS '主键ID';


--
-- Name: COLUMN example_demo.description; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.example_demo.description IS '备注/描述';


--
-- Name: COLUMN example_demo.created_at; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.example_demo.created_at IS '创建时间';


--
-- Name: COLUMN example_demo.updated_at; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.example_demo.updated_at IS '更新时间';


--
-- Name: example_demo_id_seq; Type: SEQUENCE; Schema: public; Owner: tao
--

CREATE SEQUENCE public.example_demo_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.example_demo_id_seq OWNER TO tao;

--
-- Name: example_demo_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tao
--

ALTER SEQUENCE public.example_demo_id_seq OWNED BY public.example_demo.id;


--
-- Name: gen_table; Type: TABLE; Schema: public; Owner: tao
--

CREATE TABLE public.gen_table (
    table_name character varying(200),
    table_comment character varying(500),
    sub_table_name character varying(64),
    sub_table_fk_name character varying(64),
    class_name character varying(100),
    tpl_category character varying(200),
    tpl_web_type character varying(30),
    package_name character varying(100),
    module_name character varying(30),
    business_name character varying(30),
    function_name character varying(100),
    function_author character varying(100),
    gen_type character varying(1),
    gen_path character varying(200),
    options character varying(1000),
    creator_id integer,
    id integer NOT NULL,
    description text,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


ALTER TABLE public.gen_table OWNER TO tao;

--
-- Name: TABLE gen_table; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON TABLE public.gen_table IS '代码生成表';


--
-- Name: COLUMN gen_table.table_name; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table.table_name IS '表名称';


--
-- Name: COLUMN gen_table.table_comment; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table.table_comment IS '表描述';


--
-- Name: COLUMN gen_table.sub_table_name; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table.sub_table_name IS '关联子表的表名';


--
-- Name: COLUMN gen_table.sub_table_fk_name; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table.sub_table_fk_name IS '子表关联的外键名';


--
-- Name: COLUMN gen_table.class_name; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table.class_name IS '实体类名称';


--
-- Name: COLUMN gen_table.tpl_category; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table.tpl_category IS '使用的模板（crud单表操作 tree树表操作）';


--
-- Name: COLUMN gen_table.tpl_web_type; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table.tpl_web_type IS '前端模板类型（element-ui模版 element-plus模版）';


--
-- Name: COLUMN gen_table.package_name; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table.package_name IS '生成包路径';


--
-- Name: COLUMN gen_table.module_name; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table.module_name IS '生成模块名';


--
-- Name: COLUMN gen_table.business_name; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table.business_name IS '生成业务名';


--
-- Name: COLUMN gen_table.function_name; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table.function_name IS '生成功能名';


--
-- Name: COLUMN gen_table.function_author; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table.function_author IS '生成功能作者';


--
-- Name: COLUMN gen_table.gen_type; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table.gen_type IS '生成代码方式（0zip压缩包 1自定义路径）';


--
-- Name: COLUMN gen_table.gen_path; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table.gen_path IS '生成路径（不填默认项目路径）';


--
-- Name: COLUMN gen_table.options; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table.options IS '其它生成选项';


--
-- Name: COLUMN gen_table.creator_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table.creator_id IS '创建人ID';


--
-- Name: COLUMN gen_table.id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table.id IS '主键ID';


--
-- Name: COLUMN gen_table.description; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table.description IS '备注/描述';


--
-- Name: COLUMN gen_table.created_at; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table.created_at IS '创建时间';


--
-- Name: COLUMN gen_table.updated_at; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table.updated_at IS '更新时间';


--
-- Name: gen_table_column; Type: TABLE; Schema: public; Owner: tao
--

CREATE TABLE public.gen_table_column (
    column_name character varying(200),
    column_comment character varying(500),
    column_type character varying(100),
    python_type character varying(500),
    python_field character varying(200),
    is_pk character varying(1),
    is_increment character varying(1),
    is_required character varying(1),
    is_unique character varying(1),
    is_insert character varying(1),
    is_edit character varying(1),
    is_list character varying(1),
    is_query character varying(1),
    query_type character varying(200),
    html_type character varying(200),
    dict_type character varying(200),
    sort integer,
    table_id integer,
    creator_id integer,
    id integer NOT NULL,
    description text,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


ALTER TABLE public.gen_table_column OWNER TO tao;

--
-- Name: TABLE gen_table_column; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON TABLE public.gen_table_column IS '代码生成表字段';


--
-- Name: COLUMN gen_table_column.column_name; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table_column.column_name IS '列名称';


--
-- Name: COLUMN gen_table_column.column_comment; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table_column.column_comment IS '列描述';


--
-- Name: COLUMN gen_table_column.column_type; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table_column.column_type IS '列类型';


--
-- Name: COLUMN gen_table_column.python_type; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table_column.python_type IS 'PYTHON类型';


--
-- Name: COLUMN gen_table_column.python_field; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table_column.python_field IS 'PYTHON字段名';


--
-- Name: COLUMN gen_table_column.is_pk; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table_column.is_pk IS '是否主键（1是）';


--
-- Name: COLUMN gen_table_column.is_increment; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table_column.is_increment IS '是否自增（1是）';


--
-- Name: COLUMN gen_table_column.is_required; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table_column.is_required IS '是否必填（1是）';


--
-- Name: COLUMN gen_table_column.is_unique; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table_column.is_unique IS '是否唯一（1是）';


--
-- Name: COLUMN gen_table_column.is_insert; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table_column.is_insert IS '是否为插入字段（1是）';


--
-- Name: COLUMN gen_table_column.is_edit; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table_column.is_edit IS '是否编辑字段（1是）';


--
-- Name: COLUMN gen_table_column.is_list; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table_column.is_list IS '是否列表字段（1是）';


--
-- Name: COLUMN gen_table_column.is_query; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table_column.is_query IS '是否查询字段（1是）';


--
-- Name: COLUMN gen_table_column.query_type; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table_column.query_type IS '查询方式（等于、不等于、大于、小于、范围）';


--
-- Name: COLUMN gen_table_column.html_type; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table_column.html_type IS '显示类型（文本框、文本域、下拉框、复选框、单选框、日期控件）';


--
-- Name: COLUMN gen_table_column.dict_type; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table_column.dict_type IS '字典类型';


--
-- Name: COLUMN gen_table_column.sort; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table_column.sort IS '排序';


--
-- Name: COLUMN gen_table_column.table_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table_column.table_id IS '归属表编号';


--
-- Name: COLUMN gen_table_column.creator_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table_column.creator_id IS '创建人ID';


--
-- Name: COLUMN gen_table_column.id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table_column.id IS '主键ID';


--
-- Name: COLUMN gen_table_column.description; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table_column.description IS '备注/描述';


--
-- Name: COLUMN gen_table_column.created_at; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table_column.created_at IS '创建时间';


--
-- Name: COLUMN gen_table_column.updated_at; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table_column.updated_at IS '更新时间';


--
-- Name: gen_table_column_id_seq; Type: SEQUENCE; Schema: public; Owner: tao
--

CREATE SEQUENCE public.gen_table_column_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.gen_table_column_id_seq OWNER TO tao;

--
-- Name: gen_table_column_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tao
--

ALTER SEQUENCE public.gen_table_column_id_seq OWNED BY public.gen_table_column.id;


--
-- Name: gen_table_id_seq; Type: SEQUENCE; Schema: public; Owner: tao
--

CREATE SEQUENCE public.gen_table_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.gen_table_id_seq OWNER TO tao;

--
-- Name: gen_table_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tao
--

ALTER SEQUENCE public.gen_table_id_seq OWNED BY public.gen_table.id;


--
-- Name: monitor_job; Type: TABLE; Schema: public; Owner: tao
--

CREATE TABLE public.monitor_job (
    name character varying(64),
    jobstore character varying(64),
    executor character varying(64),
    trigger character varying(64) NOT NULL,
    trigger_args text,
    func text NOT NULL,
    args text,
    kwargs text,
    "coalesce" boolean,
    max_instances integer,
    start_date character varying(64),
    end_date character varying(64),
    status boolean NOT NULL,
    creator_id integer,
    id integer NOT NULL,
    description text,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


ALTER TABLE public.monitor_job OWNER TO tao;

--
-- Name: TABLE monitor_job; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON TABLE public.monitor_job IS '定时任务调度表';


--
-- Name: COLUMN monitor_job.name; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.monitor_job.name IS '任务名称';


--
-- Name: COLUMN monitor_job.jobstore; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.monitor_job.jobstore IS '存储器';


--
-- Name: COLUMN monitor_job.executor; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.monitor_job.executor IS '执行器:将运行此作业的执行程序的名称';


--
-- Name: COLUMN monitor_job.trigger; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.monitor_job.trigger IS '触发器:控制此作业计划的 trigger 对象';


--
-- Name: COLUMN monitor_job.trigger_args; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.monitor_job.trigger_args IS '触发器参数';


--
-- Name: COLUMN monitor_job.func; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.monitor_job.func IS '任务函数';


--
-- Name: COLUMN monitor_job.args; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.monitor_job.args IS '位置参数';


--
-- Name: COLUMN monitor_job.kwargs; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.monitor_job.kwargs IS '关键字参数';


--
-- Name: COLUMN monitor_job."coalesce"; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.monitor_job."coalesce" IS '是否合并运行:是否在多个运行时间到期时仅运行作业一次';


--
-- Name: COLUMN monitor_job.max_instances; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.monitor_job.max_instances IS '最大实例数:允许的最大并发执行实例数 工作';


--
-- Name: COLUMN monitor_job.start_date; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.monitor_job.start_date IS '开始时间';


--
-- Name: COLUMN monitor_job.end_date; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.monitor_job.end_date IS '结束时间';


--
-- Name: COLUMN monitor_job.status; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.monitor_job.status IS '是否启用(True:启用 False:禁用)';


--
-- Name: COLUMN monitor_job.creator_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.monitor_job.creator_id IS '创建人ID';


--
-- Name: COLUMN monitor_job.id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.monitor_job.id IS '主键ID';


--
-- Name: COLUMN monitor_job.description; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.monitor_job.description IS '备注/描述';


--
-- Name: COLUMN monitor_job.created_at; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.monitor_job.created_at IS '创建时间';


--
-- Name: COLUMN monitor_job.updated_at; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.monitor_job.updated_at IS '更新时间';


--
-- Name: monitor_job_id_seq; Type: SEQUENCE; Schema: public; Owner: tao
--

CREATE SEQUENCE public.monitor_job_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.monitor_job_id_seq OWNER TO tao;

--
-- Name: monitor_job_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tao
--

ALTER SEQUENCE public.monitor_job_id_seq OWNED BY public.monitor_job.id;


--
-- Name: monitor_job_log; Type: TABLE; Schema: public; Owner: tao
--

CREATE TABLE public.monitor_job_log (
    id integer NOT NULL,
    job_name character varying(64) NOT NULL,
    job_group character varying(64) NOT NULL,
    job_executor character varying(64) NOT NULL,
    invoke_target character varying(500) NOT NULL,
    job_args character varying(255),
    job_kwargs character varying(255),
    job_trigger character varying(255),
    job_message character varying(500),
    exception_info character varying(2000),
    job_id integer
);


ALTER TABLE public.monitor_job_log OWNER TO tao;

--
-- Name: TABLE monitor_job_log; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON TABLE public.monitor_job_log IS '定时任务调度日志表';


--
-- Name: COLUMN monitor_job_log.id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.monitor_job_log.id IS '主键ID';


--
-- Name: COLUMN monitor_job_log.job_name; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.monitor_job_log.job_name IS '任务名称';


--
-- Name: COLUMN monitor_job_log.job_group; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.monitor_job_log.job_group IS '任务组名';


--
-- Name: COLUMN monitor_job_log.job_executor; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.monitor_job_log.job_executor IS '任务执行器';


--
-- Name: COLUMN monitor_job_log.invoke_target; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.monitor_job_log.invoke_target IS '调用目标字符串';


--
-- Name: COLUMN monitor_job_log.job_args; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.monitor_job_log.job_args IS '位置参数';


--
-- Name: COLUMN monitor_job_log.job_kwargs; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.monitor_job_log.job_kwargs IS '关键字参数';


--
-- Name: COLUMN monitor_job_log.job_trigger; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.monitor_job_log.job_trigger IS '任务触发器';


--
-- Name: COLUMN monitor_job_log.job_message; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.monitor_job_log.job_message IS '日志信息';


--
-- Name: COLUMN monitor_job_log.exception_info; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.monitor_job_log.exception_info IS '异常信息';


--
-- Name: COLUMN monitor_job_log.job_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.monitor_job_log.job_id IS '任务ID';


--
-- Name: monitor_job_log_id_seq; Type: SEQUENCE; Schema: public; Owner: tao
--

CREATE SEQUENCE public.monitor_job_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.monitor_job_log_id_seq OWNER TO tao;

--
-- Name: monitor_job_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tao
--

ALTER SEQUENCE public.monitor_job_log_id_seq OWNED BY public.monitor_job_log.id;


--
-- Name: system_dept; Type: TABLE; Schema: public; Owner: tao
--

CREATE TABLE public.system_dept (
    id integer NOT NULL,
    name character varying(40) NOT NULL,
    "order" integer NOT NULL,
    code character varying(20),
    status boolean NOT NULL,
    parent_id integer,
    description text,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


ALTER TABLE public.system_dept OWNER TO tao;

--
-- Name: TABLE system_dept; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON TABLE public.system_dept IS '部门表';


--
-- Name: COLUMN system_dept.id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_dept.id IS '主键ID';


--
-- Name: COLUMN system_dept.name; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_dept.name IS '部门名称';


--
-- Name: COLUMN system_dept."order"; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_dept."order" IS '显示排序';


--
-- Name: COLUMN system_dept.code; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_dept.code IS '部门编码';


--
-- Name: COLUMN system_dept.status; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_dept.status IS '是否启用(True:启用 False:禁用)';


--
-- Name: COLUMN system_dept.parent_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_dept.parent_id IS '父级部门ID';


--
-- Name: COLUMN system_dept.description; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_dept.description IS '备注/描述';


--
-- Name: COLUMN system_dept.created_at; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_dept.created_at IS '创建时间';


--
-- Name: COLUMN system_dept.updated_at; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_dept.updated_at IS '更新时间';


--
-- Name: system_dept_id_seq; Type: SEQUENCE; Schema: public; Owner: tao
--

CREATE SEQUENCE public.system_dept_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.system_dept_id_seq OWNER TO tao;

--
-- Name: system_dept_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tao
--

ALTER SEQUENCE public.system_dept_id_seq OWNED BY public.system_dept.id;


--
-- Name: system_dict_data; Type: TABLE; Schema: public; Owner: tao
--

CREATE TABLE public.system_dict_data (
    dict_sort integer NOT NULL,
    dict_label character varying(100) NOT NULL,
    dict_value character varying(100) NOT NULL,
    dict_type character varying(100) NOT NULL,
    status boolean NOT NULL,
    css_class character varying(100),
    list_class character varying(100),
    is_default boolean NOT NULL,
    dict_type_id integer,
    creator_id integer,
    id integer NOT NULL,
    description text,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


ALTER TABLE public.system_dict_data OWNER TO tao;

--
-- Name: TABLE system_dict_data; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON TABLE public.system_dict_data IS '字典数据表';


--
-- Name: COLUMN system_dict_data.dict_sort; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_dict_data.dict_sort IS '字典排序';


--
-- Name: COLUMN system_dict_data.dict_label; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_dict_data.dict_label IS '字典标签';


--
-- Name: COLUMN system_dict_data.dict_value; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_dict_data.dict_value IS '字典键值';


--
-- Name: COLUMN system_dict_data.dict_type; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_dict_data.dict_type IS '字典类型';


--
-- Name: COLUMN system_dict_data.status; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_dict_data.status IS '是否启用(True:启用 False:禁用)';


--
-- Name: COLUMN system_dict_data.css_class; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_dict_data.css_class IS '样式属性（其他样式扩展）';


--
-- Name: COLUMN system_dict_data.list_class; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_dict_data.list_class IS '表格回显样式';


--
-- Name: COLUMN system_dict_data.is_default; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_dict_data.is_default IS '是否默认（True是 False否）';


--
-- Name: COLUMN system_dict_data.dict_type_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_dict_data.dict_type_id IS '字典类型ID';


--
-- Name: COLUMN system_dict_data.creator_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_dict_data.creator_id IS '创建人ID';


--
-- Name: COLUMN system_dict_data.id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_dict_data.id IS '主键ID';


--
-- Name: COLUMN system_dict_data.description; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_dict_data.description IS '备注/描述';


--
-- Name: COLUMN system_dict_data.created_at; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_dict_data.created_at IS '创建时间';


--
-- Name: COLUMN system_dict_data.updated_at; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_dict_data.updated_at IS '更新时间';


--
-- Name: system_dict_data_id_seq; Type: SEQUENCE; Schema: public; Owner: tao
--

CREATE SEQUENCE public.system_dict_data_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.system_dict_data_id_seq OWNER TO tao;

--
-- Name: system_dict_data_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tao
--

ALTER SEQUENCE public.system_dict_data_id_seq OWNED BY public.system_dict_data.id;


--
-- Name: system_dict_type; Type: TABLE; Schema: public; Owner: tao
--

CREATE TABLE public.system_dict_type (
    dict_name character varying(100) NOT NULL,
    dict_type character varying(100) NOT NULL,
    status boolean NOT NULL,
    creator_id integer,
    id integer NOT NULL,
    description text,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


ALTER TABLE public.system_dict_type OWNER TO tao;

--
-- Name: TABLE system_dict_type; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON TABLE public.system_dict_type IS '字典类型表';


--
-- Name: COLUMN system_dict_type.dict_name; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_dict_type.dict_name IS '字典名称';


--
-- Name: COLUMN system_dict_type.dict_type; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_dict_type.dict_type IS '字典类型';


--
-- Name: COLUMN system_dict_type.status; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_dict_type.status IS '是否启用(True:启用 False:禁用)';


--
-- Name: COLUMN system_dict_type.creator_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_dict_type.creator_id IS '创建人ID';


--
-- Name: COLUMN system_dict_type.id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_dict_type.id IS '主键ID';


--
-- Name: COLUMN system_dict_type.description; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_dict_type.description IS '备注/描述';


--
-- Name: COLUMN system_dict_type.created_at; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_dict_type.created_at IS '创建时间';


--
-- Name: COLUMN system_dict_type.updated_at; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_dict_type.updated_at IS '更新时间';


--
-- Name: system_dict_type_id_seq; Type: SEQUENCE; Schema: public; Owner: tao
--

CREATE SEQUENCE public.system_dict_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.system_dict_type_id_seq OWNER TO tao;

--
-- Name: system_dict_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tao
--

ALTER SEQUENCE public.system_dict_type_id_seq OWNED BY public.system_dict_type.id;


--
-- Name: system_log; Type: TABLE; Schema: public; Owner: tao
--

CREATE TABLE public.system_log (
    type integer NOT NULL,
    request_path character varying(255) NOT NULL,
    request_method character varying(10) NOT NULL,
    request_payload text,
    request_ip character varying(50),
    login_location character varying(255),
    request_os character varying(64),
    request_browser character varying(64),
    response_code integer NOT NULL,
    response_json text,
    process_time character varying(20),
    creator_id integer,
    id integer NOT NULL,
    description text,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


ALTER TABLE public.system_log OWNER TO tao;

--
-- Name: TABLE system_log; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON TABLE public.system_log IS '系统日志表';


--
-- Name: COLUMN system_log.type; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_log.type IS '日志类型(1登录日志 2操作日志)';


--
-- Name: COLUMN system_log.request_path; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_log.request_path IS '请求路径';


--
-- Name: COLUMN system_log.request_method; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_log.request_method IS '请求方式';


--
-- Name: COLUMN system_log.request_payload; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_log.request_payload IS '请求体';


--
-- Name: COLUMN system_log.request_ip; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_log.request_ip IS '请求IP地址';


--
-- Name: COLUMN system_log.login_location; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_log.login_location IS '登录位置';


--
-- Name: COLUMN system_log.request_os; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_log.request_os IS '操作系统';


--
-- Name: COLUMN system_log.request_browser; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_log.request_browser IS '浏览器';


--
-- Name: COLUMN system_log.response_code; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_log.response_code IS '响应状态码';


--
-- Name: COLUMN system_log.response_json; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_log.response_json IS '响应体';


--
-- Name: COLUMN system_log.process_time; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_log.process_time IS '处理时间';


--
-- Name: COLUMN system_log.creator_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_log.creator_id IS '创建人ID';


--
-- Name: COLUMN system_log.id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_log.id IS '主键ID';


--
-- Name: COLUMN system_log.description; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_log.description IS '备注/描述';


--
-- Name: COLUMN system_log.created_at; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_log.created_at IS '创建时间';


--
-- Name: COLUMN system_log.updated_at; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_log.updated_at IS '更新时间';


--
-- Name: system_log_id_seq; Type: SEQUENCE; Schema: public; Owner: tao
--

CREATE SEQUENCE public.system_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.system_log_id_seq OWNER TO tao;

--
-- Name: system_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tao
--

ALTER SEQUENCE public.system_log_id_seq OWNED BY public.system_log.id;


--
-- Name: system_menu; Type: TABLE; Schema: public; Owner: tao
--

CREATE TABLE public.system_menu (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    type integer NOT NULL,
    "order" integer NOT NULL,
    status boolean NOT NULL,
    permission character varying(100),
    icon character varying(50),
    route_name character varying(100),
    route_path character varying(200),
    component_path character varying(200),
    redirect character varying(200),
    hidden boolean NOT NULL,
    keep_alive boolean NOT NULL,
    always_show boolean NOT NULL,
    title character varying(50),
    params json,
    affix boolean NOT NULL,
    parent_id integer,
    description text,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


ALTER TABLE public.system_menu OWNER TO tao;

--
-- Name: TABLE system_menu; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON TABLE public.system_menu IS '菜单表';


--
-- Name: COLUMN system_menu.id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_menu.id IS '主键ID';


--
-- Name: COLUMN system_menu.name; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_menu.name IS '菜单名称';


--
-- Name: COLUMN system_menu.type; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_menu.type IS '菜单类型(1:目录 2:菜单 3:按钮/权限 4:链接)';


--
-- Name: COLUMN system_menu."order"; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_menu."order" IS '显示排序';


--
-- Name: COLUMN system_menu.status; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_menu.status IS '是否启用(True:启用 False:禁用)';


--
-- Name: COLUMN system_menu.permission; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_menu.permission IS '权限标识(如：system:user:list)';


--
-- Name: COLUMN system_menu.icon; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_menu.icon IS '菜单图标';


--
-- Name: COLUMN system_menu.route_name; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_menu.route_name IS '路由名称';


--
-- Name: COLUMN system_menu.route_path; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_menu.route_path IS '路由路径';


--
-- Name: COLUMN system_menu.component_path; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_menu.component_path IS '组件路径';


--
-- Name: COLUMN system_menu.redirect; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_menu.redirect IS '重定向地址';


--
-- Name: COLUMN system_menu.hidden; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_menu.hidden IS '是否隐藏(True:隐藏 False:显示)';


--
-- Name: COLUMN system_menu.keep_alive; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_menu.keep_alive IS '是否缓存(True:是 False:否)';


--
-- Name: COLUMN system_menu.always_show; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_menu.always_show IS '是否始终显示(True:是 False:否)';


--
-- Name: COLUMN system_menu.title; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_menu.title IS '菜单标题';


--
-- Name: COLUMN system_menu.params; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_menu.params IS '路由参数(JSON对象)';


--
-- Name: COLUMN system_menu.affix; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_menu.affix IS '是否固定标签页(True:是 False:否)';


--
-- Name: COLUMN system_menu.parent_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_menu.parent_id IS '父菜单ID';


--
-- Name: COLUMN system_menu.description; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_menu.description IS '备注/描述';


--
-- Name: COLUMN system_menu.created_at; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_menu.created_at IS '创建时间';


--
-- Name: COLUMN system_menu.updated_at; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_menu.updated_at IS '更新时间';


--
-- Name: system_menu_id_seq; Type: SEQUENCE; Schema: public; Owner: tao
--

CREATE SEQUENCE public.system_menu_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.system_menu_id_seq OWNER TO tao;

--
-- Name: system_menu_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tao
--

ALTER SEQUENCE public.system_menu_id_seq OWNED BY public.system_menu.id;


--
-- Name: system_notice; Type: TABLE; Schema: public; Owner: tao
--

CREATE TABLE public.system_notice (
    notice_title character varying(50) NOT NULL,
    notice_type character varying(50) NOT NULL,
    notice_content text,
    status boolean NOT NULL,
    creator_id integer,
    id integer NOT NULL,
    description text,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


ALTER TABLE public.system_notice OWNER TO tao;

--
-- Name: TABLE system_notice; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON TABLE public.system_notice IS '通知公告表';


--
-- Name: COLUMN system_notice.notice_title; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_notice.notice_title IS '公告标题';


--
-- Name: COLUMN system_notice.notice_type; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_notice.notice_type IS '公告类型（1通知 2公告）';


--
-- Name: COLUMN system_notice.notice_content; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_notice.notice_content IS '公告内容';


--
-- Name: COLUMN system_notice.status; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_notice.status IS '是否启用(True:启用 False:禁用)';


--
-- Name: COLUMN system_notice.creator_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_notice.creator_id IS '创建人ID';


--
-- Name: COLUMN system_notice.id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_notice.id IS '主键ID';


--
-- Name: COLUMN system_notice.description; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_notice.description IS '备注/描述';


--
-- Name: COLUMN system_notice.created_at; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_notice.created_at IS '创建时间';


--
-- Name: COLUMN system_notice.updated_at; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_notice.updated_at IS '更新时间';


--
-- Name: system_notice_id_seq; Type: SEQUENCE; Schema: public; Owner: tao
--

CREATE SEQUENCE public.system_notice_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.system_notice_id_seq OWNER TO tao;

--
-- Name: system_notice_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tao
--

ALTER SEQUENCE public.system_notice_id_seq OWNED BY public.system_notice.id;


--
-- Name: system_param; Type: TABLE; Schema: public; Owner: tao
--

CREATE TABLE public.system_param (
    config_name character varying(500) NOT NULL,
    config_key character varying(500) NOT NULL,
    config_value character varying(500),
    config_type boolean,
    status boolean NOT NULL,
    creator_id integer,
    id integer NOT NULL,
    description text,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


ALTER TABLE public.system_param OWNER TO tao;

--
-- Name: TABLE system_param; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON TABLE public.system_param IS '系统参数表';


--
-- Name: COLUMN system_param.config_name; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_param.config_name IS '参数名称';


--
-- Name: COLUMN system_param.config_key; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_param.config_key IS '参数键名';


--
-- Name: COLUMN system_param.config_value; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_param.config_value IS '参数键值';


--
-- Name: COLUMN system_param.config_type; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_param.config_type IS '系统内置(True:是 False:否)';


--
-- Name: COLUMN system_param.status; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_param.status IS '是否启用(True:启用 False:禁用)';


--
-- Name: COLUMN system_param.creator_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_param.creator_id IS '创建人ID';


--
-- Name: COLUMN system_param.id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_param.id IS '主键ID';


--
-- Name: COLUMN system_param.description; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_param.description IS '备注/描述';


--
-- Name: COLUMN system_param.created_at; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_param.created_at IS '创建时间';


--
-- Name: COLUMN system_param.updated_at; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_param.updated_at IS '更新时间';


--
-- Name: system_param_id_seq; Type: SEQUENCE; Schema: public; Owner: tao
--

CREATE SEQUENCE public.system_param_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.system_param_id_seq OWNER TO tao;

--
-- Name: system_param_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tao
--

ALTER SEQUENCE public.system_param_id_seq OWNED BY public.system_param.id;


--
-- Name: system_position; Type: TABLE; Schema: public; Owner: tao
--

CREATE TABLE public.system_position (
    name character varying(40) NOT NULL,
    "order" integer NOT NULL,
    status boolean NOT NULL,
    creator_id integer,
    id integer NOT NULL,
    description text,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


ALTER TABLE public.system_position OWNER TO tao;

--
-- Name: TABLE system_position; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON TABLE public.system_position IS '岗位表';


--
-- Name: COLUMN system_position.name; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_position.name IS '岗位名称';


--
-- Name: COLUMN system_position."order"; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_position."order" IS '显示排序';


--
-- Name: COLUMN system_position.status; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_position.status IS '是否启用(True:启用 False:禁用)';


--
-- Name: COLUMN system_position.creator_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_position.creator_id IS '创建人ID';


--
-- Name: COLUMN system_position.id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_position.id IS '主键ID';


--
-- Name: COLUMN system_position.description; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_position.description IS '备注/描述';


--
-- Name: COLUMN system_position.created_at; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_position.created_at IS '创建时间';


--
-- Name: COLUMN system_position.updated_at; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_position.updated_at IS '更新时间';


--
-- Name: system_position_id_seq; Type: SEQUENCE; Schema: public; Owner: tao
--

CREATE SEQUENCE public.system_position_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.system_position_id_seq OWNER TO tao;

--
-- Name: system_position_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tao
--

ALTER SEQUENCE public.system_position_id_seq OWNED BY public.system_position.id;


--
-- Name: system_role; Type: TABLE; Schema: public; Owner: tao
--

CREATE TABLE public.system_role (
    name character varying(40) NOT NULL,
    code character varying(20),
    "order" integer NOT NULL,
    status boolean NOT NULL,
    data_scope integer NOT NULL,
    creator_id integer,
    id integer NOT NULL,
    description text,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


ALTER TABLE public.system_role OWNER TO tao;

--
-- Name: TABLE system_role; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON TABLE public.system_role IS '角色表';


--
-- Name: COLUMN system_role.name; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_role.name IS '角色名称';


--
-- Name: COLUMN system_role.code; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_role.code IS '角色编码';


--
-- Name: COLUMN system_role."order"; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_role."order" IS '显示排序';


--
-- Name: COLUMN system_role.status; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_role.status IS '是否启用(True:启用 False:禁用)';


--
-- Name: COLUMN system_role.data_scope; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_role.data_scope IS '数据权限范围';


--
-- Name: COLUMN system_role.creator_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_role.creator_id IS '创建人ID';


--
-- Name: COLUMN system_role.id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_role.id IS '主键ID';


--
-- Name: COLUMN system_role.description; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_role.description IS '备注/描述';


--
-- Name: COLUMN system_role.created_at; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_role.created_at IS '创建时间';


--
-- Name: COLUMN system_role.updated_at; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_role.updated_at IS '更新时间';


--
-- Name: system_role_depts; Type: TABLE; Schema: public; Owner: tao
--

CREATE TABLE public.system_role_depts (
    role_id integer NOT NULL,
    dept_id integer NOT NULL
);


ALTER TABLE public.system_role_depts OWNER TO tao;

--
-- Name: TABLE system_role_depts; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON TABLE public.system_role_depts IS '角色部门关联表';


--
-- Name: COLUMN system_role_depts.role_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_role_depts.role_id IS '角色ID';


--
-- Name: COLUMN system_role_depts.dept_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_role_depts.dept_id IS '部门ID';


--
-- Name: system_role_id_seq; Type: SEQUENCE; Schema: public; Owner: tao
--

CREATE SEQUENCE public.system_role_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.system_role_id_seq OWNER TO tao;

--
-- Name: system_role_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tao
--

ALTER SEQUENCE public.system_role_id_seq OWNED BY public.system_role.id;


--
-- Name: system_role_menus; Type: TABLE; Schema: public; Owner: tao
--

CREATE TABLE public.system_role_menus (
    role_id integer NOT NULL,
    menu_id integer NOT NULL
);


ALTER TABLE public.system_role_menus OWNER TO tao;

--
-- Name: TABLE system_role_menus; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON TABLE public.system_role_menus IS '角色菜单关联表';


--
-- Name: COLUMN system_role_menus.role_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_role_menus.role_id IS '角色ID';


--
-- Name: COLUMN system_role_menus.menu_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_role_menus.menu_id IS '菜单ID';


--
-- Name: system_user_positions; Type: TABLE; Schema: public; Owner: tao
--

CREATE TABLE public.system_user_positions (
    user_id integer NOT NULL,
    position_id integer NOT NULL
);


ALTER TABLE public.system_user_positions OWNER TO tao;

--
-- Name: TABLE system_user_positions; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON TABLE public.system_user_positions IS '用户岗位关联表';


--
-- Name: COLUMN system_user_positions.user_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_user_positions.user_id IS '用户ID';


--
-- Name: COLUMN system_user_positions.position_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_user_positions.position_id IS '岗位ID';


--
-- Name: system_user_roles; Type: TABLE; Schema: public; Owner: tao
--

CREATE TABLE public.system_user_roles (
    user_id integer NOT NULL,
    role_id integer NOT NULL
);


ALTER TABLE public.system_user_roles OWNER TO tao;

--
-- Name: TABLE system_user_roles; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON TABLE public.system_user_roles IS '用户角色关联表';


--
-- Name: COLUMN system_user_roles.user_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_user_roles.user_id IS '用户ID';


--
-- Name: COLUMN system_user_roles.role_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_user_roles.role_id IS '角色ID';


--
-- Name: system_users; Type: TABLE; Schema: public; Owner: tao
--

CREATE TABLE public.system_users (
    username character varying(32) NOT NULL,
    password character varying(255) NOT NULL,
    name character varying(32) NOT NULL,
    status boolean NOT NULL,
    mobile character varying(20),
    email character varying(64),
    gender character varying(1),
    avatar character varying(500),
    is_superuser boolean NOT NULL,
    last_login timestamp with time zone,
    dept_id integer,
    creator_id integer,
    id integer NOT NULL,
    description text,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


ALTER TABLE public.system_users OWNER TO tao;

--
-- Name: TABLE system_users; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON TABLE public.system_users IS '用户表';


--
-- Name: COLUMN system_users.username; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_users.username IS '用户名/登录账号';


--
-- Name: COLUMN system_users.password; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_users.password IS '密码哈希';


--
-- Name: COLUMN system_users.name; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_users.name IS '昵称';


--
-- Name: COLUMN system_users.status; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_users.status IS '是否启用(True:启用 False:禁用)';


--
-- Name: COLUMN system_users.mobile; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_users.mobile IS '手机号';


--
-- Name: COLUMN system_users.email; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_users.email IS '邮箱';


--
-- Name: COLUMN system_users.gender; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_users.gender IS '性别(0:男 1:女 2:未知)';


--
-- Name: COLUMN system_users.avatar; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_users.avatar IS '头像URL地址';


--
-- Name: COLUMN system_users.is_superuser; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_users.is_superuser IS '是否超管';


--
-- Name: COLUMN system_users.last_login; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_users.last_login IS '最后登录时间';


--
-- Name: COLUMN system_users.dept_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_users.dept_id IS '部门ID';


--
-- Name: COLUMN system_users.creator_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_users.creator_id IS '创建人ID';


--
-- Name: COLUMN system_users.id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_users.id IS '主键ID';


--
-- Name: COLUMN system_users.description; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_users.description IS '备注/描述';


--
-- Name: COLUMN system_users.created_at; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_users.created_at IS '创建时间';


--
-- Name: COLUMN system_users.updated_at; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_users.updated_at IS '更新时间';


--
-- Name: system_users_id_seq; Type: SEQUENCE; Schema: public; Owner: tao
--

CREATE SEQUENCE public.system_users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.system_users_id_seq OWNER TO tao;

--
-- Name: system_users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tao
--

ALTER SEQUENCE public.system_users_id_seq OWNED BY public.system_users.id;


--
-- Name: ai_mcp id; Type: DEFAULT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.ai_mcp ALTER COLUMN id SET DEFAULT nextval('public.ai_mcp_id_seq'::regclass);


--
-- Name: application_myapp id; Type: DEFAULT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.application_myapp ALTER COLUMN id SET DEFAULT nextval('public.application_myapp_id_seq'::regclass);


--
-- Name: example_demo id; Type: DEFAULT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.example_demo ALTER COLUMN id SET DEFAULT nextval('public.example_demo_id_seq'::regclass);


--
-- Name: gen_table id; Type: DEFAULT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.gen_table ALTER COLUMN id SET DEFAULT nextval('public.gen_table_id_seq'::regclass);


--
-- Name: gen_table_column id; Type: DEFAULT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.gen_table_column ALTER COLUMN id SET DEFAULT nextval('public.gen_table_column_id_seq'::regclass);


--
-- Name: monitor_job id; Type: DEFAULT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.monitor_job ALTER COLUMN id SET DEFAULT nextval('public.monitor_job_id_seq'::regclass);


--
-- Name: monitor_job_log id; Type: DEFAULT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.monitor_job_log ALTER COLUMN id SET DEFAULT nextval('public.monitor_job_log_id_seq'::regclass);


--
-- Name: system_dept id; Type: DEFAULT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_dept ALTER COLUMN id SET DEFAULT nextval('public.system_dept_id_seq'::regclass);


--
-- Name: system_dict_data id; Type: DEFAULT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_dict_data ALTER COLUMN id SET DEFAULT nextval('public.system_dict_data_id_seq'::regclass);


--
-- Name: system_dict_type id; Type: DEFAULT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_dict_type ALTER COLUMN id SET DEFAULT nextval('public.system_dict_type_id_seq'::regclass);


--
-- Name: system_log id; Type: DEFAULT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_log ALTER COLUMN id SET DEFAULT nextval('public.system_log_id_seq'::regclass);


--
-- Name: system_menu id; Type: DEFAULT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_menu ALTER COLUMN id SET DEFAULT nextval('public.system_menu_id_seq'::regclass);


--
-- Name: system_notice id; Type: DEFAULT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_notice ALTER COLUMN id SET DEFAULT nextval('public.system_notice_id_seq'::regclass);


--
-- Name: system_param id; Type: DEFAULT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_param ALTER COLUMN id SET DEFAULT nextval('public.system_param_id_seq'::regclass);


--
-- Name: system_position id; Type: DEFAULT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_position ALTER COLUMN id SET DEFAULT nextval('public.system_position_id_seq'::regclass);


--
-- Name: system_role id; Type: DEFAULT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_role ALTER COLUMN id SET DEFAULT nextval('public.system_role_id_seq'::regclass);


--
-- Name: system_users id; Type: DEFAULT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_users ALTER COLUMN id SET DEFAULT nextval('public.system_users_id_seq'::regclass);


--
-- Data for Name: ai_mcp; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.ai_mcp (name, type, url, command, args, env, creator_id, id, description, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: application_myapp; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.application_myapp (name, status, access_url, icon_url, creator_id, id, description, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: example_demo; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.example_demo (name, status, creator_id, id, description, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: gen_table; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.gen_table (table_name, table_comment, sub_table_name, sub_table_fk_name, class_name, tpl_category, tpl_web_type, package_name, module_name, business_name, function_name, function_author, gen_type, gen_path, options, creator_id, id, description, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: gen_table_column; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.gen_table_column (column_name, column_comment, column_type, python_type, python_field, is_pk, is_increment, is_required, is_unique, is_insert, is_edit, is_list, is_query, query_type, html_type, dict_type, sort, table_id, creator_id, id, description, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: monitor_job; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.monitor_job (name, jobstore, executor, trigger, trigger_args, func, args, kwargs, "coalesce", max_instances, start_date, end_date, status, creator_id, id, description, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: monitor_job_log; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.monitor_job_log (id, job_name, job_group, job_executor, invoke_target, job_args, job_kwargs, job_trigger, job_message, exception_info, job_id) FROM stdin;
\.


--
-- Data for Name: system_dept; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.system_dept (id, name, "order", code, status, parent_id, description, created_at, updated_at) FROM stdin;
1	集团总公司	1	GROUP001	t	\N	集团总公司	2025-09-28 23:39:32.492608	2025-09-28 23:39:32.492612
2	北京分公司	1	BJ001	t	1	北京分公司	2025-09-28 23:39:32.494236	2025-09-28 23:39:32.494238
3	上海分公司	2	SH001	t	1	上海分公司	2025-09-28 23:39:32.494238	2025-09-28 23:39:32.494239
4	技术部	1	TECH001	t	2	技术部	2025-09-28 23:39:32.495062	2025-09-28 23:39:32.495063
5	销售部	2	SALES001	t	2	销售部	2025-09-28 23:39:32.495064	2025-09-28 23:39:32.495064
6	市场部	1	MARKET001	t	3	市场部	2025-09-28 23:39:32.495064	2025-09-28 23:39:32.495065
7	人事部	2	HR001	t	3	人事部	2025-09-28 23:39:32.495065	2025-09-28 23:39:32.495065
\.


--
-- Data for Name: system_dict_data; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.system_dict_data (dict_sort, dict_label, dict_value, dict_type, status, css_class, list_class, is_default, dict_type_id, creator_id, id, description, created_at, updated_at) FROM stdin;
1	男	0	sys_user_sex	t	blue	\N	t	\N	1	1	性别男	2025-09-28 23:39:32.532995	2025-09-28 23:39:32.532996
2	女	1	sys_user_sex	t	pink	\N	f	\N	1	2	性别女	2025-09-28 23:39:32.532996	2025-09-28 23:39:32.532997
3	未知	2	sys_user_sex	t	red	\N	f	\N	1	3	性别未知	2025-09-28 23:39:32.532997	2025-09-28 23:39:32.532997
1	启用	1	sys_common_status	t		primary	f	\N	1	4	启用状态	2025-09-28 23:39:32.532998	2025-09-28 23:39:32.532998
2	停用	0	sys_common_status	t		danger	f	\N	1	5	停用状态	2025-09-28 23:39:32.532999	2025-09-28 23:39:32.532999
1	是	1	sys_yes_no	t		primary	t	\N	1	6	是	2025-09-28 23:39:32.532999	2025-09-28 23:39:32.533
2	否	0	sys_yes_no	t		danger	f	\N	1	7	否	2025-09-28 23:39:32.533	2025-09-28 23:39:32.533
99	其他	0	sys_oper_type	t		info	f	\N	1	8	其他操作	2025-09-28 23:39:32.533001	2025-09-28 23:39:32.533001
1	新增	1	sys_oper_type	t		info	f	\N	1	9	新增操作	2025-09-28 23:39:32.533001	2025-09-28 23:39:32.533002
2	修改	2	sys_oper_type	t		info	f	\N	1	10	修改操作	2025-09-28 23:39:32.533002	2025-09-28 23:39:32.533002
3	删除	3	sys_oper_type	t		danger	f	\N	1	11	删除操作	2025-09-28 23:39:32.533003	2025-09-28 23:39:32.533003
4	分配权限	4	sys_oper_type	t		primary	f	\N	1	12	授权操作	2025-09-28 23:39:32.533003	2025-09-28 23:39:32.533004
5	导出	5	sys_oper_type	t		warning	f	\N	1	13	导出操作	2025-09-28 23:39:32.533004	2025-09-28 23:39:32.533004
6	导入	6	sys_oper_type	t		warning	f	\N	1	14	导入操作	2025-09-28 23:39:32.533005	2025-09-28 23:39:32.533005
7	强退	7	sys_oper_type	t		danger	f	\N	1	15	强退操作	2025-09-28 23:39:32.533005	2025-09-28 23:39:32.533006
8	生成代码	8	sys_oper_type	t		warning	f	\N	1	16	生成操作	2025-09-28 23:39:32.533006	2025-09-28 23:39:32.533006
9	清空数据	9	sys_oper_type	t		danger	f	\N	1	17	清空操作	2025-09-28 23:39:32.533007	2025-09-28 23:39:32.533007
1	通知	1	sys_notice_type	t	blue	warning	t	\N	1	18	通知	2025-09-28 23:39:32.533007	2025-09-28 23:39:32.533008
2	公告	2	sys_notice_type	t	orange	success	f	\N	1	19	公告	2025-09-28 23:39:32.533008	2025-09-28 23:39:32.533008
1	默认(Memory)	default	sys_job_store	t		\N	t	\N	1	20	默认分组	2025-09-28 23:39:32.533009	2025-09-28 23:39:32.533009
2	数据库(Sqlalchemy)	sqlalchemy	sys_job_store	t		\N	f	\N	1	21	数据库分组	2025-09-28 23:39:32.533009	2025-09-28 23:39:32.53301
3	数据库(Redis)	redis	sys_job_store	t		\N	f	\N	1	22	reids分组	2025-09-28 23:39:32.53301	2025-09-28 23:39:32.53301
1	线程池	default	sys_job_executor	t		\N	f	\N	1	23	线程池	2025-09-28 23:39:32.533011	2025-09-28 23:39:32.533011
2	进程池	processpool	sys_job_executor	t		\N	f	\N	1	24	进程池	2025-09-28 23:39:32.533012	2025-09-28 23:39:32.533012
1	演示函数	scheduler_test.job	sys_job_function	t		\N	t	\N	1	25	演示函数	2025-09-28 23:39:32.533012	2025-09-28 23:39:32.533012
1	指定日期(date)	date	sys_job_trigger	t		\N	t	\N	1	26	指定日期任务触发器	2025-09-28 23:39:32.533013	2025-09-28 23:39:32.533013
2	间隔触发器(interval)	interval	sys_job_trigger	t		\N	f	\N	1	27	间隔触发器任务触发器	2025-09-28 23:39:32.533014	2025-09-28 23:39:32.533014
3	cron表达式	cron	sys_job_trigger	t		\N	f	\N	1	28	间隔触发器任务触发器	2025-09-28 23:39:32.533014	2025-09-28 23:39:32.533015
1	默认(default)	default	sys_list_class	t		\N	t	\N	1	29	默认表格回显样式	2025-09-28 23:39:32.533015	2025-09-28 23:39:32.533015
2	主要(primary)	primary	sys_list_class	t		\N	f	\N	1	30	主要表格回显样式	2025-09-28 23:39:32.533016	2025-09-28 23:39:32.533016
3	成功(success)	success	sys_list_class	t		\N	f	\N	1	31	成功表格回显样式	2025-09-28 23:39:32.533016	2025-09-28 23:39:32.533017
4	信息(info)	info	sys_list_class	t		\N	f	\N	1	32	信息表格回显样式	2025-09-28 23:39:32.533017	2025-09-28 23:39:32.533017
5	警告(warning)	warning	sys_list_class	t		\N	f	\N	1	33	警告表格回显样式	2025-09-28 23:39:32.533018	2025-09-28 23:39:32.533018
6	危险(danger)	danger	sys_list_class	t		\N	f	\N	1	34	危险表格回显样式	2025-09-28 23:39:32.533018	2025-09-28 23:39:32.533019
\.


--
-- Data for Name: system_dict_type; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.system_dict_type (dict_name, dict_type, status, creator_id, id, description, created_at, updated_at) FROM stdin;
用户性别	sys_user_sex	t	1	1	用户性别列表	2025-09-28 23:39:32.529905	2025-09-28 23:39:32.529906
系统是否	sys_yes_no	t	1	2	系统是否列表	2025-09-28 23:39:32.529907	2025-09-28 23:39:32.529907
系统状态	sys_common_status	t	1	3	系统状态	2025-09-28 23:39:32.529908	2025-09-28 23:39:32.529908
通知类型	sys_notice_type	t	1	4	通知类型列表	2025-09-28 23:39:32.529908	2025-09-28 23:39:32.529909
操作类型	sys_oper_type	t	1	5	操作类型列表	2025-09-28 23:39:32.529909	2025-09-28 23:39:32.529909
任务存储器	sys_job_store	t	1	6	任务分组列表	2025-09-28 23:39:32.52991	2025-09-28 23:39:32.52991
任务执行器	sys_job_executor	t	1	7	任务执行器列表	2025-09-28 23:39:32.52991	2025-09-28 23:39:32.529911
任务函数	sys_job_function	t	1	8	任务函数列表	2025-09-28 23:39:32.529911	2025-09-28 23:39:32.529912
任务触发器	sys_job_trigger	t	1	9	任务触发器列表	2025-09-28 23:39:32.529912	2025-09-28 23:39:32.529912
表格回显样式	sys_list_class	t	1	10	表格回显样式列表	2025-09-28 23:39:32.529913	2025-09-28 23:39:32.529913
\.


--
-- Data for Name: system_log; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.system_log (type, request_path, request_method, request_payload, request_ip, login_location, request_os, request_browser, response_code, response_json, process_time, creator_id, id, description, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: system_menu; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.system_menu (id, name, type, "order", status, permission, icon, route_name, route_path, component_path, redirect, hidden, keep_alive, always_show, title, params, affix, parent_id, description, created_at, updated_at) FROM stdin;
1	仪表盘	1	1	t		client	Dashboard	/dashboard	\N	/dashboard/workplace	f	t	t	仪表盘	null	f	\N	初始化数据	2025-09-28 23:39:32.503574	2025-09-28 23:39:32.503576
2	系统管理	1	2	t	\N	system	System	/system	\N	/system/menu	f	t	f	系统管理	null	f	\N	初始化数据	2025-09-28 23:39:32.503576	2025-09-28 23:39:32.503577
3	监控管理	1	3	t	\N	monitor	Monitor	/monitor	\N	/monitor/online	f	f	f	监控管理	null	f	\N	初始化数据	2025-09-28 23:39:32.503577	2025-09-28 23:39:32.503577
4	公共模块	1	4	t	\N	document	Common	/common	\N	/common/docs	f	f	f	公共模块	null	f	\N	初始化数据	2025-09-28 23:39:32.503578	2025-09-28 23:39:32.503578
5	演示模块	1	5	t	\N	el-icon-Document	Demo	/demo	\N	/demo/example	f	f	f	演示模块	null	f	\N	初始化数据	2025-09-28 23:39:32.503579	2025-09-28 23:39:32.503579
6	应用管理	1	6	t	\N	el-icon-ShoppingBag	Application	/application	\N	/application/myapp	f	f	f	应用管理	null	f	\N	初始化数据	2025-09-28 23:39:32.503579	2025-09-28 23:39:32.50358
7	AI大模型	1	8	t	\N	el-icon-Pointer	AI	/ai	\N	/ai/mcp	f	f	f	AI大模型	null	f	\N	AI大模型管理	2025-09-28 23:39:32.50358	2025-09-28 23:39:32.503581
8	代码管理	1	9	t	\N	code	Gencode	/gencode	\N	/ai/mcp	f	f	f	代码管理	null	f	\N	代码管理	2025-09-28 23:39:32.503581	2025-09-28 23:39:32.503581
9	流程管理	1	10	t	\N	el-icon-ShoppingBag	Workflow	/workflow	\N	/workflow/operator	f	f	f	流程管理	null	f	\N	流程管理	2025-09-28 23:39:32.503582	2025-09-28 23:39:32.503582
10	工作台	2	1	t	dashboard:workplace:query	homepage	Workplace	/dashboard/workplace	dashboard/workplace	\N	f	t	f	工作台	null	t	1	初始化数据	2025-09-28 23:39:32.506188	2025-09-28 23:39:32.50619
11	分析页	2	2	t	dashboard:analysis:query	el-icon-PieChart	Analysis	/dashboard/analysis	dashboard/analysis	\N	f	t	f	分析页	null	f	1	初始化数据	2025-09-28 23:39:32.50619	2025-09-28 23:39:32.506191
12	菜单管理	2	1	t	system:menu:query	menu	Menu	/system/menu	system/menu/index	\N	f	t	f	菜单管理	null	f	2	初始化数据	2025-09-28 23:39:32.506191	2025-09-28 23:39:32.506191
13	部门管理	2	2	t	system:dept:query	tree	Dept	/system/dept	system/dept/index	\N	f	t	f	部门管理	null	f	2	初始化数据	2025-09-28 23:39:32.506192	2025-09-28 23:39:32.506192
14	岗位管理	2	3	t	system:position:query	el-icon-Coordinate	Position	/system/position	system/position/index	\N	f	t	f	岗位管理	null	f	2	初始化数据	2025-09-28 23:39:32.506193	2025-09-28 23:39:32.506193
15	角色管理	2	4	t	system:role:query	role	Role	/system/role	system/role/index	\N	f	t	f	角色管理	null	f	2	初始化数据	2025-09-28 23:39:32.506193	2025-09-28 23:39:32.506194
16	用户管理	2	5	t	system:user:query	el-icon-User	User	/system/user	system/user/index	\N	f	t	f	用户管理	null	f	2	初始化数据	2025-09-28 23:39:32.506194	2025-09-28 23:39:32.506194
17	日志管理	2	6	t	system:log:query	el-icon-Aim	Log	/system/log	system/log/index	\N	f	t	f	日志管理	null	f	2	初始化数据	2025-09-28 23:39:32.506195	2025-09-28 23:39:32.506195
18	公告管理	2	7	t	system:notice:query	bell	Notice	/system/notice	system/notice/index	\N	f	t	f	公告管理	null	f	2	初始化数据	2025-09-28 23:39:32.506195	2025-09-28 23:39:32.506196
19	参数管理	2	8	t	system:param:query	setting	Config	/system/config	system/config/index	\N	f	t	f	参数管理	null	f	2	初始化数据	2025-09-28 23:39:32.506196	2025-09-28 23:39:32.506196
20	字典管理	2	9	t	system:dict_type:query	dict	Dict	/system/dict	system/dict/index	\N	f	t	f	字典管理	null	f	2	初始化数据	2025-09-28 23:39:32.506197	2025-09-28 23:39:32.506197
21	任务管理	2	1	t	monitor:job:query	el-icon-DataLine	Job	/monitor/job	monitor/job/index	\N	f	t	f	任务管理	null	f	3	初始化数据	2025-09-28 23:39:32.506198	2025-09-28 23:39:32.506198
22	在线用户	2	2	t	monitor:online:query	el-icon-Headset	MonitorOnline	/monitor/online	monitor/online/index	\N	f	f	f	在线用户	null	f	3	初始化数据	2025-09-28 23:39:32.506198	2025-09-28 23:39:32.506199
23	服务器监控	2	3	t	monitor:server:query	el-icon-Odometer	MonitorServer	/monitor/server	monitor/server/index	\N	f	f	f	服务器监控	null	f	3	初始化数据	2025-09-28 23:39:32.506199	2025-09-28 23:39:32.506199
24	缓存监控	2	4	t	monitor:cache:query	el-icon-Stopwatch	MonitorCache	/monitor/cache	monitor/cache/index	\N	f	f	f	缓存监控	null	f	3	初始化数据	2025-09-28 23:39:32.5062	2025-09-28 23:39:32.5062
25	文件管理	2	1	t	monitor:resource:query	el-icon-Files	Resource	/monitor/resource	monitor/resource/index	\N	f	t	f	文件管理	null	f	3	初始化数据	2025-09-28 23:39:32.5062	2025-09-28 23:39:32.506201
26	接口管理	4	1	t	common:docs:query	api	Docs	/common/docs	common/docs/index	\N	f	f	f	接口管理	null	f	4	初始化数据	2025-09-28 23:39:32.506201	2025-09-28 23:39:32.506201
27	文档管理	4	2	t	common:redoc:query	el-icon-Document	Redoc	/common/redoc	common/redoc/index	\N	f	f	f	文档管理	null	f	4	初始化数据	2025-09-28 23:39:32.506202	2025-09-28 23:39:32.506202
28	示例管理	2	1	t	demo:example:query	el-icon-DataLine	Example	/demo/example	demo/example/index	\N	f	t	f	示例管理	null	f	5	初始化数据	2025-09-28 23:39:32.506202	2025-09-28 23:39:32.506203
29	我的应用	2	1	t	application:myapp:query	el-icon-ShoppingCartFull	ApplicationSystem	/application/myapp	application/myapp/index	\N	f	t	f	我的应用	null	f	6	初始化数据	2025-09-28 23:39:32.506203	2025-09-28 23:39:32.506203
30	MCP应用	2	1	t	ai:mcp:chat	el-icon-ToiletPaper	MCP	/ai/mcp	ai/mcp/index	\N	f	t	f	MCP应用	null	f	7	MCP智能助手	2025-09-28 23:39:32.506204	2025-09-28 23:39:32.506204
31	代码生成	2	1	t	generator:gencode:query	code	Backcode	/gencode/backcode	gencode/backcode/index	\N	f	t	f	代码生成	null	f	8	代码生成	2025-09-28 23:39:32.506204	2025-09-28 23:39:32.506205
32	前端构建	2	2	t	gencode:webcode:query	el-icon-Wallet	webcode	/gencode/webcode	gencode/webcode/index	\N	f	t	f	前端构建	null	f	8	前端构建	2025-09-28 23:39:32.506205	2025-09-28 23:39:32.506205
33	我的流程	2	1	t	workflow:operator:query	el-icon-ShoppingBag	Operator	/workflow/operator	workflow/operator/index	\N	f	t	f	我的流程	null	f	9	我的流程	2025-09-28 23:39:32.506206	2025-09-28 23:39:32.506206
34	创建菜单	3	1	t	system:menu:create	\N	\N	\N	\N	\N	f	t	f	创建菜单	null	f	12	初始化数据	2025-09-28 23:39:32.509226	2025-09-28 23:39:32.509227
35	修改菜单	3	2	t	system:menu:update	\N	\N	\N	\N	\N	f	t	f	修改菜单	null	f	12	初始化数据	2025-09-28 23:39:32.509228	2025-09-28 23:39:32.509228
36	删除菜单	3	3	t	system:menu:delete	\N	\N	\N	\N	\N	f	t	f	删除菜单	null	f	12	初始化数据	2025-09-28 23:39:32.509228	2025-09-28 23:39:32.509229
37	批量修改菜单状态	3	4	t	system:menu:patch	\N	\N	\N	\N	\N	f	t	f	批量修改菜单状态	null	f	12	初始化数据	2025-09-28 23:39:32.509229	2025-09-28 23:39:32.509229
38	创建部门	3	1	t	system:dept:create	\N	\N	\N	\N	\N	f	t	f	创建部门	null	f	13	初始化数据	2025-09-28 23:39:32.50923	2025-09-28 23:39:32.50923
39	修改部门	3	2	t	system:dept:update	\N	\N	\N	\N	\N	f	t	f	修改部门	null	f	13	初始化数据	2025-09-28 23:39:32.509231	2025-09-28 23:39:32.509231
40	删除部门	3	3	t	system:dept:delete	\N	\N	\N	\N	\N	f	t	f	删除部门	null	f	13	初始化数据	2025-09-28 23:39:32.509231	2025-09-28 23:39:32.509232
41	批量修改部门状态	3	4	t	system:dept:patch	\N	\N	\N	\N	\N	f	t	f	批量修改部门状态	null	f	13	初始化数据	2025-09-28 23:39:32.509232	2025-09-28 23:39:32.509232
42	创建岗位	3	1	t	system:position:create	\N	\N	\N	\N	\N	f	t	f	创建岗位	null	f	14	初始化数据	2025-09-28 23:39:32.509233	2025-09-28 23:39:32.509233
43	修改岗位	3	2	t	system:position:update	\N	\N	\N	\N	\N	f	t	f	修改岗位	null	f	14	初始化数据	2025-09-28 23:39:32.509233	2025-09-28 23:39:32.509234
44	删除岗位	3	3	t	system:position:delete	\N	\N	\N	\N	\N	f	t	f	修改岗位	null	f	14	初始化数据	2025-09-28 23:39:32.509234	2025-09-28 23:39:32.509234
97	更新示例	3	2	t	demo:example:update	\N	\N	\N	\N	\N	f	t	f	更新示例	null	f	28	初始化数据	2025-09-28 23:39:32.509271	2025-09-28 23:39:32.509271
45	批量修改岗位状态	3	4	t	system:position:patch	\N	\N	\N	\N	\N	f	t	f	批量修改岗位状态	null	f	14	初始化数据	2025-09-28 23:39:32.509235	2025-09-28 23:39:32.509235
46	岗位导出	3	5	t	system:position:export	\N	\N	\N	\N	\N	f	t	f	岗位导出	null	f	14	初始化数据	2025-09-28 23:39:32.509236	2025-09-28 23:39:32.509236
47	设置角色权限	3	8	t	system:role:permission	\N	\N	\N	\N	\N	f	t	f	设置角色权限	null	f	14	初始化数据	2025-09-28 23:39:32.509236	2025-09-28 23:39:32.509237
48	创建角色	3	1	t	system:role:create	\N	\N	\N	\N	\N	f	t	f	创建角色	null	f	15	初始化数据	2025-09-28 23:39:32.509237	2025-09-28 23:39:32.509237
49	修改角色	3	2	t	system:role:update	\N	\N	\N	\N	\N	f	t	f	修改角色	null	f	15	初始化数据	2025-09-28 23:39:32.509238	2025-09-28 23:39:32.509238
50	删除角色	3	3	t	system:role:delete	\N	\N	\N	\N	\N	f	t	f	删除角色	null	f	15	初始化数据	2025-09-28 23:39:32.509238	2025-09-28 23:39:32.509239
51	批量修改角色状态	3	4	t	system:role:patch	\N	\N	\N	\N	\N	f	t	f	批量修改角色状态	null	f	15	初始化数据	2025-09-28 23:39:32.509239	2025-09-28 23:39:32.509239
52	角色导出	3	6	t	system:role:export	\N	\N	\N	\N	\N	f	t	f	角色导出	null	f	15	初始化数据	2025-09-28 23:39:32.50924	2025-09-28 23:39:32.50924
53	创建用户	3	1	t	system:user:create	\N	\N	\N	\N	\N	f	t	f	创建用户	null	f	16	初始化数据	2025-09-28 23:39:32.50924	2025-09-28 23:39:32.509241
54	修改用户	3	2	t	system:user:update	\N	\N	\N	\N	\N	f	t	f	修改用户	null	f	16	初始化数据	2025-09-28 23:39:32.509241	2025-09-28 23:39:32.509241
55	删除用户	3	3	t	system:user:delete	\N	\N	\N	\N	\N	f	t	f	删除用户	null	f	16	初始化数据	2025-09-28 23:39:32.509242	2025-09-28 23:39:32.509242
56	批量修改用户状态	3	4	t	system:user:patch	\N	\N	\N	\N	\N	f	t	f	批量修改用户状态	null	f	16	初始化数据	2025-09-28 23:39:32.509243	2025-09-28 23:39:32.509243
57	导出用户	3	5	t	system:user:export	\N	\N	\N	\N	\N	f	t	f	导出用户	null	f	16	初始化数据	2025-09-28 23:39:32.509243	2025-09-28 23:39:32.509244
58	导入用户	3	6	t	system:user:import	\N	\N	\N	\N	\N	f	t	f	导入用户	null	f	16	初始化数据	2025-09-28 23:39:32.509244	2025-09-28 23:39:32.509244
59	日志删除	3	1	t	system:operation_log:delete	\N	\N	\N	\N	\N	f	t	f	日志删除	null	f	17	初始化数据	2025-09-28 23:39:32.509245	2025-09-28 23:39:32.509245
60	日志导出	3	2	t	system:operation_log:export	\N	\N	\N	\N	\N	f	t	f	日志导出	null	f	17	初始化数据	2025-09-28 23:39:32.509245	2025-09-28 23:39:32.509246
61	公告创建	3	1	t	system:notice:create	\N	\N	\N	\N	\N	f	t	f	公告创建	null	f	18	初始化数据	2025-09-28 23:39:32.509246	2025-09-28 23:39:32.509246
62	公告修改	3	2	t	system:notice:update	\N	\N	\N	\N	\N	f	t	f	修改用户	null	f	18	初始化数据	2025-09-28 23:39:32.509247	2025-09-28 23:39:32.509247
63	公告删除	3	3	t	system:notice:delete	\N	\N	\N	\N	\N	f	t	f	公告删除	null	f	18	初始化数据	2025-09-28 23:39:32.509247	2025-09-28 23:39:32.509248
64	公告导出	3	4	t	system:notice:export	\N	\N	\N	\N	\N	f	t	f	公告导出	null	f	18	初始化数据	2025-09-28 23:39:32.509248	2025-09-28 23:39:32.509248
65	公告批量修改状态	3	5	t	system:notice:patch	\N	\N	\N	\N	\N	f	t	f	公告批量修改状态	null	f	18	初始化数据	2025-09-28 23:39:32.509249	2025-09-28 23:39:32.509249
66	创建参数	3	1	t	system:param:create	\N	\N	\N	\N	\N	f	t	f	创建参数	null	f	19	初始化数据	2025-09-28 23:39:32.509249	2025-09-28 23:39:32.50925
67	修改参数	3	2	t	system:param:update	\N	\N	\N	\N	\N	f	t	f	修改参数	null	f	19	初始化数据	2025-09-28 23:39:32.50925	2025-09-28 23:39:32.50925
68	删除参数	3	3	t	system:param:delete	\N	\N	\N	\N	\N	f	t	f	删除参数	null	f	19	初始化数据	2025-09-28 23:39:32.509251	2025-09-28 23:39:32.509251
69	导出参数	3	4	t	system:param:export	\N	\N	\N	\N	\N	f	t	f	导出参数	null	f	19	初始化数据	2025-09-28 23:39:32.509251	2025-09-28 23:39:32.509252
70	参数上传	3	5	t	system:param:upload	\N	\N	\N	\N	\N	f	t	f	参数上传	null	f	19	初始化数据	2025-09-28 23:39:32.509252	2025-09-28 23:39:32.509252
71	创建字典类型	3	1	t	system:dict_type:create	\N	\N	\N	\N	\N	f	t	f	创建字典类型	null	f	20	初始化数据	2025-09-28 23:39:32.509253	2025-09-28 23:39:32.509253
72	修改字典类型	3	2	t	system:dict_type:update	\N	\N	\N	\N	\N	f	t	f	修改字典类型	null	f	20	初始化数据	2025-09-28 23:39:32.509253	2025-09-28 23:39:32.509254
73	删除字典类型	3	3	t	system:dict_type:delete	\N	\N	\N	\N	\N	f	t	f	删除字典类型	null	f	20	初始化数据	2025-09-28 23:39:32.509254	2025-09-28 23:39:32.509254
74	导出字典类型	3	4	t	system:dict_type:export	\N	\N	\N	\N	\N	f	t	f	导出字典类型	null	f	20	初始化数据	2025-09-28 23:39:32.509255	2025-09-28 23:39:32.509255
75	批量修改字典状态	3	5	t	system:dict_type:patch	\N	\N	\N	\N	\N	f	t	f	导出字典类型	null	f	20	初始化数据	2025-09-28 23:39:32.509255	2025-09-28 23:39:32.509256
76	字典数据查询	3	6	t	system:dict_data:query	\N	\N	\N	\N	\N	f	t	f	字典数据查询	null	f	20	初始化数据	2025-09-28 23:39:32.509256	2025-09-28 23:39:32.509257
77	创建字典数据	3	7	t	system:dict_data:create	\N	\N	\N	\N	\N	f	t	f	创建字典数据	null	f	20	初始化数据	2025-09-28 23:39:32.509257	2025-09-28 23:39:32.509257
78	修改字典数据	3	8	t	system:dict_data:update	\N	\N	\N	\N	\N	f	t	f	修改字典数据	null	f	20	初始化数据	2025-09-28 23:39:32.509258	2025-09-28 23:39:32.509258
79	删除字典数据	3	9	t	system:dict_data:delete	\N	\N	\N	\N	\N	f	t	f	删除字典数据	null	f	20	初始化数据	2025-09-28 23:39:32.509258	2025-09-28 23:39:32.509259
80	导出字典数据	3	10	t	system:dict_data:export	\N	\N	\N	\N	\N	f	t	f	导出字典数据	null	f	20	初始化数据	2025-09-28 23:39:32.509259	2025-09-28 23:39:32.509259
81	批量修改字典数据状态	3	11	t	system:dict_data:patch	\N	\N	\N	\N	\N	f	t	f	批量修改字典数据状态	null	f	20	初始化数据	2025-09-28 23:39:32.50926	2025-09-28 23:39:32.50926
82	创建任务	3	1	t	monitor:job:create	\N	\N	\N	\N	\N	f	t	f	创建任务	null	f	21	初始化数据	2025-09-28 23:39:32.50926	2025-09-28 23:39:32.509261
83	修改和操作任务	3	2	t	monitor:job:update	\N	\N	\N	\N	\N	f	t	f	修改和操作任务	null	f	21	初始化数据	2025-09-28 23:39:32.509261	2025-09-28 23:39:32.509261
84	删除和清除任务	3	3	t	monitor:job:delete	\N	\N	\N	\N	\N	f	t	f	删除和清除任务	null	f	21	初始化数据	2025-09-28 23:39:32.509262	2025-09-28 23:39:32.509262
85	导出定时任务	3	4	t	monitor:job:export	\N	\N	\N	\N	\N	f	t	f	导出定时任务	null	f	21	初始化数据	2025-09-28 23:39:32.509262	2025-09-28 23:39:32.509263
86	在线用户强制下线	3	1	t	monitor:online:delete	\N	\N	\N	\N	\N	f	f	f	在线用户强制下线	null	f	22	初始化数据	2025-09-28 23:39:32.509263	2025-09-28 23:39:32.509264
87	清除缓存	3	1	t	monitor:cache:delete	\N	\N	\N	\N	\N	f	f	f	清除缓存	null	f	24	初始化数据	2025-09-28 23:39:32.509264	2025-09-28 23:39:32.509264
88	文件上传	3	1	t	monitor:resource:upload	\N	\N	\N	\N	\N	f	t	f	文件上传	null	f	25	初始化数据	2025-09-28 23:39:32.509265	2025-09-28 23:39:32.509265
89	文件下载	3	2	t	monitor:resource:download	\N	\N	\N	\N	\N	f	t	f	文件下载	null	f	25	初始化数据	2025-09-28 23:39:32.509265	2025-09-28 23:39:32.509266
90	文件删除	3	3	t	monitor:resource:delete	\N	\N	\N	\N	\N	f	t	f	文件删除	null	f	25	初始化数据	2025-09-28 23:39:32.509266	2025-09-28 23:39:32.509266
91	文件移动	3	4	t	monitor:resource:move	\N	\N	\N	\N	\N	f	t	f	文件移动	null	f	25	初始化数据	2025-09-28 23:39:32.509267	2025-09-28 23:39:32.509267
92	文件复制	3	5	t	rmonitor:resource:copy	\N	\N	\N	\N	\N	f	t	f	文件复制	null	f	25	初始化数据	2025-09-28 23:39:32.509267	2025-09-28 23:39:32.509268
93	文件重命名	3	6	t	monitor:resource:rename	\N	\N	\N	\N	\N	f	t	f	文件重命名	null	f	25	初始化数据	2025-09-28 23:39:32.509268	2025-09-28 23:39:32.509268
94	创建目录	3	7	t	monitor:resource:create_dir	\N	\N	\N	\N	\N	f	t	f	创建目录	null	f	25	初始化数据	2025-09-28 23:39:32.509269	2025-09-28 23:39:32.509269
95	导出文件列表	3	9	t	rmonitor:resource:export	\N	\N	\N	\N	\N	f	t	f	导出文件列表	null	f	25	初始化数据	2025-09-28 23:39:32.509269	2025-09-28 23:39:32.50927
96	创建示例	3	1	t	demo:example:create	\N	\N	\N	\N	\N	f	t	f	创建示例	null	f	28	初始化数据	2025-09-28 23:39:32.50927	2025-09-28 23:39:32.50927
98	删除示例	3	3	t	demo:example:delete	\N	\N	\N	\N	\N	f	t	f	删除示例	null	f	28	初始化数据	2025-09-28 23:39:32.509271	2025-09-28 23:39:32.509272
99	批量修改示例状态	3	4	t	demo:example:patch	\N	\N	\N	\N	\N	f	t	f	批量修改示例状态	null	f	28	初始化数据	2025-09-28 23:39:32.509272	2025-09-28 23:39:32.509273
100	导出示例	3	5	t	demo:example:export	\N	\N	\N	\N	\N	f	t	f	导出示例	null	f	28	初始化数据	2025-09-28 23:39:32.509273	2025-09-28 23:39:32.509273
101	导入示例	3	6	t	demo:example:import	\N	\N	\N	\N	\N	f	t	f	导入示例	null	f	28	初始化数据	2025-09-28 23:39:32.509274	2025-09-28 23:39:32.509274
102	下载导入示例模版	3	7	t	demo:example:download	\N	\N	\N	\N	\N	f	t	f	下载导入示例模版	null	f	28	初始化数据	2025-09-28 23:39:32.509274	2025-09-28 23:39:32.509275
103	创建应用	3	1	t	application:myapp:create	\N	\N	\N	\N	\N	f	t	f	创建应用	null	f	29	初始化数据	2025-09-28 23:39:32.509275	2025-09-28 23:39:32.509275
104	修改应用	3	2	t	application:myapp:update	\N	\N	\N	\N	\N	f	t	f	修改应用	null	f	29	初始化数据	2025-09-28 23:39:32.509276	2025-09-28 23:39:32.509276
105	删除应用	3	3	t	application:myapp:delete	\N	\N	\N	\N	\N	f	t	f	删除应用	null	f	29	初始化数据	2025-09-28 23:39:32.509276	2025-09-28 23:39:32.509277
106	批量修改应用状态	3	4	t	application:myapp:patch	\N	\N	\N	\N	\N	f	t	f	批量修改应用状态	null	f	29	初始化数据	2025-09-28 23:39:32.509277	2025-09-28 23:39:32.509277
107	智能对话	3	1	t	ai:mcp:chat	\N	\N	\N	\N	\N	f	t	f	智能对话	null	f	30	智能对话	2025-09-28 23:39:32.509278	2025-09-28 23:39:32.509278
108	查询代码生成业务表列表	3	1	t	generator:gencode:query	\N	\N	\N	\N	\N	f	t	f	查询代码生成业务表列表	null	f	31	查询代码生成业务表列表	2025-09-28 23:39:32.509279	2025-09-28 23:39:32.509279
109	创建表结构	3	2	t	generator:gencode:create	\N	\N	\N	\N	\N	f	t	f	创建表结构	null	f	31	创建表结构	2025-09-28 23:39:32.509279	2025-09-28 23:39:32.50928
110	编辑业务表信息	3	3	t	generator:gencode:update	\N	\N	\N	\N	\N	f	t	f	编辑业务表信息	null	f	31	编辑业务表信息	2025-09-28 23:39:32.50928	2025-09-28 23:39:32.50928
111	删除业务表信息	3	4	t	generator:gencode:delete	\N	\N	\N	\N	\N	f	t	f	删除业务表信息	null	f	31	删除业务表信息	2025-09-28 23:39:32.509281	2025-09-28 23:39:32.509281
112	导入表结构	3	5	t	generator:gencode:import	\N	\N	\N	\N	\N	f	t	f	导入表结构	null	f	31	导入表结构	2025-09-28 23:39:32.509281	2025-09-28 23:39:32.509282
113	批量生成代码	3	6	t	generator:gencode:operate	\N	\N	\N	\N	\N	f	t	f	批量生成代码	null	f	31	批量生成代码	2025-09-28 23:39:32.509282	2025-09-28 23:39:32.509282
114	生成代码到指定路径	3	7	t	generator:gencode:code	\N	\N	\N	\N	\N	f	t	f	生成代码到指定路径	null	f	31	生成代码到指定路径	2025-09-28 23:39:32.509283	2025-09-28 23:39:32.509283
115	查询数据库表列表	3	8	t	generator:dblist:query	\N	\N	\N	\N	\N	f	t	f	查询数据库表列表	null	f	31	查询数据库表列表	2025-09-28 23:39:32.509283	2025-09-28 23:39:32.509284
116	同步数据库	3	9	t	generator:db:sync	\N	\N	\N	\N	\N	f	t	f	同步数据库	null	f	31	同步数据库	2025-09-28 23:39:32.509284	2025-09-28 23:39:32.509284
\.


--
-- Data for Name: system_notice; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.system_notice (notice_title, notice_type, notice_content, status, creator_id, id, description, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: system_param; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.system_param (config_name, config_key, config_value, config_type, status, creator_id, id, description, created_at, updated_at) FROM stdin;
网站名称	sys_web_title	FastAPI Vue3 Admin	t	t	1	1	网站名称	2025-09-28 23:39:32.527047	2025-09-28 23:39:32.527049
网站描述	sys_web_description	FastAPI Vue3 Admin 是完全开源的权限管理系统	t	t	1	2	网站描述	2025-09-28 23:39:32.527049	2025-09-28 23:39:32.52705
网页图标	sys_web_favicon	https://service.fastapiadmin.com/api/v1/static/image/favicon.png	t	t	1	3	网页图标	2025-09-28 23:39:32.52705	2025-09-28 23:39:32.527051
网站Logo	sys_web_logo	https://service.fastapiadmin.com/api/v1/static/image/logo.png	t	t	1	4	网站Logo	2025-09-28 23:39:32.527051	2025-09-28 23:39:32.527051
登录背景	sys_login_background	https://service.fastapiadmin.com/api/v1/static/image/background.svg	t	t	1	5	登录背景	2025-09-28 23:39:32.527052	2025-09-28 23:39:32.527052
版权信息	sys_web_copyright	Copyright © 2025-2026 service.fastapiadmin.com 版权所有	t	t	1	6	版权信息	2025-09-28 23:39:32.527053	2025-09-28 23:39:32.527053
备案信息	sys_keep_record	陕ICP备2025069493号-1	t	t	1	7	备案信息	2025-09-28 23:39:32.527053	2025-09-28 23:39:32.527054
帮助文档	sys_help_doc	https://service.fastapiadmin.com	t	t	1	8	帮助文档	2025-09-28 23:39:32.527054	2025-09-28 23:39:32.527054
隐私政策	sys_web_privacy	https://github.com/1014TaoTao/fastapi_vue3_admin/blob/master/LICENSE	t	t	1	9	隐私政策	2025-09-28 23:39:32.527055	2025-09-28 23:39:32.527055
用户协议	sys_web_clause	https://github.com/1014TaoTao/fastapi_vue3_admin/blob/master/LICENSE	t	t	1	10	用户协议	2025-09-28 23:39:32.527056	2025-09-28 23:39:32.527056
源码代码	sys_git_code	https://github.com/1014TaoTao/fastapi_vue3_admin.git	t	t	1	11	源码代码	2025-09-28 23:39:32.527056	2025-09-28 23:39:32.527057
项目版本	sys_web_version	2.0.0	t	t	1	12	项目版本	2025-09-28 23:39:32.527057	2025-09-28 23:39:32.527057
白名单接口	white_api_list_path	["/api/v1/system/auth/login", "/api/v1/system/auth/token/refresh", "/api/v1/system/auth/captcha/get", "/api/v1/system/auth/logout", "/api/v1/system/config/info", "/api/v1/system/user/current/info", "/api/v1/system/notice/available"]	t	t	1	13	演示模式白名单路径列表	2025-09-28 23:39:32.527058	2025-09-28 23:39:32.527058
黑名单接口	black_api_list_path	["/auth/login"]	t	t	1	14	演示模式黑名单路径列表	2025-09-28 23:39:32.527058	2025-09-28 23:39:32.527059
访问IP白名单	ip_white_list	["127.0.0.1", "117.10.167.220", "223.104.208.30", "42.80.102.171"]	t	t	1	15	演示模式IP白名单列表	2025-09-28 23:39:32.527059	2025-09-28 23:39:32.52706
权限认证白名单接口	token_request_path_exclude	["api/v1/auth/login"]	t	t	1	16	无需JWT认证的路径白名单	2025-09-28 23:39:32.52706	2025-09-28 23:39:32.52706
允许上传文件类型	allowed_extensions	[".bmp", ".gif", ".jpg", ".jpeg", ".png", ".ico", ".svg", ".csv", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".html", ".htm", ".txt", ".pdf", ".rar", ".zip", ".gz", ".bz2", ".mp4", ".avi", ".rmvb"]	t	t	1	17	允许上传的文件类型列表	2025-09-28 23:39:32.527061	2025-09-28 23:39:32.527061
最大文件上传大小	max_file_size	10485760	t	t	1	18	最大文件上传大小(字节)，默认10MB	2025-09-28 23:39:32.527061	2025-09-28 23:39:32.527062
操作日志记录开关	operation_log_record	True	t	t	1	19	是否记录操作日志	2025-09-28 23:39:32.527062	2025-09-28 23:39:32.527062
操作日志记录方法	operation_record_method	["POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"]	t	t	1	20	需要记录操作日志的HTTP方法列表	2025-09-28 23:39:32.527063	2025-09-28 23:39:32.527063
忽略操作日志函数	ignore_operation_function	["get_captcha_for_login"]	t	t	1	21	忽略记录操作日志的函数列表	2025-09-28 23:39:32.527063	2025-09-28 23:39:32.527064
演示模式启用	demo_enable	False	t	t	1	22	是否开启演示模式	2025-09-28 23:39:32.527064	2025-09-28 23:39:32.527065
\.


--
-- Data for Name: system_position; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.system_position (name, "order", status, creator_id, id, description, created_at, updated_at) FROM stdin;
董事长岗	1	t	1	1	董事长岗位	2025-09-28 23:39:32.524558	2025-09-28 23:39:32.52456
\.


--
-- Data for Name: system_role; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.system_role (name, code, "order", status, data_scope, creator_id, id, description, created_at, updated_at) FROM stdin;
管理员角色	ADMIN	1	t	4	1	1	管理员	2025-09-28 23:39:32.518176	2025-09-28 23:39:32.518177
\.


--
-- Data for Name: system_role_depts; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.system_role_depts (role_id, dept_id) FROM stdin;
1	1
\.


--
-- Data for Name: system_role_menus; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.system_role_menus (role_id, menu_id) FROM stdin;
1	1
1	2
1	3
1	4
1	5
1	6
1	7
1	8
1	9
1	10
1	11
1	12
1	13
1	14
1	15
1	16
1	17
1	18
1	19
1	20
1	21
1	22
1	23
1	24
1	25
1	26
1	27
1	28
1	29
1	30
1	31
1	32
1	33
1	34
1	35
1	36
1	37
1	38
1	39
1	40
1	41
1	42
1	43
1	44
1	45
1	46
1	47
1	48
1	49
1	50
1	51
1	52
1	53
1	54
1	55
1	56
1	57
1	58
1	59
1	60
1	61
1	62
1	63
1	64
1	65
1	66
1	67
1	68
1	69
1	70
1	71
1	72
1	73
1	74
1	75
1	76
1	77
1	78
1	79
1	80
1	81
1	82
1	83
1	84
1	85
1	86
1	87
1	88
1	89
1	90
1	91
1	92
1	93
1	94
1	95
1	96
1	97
1	98
1	99
1	100
1	101
1	102
1	103
1	104
1	105
1	106
1	107
1	108
1	109
1	110
1	111
1	112
1	113
1	114
1	115
\.


--
-- Data for Name: system_user_positions; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.system_user_positions (user_id, position_id) FROM stdin;
1	1
2	1
\.


--
-- Data for Name: system_user_roles; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.system_user_roles (user_id, role_id) FROM stdin;
1	1
2	1
\.


--
-- Data for Name: system_users; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.system_users (username, password, name, status, mobile, email, gender, avatar, is_superuser, last_login, dept_id, creator_id, id, description, created_at, updated_at) FROM stdin;
admin	$2b$12$e2IJgS/cvHgJ0H3G7Xa08OXoXnk6N/NX3IZRtubBDElA0VLZhkNOa	管理员	t	15382112222	admin@qq.com	0	https://service.fastapiadmin.com/api/v1/static/image/avatar.png	t	\N	1	\N	1	管理员	2025-09-28 23:39:32.515946	2025-09-28 23:39:32.515947
demo	$2b$12$e2IJgS/cvHgJ0H3G7Xa08OXoXnk6N/NX3IZRtubBDElA0VLZhkNOa	演示用户	t	15382112121	demo@qq.com	0	https://service.fastapiadmin.com/api/v1/static/image/avatar.png	f	\N	1	1	2	演示用户	2025-09-28 23:39:32.515948	2025-09-28 23:39:32.515948
\.


--
-- Name: ai_mcp_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tao
--

SELECT pg_catalog.setval('public.ai_mcp_id_seq', 1, false);


--
-- Name: application_myapp_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tao
--

SELECT pg_catalog.setval('public.application_myapp_id_seq', 1, false);


--
-- Name: example_demo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tao
--

SELECT pg_catalog.setval('public.example_demo_id_seq', 1, false);


--
-- Name: gen_table_column_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tao
--

SELECT pg_catalog.setval('public.gen_table_column_id_seq', 1, false);


--
-- Name: gen_table_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tao
--

SELECT pg_catalog.setval('public.gen_table_id_seq', 1, false);


--
-- Name: monitor_job_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tao
--

SELECT pg_catalog.setval('public.monitor_job_id_seq', 1, false);


--
-- Name: monitor_job_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tao
--

SELECT pg_catalog.setval('public.monitor_job_log_id_seq', 1, false);


--
-- Name: system_dept_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tao
--

SELECT pg_catalog.setval('public.system_dept_id_seq', 7, true);


--
-- Name: system_dict_data_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tao
--

SELECT pg_catalog.setval('public.system_dict_data_id_seq', 34, true);


--
-- Name: system_dict_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tao
--

SELECT pg_catalog.setval('public.system_dict_type_id_seq', 10, true);


--
-- Name: system_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tao
--

SELECT pg_catalog.setval('public.system_log_id_seq', 1, false);


--
-- Name: system_menu_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tao
--

SELECT pg_catalog.setval('public.system_menu_id_seq', 116, true);


--
-- Name: system_notice_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tao
--

SELECT pg_catalog.setval('public.system_notice_id_seq', 1, false);


--
-- Name: system_param_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tao
--

SELECT pg_catalog.setval('public.system_param_id_seq', 22, true);


--
-- Name: system_position_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tao
--

SELECT pg_catalog.setval('public.system_position_id_seq', 1, true);


--
-- Name: system_role_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tao
--

SELECT pg_catalog.setval('public.system_role_id_seq', 1, true);


--
-- Name: system_users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tao
--

SELECT pg_catalog.setval('public.system_users_id_seq', 2, true);


--
-- Name: ai_mcp ai_mcp_name_key; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.ai_mcp
    ADD CONSTRAINT ai_mcp_name_key UNIQUE (name);


--
-- Name: ai_mcp ai_mcp_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.ai_mcp
    ADD CONSTRAINT ai_mcp_pkey PRIMARY KEY (id);


--
-- Name: application_myapp application_myapp_name_key; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.application_myapp
    ADD CONSTRAINT application_myapp_name_key UNIQUE (name);


--
-- Name: application_myapp application_myapp_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.application_myapp
    ADD CONSTRAINT application_myapp_pkey PRIMARY KEY (id);


--
-- Name: example_demo example_demo_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.example_demo
    ADD CONSTRAINT example_demo_pkey PRIMARY KEY (id);


--
-- Name: gen_table_column gen_table_column_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.gen_table_column
    ADD CONSTRAINT gen_table_column_pkey PRIMARY KEY (id);


--
-- Name: gen_table gen_table_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.gen_table
    ADD CONSTRAINT gen_table_pkey PRIMARY KEY (id);


--
-- Name: monitor_job_log monitor_job_log_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.monitor_job_log
    ADD CONSTRAINT monitor_job_log_pkey PRIMARY KEY (id);


--
-- Name: monitor_job monitor_job_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.monitor_job
    ADD CONSTRAINT monitor_job_pkey PRIMARY KEY (id);


--
-- Name: system_dept system_dept_code_key; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_dept
    ADD CONSTRAINT system_dept_code_key UNIQUE (code);


--
-- Name: system_dept system_dept_name_key; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_dept
    ADD CONSTRAINT system_dept_name_key UNIQUE (name);


--
-- Name: system_dept system_dept_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_dept
    ADD CONSTRAINT system_dept_pkey PRIMARY KEY (id);


--
-- Name: system_dict_data system_dict_data_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_dict_data
    ADD CONSTRAINT system_dict_data_pkey PRIMARY KEY (id);


--
-- Name: system_dict_type system_dict_type_dict_name_key; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_dict_type
    ADD CONSTRAINT system_dict_type_dict_name_key UNIQUE (dict_name);


--
-- Name: system_dict_type system_dict_type_dict_type_key; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_dict_type
    ADD CONSTRAINT system_dict_type_dict_type_key UNIQUE (dict_type);


--
-- Name: system_dict_type system_dict_type_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_dict_type
    ADD CONSTRAINT system_dict_type_pkey PRIMARY KEY (id);


--
-- Name: system_log system_log_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_log
    ADD CONSTRAINT system_log_pkey PRIMARY KEY (id);


--
-- Name: system_menu system_menu_name_key; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_menu
    ADD CONSTRAINT system_menu_name_key UNIQUE (name);


--
-- Name: system_menu system_menu_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_menu
    ADD CONSTRAINT system_menu_pkey PRIMARY KEY (id);


--
-- Name: system_notice system_notice_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_notice
    ADD CONSTRAINT system_notice_pkey PRIMARY KEY (id);


--
-- Name: system_param system_param_config_key_key; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_param
    ADD CONSTRAINT system_param_config_key_key UNIQUE (config_key);


--
-- Name: system_param system_param_config_name_key; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_param
    ADD CONSTRAINT system_param_config_name_key UNIQUE (config_name);


--
-- Name: system_param system_param_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_param
    ADD CONSTRAINT system_param_pkey PRIMARY KEY (id);


--
-- Name: system_position system_position_name_key; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_position
    ADD CONSTRAINT system_position_name_key UNIQUE (name);


--
-- Name: system_position system_position_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_position
    ADD CONSTRAINT system_position_pkey PRIMARY KEY (id);


--
-- Name: system_role system_role_code_key; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_role
    ADD CONSTRAINT system_role_code_key UNIQUE (code);


--
-- Name: system_role_depts system_role_depts_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_role_depts
    ADD CONSTRAINT system_role_depts_pkey PRIMARY KEY (role_id, dept_id);


--
-- Name: system_role_menus system_role_menus_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_role_menus
    ADD CONSTRAINT system_role_menus_pkey PRIMARY KEY (role_id, menu_id);


--
-- Name: system_role system_role_name_key; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_role
    ADD CONSTRAINT system_role_name_key UNIQUE (name);


--
-- Name: system_role system_role_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_role
    ADD CONSTRAINT system_role_pkey PRIMARY KEY (id);


--
-- Name: system_user_positions system_user_positions_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_user_positions
    ADD CONSTRAINT system_user_positions_pkey PRIMARY KEY (user_id, position_id);


--
-- Name: system_user_roles system_user_roles_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_user_roles
    ADD CONSTRAINT system_user_roles_pkey PRIMARY KEY (user_id, role_id);


--
-- Name: system_users system_users_email_key; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_users
    ADD CONSTRAINT system_users_email_key UNIQUE (email);


--
-- Name: system_users system_users_mobile_key; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_users
    ADD CONSTRAINT system_users_mobile_key UNIQUE (mobile);


--
-- Name: system_users system_users_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_users
    ADD CONSTRAINT system_users_pkey PRIMARY KEY (id);


--
-- Name: system_users system_users_username_key; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_users
    ADD CONSTRAINT system_users_username_key UNIQUE (username);


--
-- Name: ix_ai_mcp_creator_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_ai_mcp_creator_id ON public.ai_mcp USING btree (creator_id);


--
-- Name: ix_application_myapp_creator_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_application_myapp_creator_id ON public.application_myapp USING btree (creator_id);


--
-- Name: ix_example_demo_creator_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_example_demo_creator_id ON public.example_demo USING btree (creator_id);


--
-- Name: ix_gen_table_column_creator_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_gen_table_column_creator_id ON public.gen_table_column USING btree (creator_id);


--
-- Name: ix_gen_table_creator_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_gen_table_creator_id ON public.gen_table USING btree (creator_id);


--
-- Name: ix_monitor_job_creator_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_monitor_job_creator_id ON public.monitor_job USING btree (creator_id);


--
-- Name: ix_system_dept_parent_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_system_dept_parent_id ON public.system_dept USING btree (parent_id);


--
-- Name: ix_system_dict_data_creator_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_system_dict_data_creator_id ON public.system_dict_data USING btree (creator_id);


--
-- Name: ix_system_dict_type_creator_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_system_dict_type_creator_id ON public.system_dict_type USING btree (creator_id);


--
-- Name: ix_system_log_creator_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_system_log_creator_id ON public.system_log USING btree (creator_id);


--
-- Name: ix_system_menu_parent_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_system_menu_parent_id ON public.system_menu USING btree (parent_id);


--
-- Name: ix_system_notice_creator_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_system_notice_creator_id ON public.system_notice USING btree (creator_id);


--
-- Name: ix_system_param_creator_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_system_param_creator_id ON public.system_param USING btree (creator_id);


--
-- Name: ix_system_position_creator_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_system_position_creator_id ON public.system_position USING btree (creator_id);


--
-- Name: ix_system_role_creator_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_system_role_creator_id ON public.system_role USING btree (creator_id);


--
-- Name: ix_system_users_creator_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_system_users_creator_id ON public.system_users USING btree (creator_id);


--
-- Name: ix_system_users_dept_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_system_users_dept_id ON public.system_users USING btree (dept_id);


--
-- Name: gen_table_column gen_table_column_table_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.gen_table_column
    ADD CONSTRAINT gen_table_column_table_id_fkey FOREIGN KEY (table_id) REFERENCES public.gen_table(id);


--
-- Name: monitor_job_log monitor_job_log_job_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.monitor_job_log
    ADD CONSTRAINT monitor_job_log_job_id_fkey FOREIGN KEY (job_id) REFERENCES public.monitor_job(id);


--
-- Name: system_dept system_dept_parent_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_dept
    ADD CONSTRAINT system_dept_parent_id_fkey FOREIGN KEY (parent_id) REFERENCES public.system_dept(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: system_dict_data system_dict_data_dict_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_dict_data
    ADD CONSTRAINT system_dict_data_dict_type_id_fkey FOREIGN KEY (dict_type_id) REFERENCES public.system_dict_type(id);


--
-- Name: system_menu system_menu_parent_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_menu
    ADD CONSTRAINT system_menu_parent_id_fkey FOREIGN KEY (parent_id) REFERENCES public.system_menu(id) ON DELETE SET NULL;


--
-- Name: system_role_depts system_role_depts_dept_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_role_depts
    ADD CONSTRAINT system_role_depts_dept_id_fkey FOREIGN KEY (dept_id) REFERENCES public.system_dept(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: system_role_depts system_role_depts_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_role_depts
    ADD CONSTRAINT system_role_depts_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.system_role(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: system_role_menus system_role_menus_menu_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_role_menus
    ADD CONSTRAINT system_role_menus_menu_id_fkey FOREIGN KEY (menu_id) REFERENCES public.system_menu(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: system_role_menus system_role_menus_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_role_menus
    ADD CONSTRAINT system_role_menus_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.system_role(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: system_user_positions system_user_positions_position_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_user_positions
    ADD CONSTRAINT system_user_positions_position_id_fkey FOREIGN KEY (position_id) REFERENCES public.system_position(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: system_user_positions system_user_positions_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_user_positions
    ADD CONSTRAINT system_user_positions_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.system_users(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: system_user_roles system_user_roles_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_user_roles
    ADD CONSTRAINT system_user_roles_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.system_role(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: system_user_roles system_user_roles_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_user_roles
    ADD CONSTRAINT system_user_roles_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.system_users(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: system_users system_users_dept_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_users
    ADD CONSTRAINT system_users_dept_id_fkey FOREIGN KEY (dept_id) REFERENCES public.system_dept(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- PostgreSQL database dump complete
--

