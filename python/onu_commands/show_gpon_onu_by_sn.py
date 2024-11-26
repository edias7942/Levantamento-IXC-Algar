def show_gpon_onu_by_sn(connection, onu_sn):
    """
    Exibe informações de uma ONU (Optical Network Unit) com base no número de série.

    Esta função envia comandos para uma OLT (Optical Line Terminal) através de uma conexão
    Telnet para buscar detalhes de uma ONU específica pelo seu número de série. Os detalhes
    incluem identificadores de OLT, placa, porta PON e ONU.

    Parâmetros:
    ----------
    onu_sn : str
        Número de série da ONU que se deseja consultar.

    Retorno:
    -------
    dict
        Um dicionário contendo informações detalhadas da ONU consultada, com as seguintes chaves:
        - `olt_id` : int -> Identificador da OLT.
        - `board_id` : int -> Identificador da placa.
        - `pon_id` : int -> Identificador da porta PON.
        - `onu_id` : int -> Identificador da ONU.
        - `text` : str -> Resposta completa da OLT para o comando.

    Exceções:
    ,
    --------
    Pode lançar exceções de conexão caso a conexão Telnet falhe.

    Etapas do Processo:
    -------------------
    1. Inicia a conexão Telnet com a OLT utilizando `self.start_conn()`.
    2. Configura o terminal para não limitar o comprimento da saída.
    3. Envia o comando `show gpon onu by sn {onu_sn}` para a OLT e lê a resposta.
    4. Processa a resposta para separar e identificar cada informação relevante.
    5. Converte as informações processadas em um dicionário e retorna.

    Exemplo de Uso:
    --------------
    ```python
    onu_info = show_gpon_onu_by_sn("ONU123456")
    print(onu_info)
    # Saída:
    # {
    #    "olt_id": 1,
    #    "board_id": 2,
    #    "pon_id": 3,
    #    "onu_id": 4,
    #    "text": "Informação completa da OLT sobre a ONU"
    # }
    ```
    """
    connection.start_conn()

    connection.tn.write("terminal length 0\n".encode())
    connection.tn.read_until(b"#").decode()
    connection.tn.write(f"show gpon onu by sn {onu_sn}\n".encode())
    oltResponse = connection.tn.read_until(b"#").decode()

    oltResponse = oltResponse.split("\r\n")
    oltResponse = oltResponse[3:-1][0]

    text = oltResponse
    parts = oltResponse.split("-")[1].replace("/", ":").split(":")

    list = {}
    list["olt_id"] = int(parts[0])
    list["board_id"] = int(parts[1])
    list["pon_id"] = int(parts[2])
    list["onu_id"] = int(parts[3])
    list["text"] = text

    oltResponse = list

    return oltResponse