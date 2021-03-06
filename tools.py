from socket import socket, timeout
from datetime import datetime

from PyQt5.QtCore import QDateTime, QThread, pyqtSignal
from PyQt5.QtWidgets import QListWidgetItem
from requests import get as load_document


class Server:
    def __init__(self):
        self.s = socket()
        self.s.settimeout(3.0)
        try:
            self.s.connect(self.server_ip_and_port())
        except ConnectionRefusedError:
            raise ServerUnreachableException
        self.correct_public_key()
        self.send_private_key()
        self.json_key = ''
        try:
            while not self.json_key or self.json_key[-2] != '}':
                self.json_key += self.s.recv(32768).decode()
        except timeout:
            pass

    @staticmethod
    def server_ip_and_port():
        server_port = 14600
        server_ip = load_document(
            'https://docs.google.com/document/d/1NNOzkKw3Cte_lM2tqhCmSrrzHz17Y6btJo39OajEXNM/edit'
        ).content.split(b'<meta property="og:description" content="', 1)[1].split(b'"', 1)[
            0].decode()
        return server_ip, server_port

    def correct_public_key(self):
        if self.s.recv(4096).decode() == open('System Files/public key.txt').read():
            return True
        return False

    def send_private_key(self):
        self.s.send(bytes(open('System Files/private key.txt').read().encode()))

    def make_request(self, request, window):
        try:
            self.s.send(bytes(request.encode()))
            return self.s.recv(4096).decode().split('~')
        except ConnectionError:
            window.disable_window()
            return []
        except timeout:
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
            except ServerUnreachableException:
                self.disconnected.emit()
            except TimeoutError:
                self.disconnected.emit()
            except timeout:
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
