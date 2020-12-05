import ctypes
import os
import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from auth import AuthDialog
from mainwindow import MainWindow


def is_admin():
    return ctypes.windll.shell32.IsUserAnAdmin()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('System Files\\Logo.ico'))
    need_auth = True
    while need_auth:
        auth = AuthDialog()
        auth.exec()
        need_auth = False
        if auth.authorized:
            main = MainWindow(auth.table_tasks, auth.personal_data, auth.service,
                              auth.spreadsheet_id)
            main.show()
            main.exec()
            need_auth = main.need_auth
    if os.path.exists('homework-spreadsheet-d24c606fd7ba.json'):
        os.remove('homework-spreadsheet-d24c606fd7ba.json')
    sys.exit()
