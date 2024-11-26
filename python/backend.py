from onu_commands.show_gpon_onu_detail_info import show_gpon_onu_detail_info
from onu_commands.show_gpon_onu_baseinfo import show_gpon_onu_baseinfo
from olt_connection import olt_connection

from typing import TypedDict
import sys
import sqlite3


from openpyxl import load_workbook

# Abrindo Conexão com o Banco de Dados
conn = sqlite3.connect("./database.db")
cursor = conn.cursor()

# Conectando com a OLT
oltAccessInfo = {
    "ip": "10.40.150.6",
    "usuario": "smartolt",
    "senha": "kwRed5@lirft+",
}
connection = olt_connection(oltAccessInfo)

# Requisitando informações da OLT
olt_id = 1
board_id = 12
pon_id = 1

# Abrindo Planilha
sheet_file_path = "informacoes-algar.xlsx"
workbook = load_workbook(sheet_file_path)
sheet = workbook.active


class QueryDatabase(TypedDict):
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


while board_id <= 17:
    pon_id = 10
    boards = [2, 3, 4, 5, 6, 7, 8, 9, 12, 13, 14, 15, 16, 17]
    if not board_id in boards:
        board_id += 1
        continue

    print(f"\n\033[32mINICIANDO LEITURA DO SLOT {board_id}\033[37m\n")

    # Loop Pon by Pon
    while pon_id <= 16:
        # print(f"GETTING {olt_id}/{board_id}/{pon_id}")
        result = show_gpon_onu_baseinfo(connection, olt_id, board_id, pon_id)

        def barra_progresso(total, progressado, tamanho=50):
            progresso = progressado / total
            barra = "█" * int(progresso * tamanho)
            espaços = " " * (tamanho - len(barra))
            percent = int(progresso * 100)
            sys.stdout.write(
                f"\r[{barra}{espaços}] {percent}% {progressado}/{total}    "
            )
            sys.stdout.flush()
            if total == progressado:
                print(
                    f"\n\033[32mPON {olt_id}/{board_id}/{pon_id} Concluída - {pon_id} de 16\033[37m\n"
                )

        # Exemplo de array de clientes
        clientes = ["Cliente {}".format(i) for i in range(1, 251)]  # 250 clientes

        # Loop Client by Client
        for idx, item in enumerate(result):

            barra_progresso(len(result), idx + 1)

            # Buscando informações detalhadas do cliente
            detail_info = show_gpon_onu_detail_info(
                connection,
                item["olt_id"],
                item["board_id"],
                item["pon_id"],
                item["onu_id"],
            )[0]

            login_client = detail_info["name"].lower()

            # Captação de id_cliente & id_contrato
            query_obj: QueryDatabase = {
                "columns": "id_cliente, id_contrato",
                "table": "radusuarios",
                "where": f"login = '{login_client}'",
            }

            [id_cliente, id_contrato] = get_database_info(query_obj)

            # Captação de nome_cliente
            query_obj: QueryDatabase = {
                "columns": "razao",
                "table": "clientes",
                "where": f"id = '{id_cliente}'",
            }
            nome_cliente = get_database_info(query_obj)[0]

            if not nome_cliente:
                nome_cliente = login_client

            # Captação de contrato_cliente
            query_obj: QueryDatabase = {
                "columns": "contrato",
                "table": "cliente_contrato",
                "where": f"id = '{id_contrato}'",
            }
            contrato_cliente = get_database_info(query_obj)[0]
            if not contrato_cliente:
                contrato_cliente = "Sem contrato"

            # print(
            #     f"{login_client} - {id_cliente} - {id_contrato} - {nome_cliente} - {contrato_cliente}"
            # )

            sheet_line = [
                f"{item['olt_id']}.{item['board_id']}.{item['pon_id']}.{item['onu_id']}",
                nome_cliente,
                contrato_cliente,
                oltAccessInfo["ip"],
                "ZXA10 C600",
                "Hibryd",
                "1",
                item["board_id"],
                item["pon_id"],
                item["onu_id"],
                item["onu_type"],
                item["sn"],
                item["onu_id"],
                "FRANQUEADOR",
            ]

            sheet.append(sheet_line)

        pon_id += 1
        workbook.save(sheet_file_path)

    board_id += 1
