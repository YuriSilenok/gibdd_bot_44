"""Проверка, находится ли инспектор в патруле"""

from database.models import Role, User, Patrol, UserRole


def get_patrol(inspector: User) -> Patrol:
    """Проверяет наличие роли патрульного и незавершенного патруля
    и возвращет его"""

    return (
        Patrol.select()
        .join(UserRole, on=UserRole.user == Patrol.inspector)
        .where(
            (Patrol.inspector == inspector)
            & (Patrol.end.is_null())
            & (UserRole.role == Role.get(name="Инспектор"))
        )
        .first()
    )
