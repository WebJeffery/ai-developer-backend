from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.v1.module_system.ticket.schema import TicketCreate, TicketUpdate, TicketOut
from app.api.v1.module_system.ticket.service import ticket_service
from app.core.database import get_db

router = APIRouter(prefix="/tickets", tags=["工单管理"])


@router.post("/", response_model=TicketOut)
def create_ticket(ticket: TicketCreate, db: Session = Depends(get_db)):
    """创建工单"""
    return ticket_service.create_ticket(db, ticket)


@router.get("/{ticket_id}", response_model=TicketOut)
def get_ticket(ticket_id: int, db: Session = Depends(get_db)):
    """获取工单详情"""
    db_ticket = ticket_service.get_ticket(db, ticket_id)
    if db_ticket is None:
        raise HTTPException(status_code=404, detail="工单不存在")
    return db_ticket


@router.get("/", response_model=list[TicketOut])
def get_tickets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """获取工单列表"""
    return ticket_service.get_tickets(db, skip=skip, limit=limit)


@router.put("/{ticket_id}", response_model=TicketOut)
def update_ticket(ticket_id: int, ticket: TicketUpdate, db: Session = Depends(get_db)):
    """更新工单"""
    db_ticket = ticket_service.update_ticket(db, ticket_id, ticket)
    if db_ticket is None:
        raise HTTPException(status_code=404, detail="工单不存在")
    return db_ticket


@router.delete("/{ticket_id}", response_model=TicketOut)
def delete_ticket(ticket_id: int, db: Session = Depends(get_db)):
    """删除工单"""
    db_ticket = ticket_service.get_ticket(db, ticket_id)
    if db_ticket is None:
        raise HTTPException(status_code=404, detail="工单不存在")
    return ticket_service.delete_ticket(db, ticket_id)


@router.get("/status/{status}", response_model=list[TicketOut])
def get_tickets_by_status(status: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """根据状态获取工单列表"""
    return ticket_service.get_tickets_by_status(db, status=status, skip=skip, limit=limit)


@router.get("/assignee/{assignee_id}", response_model=list[TicketOut])
def get_tickets_by_assignee(assignee_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """根据指派用户获取工单列表"""
    return ticket_service.get_tickets_by_assignee(db, assignee_id=assignee_id, skip=skip, limit=limit)