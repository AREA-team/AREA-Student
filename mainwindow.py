from PyQt5.QtGui import QIcon, QPixmap

from redefined_widgets import Window
from UI.mainwindow_ui import Ui_MainWindow
from tools import ConnectThread, Server, Task
from task_dialog import TaskDialog


class MainWindow(Window, Ui_MainWindow):
    def __init__(self, task_table, personal_data, service, spreadsheet_id):
        super(MainWindow, self).__init__(self.setupUi)
        self.spreadsheet_id = spreadsheet_id
        self.service = service
        self.db: Server
        self.db = None
        self.good_conn = False
        self.need_auth = False
        self.task_table = task_table
        self.first_name, self.last_name, self.class_number, self.class_letter = personal_data
        self.deadlines = None
        self.subjects = None
        self.tasks = None
        self.tasks_deadlines = None
        self.index = None
        self.main_label.setText(f'{self.first_name} {self.last_name} '
                                f'{self.class_number + self.class_letter}')
        self.header.setHeight(30)
        self.logo_label.setPixmap(QPixmap('System Files/Logo.png'))
        self.add_task_btn.setIcon(QIcon('System Files/add_icon.png'))
        self.change_task_btn.setIcon(QIcon('System Files/change_icon.png'))
        self.submit_task_btn.setIcon(QIcon('System Files/submit_icon.png'))
        self.quit_btn.setIcon(QIcon('System Files/exit_icon.png'))

        self.connectThread = ConnectThread(self)
        self.connectThread.start()
        self.header.conn_state.clicked.connect(self.connectThread.start)
        self.connectThread.connected.connect(self.connected)
        self.connectThread.disconnected.connect(self.disable_window)
        self.quit_btn.clicked.connect(self.exit)
        self.parse_task_table()
        self.update_calendar()
        self.calendar.selectionChanged.connect(self.update_calendar)
        self.add_task_btn.clicked.connect(self.add_task)
        self.change_task_btn.clicked.connect(self.change_task)
        self.submit_task_btn.clicked.connect(self.submit_task)

    def add_task(self):
        task = self.tasks_list.selectedItems()[0] if self.tasks_list.selectedItems() else None
        tw = TaskDialog(mode='add',
                        task=task,
                        service=self.service,
                        task_table=self.task_table,
                        spreadsheet_id=self.spreadsheet_id
                        )
        tw.show()
        tw.exec()
        self.task_table = self.service.values().get(spreadsheetId=self.spreadsheet_id,
                                                    range='Контроль сдачи!A:DT').execute()
        self.parse_task_table()
        self.update_calendar()

    def change_task(self):
        if self.tasks_list.selectedItems():
            tw = TaskDialog(mode='change',
                            task=self.tasks_list.selectedItems()[0],
                            service=self.service,
                            task_table=self.task_table,
                            student_index=self.index,
                            spreadsheet_id=self.spreadsheet_id
                            )
            tw.show()
            tw.exec()
            self.task_table = self.service.values().get(spreadsheetId=self.spreadsheet_id,
                                                        range='Контроль сдачи!A:DT').execute()
            self.parse_task_table()
            self.update_calendar()

    def submit_task(self):
        if self.tasks_list.selectedItems():
            tw = TaskDialog(task=self.tasks_list.selectedItems()[0],
                            service=self.service,
                            task_table=self.task_table,
                            student_index=self.index,
                            spreadsheet_id=self.spreadsheet_id
                            )
            tw.show()
            tw.exec()
            self.task_table = self.service.values().get(spreadsheetId=self.spreadsheet_id,
                                                        range='Контроль сдачи!A:DT').execute()
            self.parse_task_table()
            self.update_calendar()

    def parse_task_table(self):
        self.subjects = self.task_table['values'][0][3:]
        for i in range(1, len(self.subjects)):
            if not self.subjects[i]:
                self.subjects[i] = self.subjects[i - 1]
        self.tasks = self.task_table['values'][2][3:]
        self.tasks_deadlines = self.task_table['values'][3][3:]

        for index, first_name, last_name, *deadlines in self.task_table['values'][4:]:
            if first_name == self.first_name and last_name == self.last_name:
                self.deadlines = deadlines
                self.index = index

    def update_calendar(self):
        self.tasks_list.clear()
        current_subject = None
        year, month, day = self.calendar.selectedDate().toPyDate().__str__().split('-')
        for tdi in range(len(self.tasks_deadlines)):
            if month == self.tasks_deadlines[tdi][3:5] and day == self.tasks_deadlines[tdi][:2] \
                    and not self.deadlines[tdi]:
                subject = self.subjects[tdi]
                task = self.tasks[tdi]
                hour, minute = self.tasks_deadlines[tdi][6:].split(':')
                if not current_subject or current_subject != subject:
                    self.tasks_list.addItem(
                        Task(year, month, day, hour, minute, subject, task, True))
                    current_subject = subject
                else:
                    self.tasks_list.addItem(Task(year, month, day, hour, minute, subject, task))
                self.update()
                self.repaint()

    def exit(self):
        self.need_auth = True
        self.close()

    def disable_window(self):
        self.connectThread.quit()
        self.header.conn_state.setIcon(QIcon(QPixmap('System Files/no_connection.png')))
        self.good_conn = False
        self.verticalLayout_2.setEnabled(False)
        self.header.setEnabled(True)

    def connected(self):
        self.connectThread.quit()
        self.db = self.connectThread.db
        self.header.conn_state.setIcon(QIcon(QPixmap('System Files/good_connection.png')))
        self.setEnabled(True)
        self.good_conn = True
