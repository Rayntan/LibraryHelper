import dataclasses
from services.base_service import BaseModelService


class BaseMiddleModelService(BaseModelService):
    """
    Обеспечивает работу с промежуточной таблицей для более сложных запросов
    """

    def join(self, target_service: BaseModelService, join_field: str, **condition):
        """
        Выполняет соединение таблиц self.TABLE_NAME и target_service.TABLE_NAME через условия
        {target_service.TABLE_NAME}.id = {self.TABLE_NAME}.join_field и
        {self.TABLE_NAME}.condition_key = condition_value
        """
        field_names = [field.name for field in dataclasses.fields(target_service.OUT_MODEL)]
        where_field = list(condition.keys())[0]
        value = list(condition.values())[0]

        query = f"""
            select {','.join([f'{target_service.TABLE_NAME}.{field_name}' for field_name in field_names])}
            from {target_service.TABLE_NAME}
            inner join {self.TABLE_NAME}
            on {target_service.TABLE_NAME}.id = {self.TABLE_NAME}.{join_field}
            where {self.TABLE_NAME}.{where_field} = {value}
            {"order by " + target_service.TABLE_NAME + "." + target_service.get_order_by() 
                if target_service.get_order_by() else ""}
        """

        with self.conn.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
        return [target_service.OUT_MODEL(*row) for row in rows]

    def delete(self, **conditions) -> None:
        """
        Удаляет запись из таблицы TABLE_NAME, у которой condition1_key=condition1_value
        """
        query = f"delete from {self.TABLE_NAME}\n"
        query += f"where {' and '.join(f'{field}={value}' for (field, value) in conditions.items())}"

        with self.conn.cursor() as cursor:
            cursor.execute(query)
        self.conn.commit()
