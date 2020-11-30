import sys

from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication

from redefined_widgets import Window
from UI.mainwindow_ui import Ui_MainWindow
from tools import Server, ServerUnreachableException


class MainWindow(Window, Ui_MainWindow):
    def __init__(self, task_table, personal_data):
        super(MainWindow, self).__init__(self.setupUi)
        self.db = None
        self.good_conn = False
        self.need_auth = False
        self.task_table = task_table
        self.first_name, self.last_name, self.class_number, self.class_letter = personal_data
        self.main_label.setText(f'{self.first_name} {self.last_name} '
                                f'{self.class_number + self.class_letter}')
        self.header.setHeight(30)
        self.logo_label.setPixmap(QPixmap('System Files/Logo.png'))
        self.connect_with_server()
        self.header.conn_state.clicked.connect(self.connect_with_server)
        self.quit_btn.clicked.connect(self.exit)

    def exit(self):
        self.need_auth = True
        self.close()

    def connect_with_server(self):
        if not self.good_conn:
            try:
                self.db = Server()
                self.header.conn_state.setIcon(QIcon(QPixmap('System Files/good_connection.png')))
                self.verticalLayout_2.setEnabled(True)
                self.good_conn = True
            except ServerUnreachableException:
                self.disable_window()

    def disable_window(self):
        self.header.conn_state.setP(QIcon(QPixmap('System Files/no_connection.png')))
        self.good_conn = False
        self.verticalLayout_2.setEnabled(False)
        self.header.setEnabled(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wnd = MainWindow(1, ('Никулин', 'Василий', '10', 'А'))
    wnd.show()
    sys.exit(app.exec())
