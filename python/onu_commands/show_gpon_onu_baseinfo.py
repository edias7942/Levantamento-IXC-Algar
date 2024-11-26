from .util import filter_object_attributes


def show_gpon_onu_baseinfo(self, olt_no, slot_no, pon_no):
    self.start_conn()

    self.tn.write(
        f"show gpon onu baseinfo gpon_olt-{olt_no}/{slot_no}/{pon_no}\n".encode()
    )

    oltResponse = self.tn.read_until(b"#").decode()

    # Separar as linhas do texto
    lines = oltResponse.strip().split("\n")

    # Pular as duas primeiras linhas (cabeçalho e separador)
    lines = lines[3:-1]

    # Criar uma lista para armazenar os resultados
    onu_data = []  # Criar uma lista para armazenar os resultados
    current_line = ""

    # Processar cada linha
    for idx, line in enumerate(lines):
        # Verificar se a linha contém dados válidos (não é continuação de outra linha)
        print(line)
        if not line.startswith("gpon_onu"):
            continue

        if idx == len(lines) - 1:
            break

        if lines[idx + 1].startswith("gpon_onu"):
            line = f"{line[:32]}{line[31:]}"
# gpon_onu-1/12/10:10 F670L0 sn      SN:ZTEGCF22255C         ready
        else:
            line = f"{line[:32].strip()}{lines[idx + 1].strip()} {line[32:]}"
        
        onu_data.append(line.strip())

    # Processar cada linha para capturar os atributos
    result = []

    # Processar cada linha
    for line in onu_data:
        print(line)
        # Dividir a linha em partes com base em espaçamentos fixos
        onu_index_string = line[:20].strip()
        onu_index = onu_index_string.split("-")[1]
        [olt_id, board_id, pon_onu_ids] = onu_index.split("/")
        [pon_id, onu_id] = pon_onu_ids.split(":")

        olt_id = int(olt_id)
        board_id = int(board_id)
        pon_id = int(pon_id)
        onu_id = int(onu_id)

        onu_type = line[20:32].strip()
        mode = line[32:40].strip()
        sn = line[40:60].strip().split(":")[1]
        state = line[60:].strip()

        # Adicionar os valores em um dicionário
        result.append(
            {
                "onu_index": onu_index_string,
                "olt_id": olt_id,
                "board_id": board_id,
                "pon_id": pon_id,
                "onu_id": onu_id,
                "sn": sn,
                "onu_type": onu_type,
                "mode": mode,
                "state": state,
            }
        )

    return result
