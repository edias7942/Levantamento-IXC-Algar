from .util import filter_object_attributes


def display_ont_info_summary(self, slot_no):
    self.start_conn()

    # self.tn.write(
    #     f"config".encode()
    # )

    # oltResponse = self.tn.read_until(b"#").decode()

    self.tn.write(
        f"display ont info summary 0/{slot_no} | no-more\n".encode()
    )

    oltResponse = self.tn.read_until(b":").decode()
    self.tn.write(f"\n".encode())
    
    oltResponse = self.tn.read_until(b"#").decode()
    
    result = oltResponse.split("\r\n")

    return result

