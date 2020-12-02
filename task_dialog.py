import sys

from PyQt5.QtCore import QDateTime
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication
from redefined_widgets import Window
from UI.task_dialog_ui import Ui_Dialog
from tools import ConnectThread
from datetime import datetime


class TaskDialog(Window, Ui_Dialog):
    def __init__(self, mode='submit', task=None, service=None, task_table=None, student_index=1,
                 spreadsheet_id=''):
        super(TaskDialog, self).__init__(self.setupUi)
        self.spreadsheet_id = spreadsheet_id
        self.task_index = None
        self.student_index = student_index
        self.task_table = task_table
        self.service = service
        self.task = task
        self.good_conn = False
        self.header.setHeight(30)
        self.connectThread = ConnectThread(self)
        self.connectThread.start()
        self.header.conn_state.clicked.connect(self.connectThread.start)
        self.connectThread.connected.connect(self.connected)
        self.connectThread.disconnected.connect(self.disable_window)
        self.cancel_btn.clicked.connect(self.close)
        if mode == 'submit':
            self.submit_mode()
            self.ok_btn.clicked.connect(self.submit_task)
        elif mode == 'change':
            pass
        elif mode == 'add':
            pass

    def submit_mode(self):
        self.subjects_cb.addItem(self.task.subject)
        self.task_tb.setPlainText(self.task.task)
        self.task_tb.setReadOnly(True)
        self.deadline_time.setDateTime(self.task.deadline)
        self.deadline_time.setReadOnly(True)
        self.delivery_time.setDateTime(QDateTime(datetime.now()))

    def submit_task(self):
        self.task_index = self.task_table['values'][0].index(self.task.subject)
        self.task_index += self.task_table['values'][2][self.task_index:].index(self.task.task)
        self.task_index += self.task_table['values'][3][self.task_index:].index(
            f"{self.task.deadline.toPyDateTime().strftime('%d.%m %H:%M')}")
        task_letter = self.get_task_letter(self.task_index)
        self.service.values().batchUpdate(spreadsheetId=self.spreadsheet_id,
                                          body={
                                              "valueInputOption": "USER_ENTERED",
                                              "data": [
                                                  {"range": 'Контроль сдачи!' + task_letter + str(
                                                      int(self.student_index) + 4),
                                                   "majorDimension": "ROWS",
                                                   "values": [
                                                       [self.delivery_time.dateTime().toPyDateTime(
                                                       ).strftime('%d.%m %H:%M')]]}]}).execute()
        self.close()

    @staticmethod
    def get_task_letter(task_index):
        task_letter = ''
        alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        for _ in range(task_index // 26 + 1):
            if task_index >= 26:
                task_letter += alphabet[task_index // 26 - 1]
                task_index %= 26
            else:
                task_letter += alphabet[task_index % 26]
                task_index -= 26
        return task_letter

    def disable_window(self):
        self.connectThread.quit()
        self.header.conn_state.setIcon(QIcon(QPixmap('System Files/no_connection.png')))
        self.good_conn = False
        self.verticalLayout_2.setEnabled(False)
        self.header.setEnabled(True)

    def connected(self):
        self.connectThread.quit()
        self.header.conn_state.setIcon(QIcon(QPixmap('System Files/good_connection.png')))
        self.setEnabled(True)
        self.good_conn = True


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wnd = TaskDialog()
    wnd.show()
    sys.exit(app.exec())
