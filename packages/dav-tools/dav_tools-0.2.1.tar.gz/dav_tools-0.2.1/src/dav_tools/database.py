import psycopg2 as _psycopg2
from psycopg2 import sql as _sql

class PostgreSQL:
    def __init__(self, database: str, host: str, user: str, password: str) -> None:        
        self._connection = _psycopg2.connect(database=database,
                                host=host,
                                user=user,
                                password=password)

        self._cursor = self._connection.cursor()

    def insert(self, schema: str, table: str, data: dict[str, any], commit: bool = True, return_fields: list[str] = []):
        if len(return_fields) > 0:
            base_query = 'INSERT INTO {schema}.{table}({fields}) VALUES({values}) RETURNING {return_fields}'
        else:
            base_query = 'INSERT INTO {schema}.{table}({fields}) VALUES({values})'

        query = _sql.SQL(base_query).format(
            schema=_sql.Identifier(schema),
            table=_sql.Identifier(table),
            fields=_sql.SQL(',').join([_sql.Identifier(key) for key in data.keys()]),
            values=_sql.SQL(',').join([_sql.Placeholder(key) for key in data.keys()]),
            return_fields=_sql.SQL(',').join([_sql.Placeholder(key) for key in return_fields])
        )

        self._cursor.execute(query, data)

        return_value = None
        if len(return_fields) > 0:
            return_value = self._cursor.fetchone()

        if commit:
            self._connection.commit()

        return return_value
