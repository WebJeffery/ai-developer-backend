from sqlalchemy.orm import Session
from app.api.v1.module_system.version.crud import version_crud
from app.api.v1.module_system.version.schema import VersionCreate, VersionUpdate


class VersionService:
    """版本服务类"""
    
    @staticmethod
    def create_version(db: Session, version_create: VersionCreate):
        """创建版本"""
        return version_crud.create(db, obj_in=version_create)
    
    @staticmethod
    def get_version(db: Session, version_id: int):
        """获取版本"""
        return version_crud.get(db, id=version_id)
    
    @staticmethod
    def get_versions(db: Session, skip: int = 0, limit: int = 100):
        """获取版本列表"""
        return version_crud.get_multi(db, skip=skip, limit=limit)
    
    @staticmethod
    def update_version(db: Session, version_id: int, version_update: VersionUpdate):
        """更新版本"""
        db_version = version_crud.get(db, id=version_id)
        if db_version:
            return version_crud.update(db, db_obj=db_version, obj_in=version_update)
        return None
    
    @staticmethod
    def delete_version(db: Session, version_id: int):
        """删除版本"""
        return version_crud.remove(db, id=version_id)
    
    @staticmethod
    def get_version_by_number(db: Session, version_number: str):
        """根据版本号获取版本"""
        return version_crud.get_version_by_number(db, version_number=version_number)
    
    @staticmethod
    def get_versions_by_status(db: Session, status: str, skip: int = 0, limit: int = 100):
        """根据状态获取版本列表"""
        return version_crud.get_versions_by_status(db, status=status, skip=skip, limit=limit)


version_service = VersionService()