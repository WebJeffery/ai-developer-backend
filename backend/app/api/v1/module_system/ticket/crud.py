from sqlalchemy.orm import Session
from typing import List
from app.api.v1.module_system.ticket.model import Ticket
from app.api.v1.module_system.ticket.schema import TicketCreate, TicketUpdate
from app.core.base_crud import CRUDBase


class CRUDTicket(CRUDBase[Ticket, TicketCreate, TicketUpdate]):
    """工单 CRUD 操作"""
    
    def get_ticket_by_id(self, db: Session, ticket_id: int) -> Ticket:
        """根据ID获取工单"""
        return db.query(self.model).filter(self.model.id == ticket_id).first()
    
    def get_tickets(self, db: Session, skip: int = 0, limit: int = 100) -> List[Ticket]:
        """获取工单列表"""
        return db.query(self.model).offset(skip).limit(limit).all()
    
    def get_tickets_by_status(self, db: Session, status: str, skip: int = 0, limit: int = 100) -> List[Ticket]:
        """根据状态获取工单列表"""
        return db.query(self.model).filter(self.model.status == status).offset(skip).limit(limit).all()
    
    def get_tickets_by_assignee(self, db: Session, assignee_id: int, skip: int = 0, limit: int = 100) -> List[Ticket]:
        """根据指派用户获取工单列表"""
        return db.query(self.model).filter(self.model.assignee_id == assignee_id).offset(skip).limit(limit).all()


ticket_crud = CRUDTicket(Ticket)