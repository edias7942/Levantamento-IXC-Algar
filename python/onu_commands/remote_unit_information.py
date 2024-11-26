def remote_unit_information(self, olt_no, slot_no, pon_no, onu_id):
    self.start_conn()

    self.tn.write(
        f"show remote-unit information gpon_olt-{olt_no}/{slot_no}/{pon_no} {onu_id}\n".encode()
    )
    oltResponse = self.tn.read_until(b"#").decode()

    oltResponse = oltResponse.split("\r\n")
    oltResponse = oltResponse[2:-2]

    list = {}
    region_setting = False

    for info in oltResponse:

        info = info.split(":")

        for variable in info:

            if "Region" in variable:
                region_setting = variable[-1:]
                list[f"Region_{region_setting}"] = {}
                continue

            attribute = info[0]
            attribute = attribute.strip()

            value = info[1]
            value = value.strip()

            if region_setting:
                list[f"Region_{region_setting}"][attribute] = value
                continue

            list[attribute] = value

    oltResponse = list

    return oltResponse
