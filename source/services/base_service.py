import dataclasses
from abc import ABC
from services.exceptions import UniqueException

from psycopg2.errorcodes import UNIQUE_VIOLATION
from psycopg2 import errors


class BaseModelService(ABC):
    """
    Обеспечивает создание и выполнение простых sql-запросов на одной таблице
    """
    TABLE_NAME = None
    IN_MODEL = None
    OUT_MODEL = None

    def __init__(self, conn):
        self.conn = conn

    @staticmethod
    def get_default_fields() -> dict:
        return {}

    @staticmethod
    def get_order_by() -> str:
        return ""

    def create(self, data: IN_MODEL) -> OUT_MODEL:
        """
        Создает новую запись в таблице TABLE_NAME c данными из полей data и полей по умолчанию
        """
        fields = {**data.__dict__, **self.get_default_fields()}
        field_names = fields.keys()

        query = f"insert into {self.TABLE_NAME}({','.join(field_names)})\n"
        query += f"values({','.join([f'%({field_name})s' for field_name in field_names])})\n"
        query += "returning id;"

        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, fields)
                data_id = cursor.fetchone()[0]
            out_data = self.OUT_MODEL(id=data_id, **fields)
            self.conn.commit()
            return out_data
        except errors.lookup(UNIQUE_VIOLATION):
            self.conn.rollback()
            raise UniqueException()

    def delete(self, data_id: int) -> None:
        """
        Удаляет запись с id=data_id из таблицы TABLE_NAME
        """
        query = f"delete from {self.TABLE_NAME}\n"
        query += f"where id = %s;"

        with self.conn.cursor() as cursor:
            cursor.execute(query, (data_id,))
        self.conn.commit()

    def update(self, data: OUT_MODEL) -> OUT_MODEL:
        """
        Обновляет запись с id=data.id в таблице TABLE_NAME
        """
        fields = data.__dict__
        field_names = set(fields.keys())
        field_names.remove('id')

        query = f"update {self.TABLE_NAME}\n"
        query += "set\n"
        query += ',\n'.join([f'{field_name}=%({field_name})s' for field_name in field_names])
        query += "\nwhere id=%(id)s;"

        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, fields)
            self.conn.commit()
            return data
        except errors.lookup(UNIQUE_VIOLATION):
            self.conn.rollback()
            raise UniqueException()

    def get_list_by_search_conditions(self, **conditions):
        """
        Возвращает записи таблицы TABLE_NAME по условиям фильтрации вида: condition_key=condition_value
        """
        field_names = [field.name for field in dataclasses.fields(self.OUT_MODEL)]

        query = f"select {','.join([f'{field_name}' for field_name in field_names])}\n"
        query += f"from {self.TABLE_NAME}\n"

        if conditions:
            text_conditions = []
            for (condition_field_name, value) in conditions.items():
                if value.strip():
                    text_conditions.append(f"{condition_field_name} ilike '%{value.strip()}%'")
            if text_conditions:
                query += "where " + " and ".join(text_conditions) + "\n"

        order_by_query_part = self.get_order_by()
        if order_by_query_part:
            query += "order by " + order_by_query_part

        with self.conn.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
        return [self.OUT_MODEL(*row) for row in rows]
