import sqlite3

# Abrindo Conexão com o Banco de Dados
conn = sqlite3.connect("./database.db")
cursor = conn.cursor()


class QueryDatabase:
    """
    Dict para requisição no Banco de Dados.

    Attributes:
        columns: str - Colunas a serem retornadas. ex: 'id_cliente, login'
        table: str - Tabela para a requisção. ex: 'clientes'
        where: str - Condição para a requisição. ex: 'id = 1'
    """

    columns: str
    table: str
    where: str


def get_database_info(
    query_obj: dict = {
        "columns": "column1, column2",
        "table": "clientes",
        "where": "id = '1'",
    }
):
    query = f"SELECT {query_obj["columns"]} FROM {query_obj["table"]} WHERE {query_obj["where"]}"
    cursor.execute(query)

    try:
        result = cursor.fetchall()[0]
    except:
        result = ["", ""]

    return result
