"""Общие фильтры для административных обработчиков"""

from filters.admin import IsAdmin
from filters.chief import IsChief


class AdminOrChiefFilter:
    """Фильтр для проверки роли Администратор или Начальник"""

    def __init__(self):
        self.admin_filter = IsAdmin()
        self.chief_filter = IsChief()

    async def __call__(self, callback) -> bool:
        """Является ли пользователь администратором или начальником"""
        is_admin = await self.admin_filter(callback)
        is_chief = await self.chief_filter(callback)
        return is_admin or is_chief

    def check_permissions(self, current_user, target_role_name: str) -> bool:
        """Проверяет права доступа для операций"""
        is_chief = self.chief_filter.check(current_user.tg_id)
        return is_chief or target_role_name != "Администратор"
