#!/bin/bash

# 设置全局变量
PROJECT_NAME="fastapi_vue3_admin"
WORK_DIR="."
GIT_REPO="https://gitee.com/tao__tao/${PROJECT_NAME}.git"

# 是否有更新前端
UPDATE_FRONTEND=false
# 是否有更新移动端
UPDATE_FASTAPP=false
# 是否有更新官网
UPDATE_FASTDOCS=false

# 日志级别控制
LOG_LEVEL=${LOG_LEVEL:-INFO}

# 打印带时间戳的日志
log() {
    local message="$1"
    local level=${2:-INFO}
    
    # 根据日志级别决定是否输出
    case $LOG_LEVEL in
        DEBUG) ;;
        INFO) [[ $level == "DEBUG" ]] && return ;;
        WARN) [[ $level == "DEBUG" || $level == "INFO" ]] && return ;;
        ERROR) [[ $level != "ERROR" ]] && return ;;
    esac
    
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [$level] $message"
}

# 检查系统依赖
check_permissions() {
    log "==========🔍 检查权限...==========" "INFO"
    # 检查脚本文件是否有执行权限
    if [ ! -x "$0" ]; then
        log "⚠️ 当前脚本没有执行权限，请使用 chmod +x $0 添加执行权限" "ERROR"
        exit 1
    else
        log "✅ 脚本已有执行权限" "INFO"
    fi

    log "==========🔍 检查系统依赖...==========" "INFO"
    local missing_deps=()
    
    for cmd in git docker node npm pnpm; do
        if ! command -v $cmd &> /dev/null; then
            missing_deps+=($cmd)
            log "❌ $cmd 未安装" "ERROR"
        else
            log "🎉 $cmd 已安装 - $($cmd --version 2>/dev/null || $cmd -v)" "INFO"
        fi
    done
    
    if [ ${#missing_deps[@]} -ne 0 ]; then
        log "❌ 缺少依赖: ${missing_deps[*]}" "ERROR"
        exit 1
    fi
    
    log "✅ 所有依赖检查通过" "INFO"
}

# 停止项目容器
stop_project() {
    log "==========⏹️ 停止项目容器...==========" "INFO"
    if [ -d "${WORK_DIR}/${PROJECT_NAME}" ]; then
        cd "${WORK_DIR}/${PROJECT_NAME}" || { log "❌ 无法进入项目目录：${WORK_DIR}/${PROJECT_NAME}" "ERROR"; exit 1; }
        
        if [ -f "docker-compose.yaml" ] || [ -f "docker-compose.yml" ]; then
            docker compose down || { log "❌ 停止容器失败" "ERROR"; exit 1; }
            log "✅ 项目容器已停止并删除" "INFO"
        else
            log "❌ docker-compose 文件未找到" "ERROR"
            exit 1
        fi
    else
        log "❌ 项目目录不存在：${WORK_DIR}/${PROJECT_NAME}" "ERROR"
        exit 1
    fi
}

# 更新代码
update_code() {
    log "==========🔍 更新最新代码...==========" "INFO"
    if [ -d "${WORK_DIR}/${PROJECT_NAME}/" ]; then
        log "🔄 开始更新代码" "INFO"
        cd "${PROJECT_NAME}" || { log "❌ 无法进入项目目录：${PROJECT_NAME}" "ERROR"; exit 1; }
        git pull --force || { log "❌ 拉取更新失败" "ERROR"; exit 1; }
        git log -1 || { log "❌ 获取提交信息失败" "ERROR"; exit 1; }
        if [ -f "frontend" ]; then
            UPDATE_FRONTEND=true
            log "📦 项目更新了前端工程" "INFO"
        fi
        if [ -f "fastapp" ]; then
            UPDATE_FASTAPP=true
            log "📦 项目更新了移动端工程" "INFO"
        fi
        if [ -f "fastdocs" ]; then
            UPDATE_FASTDOCS=true
            log "📦 项目更新了官网工程" "INFO"
        fi
        log "✅ 代码更新成功" "INFO"
    else
        log "📥 项目不存在，开始克隆代码" "INFO"
        git clone "${GIT_REPO}" || { log "❌ 项目克隆失败：${GIT_REPO}" "ERROR"; exit 1; }
        cd "${PROJECT_NAME}" || { log "❌ 无法进入项目目录：${PROJECT_NAME}" "ERROR"; exit 1; }
        UPDATE_FRONTEND=true
        UPDATE_FASTAPP=true
        UPDATE_FASTDOCS=true
        log "✅ 代码克隆成功" "INFO"
    fi
}

# 打包前端
build_frontend() {
    log "==========🚀 打包前端...==========" "INFO"
    
    # 构建前端
    if [ -d "frontend" ] && [ "$UPDATE_FRONTEND" = true ]; then
        cd frontend || { log "❌ 无法进入前端目录" "ERROR"; exit 1; }
        log "📦 安装前端依赖..." "INFO"
        pnpm install || { log "❌ 前端依赖安装失败" "ERROR"; exit 1; }
        log "🔨 打包前端工程..." "INFO"
        pnpm run build || { log "❌ 前端工程打包失败" "ERROR"; exit 1; }
        log "✅ 前端工程打包成功" "INFO"
        cd .. || { log "❌ 无法返回项目根目录" "ERROR"; exit 1; }
    fi

    # 构建小程序
    if [ -d "fastapp" ] && [ "$UPDATE_FASTAPP" = true ]; then
        cd fastapp || { log "❌ 无法进入小程序目录" "ERROR"; exit 1; }
        log "📦 安装小程序依赖..." "INFO"
        pnpm install || { log "❌ 小程序依赖安装失败" "ERROR"; exit 1; }
        log "🔨 打包小程序工程..." "INFO"
        pnpm run build:h5 || { log "❌ 小程序工程打包失败" "ERROR"; exit 1; }
        log "✅ 小程序工程打包成功" "INFO"
        cd .. || { log "❌ 无法返回项目根目录" "ERROR"; exit 1; }
    fi

    # 构建项目文档
    if [ -d "fastdocs" ] && [ "$UPDATE_FASTDOCS" = true ]; then
        cd fastdocs || { log "❌ 无法进入项目文档目录" "ERROR"; exit 1; }
        log "📦 安装项目文档依赖..." "INFO"
        pnpm install || { log "❌ 项目文档依赖安装失败" "ERROR"; exit 1; }
        log "🔨 打包项目文档..." "INFO"
        pnpm run docs:build || { log "❌ 项目文档打包生成失败" "ERROR"; exit 1; }
        log "✅ 项目文档打包成功" "INFO"
        cd .. || { log "❌ 无法返回项目根目录" "ERROR"; exit 1; }
    fi
}

# 构建镜像&启动容器
start_containers() {
    log "==========🚀 构建镜像&启动容器...==========" "INFO"
    docker compose build || { log "❌ 镜像构建失败" "ERROR"; exit 1; }
    log "✅  Docker镜像构建成功" "INFO"
    docker compose up -d --force-recreate || { log "❌ 容器启动失败" "ERROR"; exit 1; }
    sleep 5
    log "✅ 容器启动成功" "INFO"

    log "==========🗑️ 清理72小时前的旧镜像...==========" "INFO"
    # 只清理与项目相关的镜像
    local project_images=$(docker images | grep ${PROJECT_NAME} | awk '{print $3}' | wc -l)
    if [ $project_images -gt 0 ]; then
        local before_count=$(docker images | grep ${PROJECT_NAME} | wc -l)
        # 修改: 使用更准确的过滤方式清理镜像
        docker image prune -f --filter "until=72h" --filter "label=com.docker.compose.project=${PROJECT_NAME}" >/dev/null 2>&1
        local after_count=$(docker images | grep ${PROJECT_NAME} | wc -l)
        log "✅ 旧镜像清理完成，清理了 $((before_count - after_count)) 个镜像" "INFO"
    else
        log "⚠️  没有找到项目相关镜像，跳过清理" "WARN"
    fi
}

# 显示所有完整日志的函数
show_containers_logs() {
    log "==========📋 查看所有应用完整日志 ==========" "INFO"
    cd "${WORK_DIR}/${PROJECT_NAME}" || { log "❌ 无法进入项目目录" "ERROR"; exit 1; }
    
    # 显示容器状态
    log "🔍 检查容器状态..." "INFO"
    docker compose ps || { log "❌ 容器状态获取失败" "ERROR"; exit 1; }
    
    # 显示容器日志
    log "📋 获取容器日志..." "INFO"
    docker compose logs --tail=300 || log "⚠️ 后端日志获取失败" "WARN"
}

# 信号处理
handle_interrupt() {
    log "==========⚠️ 收到中断信号，正在停止部署...==========" "WARN"
    # 如果在容器启动阶段中断，尝试停止容器
    if [ -d "${WORK_DIR}/${PROJECT_NAME}" ]; then
        cd "${WORK_DIR}/${PROJECT_NAME}"
        docker compose down >/dev/null 2>&1
    fi
    exit 130
}

# 主函数
main() {
    log "==========🚀 开始部署流程==========" "INFO"
    check_permissions
    stop_project
    update_code
    # build_frontend (由于本地资源较小，在服务器上构建应用改用本地构建好，上传到服务器)
    start_containers
    show_logs
    
    log "🎉 部署完成！以下是访问信息：
    📌 官网: https://service.fastapiadmin.com
    📌 前端: https://service.fastapiadmin.com/web
    📌 小程序: https://service.fastapiadmin.com/app
    📌 后端接口: https://service.fastapiadmin.com/api/v1/docs
    📌 登录信息: 账号 admin，密码 123456" "INFO"
}

# 设置信号处理
trap handle_interrupt INT TERM


# 解析命令行参数
# 如果没有参数，则默认执行部署流程
if [ $# -eq 0 ]; then
    main "$@"
    exit 0
fi

while [[ $# -gt 0 ]]; do
    case $1 in
        --stop)
            stop_project
            exit 0
            ;;
        --start)
            main
            exit 0
            ;;
        --logs|-l)
            show_containers_logs
            exit 0
            ;;
        --help|-h)
            echo "Usage: $0 [--stop] [--start] [--logs]"
            echo "  --stop      停止项目容器"
            echo "  --start     启动项目容器"
            echo "  --logs      查看容器最近日志（摘要）"
            echo "  不带参数时默认执行完整部署流程"
            exit 0
            ;;
        *)
            echo "未知参数: $1"
            exit 1
            ;;
    esac
done

main "$@"