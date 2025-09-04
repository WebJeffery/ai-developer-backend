# -*- coding: utf-8 -*-

import os
import shutil
import hashlib
import io
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path

from fastapi import UploadFile
from PIL import Image
try:
    import magic
    MAGIC_AVAILABLE = True
except ImportError:
    MAGIC_AVAILABLE = False

from app.core.exceptions import CustomException
from app.core.logger import logger
from app.utils.excel_util import ExcelUtil
from app.config.setting import settings
from ...module_system.auth.schema import AuthSchema
from .param import ResourceQueryParams
from .schema import (
    ResourceItemSchema,
    ResourceDirectorySchema,
    ResourceStatsSchema,
    ResourceSearchSchema,
    ResourceUploadSchema,
    ResourceMoveSchema,
    ResourceCopySchema,
    ResourceRenameSchema,
    ResourceCreateDirSchema,
    ResourceType
)


class ResourceService:
    """
    资源管理模块服务层 - 直接操作文件系统
    """
    
    # 默认挂载点配置
    DEFAULT_MOUNT_POINT = getattr(settings, 'RESOURCE_MOUNT_POINT', '/Users/tao/workspace/fastapi_vue3_admin/backend/static/upload')
    ALLOWED_MOUNT_POINTS = getattr(settings, 'ALLOWED_MOUNT_POINTS', ['/Users/tao/workspace/fastapi_vue3_admin/backend/static', '/Users/tao/workspace/fastapi_vue3_admin/backend/static/upload'])
    
    @classmethod
    def _get_safe_path(cls, path: str) -> str:
        """获取安全的文件路径"""
        if not path:
            return cls.DEFAULT_MOUNT_POINT
            
        # 规范化路径
        safe_path = os.path.normpath(os.path.abspath(path))
        
        # 检查路径是否在允许的挂载点内
        allowed = False
        for mount_point in cls.ALLOWED_MOUNT_POINTS:
            mount_abs = os.path.normpath(os.path.abspath(mount_point))
            if safe_path.startswith(mount_abs):
                allowed = True
                break
                
        if not allowed:
            raise CustomException(msg=f'访问路径不在允许范围内: {path}')
            
        return safe_path
    
    @classmethod
    def _path_exists(cls, path: str) -> bool:
        """检查路径是否存在"""
        try:
            safe_path = cls._get_safe_path(path)
            return os.path.exists(safe_path)
        except:
            return False
    
    @classmethod
    def _get_file_info(cls, file_path: str) -> Dict[str, Any]:
        """获取文件信息"""
        try:
            safe_path = cls._get_safe_path(file_path)
            if not os.path.exists(safe_path):
                return {}
                
            stat = os.stat(safe_path)
            path_obj = Path(safe_path)
            
            # 获取文件扩展名和类型
            file_extension = path_obj.suffix.lower() if path_obj.suffix else None
            file_type = cls._get_mime_type_from_extension(file_extension) if file_extension else None
            resource_type = cls._determine_resource_type(file_type, file_extension)
            
            return {
                'name': path_obj.name,
                'path': safe_path,
                'relative_path': os.path.relpath(safe_path, cls.DEFAULT_MOUNT_POINT),
                'is_file': os.path.isfile(safe_path),
                'is_dir': os.path.isdir(safe_path),
                'size': stat.st_size if os.path.isfile(safe_path) else None,
                'file_type': file_type,
                'file_extension': file_extension,
                'resource_type': resource_type,
                'created_time': datetime.fromtimestamp(stat.st_ctime),
                'modified_time': datetime.fromtimestamp(stat.st_mtime),
                'accessed_time': datetime.fromtimestamp(stat.st_atime),
                'parent_path': str(path_obj.parent),
                'depth': len(path_obj.relative_to(cls.DEFAULT_MOUNT_POINT).parts) if cls.DEFAULT_MOUNT_POINT in safe_path else 0
            }
        except Exception as e:
            logger.error(f'获取文件信息失败: {str(e)}')
            return {}
    
    @classmethod
    async def get_directory_list_service(
        cls, 
        auth: AuthSchema, 
        path: Optional[str] = None,
        recursive: bool = False,
        include_hidden: bool = False
    ) -> Dict:
        """获取目录列表"""
        try:
            target_path = path or cls.DEFAULT_MOUNT_POINT
            safe_path = cls._get_safe_path(target_path)
            
            if not os.path.exists(safe_path):
                raise CustomException(msg='目录不存在')
                
            if not os.path.isdir(safe_path):
                raise CustomException(msg='路径不是目录')
            
            items = []
            total_files = 0
            total_dirs = 0
            total_size = 0
            
            try:
                for item_name in os.listdir(safe_path):
                    # 跳过隐藏文件
                    if not include_hidden and item_name.startswith('.'):
                        continue
                        
                    item_path = os.path.join(safe_path, item_name)
                    file_info = cls._get_file_info(item_path)
                    
                    if file_info:
                        items.append(ResourceItemSchema(**file_info))
                        
                        if file_info['is_file']:
                            total_files += 1
                            total_size += file_info.get('size', 0) or 0
                        elif file_info['is_dir']:
                            total_dirs += 1
                            
                            # 递归统计子目录
                            if recursive:
                                sub_stats = await cls._get_directory_stats(item_path, include_hidden)
                                total_files += sub_stats['files']
                                total_dirs += sub_stats['dirs']
                                total_size += sub_stats['size']
                                
            except PermissionError:
                raise CustomException(msg='没有权限访问此目录')
            
            return ResourceDirectorySchema(
                path=safe_path,
                name=os.path.basename(safe_path),
                items=items,
                total_files=total_files,
                total_dirs=total_dirs,
                total_size=total_size
            ).model_dump()
            
        except CustomException:
            raise
        except Exception as e:
            logger.error(f'获取目录列表失败: {str(e)}')
            raise CustomException(msg=f'获取目录列表失败: {str(e)}')
    
    @classmethod
    async def _get_directory_stats(cls, path: str, include_hidden: bool = False) -> Dict[str, int]:
        """递归获取目录统计信息"""
        stats = {'files': 0, 'dirs': 0, 'size': 0}
        
        try:
            for root, dirs, files in os.walk(path):
                # 过滤隐藏目录
                if not include_hidden:
                    dirs[:] = [d for d in dirs if not d.startswith('.')]
                    files = [f for f in files if not f.startswith('.')]
                
                stats['dirs'] += len(dirs)
                stats['files'] += len(files)
                
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        stats['size'] += os.path.getsize(file_path)
                    except (OSError, IOError):
                        continue
                        
        except Exception:
            pass
            
        return stats
    
    @classmethod
    async def search_resources_service(
        cls,
        auth: AuthSchema,
        search: ResourceSearchSchema
    ) -> List[Dict]:
        """搜索资源"""
        try:
            mount_point = cls.DEFAULT_MOUNT_POINT
            results = []
            
            for root, dirs, files in os.walk(mount_point):
                # 控制搜索深度
                depth = len(Path(root).relative_to(mount_point).parts)
                if depth > search.max_depth:
                    continue
                
                # 过滤隐藏文件夹
                if not search.include_hidden:
                    dirs[:] = [d for d in dirs if not d.startswith('.')]
                    files = [f for f in files if not f.startswith('.')]
                
                # 搜索文件
                for file in files:
                    file_path = os.path.join(root, file)
                    file_info = cls._get_file_info(file_path)
                    
                    if cls._match_search_criteria(file_info, search):
                        results.append(file_info)
            
            # 排序结果
            return cls._sort_results(results, search)
            
        except Exception as e:
            logger.error(f'搜索资源失败: {str(e)}')
            raise CustomException(msg=f'搜索资源失败: {str(e)}')
    
    @classmethod
    def _match_search_criteria(cls, file_info: Dict, search: ResourceSearchSchema) -> bool:
        """检查文件是否匹配搜索条件"""
        if not file_info or not file_info.get('is_file'):
            return False
        
        # 关键词搜索
        if search.keyword:
            if search.keyword.lower() not in file_info.get('name', '').lower():
                return False
        
        # 文件类型搜索
        if search.file_type:
            if search.file_type.lower() != file_info.get('file_type', '').lower():
                return False
        
        # 资源类型搜索
        if search.resource_type:
            if search.resource_type != file_info.get('resource_type'):
                return False
        
        # 文件大小搜索
        file_size = file_info.get('size', 0) or 0
        if search.min_size and file_size < search.min_size:
            return False
        if search.max_size and file_size > search.max_size:
            return False
        
        # 扩展名搜索
        if search.extensions:
            file_ext = file_info.get('file_extension', '')
            if file_ext not in search.extensions:
                return False
        
        # 时间范围搜索
        modified_time = file_info.get('modified_time')
        if modified_time:
            if search.start_date and modified_time < search.start_date:
                return False
            if search.end_date and modified_time > search.end_date:
                return False
        
        return True
    
    @classmethod
    def _sort_results(cls, results: List[Dict], search: ResourceSearchSchema) -> List[Dict]:
        """排序搜索结果"""
        sort_key = 'name'
        if hasattr(search, 'sort_by') and search.sort_by:
            sort_key = search.sort_by
        
        reverse = False
        if hasattr(search, 'sort_order') and search.sort_order == 'desc':
            reverse = True
        
        try:
            return sorted(results, key=lambda x: x.get(sort_key, ''), reverse=reverse)
        except:
            return results

    @classmethod
    async def upload_file_service(
        cls, 
        auth: AuthSchema, 
        file: UploadFile, 
        target_path: Optional[str] = None
    ) -> Dict:
        """上传文件到指定目录"""
        if not file or not file.filename:
            raise CustomException(msg="请选择要上传的文件")
        
        try:
            # 确定上传目录
            upload_dir = target_path or cls.DEFAULT_MOUNT_POINT
            safe_dir = cls._get_safe_path(upload_dir)
            
            # 创建目录（如果不存在）
            os.makedirs(safe_dir, exist_ok=True)
            
            # 生成文件路径
            filename = file.filename
            file_path = os.path.join(safe_dir, filename)
            
            # 检查文件是否已存在
            if os.path.exists(file_path):
                # 生成唯一文件名
                base_name, ext = os.path.splitext(filename)
                counter = 1
                while os.path.exists(file_path):
                    new_filename = f"{base_name}_{counter}{ext}"
                    file_path = os.path.join(safe_dir, new_filename)
                    counter += 1
                filename = os.path.basename(file_path)
            
            # 保存文件
            content = await file.read()
            with open(file_path, 'wb') as f:
                f.write(content)
            
            # 获取文件信息
            file_info = cls._get_file_info(file_path)
            
            logger.info(f"文件上传成功: {filename}")
            
            return ResourceUploadSchema(
                filename=filename,
                file_path=file_path,
                file_url=f"/resource/download?path={file_path}",
                file_size=file_info.get('size', 0),
                resource_type=file_info.get('resource_type', ResourceType.OTHER),
                upload_time=datetime.now()
            ).model_dump()
            
        except Exception as e:
            logger.error(f"文件上传失败: {str(e)}")
            raise CustomException(msg=f"文件上传失败: {str(e)}")

    @classmethod
    async def download_file_service(cls, auth: AuthSchema, file_path: str) -> str:
        """下载文件（返回文件路径）"""
        try:
            safe_path = cls._get_safe_path(file_path)
            
            if not os.path.exists(safe_path):
                raise CustomException(msg='文件不存在')
            
            if not os.path.isfile(safe_path):
                raise CustomException(msg='路径不是文件')
            
            logger.info(f"下载文件: {safe_path}")
            return safe_path
            
        except CustomException:
            raise
        except Exception as e:
            logger.error(f"下载文件失败: {str(e)}")
            raise CustomException(msg=f"下载文件失败: {str(e)}")

    @classmethod
    async def delete_file_service(cls, auth: AuthSchema, paths: List[str]) -> None:
        """删除文件或目录"""
        if not paths:
            raise CustomException(msg='删除失败，删除路径不能为空')
        
        for path in paths:
            try:
                safe_path = cls._get_safe_path(path)
                
                if not os.path.exists(safe_path):
                    logger.warning(f"路径不存在，跳过: {path}")
                    continue
                
                if os.path.isfile(safe_path):
                    os.remove(safe_path)
                    logger.info(f"删除文件成功: {safe_path}")
                elif os.path.isdir(safe_path):
                    shutil.rmtree(safe_path)
                    logger.info(f"删除目录成功: {safe_path}")
                    
            except Exception as e:
                logger.error(f"删除失败 {path}: {str(e)}")
                raise CustomException(msg=f"删除失败 {path}: {str(e)}")

    @classmethod
    async def move_file_service(cls, auth: AuthSchema, data: ResourceMoveSchema) -> None:
        """移动文件或目录"""
        try:
            source_path = cls._get_safe_path(data.source_path)
            target_path = cls._get_safe_path(data.target_path)
            
            if not os.path.exists(source_path):
                raise CustomException(msg='源路径不存在')
            
            # 检查目标路径是否已存在
            if os.path.exists(target_path):
                if not data.overwrite:
                    raise CustomException(msg='目标路径已存在')
                else:
                    # 删除目标路径
                    if os.path.isfile(target_path):
                        os.remove(target_path)
                    else:
                        shutil.rmtree(target_path)
            
            # 确保目标目录存在
            target_dir = os.path.dirname(target_path)
            os.makedirs(target_dir, exist_ok=True)
            
            # 移动文件
            shutil.move(source_path, target_path)
            logger.info(f"移动成功: {source_path} -> {target_path}")
            
        except CustomException:
            raise
        except Exception as e:
            logger.error(f"移动失败: {str(e)}")
            raise CustomException(msg=f"移动失败: {str(e)}")

    @classmethod
    async def copy_file_service(cls, auth: AuthSchema, data: ResourceCopySchema) -> None:
        """复制文件或目录"""
        try:
            source_path = cls._get_safe_path(data.source_path)
            target_path = cls._get_safe_path(data.target_path)
            
            if not os.path.exists(source_path):
                raise CustomException(msg='源路径不存在')
            
            # 检查目标路径是否已存在
            if os.path.exists(target_path) and not data.overwrite:
                raise CustomException(msg='目标路径已存在')
            
            # 确保目标目录存在
            target_dir = os.path.dirname(target_path)
            os.makedirs(target_dir, exist_ok=True)
            
            # 复制文件或目录
            if os.path.isfile(source_path):
                shutil.copy2(source_path, target_path)
            else:
                shutil.copytree(source_path, target_path, dirs_exist_ok=data.overwrite)
            
            logger.info(f"复制成功: {source_path} -> {target_path}")
            
        except CustomException:
            raise
        except Exception as e:
            logger.error(f"复制失败: {str(e)}")
            raise CustomException(msg=f"复制失败: {str(e)}")

    @classmethod
    async def rename_file_service(cls, auth: AuthSchema, data: ResourceRenameSchema) -> None:
        """重命名文件或目录"""
        try:
            old_path = cls._get_safe_path(data.old_path)
            
            if not os.path.exists(old_path):
                raise CustomException(msg='文件或目录不存在')
            
            # 生成新路径
            parent_dir = os.path.dirname(old_path)
            new_path = os.path.join(parent_dir, data.new_name)
            
            if os.path.exists(new_path):
                raise CustomException(msg='目标名称已存在')
            
            # 重命名
            os.rename(old_path, new_path)
            logger.info(f"重命名成功: {old_path} -> {new_path}")
            
        except CustomException:
            raise
        except Exception as e:
            logger.error(f"重命名失败: {str(e)}")
            raise CustomException(msg=f"重命名失败: {str(e)}")

    @classmethod
    async def create_directory_service(cls, auth: AuthSchema, data: ResourceCreateDirSchema) -> None:
        """创建目录"""
        try:
            parent_path = cls._get_safe_path(data.parent_path)
            
            if not os.path.exists(parent_path):
                raise CustomException(msg='父目录不存在')
            
            if not os.path.isdir(parent_path):
                raise CustomException(msg='父路径不是目录')
            
            # 生成新目录路径
            new_dir_path = os.path.join(parent_path, data.dir_name)
            
            if os.path.exists(new_dir_path):
                raise CustomException(msg='目录已存在')
            
            # 创建目录
            os.makedirs(new_dir_path)
            logger.info(f"创建目录成功: {new_dir_path}")
            
        except CustomException:
            raise
        except Exception as e:
            logger.error(f"创建目录失败: {str(e)}")
            raise CustomException(msg=f"创建目录失败: {str(e)}")

    @classmethod
    async def get_stats_service(cls, auth: AuthSchema) -> Dict:
        """获取资源统计信息"""
        try:
            mount_point = cls.DEFAULT_MOUNT_POINT
            
            # 获取磁盘空间信息
            statvfs = os.statvfs(mount_point)
            total_space = statvfs.f_frsize * statvfs.f_blocks
            free_space = statvfs.f_frsize * statvfs.f_bavail
            used_space = total_space - free_space
            
            # 统计文件信息
            total_files = 0
            total_dirs = 0
            total_size = 0
            type_stats = {}
            extension_stats = {}
            
            for root, dirs, files in os.walk(mount_point):
                total_dirs += len(dirs)
                
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        file_info = cls._get_file_info(file_path)
                        if file_info:
                            total_files += 1
                            total_size += file_info.get('size', 0) or 0
                            
                            # 类型统计
                            resource_type = file_info.get('resource_type')
                            if resource_type:
                                type_name = resource_type.value if hasattr(resource_type, 'value') else str(resource_type)
                                type_stats[type_name] = type_stats.get(type_name, 0) + 1
                            
                            # 扩展名统计
                            extension = file_info.get('file_extension', '')
                            if extension:
                                extension_stats[extension] = extension_stats.get(extension, 0) + 1
                                
                    except Exception:
                        continue
            
            return ResourceStatsSchema(
                mount_point=mount_point,
                total_files=total_files,
                total_dirs=total_dirs,
                total_size=total_size,
                free_space=free_space,
                used_space=used_space,
                total_space=total_space,
                type_stats=type_stats,
                extension_stats=extension_stats
            ).model_dump()
            
        except Exception as e:
            logger.error(f"获取统计信息失败: {str(e)}")
            raise CustomException(msg=f"获取统计信息失败: {str(e)}")

    @classmethod
    async def export_resource_service(cls, data_list: List[Dict[str, Any]]) -> bytes:
        """导出资源列表"""
        mapping_dict = {
            'name': '文件名',
            'path': '文件路径',
            'size': '文件大小',
            'file_type': 'MIME类型',
            'file_extension': '文件扩展名',
            'resource_type': '资源类型',
            'created_time': '创建时间',
            'modified_time': '修改时间',
            'parent_path': '父目录'
        }

        # 复制数据并转换状态
        export_data = data_list.copy()
        for item in export_data:
            # 处理枚举值
            if 'resource_type' in item and hasattr(item['resource_type'], 'value'):
                item['resource_type'] = item['resource_type'].value
            
            # 格式化文件大小
            if item.get('size'):
                item['size'] = cls._format_file_size(item['size'])

        return ExcelUtil.export_list2excel(list_data=export_data, mapping_dict=mapping_dict)

    @classmethod
    def _determine_resource_type(cls, file_type: str, file_extension: str) -> ResourceType:
        """根据MIME类型和文件扩展名确定资源类型"""
        if not file_type:
            return ResourceType.OTHER
            
        if file_type.startswith('image/'):
            return ResourceType.IMAGE
        elif file_type.startswith('video/'):
            return ResourceType.VIDEO
        elif file_type.startswith('audio/'):
            return ResourceType.AUDIO
        elif file_type in ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                          'application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                          'application/vnd.ms-powerpoint', 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
                          'text/plain', 'text/csv']:
            return ResourceType.DOCUMENT
        elif file_type in ['application/zip', 'application/x-rar-compressed', 'application/x-7z-compressed',
                          'application/gzip', 'application/x-tar']:
            return ResourceType.ARCHIVE
        else:
            return ResourceType.OTHER

    @classmethod
    def _format_file_size(cls, size_bytes: int) -> str:
        """格式化文件大小"""
        if size_bytes == 0:
            return "0B"
        
        size_names = ["B", "KB", "MB", "GB", "TB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        
        return f"{size_bytes:.2f}{size_names[i]}"

    @classmethod
    def _get_mime_type_from_extension(cls, file_extension: str) -> str:
        """根据文件扩展名获取MIME类型"""
        if not file_extension:
            return 'application/octet-stream'
            
        mime_types = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.bmp': 'image/bmp',
            '.webp': 'image/webp',
            '.svg': 'image/svg+xml',
            '.mp4': 'video/mp4',
            '.avi': 'video/x-msvideo',
            '.mov': 'video/quicktime',
            '.wmv': 'video/x-ms-wmv',
            '.flv': 'video/x-flv',
            '.mp3': 'audio/mpeg',
            '.wav': 'audio/wav',
            '.aac': 'audio/aac',
            '.ogg': 'audio/ogg',
            '.pdf': 'application/pdf',
            '.doc': 'application/msword',
            '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            '.xls': 'application/vnd.ms-excel',
            '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            '.ppt': 'application/vnd.ms-powerpoint',
            '.pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
            '.txt': 'text/plain',
            '.csv': 'text/csv',
            '.zip': 'application/zip',
            '.rar': 'application/x-rar-compressed',
            '.7z': 'application/x-7z-compressed',
            '.tar': 'application/x-tar',
            '.gz': 'application/gzip'
        }
        return mime_types.get(file_extension.lower(), 'application/octet-stream')