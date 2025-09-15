from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.v1.module_system.version.schema import VersionCreate, VersionUpdate, VersionOut
from app.api.v1.module_system.version.service import version_service
from app.core.database import get_db

router = APIRouter(prefix="/versions", tags=["版本管理"])


@router.post("/", response_model=VersionOut)
def create_version(version: VersionCreate, db: Session = Depends(get_db)):
    """创建版本"""
    return version_service.create_version(db, version)


@router.get("/{version_id}", response_model=VersionOut)
def get_version(version_id: int, db: Session = Depends(get_db)):
    """获取版本详情"""
    db_version = version_service.get_version(db, version_id)
    if db_version is None:
        raise HTTPException(status_code=404, detail="版本不存在")
    return db_version


@router.get("/", response_model=list[VersionOut])
def get_versions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """获取版本列表"""
    return version_service.get_versions(db, skip=skip, limit=limit)


@router.put("/{version_id}", response_model=VersionOut)
def update_version(version_id: int, version: VersionUpdate, db: Session = Depends(get_db)):
    """更新版本"""
    db_version = version_service.update_version(db, version_id, version)
    if db_version is None:
        raise HTTPException(status_code=404, detail="版本不存在")
    return db_version


@router.delete("/{version_id}", response_model=VersionOut)
def delete_version(version_id: int, db: Session = Depends(get_db)):
    """删除版本"""
    db_version = version_service.get_version(db, version_id)
    if db_version is None:
        raise HTTPException(status_code=404, detail="版本不存在")
    return version_service.delete_version(db, version_id)


@router.get("/number/{version_number}", response_model=VersionOut)
def get_version_by_number(version_number: str, db: Session = Depends(get_db)):
    """根据版本号获取版本"""
    db_version = version_service.get_version_by_number(db, version_number)
    if db_version is None:
        raise HTTPException(status_code=404, detail="版本不存在")
    return db_version


@router.get("/status/{status}", response_model=list[VersionOut])
def get_versions_by_status(status: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """根据状态获取版本列表"""
    return version_service.get_versions_by_status(db, status=status, skip=skip, limit=limit)