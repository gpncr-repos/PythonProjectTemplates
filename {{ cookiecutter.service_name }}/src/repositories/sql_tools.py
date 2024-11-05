# thirdparty
# project
from interfaces.base_raw_sql_creator import BaseRawSQLCreator
from psycopg import sql


class PsycopgRawSQLCreator(BaseRawSQLCreator):
    """
    Класс для создания sql-query, реализованный через psycopg
    """

    def make_insert_query(self, table: str, columns: list[str]):
        """
        Сформировать sql строку для создания записи в таблицу
        :param table: имя таблицы в бд
        :param columns: список колонок таблицы
        """
        return sql.SQL("INSERT INTO {table} ({fields}) VALUES ({placeholders})").format(
            table=sql.Identifier(table),
            fields=sql.SQL(", ").join(map(sql.Identifier, columns)),
            placeholders=sql.SQL(", ").join(sql.Placeholder() * len(columns)),
        )

    def make_select_query(self, table: str, conditions: list[str] | None = None):
        """
        Сформировать sql строку для получения записей из таблицы
        :param table: имя таблицы в бд
        :param conditions: список колонок, по которым требуется фильтрация
        """
        cond_clause = sql.SQL(", ").join(
            sql.SQL("{} = {}").format(sql.Identifier(c), sql.Placeholder()) for c in conditions
        )
        select_query = sql.SQL("SELECT * FROM {table}").format(table=sql.Identifier(table))
        if conditions:
            select_query += sql.SQL(" WHERE {cond_clause}").format(cond_clause=cond_clause)
        return select_query

    def make_update_query(self, table: str, columns: list[str], conditions: list[str]):
        """
        Сформировать sql строку для обновления записей таблицы
        :param table: имя таблицы в бд
        :param columns: список колонок таблицы
        :param conditions: список колонок, по которым требуется фильтрация
        """
        set_clause = sql.SQL(", ").join(
            sql.SQL("{} = {}").format(sql.Identifier(c), sql.Placeholder()) for c in columns
        )
        cond_clause = sql.SQL(", ").join(
            sql.SQL("{} = {}").format(sql.Identifier(c), sql.Placeholder()) for c in conditions
        )
        update_query = sql.SQL("UPDATE {table} SET {set_clause} WHERE {conditions}").format(
            table=sql.Identifier(table),
            set_clause=set_clause,
            conditions=cond_clause,
        )
        return update_query

    def make_delete_query(self, table: str, conditions: list[str]):
        """
        Сформировать sql строку для удаления записей из таблицы
        :param table: имя таблицы в бд
        :param conditions: список колонок, по которым требуется фильтрация
        """
        cond_clause = sql.SQL(", ").join(
            sql.SQL("{} = {}").format(sql.Identifier(c), sql.Placeholder()) for c in conditions
        )
        delete_query = sql.SQL("DELETE FROM {table} WHERE {conditions}").format(
            table=sql.Identifier(table), conditions=cond_clause
        )
        return delete_query
