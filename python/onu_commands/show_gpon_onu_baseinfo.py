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
        if not line.startswith("gpon_onu"):
            continue
          
        if idx == len(lines) - 1 and len(lines) > 1:
            break

        try:
            if lines[idx + 1].startswith("gpon_onu"):
                line = f"{line[:32]}{line[31:]}"
            else:
                if lines[idx + 1][0] == " ":
                    line = f"{line[:32].strip()}{lines[idx + 1].strip()} {line[32:]}"
                else:
                    line = f"{line[:19].strip()}{lines[idx + 1].strip()} {line[19:]}"
        except:
            pass

        # gpon_onu-1/12/10:10 F670L0 sn      SN:ZTEGCF22255C         ready

        onu_data.append(line.strip())

    # Processar cada linha para capturar os atributos
    result = []

    # Processar cada linha
    for line in onu_data:
        [first_part, second_part] = line.split("sn")
        
        first_part = first_part.strip().split(' ')
        onu_index_string = first_part[0]
        onu_type = first_part[-1]
        onu_index = onu_index_string.split("-")[1]
        [olt_id, board_id, pon_onu_ids] = onu_index.split("/")
        [pon_id, onu_id] = pon_onu_ids.split(":")
        
        second_part = second_part.strip().split(" ")
        sn = second_part[0].replace("SN:", "")
        state = second_part[-1]
        
        print(f"{onu_index_string} - {onu_type} - {sn} - {state}")
    
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
                "state": state,
            }
        )

    return result

