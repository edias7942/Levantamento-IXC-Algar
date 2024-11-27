# import time
# import sys

# def barra_progresso(total, progressado, tamanho=40):
#     progresso = progressado / total
#     barra = '█' * int(progresso * tamanho)
#     espaços = ' ' * (tamanho - len(barra))
#     percent = int(progresso * 100)
#     sys.stdout.write(f"\r[{barra}{espaços}] {percent}%")
#     sys.stdout.flush()

# # Exemplo de array de clientes
# clientes = ["Cliente {}".format(i) for i in range(1, 251)]  # 250 clientes

# # Iterando com enumerate para obter índice e valor do cliente
# total_clientes = len(clientes)

# for i, cliente in enumerate(clientes):
#     # Aqui seria a lógica de análise do cliente
#     time.sleep(0.05)  # Simula a análise de cada cliente

#     # Atualiza a barra de progresso a cada cliente analisado
#     barra_progresso(total_clientes, i + 1)  # i + 1 porque o índice começa em 0

# print()  # Para garantir que a linha final da barra de progresso seja impressa corretamente

from onu_commands_huawei.display_ont_info_summary import display_ont_info_summary
from olt_connection_huawei import olt_connection
from secrets_variables import oltAccessInfo

connection = olt_connection(oltAccessInfo)

result = display_ont_info_summary(connection, 1)

print(result)

