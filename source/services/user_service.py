import datetime
from dataclasses import dataclass
from services.base_service import BaseModelService


@dataclass
class InUser:
    firstname: str
    lastname: str
    middlename: str
    phone: str


@dataclass
class OutUser(InUser):
    id: int
    register_date: datetime.date


@dataclass
class OutBookHistoryItem:
    name: str
    take_date: datetime.date
    is_returned: bool


class UserService(BaseModelService):
    TABLE_NAME = 'users'
    IN_MODEL = InUser
    OUT_MODEL = OutUser

    @staticmethod
    def get_default_fields() -> dict:
        return dict(register_date=datetime.date.today())

    @staticmethod
    def get_order_by() -> str:
        return "lastname, firstname, middlename"

    def get_user_book_history(self, user_id: int):
        query = f"""
            select b.name, bfu.take_date,
                case when bfu.real_return_date is null
                then 0 else 1 end
            from books b
            inner join books_for_users bfu
            on b.id = bfu.book_id
            where bfu.user_id = {user_id}
            order by bfu.take_date desc
        """
        with self.conn.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
        return [OutBookHistoryItem(*row) for row in rows]
