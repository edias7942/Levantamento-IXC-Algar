from termcolor import colored
from openpyxl import Workbook
from utils import refresh_progress_bar
from secrets_variables import oltAccessInfo
from olt_connection_huawei import olt_connection
from huawei.ont_commands.display_ont_info_summary import (
    display_ont_info_summary,
    OntObject,
)


# Conectando com a OLT
connection = olt_connection(oltAccessInfo)

# Requisitando informações da OLT
olt_id, board_id = 0, 0

# Novo Arquivo de Planilha
workbook = Workbook()

# Abrindo Planilha
sheet = workbook.active
sheet.title = "HUAWEI-CAETANO-ALVARES"

ont_attributes = [
    "ont_identification",
    "id",
    "state",
    "last_uptime",
    "last_downtime",
    "last_downcause",
    "sn",
    "type",
    "distance",
    "rx_tx_power",
    "description",
]

sheet.append(ont_attributes)

sheet_file_save = "./sheets/informacoes-algar-HUAWEI-CAETANO-ALVARES.xlsx"
boards = [0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14]

while board_id <= 17:
    pon_id = 0

    if not board_id in boards:
        board_id += 1
        continue

    message = f"INICIANDO LEITURA DO SLOT {board_id}"
    print(colored(message, "green", attrs=["bold"]))

    # Loop Pon by Pon
    while pon_id <= 16:

        result = display_ont_info_summary(connection, 1, pon_id)

        # Loop Client by Client
        for idx, item in enumerate(result):

            item: OntObject

            refresh_progress_bar(len(result), idx + 1)

            if len(result) == idx + 1:
                message = f"PON {olt_id}/{board_id}/{pon_id} Concluída - {pon_id} de 16"
                print(colored(message, "green", attrs=["bold"]))

            login_client = item.description

            sheet_line = [f"{olt_id}/{board_id}/{pon_id}:{item.id}"]
            item_list = []
            for attribute in vars(item):
                sheet_line.append(getattr(item, attribute))

            sheet.append(sheet_line)

        pon_id += 1
        workbook.save(sheet_file_save)

    board_id += 1
