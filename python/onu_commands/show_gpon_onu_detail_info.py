from .util import filter_object_attributes


def show_gpon_onu_detail_info(
    self, olt_no, slot_no, pon_no, onu_id, required_attributes_array=False
):
    self.start_conn()

    self.tn.write(
        f"show gpon onu detail-info gpon_onu-{olt_no}/{slot_no}/{pon_no}:{onu_id}\n".encode()
    )
    oltResponse = self.tn.read_until(b"#").decode()

    [first_info, second_info] = oltResponse.split(
        "------------------------------------------"
    )
    first_info = first_info.split("\r\n")
    first_info = first_info[3:-1]

    first_info_list = {}

    for info in first_info:

        info = info.split(":")

        [attribute, value] = info

        attribute = attribute.strip().replace(" ", "_").lower()
        value = value.strip()

        first_info_list[attribute] = value

    if required_attributes_array:
        first_info_list = filter_object_attributes(
            first_info_list, required_attributes_array
        )

    second_info = second_info.split("\r\n")
    second_info = second_info[2:-3]

    #
    second_info_list = []

    for info in second_info:

        info = info.split("  ")

        id = info[1].strip()
        authpass_time = info[2].strip()
        offline_time = info[4].strip()
        cause = info[6].strip()

        info_item = {
            "id": id,
            "authpass_time": authpass_time,
            "offline_time": offline_time,
            "cause": cause,
        }

        second_info_list.append(info_item)

    oltResponse = [first_info_list, second_info_list]

    return oltResponse
