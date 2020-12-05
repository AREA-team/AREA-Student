import sys

from subprocess import call

import googleapiclient.discovery
import httplib2

from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QApplication

from oauth2client.service_account import ServiceAccountCredentials

from redefined_widgets import Window
from tools import BadPasswordException, UserNotRegisteredException, \
    UserRegisteredException, ConnectThread
from UI.auth_ui import Ui_Dialog

SERVER_IP = '188.19.106.140'
SERVER_PORT = 14600


class AuthDialog(Window, Ui_Dialog):
    def __init__(self):
        super(AuthDialog, self).__init__(self.setupUi)
        self.bad_stylesheet = 'QLabel{font: 57 14pt "IBM Plex Sans"; color: rgb(255, 0, 0)}'
        self.good_stylesheet = 'QLabel{font: 57 14pt "IBM Plex Sans"; color: rgb(0, 170, 0)}'
        self.authorized = False
        self.header.setHeight(30)
        self.personal_data = None
        self.table_tasks = None
        self.table_emails = None
        self.good_conn = False
        self.changing = False
        self.widget_type = None
        self.db = None
        self.countries = None
        self.cities = None
        self.schools = None
        self.class_numbers = None
        self.class_letters = None
        self.service = None
        self.spreadsheet_id = None
        self.setMouseTracking(True)

        self.header.update_tables.setVisible(False)
        self.header.update_tables.setDisabled(True)
        self.header.setObjectName('')
        self.connectThread = ConnectThread(self)
        self.connectThread.start()
        self.header.conn_state.clicked.connect(self.connectThread.start)
        self.connectThread.connected.connect(self.connected)
        self.connectThread.disconnected.connect(self.disable_window)
        self.sign_in_btn.clicked.connect(self.sign_in)
        self.sign_up_btn.clicked.connect(self.sign_up)

    def check_cookie(self):
        lines = list(map(lambda x: x.strip(), open('System Files/cookie.txt',
                                                   encoding='utf-8').readlines()))
        if len(lines) == 7:
            email, cookie, first_name, last_name, class_number, class_letter, school = lines
            password = self.db.make_request(f'get_password~{email}', self)[0]
            if hash(password) == hash(cookie):
                self.authorized = True
                self.personal_data = first_name, last_name, class_number, class_letter
                credentials_file = 'homework-spreadsheet-d24c606fd7ba.json'
                credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, [
                    'https://www.googleapis.com/auth/spreadsheets',
                    'https://www.googleapis.com/auth/drive'])
                http_auth = credentials.authorize(httplib2.Http())
                self.service = googleapiclient.discovery.build('sheets', 'v4',
                                                               http=http_auth).spreadsheets()
                self.spreadsheet_id = self.db.make_request(
                    f"get_class_journal_link~{school}~{class_number}~{class_letter}", self)[0]
                self.table_tasks = self.service.values(). \
                    get(spreadsheetId=self.spreadsheet_id, range='Контроль сдачи!A:DT').execute()
                self.close()
                return True

    def get_tables(self, school, class_number, class_letter):
        credentials_file = 'homework-spreadsheet-d24c606fd7ba.json'
        credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'])
        http_auth = credentials.authorize(httplib2.Http())
        service = googleapiclient.discovery.build('sheets', 'v4', http=http_auth)
        spreadsheet_id = self.db.make_request(f"get_class_journal_link~{school}~{class_number}~"
                                              f"{class_letter}", self)[0]
        self.table_tasks = service.spreadsheets().values(). \
            get(spreadsheetId=spreadsheet_id, range='Контроль сдачи!A:DT').execute()
        self.table_emails = service.spreadsheets().values(). \
            get(spreadsheetId=spreadsheet_id, range='Электронные почты!A:D').execute()
        self.service = service.spreadsheets()
        self.spreadsheet_id = spreadsheet_id
        return service.spreadsheets(), spreadsheet_id

    def authorize(self, mode='auth'):
        if mode == 'auth':
            school = self.school_cb_1.currentText()
            class_number = self.class_number_cb_1.currentText()
            class_letter = self.class_letter_cb_1.currentText()
            first_name = self.first_name_le_1.text()
            last_name = self.last_name_le_1.text()
            password = self.password_le_1.text()
            self.personal_data = first_name, last_name, class_number, class_letter
            self.get_tables(school, class_number, class_letter)
            for index, first_name_val, last_name_val, *email_val in self.table_emails['values']:
                if first_name_val == first_name and last_name_val == last_name and email_val:
                    email = email_val[0]
                    normal_password = self.db.make_request(f'get_password~{email}', self)[0]
                    if normal_password == ' ':
                        raise UserNotRegisteredException
                    elif password == normal_password:
                        f = open('System Files/cookie.txt', 'w', encoding='utf-8')
                        f.write(('\n'.join([email, password, *self.personal_data, school])))
                        return True
                    raise BadPasswordException
            raise UserNotRegisteredException
        elif mode == 'register':
            school = self.school_cb_2.currentText()
            class_number = self.class_number_cb_2.currentText()
            class_letter = self.class_letter_cb_2.currentText()
            first_name = self.first_name_le_2.text()
            last_name = self.last_name_le_2.text()
            password = self.password_le_2.text()
            email = self.email_le_2.text()
            self.personal_data = first_name, last_name, class_number, class_letter
            table_email, spreadsheet_id = self.get_tables(school, class_number, class_letter)
            for index, first_name_val, last_name_val, *email_val in self.table_emails['values']:
                if first_name_val == first_name and last_name_val == last_name:
                    table_email.values().batchUpdate(spreadsheetId=spreadsheet_id,
                                                     body={"valueInputOption": "USER_ENTERED",
                                                           "data": [
                                                               {
                                                                   "range": 'Электронные почты!D' +
                                                                            str(int(index) + 1),
                                                                   "majorDimension": "ROWS",
                                                                   "values": [[email]]}
                                                           ]
                                                           }).execute()
                    if self.db.make_request(f'add_email~{email}~{password}', self)[0] == \
                            'Successful':
                        f = open('System Files/cookie.txt', 'w', encoding='utf-8')
                        f.write('\n'.join([email, password, *self.personal_data, school]))
                        return True
                    raise UserRegisteredException
                elif first_name_val == first_name and last_name_val == last_name and email_val:
                    raise UserRegisteredException
            else:
                raise UserNotRegisteredException

    def sign_in(self):
        first_name = self.first_name_le_1.text()
        last_name = self.last_name_le_1.text()
        password = self.password_le_1.text()
        self.state_label1.setStyleSheet(self.bad_stylesheet)
        if not first_name:
            self.state_label1.setText('Введите фамилию')
        elif not last_name:
            self.state_label1.setText('Введите имя')
        elif not password:
            self.state_label1.setText('Введите пароль')
        else:
            self.state_label1.setText('Авторизация...')
            self.state_label1.setStyleSheet(self.good_stylesheet)
            self.repaint()
            try:
                if self.authorize():
                    self.authorized = True
                    self.close()
            except UserNotRegisteredException:
                self.state_label1.setText('Вы не зарегистрированы')
            except BadPasswordException:
                self.state_label1.setText('Неверный пароль')
            finally:
                self.state_label1.setStyleSheet(self.bad_stylesheet)

    def sign_up(self):
        first_name = self.first_name_le_2.text()
        last_name = self.last_name_le_2.text()
        password = self.password_le_2.text()
        password_repeat = self.password_repeat_le_2.text()
        self.state_label2.setStyleSheet(self.bad_stylesheet)
        if not first_name:
            self.state_label2.setText('Введите фамилию')
        elif not last_name:
            self.state_label2.setText('Введите имя')
        elif not password:
            self.state_label2.setText('Введите пароль')
        elif password != password_repeat:
            self.state_label2.setText('Пароли не совпадают')
        else:
            self.state_label2.setText('Регистрация...')
            self.state_label2.setStyleSheet(self.good_stylesheet)
            self.repaint()
            try:
                if self.authorize(mode='register'):
                    self.authorized = True
                    self.db = None
                    self.close()
            except UserRegisteredException:
                self.state_label2.setText('Вы уже зарегистрированы')
            except UserNotRegisteredException:
                self.state_label2.setText('Вас нет в списке класса')
            except BadPasswordException:
                self.state_label2.setText('Неверный пароль')
            finally:
                self.state_label2.setStyleSheet(self.bad_stylesheet)

    def setup_widgets(self):
        self.changing = True
        self.country_cb_1.clear()
        self.country_cb_2.clear()
        self.countries = self.db.make_request(f"get_countries", self, self.countries)
        self.country_cb_1.addItems(self.countries)
        self.country_cb_2.addItems(self.countries)

    def connect_widgets_updates(self):
        self.country_cb_1.currentTextChanged.connect(self.country_changed)
        self.country_cb_2.currentTextChanged.connect(self.country_changed)
        self.city_cb_1.currentTextChanged.connect(self.city_changed)
        self.city_cb_2.currentTextChanged.connect(self.city_changed)
        self.school_cb_1.currentTextChanged.connect(self.school_changed)
        self.school_cb_2.currentTextChanged.connect(self.school_changed)
        self.class_number_cb_1.currentTextChanged.connect(self.class_number_changed)
        self.class_number_cb_2.currentTextChanged.connect(self.class_number_changed)
        self.class_letter_cb_1.currentTextChanged.connect(self.class_letter_changed)
        self.class_letter_cb_2.currentTextChanged.connect(self.class_letter_changed)
        self.first_name_le_1.textChanged.connect(self.first_name_changed)
        self.first_name_le_2.textChanged.connect(self.first_name_changed)
        self.last_name_le_1.textChanged.connect(self.last_name_changed)
        self.last_name_le_2.textChanged.connect(self.last_name_changed)
        self.password_le_1.textChanged.connect(self.password_changed)
        self.password_le_2.textChanged.connect(self.password_changed)

    def country_changed(self):
        if not self.changing and self.sender().currentText():
            self.changing = True
            text = self.sender().currentText()
            self.country_cb_1.clear()
            self.country_cb_2.clear()
            self.countries = self.db.make_request(f"get_countries", self, self.countries)
            self.country_cb_1.addItems(self.countries)
            self.country_cb_2.addItems(self.countries)
            self.country_cb_1.setCurrentText(text)
            self.country_cb_2.setCurrentText(text)
            self.city_changed(False)

    def city_changed(self, native=True):
        if not self.changing or not native and self.sender().currentText():
            self.changing = True
            text = self.sender().currentText()
            self.city_cb_1.clear()
            self.city_cb_2.clear()
            self.cities = self.db.make_request(f"get_cities~{self.country_cb_1.currentText()}",
                                               self, self.cities)
            self.city_cb_1.addItems(self.cities)
            self.city_cb_2.addItems(self.cities)
            if native:
                self.city_cb_1.setCurrentText(text)
                self.city_cb_2.setCurrentText(text)
            self.school_changed(False)

    def school_changed(self, native=True):
        if not self.changing or not native and self.sender().currentText():
            self.changing = True
            text = self.sender().currentText()
            self.school_cb_1.clear()
            self.school_cb_2.clear()
            self.schools = self.db.make_request(f"get_schools~{self.country_cb_1.currentText()}~"
                                                f"{self.city_cb_1.currentText()}",
                                                self, self.schools)
            self.school_cb_1.addItems(self.schools)
            self.school_cb_2.addItems(self.schools)
            if native:
                self.school_cb_1.setCurrentText(text)
                self.school_cb_2.setCurrentText(text)
            self.class_number_changed(False)

    def class_number_changed(self, native=True):
        if not self.changing or not native and self.sender().currentText():
            self.changing = True
            text = self.sender().currentText()
            self.class_number_cb_1.clear()
            self.class_number_cb_2.clear()
            self.class_numbers = self.db.make_request(f"get_class_numbers~"
                                                      f"{self.school_cb_1.currentText()}",
                                                      self, self.class_numbers)
            self.class_number_cb_1.addItems(self.class_numbers)
            self.class_number_cb_2.addItems(self.class_numbers)
            if native:
                self.class_number_cb_1.setCurrentText(text)
                self.class_number_cb_2.setCurrentText(text)
            self.class_letter_changed(False)

    def class_letter_changed(self, native=True):
        if not self.changing or not native and self.sender().currentText():
            self.changing = True
            text = self.sender().currentText()
            self.class_letter_cb_1.clear()
            self.class_letter_cb_2.clear()
            self.class_letters = self.db.make_request(
                f"get_class_letters~{self.school_cb_1.currentText()}~"
                f"{self.class_number_cb_1.currentText()}", self, self.class_letters)
            self.class_letter_cb_1.addItems(self.class_letters)
            self.class_letter_cb_2.addItems(self.class_letters)
            if native:
                self.class_letter_cb_1.setCurrentText(text)
                self.class_letter_cb_2.setCurrentText(text)
            self.changing = False

    def first_name_changed(self):
        text = self.sender().text()
        self.first_name_le_1.setText(text)
        self.first_name_le_2.setText(text)

    def last_name_changed(self):
        text = self.sender().text()
        self.last_name_le_1.setText(text)
        self.last_name_le_2.setText(text)

    def password_changed(self):
        text = self.sender().text()
        self.password_le_1.setText(text)
        self.password_le_2.setText(text)

    def connected(self):
        self.connectThread.quit()
        self.db = self.connectThread.db
        self.header.conn_state.setIcon(QIcon(QPixmap('System Files/good_connection.png')))
        self.tabWidget.setDisabled(False)
        self.good_conn = True
        self.get_json_key()
        if not self.check_cookie():
            self.connect_widgets_updates()
            self.country_cb_1.addItems(self.db.make_request(f"get_countries", self))
            self.show()

    def disable_window(self):
        self.connectThread.quit()
        self.header.conn_state.setIcon(QIcon(QPixmap('System Files/no_connection.png')))
        self.good_conn = False
        self.tabWidget.setDisabled(True)
        self.header.setEnabled(True)
        self.show()

    def get_json_key(self):
        f = open('homework-spreadsheet-d24c606fd7ba.json', 'w')
        f.write(self.db.get_json_key())
        f.close()
        call(['attrib', '+h', 'homework-spreadsheet-d24c606fd7ba.json'])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wnd = AuthDialog()
    wnd.show()
    sys.exit(app.exec())
