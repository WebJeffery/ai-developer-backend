# -*- coding: utf-8 -*-

from typing import Dict, List, Sequence, Optional

from app.core.base_crud import CRUDBase
from .model import RoleModel
from .schema import RoleCreateSchema, RoleUpdateSchema
from ..auth.schema import AuthSchema
from ..menu.crud import MenuCRUD
from ..dept.crud import DeptCRUD


class RoleCRUD(CRUDBase[RoleModel, RoleCreateSchema, RoleUpdateSchema]):
    """角色模块数据层"""

    def __init__(self, auth: AuthSchema) -> None:
        self.auth = auth
        super().__init__(model=RoleModel, auth=auth)

    async def get_by_id_crud(self, id: int) -> Optional[RoleModel]:
        """根据id获取角色信息"""
        return await self.get(id=id)

    async def get_list_crud(self, search: Optional[Dict] = None, order_by: Optional[List[Dict[str, str]]] = None) -> Sequence[RoleModel]:
        """获取角色列表"""
        return await self.list(search=search, order_by=order_by)

    async def set_role_menus_crud(self, role_ids: List[int], menu_ids: List[int]) -> None:
        """设置角色的菜单权限"""
        roles = await self.list(search={"id": ("in", role_ids)})
        menus = await MenuCRUD(self.auth).get_list_crud(search={"id": ("in", menu_ids)})

        for obj in roles:
            relationship = obj.menus
            relationship.clear()
            relationship.extend(menus)
        await self.db.flush()

    async def set_role_data_scope_crud(self, role_ids: List[int], data_scope: int) -> None:
        """设置角色的数据范围"""
        await self.set(ids=role_ids, data_scope=data_scope)

    async def set_role_depts_crud(self, role_ids: List[int], dept_ids: List[int]) -> None:
        """设置角色的部门权限"""
        roles = await self.list(search={"id": ("in", role_ids)})
        depts = await DeptCRUD(self.auth).get_list_crud(search={"id": ("in", dept_ids)})

        for obj in roles:
            relationship = obj.depts
            relationship.clear()
            relationship.extend(depts)
        await self.db.flush()

    async def set_available_crud(self, ids: List[int], status: bool) -> None:
        """设置角色的可用状态"""
        await self.set(ids=ids, status=status)
