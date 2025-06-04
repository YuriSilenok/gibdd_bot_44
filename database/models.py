"""Модуль для базы данных"""

from datetime import datetime
from peewee import (
    SqliteDatabase,
    Model,
    CharField,
    IntegerField,
    DateTimeField,
    ForeignKeyField,
    BooleanField,
    FloatField,
)

# pylint: disable=R0903
DB = SqliteDatabase("sqlite.db")


class Table(Model):
    """Базовая модель"""

    class Meta:
        """Класс мета"""

        database = DB


class User(Table):
    """Класс пользователя"""

    tg_id = IntegerField(unique=True)
    at_created = DateTimeField(default=datetime.now())
    username = CharField(null=True)
    last_name = CharField(null=True)
    first_name = CharField(null=True)
    is_ban = BooleanField(default=False)

    @property
    def full_name(self):
        """Возвращает полное имя пользователя."""
        return f"{self.first_name or ''} {self.last_name or ''}".strip()


class Role(Table):
    """Класс ролей"""

    name = CharField()


class UserRole(Table):
    """Класс роли пользователей"""

    user = ForeignKeyField(User, backref='user_roles', on_update="CASCADE",
                           on_delete="CASCADE"
                           )
    role = ForeignKeyField(Role, backref='role_users', on_update="CASCADE",
                           on_delete="CASCADE"
                           )


class Message(Table):
    """Класс сообщений пользователя"""

    to_user = ForeignKeyField(User, on_update="CASCADE", on_delete="CASCADE")
    from_user = ForeignKeyField(User, on_update="CASCADE", on_delete="CASCADE")
    text = CharField(max_length=4096, null=True)
    at_created = DateTimeField(default=datetime.now())
    tg_message_id = IntegerField()
    is_delete = BooleanField(default=False)


class Photo(Table):
    """Сведения о фотографии"""

    message = ForeignKeyField(
        Message, on_update="CASCADE", on_delete="CASCADE"
    )
    file_id = CharField(max_length=128)


class Location(Table):
    """Класс для хранения геолокационных данных"""

    message = ForeignKeyField(
        Message, on_update="CASCADE", on_delete="CASCADE"
    )
    longitude = FloatField()
    latitude = FloatField()


class Video(Table):
    """Сведения о видео"""

    message = ForeignKeyField(
        Message, on_update="CASCADE", on_delete="CASCADE"
    )
    file_id = CharField(max_length=128)


class Patrol(Table):
    """Класс для сообщения о выезде инспектора"""

    inspector = ForeignKeyField(User, on_update="CASCADE", on_delete="CASCADE")
    start = DateTimeField(default=datetime.now())
    end = DateTimeField(null=True)


class Admin(Table):
    """Класс для хранения настроек администратора"""

    user = ForeignKeyField(User, on_update="CASCADE", on_delete="CASCADE")
    is_notify = BooleanField(default=False)


if __name__ == "__main__":
    DB.connect()
    DB.create_tables(
        [User, Role, UserRole, Message, Patrol, Admin, Photo, Location, Video],
        safe=True,
    )
    DB.close()
    admin_role, _ = Role.get_or_create(name="Администратор")
    Role.get_or_create(name="Инспектор")
    admin, _ = User.get_or_create(tg_id=320720102)
    UserRole.get_or_create(
        user=admin,
        role=admin_role,
    )
