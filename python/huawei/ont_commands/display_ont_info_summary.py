from typing import TypedDict
from dataclasses import dataclass
import math

# @dataclass
class OntObject:
    id: str = ""
    state: str = ""
    last_uptime: str = ""
    last_downtime: str = ""
    last_downcause: str = ""
    sn: str = ""
    type: str = ""
    distance: str = ""
    rx_tx_power: str = ""
    description: str = ""

def display_ont_info_summary(self, slot_no, pon_no):
    self.start_conn()

    # self.tn.write(
    #     f"config".encode()
    # )

    # oltResponse = self.tn.read_until(b"#").decode()

    self.tn.write(f"display ont info summary 0/{slot_no}/{pon_no} | no-more\n".encode())

    oltResponse = self.tn.read_until(b":").decode()
    self.tn.write(f"\n".encode())

    oltResponse = self.tn.read_until(b"#").decode()
    
    oltResponse = oltResponse.replace(
        "  ------------------------------------------------------------------------------",
        "",
    )

    oltResponse = oltResponse.replace(
        "  ONT  Run     Last                Last                Last                   ",
        "",
    )

    oltResponse = oltResponse.replace(
        "  ID   State   UpTime              DownTime            DownCause",
        "",
    )

    oltResponse = oltResponse.replace(
        "  ID                                    (m)      (dBm)",
        "",
    )

    oltResponse = oltResponse.replace(
        "  ONT        SN        Type          Distance Rx/Tx power  Description",
        "",
    )

    oltResponse = oltResponse.split("\r\n")

    oltResponse = [item for item in oltResponse if item]

    oltResponse = oltResponse[4:-2]

    oltResponseLength = len(oltResponse)
    information_divisor = math.ceil(oltResponseLength / 2)
    first_information = oltResponse[1:information_divisor]
    #  1    online  2024-10-27 13:25:26 2024-10-27 13:21:54 dying-gasp
    second_information = oltResponse[information_divisor:]

    @dataclass
    class OntObject:
        id: str = ""
        state: str = ""
        last_uptime: str = ""
        last_downtime: str = ""
        last_downcause: str = ""
        sn: str = ""
        type: str = ""
        distance: str = ""
        rx_tx_power: str = ""
        description: str = ""
        

    ont_list = []

    for idx, item in enumerate(first_information):
        #  1    online  2024-10-27 13:25:26 2024-10-27 13:21:54 dying-gasp
        ont_object = OntObject()
        ont_object.id = item[:5].strip()
        ont_object.state = item[6:14].strip()
        ont_object.last_uptime = item[14:34].strip()
        ont_object.last_downtime = item[35:54].strip()
        ont_object.last_downcause = item[55:].strip()

        ont_list.append(ont_object)

    for idx, item in enumerate(second_information):
        #   2   48575443525C3BAE EG8145X6-10      3076  -18.29/1.93  fabian244553
        ont_object:OntObject = ont_list[idx]
        ont_object.sn = item[6:22].strip()
        ont_object.type = item[23:39].strip()
        ont_object.distance = item[40:45].strip()
        ont_object.rx_tx_power = item[46:58].strip()
        ont_object.description = item[59:].strip()
        
        if "_zone" in ont_object.description:
            
            invalid_index = ont_object.description.find("_zo")
            ont_object.description = ont_object.description[:invalid_index]

        ont_list[idx] = ont_object
        
    # 0123456789012345678901234567890123456789012345678901234567890123456789
    # 0         1         2         3         4         5         6
    
    return ont_list
