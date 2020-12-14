import os
import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from auth import AuthDialog
from mainwindow import MainWindow

__author__ = "Nikulin Vasiliy"
__credits__ = ["Pritchin Vsevolod", "Emelyanova Alexandra"]
__version__ = "1.0"
__maintainer__ = "Nikulin Vasiliy"
__email__ = "nikulin.vasily.777@yandex.ru"
__status__ = "Production"

if __name__ == '__main__':
    if os.path.exists('homework-spreadsheet-d24c606fd7ba.json'):
        os.remove('homework-spreadsheet-d24c606fd7ba.json')
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('System Files/Logo.ico'))
    need_auth = True
    while need_auth:
        auth = AuthDialog()
        auth.exec()
        if auth.good_conn:
            auth.db.s.send(bytes('end'.encode()))
            auth.db.s.close()
        need_auth = False
        if auth.authorized:
            main = MainWindow(auth.table_tasks, auth.personal_data, auth.service,
                              auth.spreadsheet_id)
            main.show()
            main.exec()
            main.db.s.send(bytes('end'.encode()))
            main.db.s.close()
            need_auth = main.need_auth
    if os.path.exists('homework-spreadsheet-d24c606fd7ba.json'):
        os.remove('homework-spreadsheet-d24c606fd7ba.json')
    sys.exit()
