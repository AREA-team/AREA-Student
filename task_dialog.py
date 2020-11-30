import sys

from PyQt5.QtWidgets import QApplication, QMainWindow

from UI.task_dialog_ui import Ui_Dialog


class Dialog(QMainWindow, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.cancel_btn.clicked.connect(self.close)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wnd = Dialog()
    wnd.show()
    sys.exit(app.exec())
