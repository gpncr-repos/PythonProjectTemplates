# thirdparty
from psycopg import sql


def make_insert_query(table: str, columns: list[str]):
    """
    Сформировать sql строку для создания записи в таблицу
    """
    return sql.SQL("INSERT INTO {table} ({fields}) VALUES ({placeholders})").format(
        table=sql.Identifier(table),
        fields=sql.SQL(', ').join(map(sql.Identifier, columns)),
        placeholders=sql.SQL(', ').join(sql.Placeholder() * len(columns))
    )


def make_select_query(table: str, conditions: list[str] | None = None):
    """
    Сформировать sql строку для получения записей из таблицы
    """
    cond_clause = sql.SQL(', ').join(
        sql.SQL("{} = {}").format(sql.Identifier(c), sql.Placeholder()) for c in conditions
    )
    select_query = sql.SQL("SELECT * FROM {table}").format(table=sql.Identifier(table))
    if conditions:
        select_query += sql.SQL(" WHERE {cond_clause}").format(cond_clause=cond_clause)
    return select_query


def make_update_query(table: str, columns: list[str], conditions: list[str]):
    """
    Сформировать sql строку для обновления записей таблицы
    """
    set_clause = sql.SQL(', ').join(
        sql.SQL("{} = {}").format(sql.Identifier(c), sql.Placeholder()) for c in columns
    )
    cond_clause = sql.SQL(', ').join(
        sql.SQL("{} = {}").format(sql.Identifier(c), sql.Placeholder()) for c in conditions
    )
    update_query = sql.SQL("UPDATE {table} SET {set_clause} WHERE {conditions}").format(
        table=sql.Identifier(table),
        set_clause=set_clause,
        conditions=cond_clause,
    )
    return update_query


def make_delete_query(table: str, conditions: list[str]):
    """
    Сформировать sql строку для удаления записей из таблицы
    """
    cond_clause = sql.SQL(', ').join(
        sql.SQL("{} = {}").format(sql.Identifier(c), sql.Placeholder()) for c in conditions
    )
    delete_query = sql.SQL("DELETE FROM {table} WHERE {conditions}").format(
        table=sql.Identifier(table),
        conditions=cond_clause
    )
    return delete_query
