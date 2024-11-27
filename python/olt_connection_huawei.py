#!/usr/bin/python3
# _*_ coding:utf-8 _*_

import telnetlib


class olt_connection:
    def __init__(self, dado):
        self.ip = dado["ip"]
        self.usuario = dado["usuario"]
        self.senha = dado["senha"]

    def start_conn(self):
        self.tn = telnetlib.Telnet()
        self.tn.open(self.ip, "23", 100)
        print(self.tn.read_until("name:".encode()))
        self.tn.write((self.usuario + "\n").encode())
        print(self.tn.read_until(b":"))
        self.tn.write((self.senha + "\n").encode())
        print(self.tn.read_until(b">").decode())
        print(self.tn.read_until(b">").decode())

        self.tn.write("enable\n".encode())
        print(self.tn.read_until(b"#").decode())

        return self

    def command(self, command):
        self.start_conn()

        self.tn.write(f"{command}\n".encode())

        oltResponse = self.tn.read_until(b"#").decode()

        return oltResponse

    def open_terminal(self):
        self.start_conn()

        command = ""

        start_with = ""
        while command != "exit!":

            command = input(f"#{start_with} ")

            if command == "":
                continue

            if "?" in command:
                self.tn.write(f"{command}".encode())
                oltResponse = self.tn.read_until(f"#{command[:-2]}".encode()).decode()
                start_with = command[:-2]

            else:
                self.tn.write(f"{command}\n".encode())
                oltResponse = self.tn.read_until(b"#").decode()
                start_with = ""

            print(oltResponse)
