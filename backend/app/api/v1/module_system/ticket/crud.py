from sqlalchemy.orm import Session
from typing import List
from app.api.v1.module_system.ticket.model import Ticket
from app.api.v1.module_system.ticket.schema import TicketCreate, TicketUpdate
from app.core.base_crud import CRUDBase
from ..auth.schema import AuthSchema

class CRUDTicket(CRUDBase[Ticket, TicketCreate, TicketUpdate]):
    """工单 CRUD 操作"""

    def __init__(self, auth: AuthSchema) -> None:
        """初始化工单CRUD"""
        self.auth = auth
        super().__init__(model=Ticket, auth=auth)
    
    pass
