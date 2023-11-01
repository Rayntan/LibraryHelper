import psycopg2


def get_connection(db_data: dict):
    """
    Получение сессии базы данных
    """
    conn = psycopg2.connect(
        **db_data
    )
    return conn
