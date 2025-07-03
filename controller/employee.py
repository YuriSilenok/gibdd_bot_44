"""Логика при взаимодействии над сотрудником"""

from database.models import Role, User, UserRole


def is_employee(user: User) -> bool:
    """Проверка является ли пользователь сотрудником"""

    return UserRole.select().where(
        (UserRole.user == user)
        & (
            UserRole.role.in_([
                Role.get(name="Начальник"),
                Role.get(name="Администратор"),
                Role.get(name="Инспектор"),
            ])
        )
    ).first() is not None
