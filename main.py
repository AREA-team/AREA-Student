import sys
from PyQt5.QtWidgets import QApplication
from auth import AuthDialog
from mainwindow import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
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
    sys.exit()
