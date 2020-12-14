import sys
import webbrowser

from PyQt5.QtCore import QDateTime
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication
from redefined_widgets import Window
from UI.task_dialog_ui import Ui_Dialog
from tools import ConnectThread


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
        self.header.update_tables.setVisible(False)
        self.header.update_tables.setDisabled(True)
        self.header.setObjectName('')

        self.connectThread = ConnectThread(self)
        self.connectThread.start()
        self.header.conn_state.clicked.connect(self.connectThread.start)
        self.connectThread.connected.connect(self.connected)
        self.connectThread.disconnected.connect(self.disable_window)
        self.cancel_btn.clicked.connect(self.close)
        self.open_link_btn.clicked.connect(self.open_link)
        if mode == 'submit':
            self.submit_mode()
            self.ok_btn.clicked.connect(self.submit_task)
        elif mode == 'change':
            self.change_mode()
            self.ok_btn.clicked.connect(self.change_task)
        elif mode == 'add':
            self.add_mode()
            self.ok_btn.clicked.connect(self.add_task)

    def add_mode(self):
        self.formLayout.removeRow(4)
        subjects = sorted(set(filter(lambda x: x not in ['ФИО', '', 'Сделано / Не сделано / Всего'],
                                     self.task_table['values'][0])))
        self.subjects_cb.addItems(subjects)
        if not self.task:
            self.deadline_time.setDateTime(QDateTime().currentDateTime())
        else:
            self.deadline_time.setDateTime(self.task.deadline)

    def add_task(self):
        subject = self.subjects_cb.currentText()
        subjects = self.task_table['values'][0]
        index = subjects.index(subject) + 1
        while not subjects[index]:
            index += 1
        self.service.batchUpdate(spreadsheetId=self.spreadsheet_id,
                                 body={"requests": [
                                     {
                                         "insertDimension": {
                                             "range": {
                                                 "dimension": "COLUMNS",
                                                 "startIndex": index,
                                                 "endIndex": index + 1
                                             },
                                             "inheritFromBefore": True
                                         }
                                     }]}).execute()
        self.task_index = index
        task_letter = self.get_task_letter(self.task_index)
        excludes = [row[index - 1] if row[index - 1] == 'x' else ''
                    for row in self.task_table['values'][4:]]
        self.service.values().batchUpdate(spreadsheetId=self.spreadsheet_id,
                                          body={
                                              "valueInputOption": "USER_ENTERED",
                                              "data": [
                                                  {"range": 'Контроль сдачи!' + task_letter + '5:' +
                                                            task_letter + str(len(excludes) + 4),
                                                   "majorDimension": "COLUMNS",
                                                   "values": [excludes]}]}).execute()
        self.change_task()

    def open_link(self):
        link = self.link_le.text()
        if link:
            if link.startswith('http://') or link.startswith('https://'):
                webbrowser.open(link)
            else:
                webbrowser.open('https://' + link)

    def change_mode(self):
        self.subjects_cb.addItem(self.task.subject)
        self.task_tb.setPlainText(self.task.task)
        self.deadline_time.setDateTime(self.task.deadline)
        self.formLayout.removeRow(4)
        self.task_index = self.task_table['values'][0].index(self.task.subject)
        self.task_index += self.task_table['values'][2][self.task_index:].index(self.task.task)
        self.task_index += self.task_table['values'][3][self.task_index:].index(
            f"{self.task.deadline.toPyDateTime().strftime('%d.%m %H:%M')}")
        task_letter = self.get_task_letter(self.task_index)
        link = self.service.get(
            spreadsheetId=self.spreadsheet_id,
            ranges='Контроль сдачи!' + task_letter + '3',
            fields="sheets/data/rowData/values/hyperlink"
        ).execute()['sheets'][0]['data'][0]
        link = self.service.get(
            spreadsheetId=self.spreadsheet_id,
            ranges='Контроль сдачи!' + task_letter + '3',
            fields="sheets/data/rowData/values/hyperlink"
        ).execute()['sheets'][0]['data'][0]['rowData'][0]['values'][0]['hyperlink'] if link else ''
        self.link_le.setText(link)

    def change_task(self):
        task_letter = self.get_task_letter(self.task_index)
        link = self.link_le.text()
        text = self.task_tb.toPlainText().replace("\"", "\"\"")
        if link:
            self.service.values().batchUpdate(spreadsheetId=self.spreadsheet_id,
                                              body={
                                                  "valueInputOption": "USER_ENTERED",
                                                  "data": [
                                                      {"range": 'Контроль сдачи!' + task_letter +
                                                                '3' + ':' + task_letter + '4',
                                                       "majorDimension": "COLUMNS",
                                                       "values": [
                                                           [f'=ГИПЕРССЫЛКА("{link}'
                                                            f'";"{text}")',
                                                            self.deadline_time.dateTime(
                                                            ).toPyDateTime().strftime(
                                                                '%d.%m %H:%M')]]}]}).execute()
        else:
            self.service.values().batchUpdate(spreadsheetId=self.spreadsheet_id,
                                              body={
                                                  "valueInputOption": "USER_ENTERED",
                                                  "data": [
                                                      {"range": 'Контроль сдачи!' + task_letter +
                                                                '3' + ':' + task_letter + '4',
                                                       "majorDimension": "COLUMNS",
                                                       "values": [
                                                           [self.task_tb.toPlainText(),
                                                            self.deadline_time.dateTime(
                                                            ).toPyDateTime().strftime(
                                                                '%d.%m %H:%M')]]}]}).execute()
        self.close()

    def submit_mode(self):
        self.subjects_cb.addItem(self.task.subject)
        self.task_tb.setPlainText(self.task.task)
        self.task_tb.setReadOnly(True)
        self.link_le.setReadOnly(True)
        self.deadline_time.setDateTime(self.task.deadline)
        self.deadline_time.setReadOnly(True)
        self.delivery_time.setDateTime(QDateTime().currentDateTime())
        self.task_index = self.task_table['values'][0].index(self.task.subject)
        self.task_index += self.task_table['values'][2][self.task_index:].index(self.task.task)
        self.task_index += self.task_table['values'][3][self.task_index:].index(
            f"{self.task.deadline.toPyDateTime().strftime('%d.%m %H:%M')}")
        task_letter = self.get_task_letter(self.task_index)
        link = self.service.get(
            spreadsheetId=self.spreadsheet_id,
            ranges='Контроль сдачи!' + task_letter + '3',
            fields="sheets/data/rowData/values/hyperlink"
        ).execute()['sheets'][0]['data'][0]
        link = self.service.get(
            spreadsheetId=self.spreadsheet_id,
            ranges='Контроль сдачи!' + task_letter + '3',
            fields="sheets/data/rowData/values/hyperlink"
        ).execute()['sheets'][0]['data'][0]['rowData'][0]['values'][0]['hyperlink'] if link else ''
        self.link_le.setText(link)

    def submit_task(self):
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
        while task_index >= 0:
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
