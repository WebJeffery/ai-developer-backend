from sqlalchemy.orm import Session
from app.api.v1.module_system.ticket.crud import ticket_crud
from app.api.v1.module_system.ticket.schema import TicketCreate, TicketUpdate


class TicketService:
    """工单服务类"""
    
    @staticmethod
    def create_ticket(db: Session, ticket_create: TicketCreate):
        """创建工单"""
        return ticket_crud.create(db, obj_in=ticket_create)
    
    @staticmethod
    def get_ticket(db: Session, ticket_id: int):
        """获取工单"""
        return ticket_crud.get(db, id=ticket_id)
    
    @staticmethod
    def get_tickets(db: Session, skip: int = 0, limit: int = 100):
        """获取工单列表"""
        return ticket_crud.get_multi(db, skip=skip, limit=limit)
    
    @staticmethod
    def update_ticket(db: Session, ticket_id: int, ticket_update: TicketUpdate):
        """更新工单"""
        db_ticket = ticket_crud.get(db, id=ticket_id)
        if db_ticket:
            return ticket_crud.update(db, db_obj=db_ticket, obj_in=ticket_update)
        return None
    
    @staticmethod
    def delete_ticket(db: Session, ticket_id: int):
        """删除工单"""
        return ticket_crud.remove(db, id=ticket_id)
    
    @staticmethod
    def get_tickets_by_status(db: Session, status: str, skip: int = 0, limit: int = 100):
        """根据状态获取工单列表"""
        return ticket_crud.get_tickets_by_status(db, status=status, skip=skip, limit=limit)
    
    @staticmethod
    def get_tickets_by_assignee(db: Session, assignee_id: int, skip: int = 0, limit: int = 100):
        """根据指派用户获取工单列表"""
        return ticket_crud.get_tickets_by_assignee(db, assignee_id=assignee_id, skip=skip, limit=limit)


ticket_service = TicketService()