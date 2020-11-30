from socket import socket

SERVER_IP = '188.19.106.140'
SERVER_PORT = 14600


class Server:
    def __init__(self):
        self.s = socket()
        try:
            self.s.connect((SERVER_IP, SERVER_PORT))
        except ConnectionError:
            raise ServerUnreachableException
        if self.correct_public_key():
            self.send_private_key()
        else:
            raise ServerUnreachableException

    def correct_public_key(self):
        return self.s.recv(1024).decode('utf-8') == open('System Files/public key.txt').read()

    def send_private_key(self):
        self.s.send(bytes(open('System Files/private key.txt').read().encode('utf-8')))

    def make_request(self, request, window, current_items=None):
        if current_items is None:
            current_items = []
        try:
            self.s.send(bytes(request.encode('utf-8')))
            return self.s.recv(1024).decode('utf-8').split('~')
        except ConnectionError:
            window.disable_window()
            return current_items


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
