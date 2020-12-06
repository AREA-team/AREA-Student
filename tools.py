from datetime import datetime
from socket import socket
from urllib.request import urlopen

from PyQt5.QtCore import QThread, pyqtSignal, QDateTime
from PyQt5.QtWidgets import QListWidgetItem

SERVER_IP = urlopen('https://github.com/AREA-team/AREA-Student/releases/download/v1.0/IP_SERVER.txt'
                    ).read().decode()
SERVER_PORT = 14600


class Server:
    def __init__(self):
        self.s = socket()
        self.s.settimeout(1.0)
        try:
            self.s.connect((SERVER_IP, SERVER_PORT))
        except ConnectionError:
            raise ServerUnreachableException
        self.correct_public_key()
        self.send_private_key()
        self.json_key = self.s.recv(4096).decode('utf-8') + self.s.recv(4096).decode('utf-8')

    def correct_public_key(self):
        if self.s.recv(4096).decode('utf-8') == open('System Files/public key.txt').read():
            return True
        else:
            raise ServerUnreachableException

    def send_private_key(self):
        self.s.send(bytes(open('System Files/private key.txt').read().encode('utf-8')))

    def make_request(self, request, window):
        try:
            self.s.send(bytes(request.encode('utf-8')))
            return self.s.recv(4096).decode('utf-8').split('~')
        except ConnectionError:
            window.disable_window()
            return []

    def get_json_key(self):
        return self.json_key


class ConnectThread(QThread):
    connected = pyqtSignal()
    disconnected = pyqtSignal()

    def __init__(self, window):
        super().__init__()
        self.db = None
        self.window = window

    def run(self):
        if not self.window.good_conn:
            try:
                self.db = Server()
                self.connected.emit()
            except ServerUnreachableException or TimeoutError:
                self.disconnected.emit()


class Task(QListWidgetItem):
    def __init__(self, year, month, day, hour, minute, subject, task, need_show_subject=False):
        self.task = task
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.subject = subject
        self.deadline = QDateTime(datetime(*map(int, (year, month, day, hour, minute))))
        if not need_show_subject:
            super(Task, self).__init__(f'    {hour}:{minute} | {task}')
        else:
            super(Task, self).__init__(f'{subject}:\n    {hour}:{minute} | {task}')


class ServerUnreachableException(ConnectionError):
    pass


class UserNotRegisteredException(Exception):
    pass


class BadPasswordException(Exception):
    pass


class UserAuthorizedException(Exception):
    pass


class UserRegisteredException(Exception):
    pass
