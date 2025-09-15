from sqlalchemy.orm import Session
from typing import List
from app.api.v1.module_system.version.model import Version
from app.api.v1.module_system.version.schema import VersionCreate, VersionUpdate
from app.core.base_crud import CRUDBase


class CRUDVersion(CRUDBase[Version, VersionCreate, VersionUpdate]):
    """版本 CRUD 操作"""
    
    def get_version_by_id(self, db: Session, version_id: int) -> Version:
        """根据ID获取版本"""
        return db.query(self.model).filter(self.model.id == version_id).first()
    
    def get_versions(self, db: Session, skip: int = 0, limit: int = 100) -> List[Version]:
        """获取版本列表"""
        return db.query(self.model).offset(skip).limit(limit).all()
    
    def get_version_by_number(self, db: Session, version_number: str) -> Version:
        """根据版本号获取版本"""
        return db.query(self.model).filter(self.model.version_number == version_number).first()
    
    def get_versions_by_status(self, db: Session, status: str, skip: int = 0, limit: int = 100) -> List[Version]:
        """根据状态获取版本列表"""
        return db.query(self.model).filter(self.model.status == status).offset(skip).limit(limit).all()


version_crud = CRUDVersion(Version)