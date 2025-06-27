"""Проверка, находится ли инспектор в патруле"""

from database.models import User, Patrol, UserRole
from filters.inspector import IsInspector


def get_patrol(inspector: User) -> Patrol:
    """Проверяет наличие роли патрульного и незавершенного патруля
    и возвращет его"""

    return (
        Patrol.select()
        .join(UserRole, on=UserRole.user == Patrol.inspector)
        .where(
            (Patrol.inspector == inspector)
            & (Patrol.end.is_null())
            & (UserRole.role == IsInspector.role)
        ).first()
    )
