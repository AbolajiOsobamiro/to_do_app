import os
import json
from PySide6.QtCore import Qt, QTimer, QDateTime,QTime,QSize
from PySide6.QtGui import QColor, QPalette,QFont
from PySide6.QtWidgets import (
    QWidget,QMessageBox,QVBoxLayout,QPushButton,QListWidget,QLineEdit,QHBoxLayout,QListWidgetItem,
    QLabel,QDateTimeEdit,QApplication)
from PySide6.QtCore import QDate
import datetime
import os
import platform
from plyer import notification



class General:
    def __init__(self):
        self.todo_list = QListWidget()


class Additem (QWidget):
    def __init__(self,todo_list,save_callback):
        super().__init__()
        
    
        self.todo_list = todo_list
        self.save_callback = save_callback
        self.new_task_input = QLineEdit()
        self.new_task_input.returnPressed.connect(self.return_pressed)
        self.due_date_input = QDateTimeEdit()
        self.due_date_input.setCalendarPopup(True)
        self.due_date_input.setDate(QDate.currentDate())
        self.add_button = QPushButton("Add Task")
        self.add_button.clicked.connect(self.add_task)


        h_laout = QHBoxLayout()
        h_laout.addWidget(QLabel("Task:"))
        h_laout.addWidget(self.new_task_input)

        n_laout = QHBoxLayout()
        n_laout.addWidget(QLabel("Due Date:"))
        n_laout.addWidget(self.due_date_input)

        task_input_layout = QVBoxLayout()
        task_input_layout.addLayout(h_laout)
        task_input_layout.addLayout(n_laout)
        task_input_layout.addWidget(self.add_button)
        self.setLayout(task_input_layout)

        
    def add_task(self):
        task = self.new_task_input.text()
        due_date = self.due_date_input.date().toString("yyyy-MM-dd")
        due_time = self.due_date_input.time().toString("hh:mm")
        og_due_date = self.due_date_input.date().toString("yyyy-MM-dd hh:mm")
        if task:
            item = QListWidgetItem(f"{task} Deadline: {due_date} Time: {due_time}")
            item.setData(Qt.UserRole, [due_date,due_time])
            self.apply_item_styles(item)
            self.todo_list.addItem(item)
            self.new_task_input.clear()
            self.schedule_notification(task,due_date,due_time)
            self.save_callback()
            self.close()
            
        else:
            QMessageBox.warning(self,"Warning", "Task cannot be empty")

    def apply_item_styles(self,item):
            item.setBackground(Qt.darkBlue)
            item.setForeground(Qt.white)
            item.setFont(self.new_task_input.font())
            item.setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
            item.setSizeHint(item.sizeHint() + QSize(0,20))

    def return_pressed(self):
        self.add_task()


    def schedule_notification(self,task,due_date,due_time):
        try:
            due_date_dt = datetime.datetime.strptime(due_date, "%Y-%m-%d")
            due_date_str = self.due_date_input.dateTime().toString("yyyy-MM-dd hh:mm")

            interval = 30*60*1000
            self.timer = QTimer(self)
            self.timer.timeout.connect(lambda:self.show_notification(task,due_date_str))
            self.timer.start(interval)

            os_name = platform.system()
            if os_name == "Linux":
                self.schedule_linux_notification(task,due_date_dt,due_time)
            else:
                raise NotImplementedError(f"Unsupported OS: {os_name}")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to schedule notification: {e}")


    def show_notification(self,task,due_date_str):  
        current_time = datetime.datetime.now()
        due_date_dt = datetime.datetime.strptime(due_date_str, '%Y-%m-%d %H:%M')

        if current_time >= due_date_dt:
            self.timer.stop()
        else:        
            notification.notify(
                title = "Task Reminder",
                message = f"Reminder for task: {task} (Due: {due_date_dt})",
                timeout = 10
            )
    def schedule_linux_notification(self,task,due_date,due_time):
        try:
            due_date_str = due_date.strftime('%Y-%m-%d')
            due_time_str = due_time

            #event_command = f'calcurse -a -D "{task}" -c "/home/zero/.local/share/calcurse/apts"'
            #os.system(event_command)

            #notify_command = f'echo "notify-send \'Task Reminder\' \'{task}\'" | at {due_date.strftime("%H:%M %m/%d/%Y")}'
            #os.system(notify_command)

            print(f"Task '{task}' scheduled for {due_date_str} and time {due_time_str}")
        except Exception as e:
            print(f"Failed to schedule notificaton: {e}")


class TodoApp (QWidget,General):
    def __init__(self):
        QWidget.__init__(self)
        General.__init__(self)
        self.setWindowTitle("Task Scheduler")


        self.todo_list = QListWidget()
        self.w = None
        self.delete_button = QPushButton("Delete Task")
        self.load_tasks()

        self.delete_button.clicked.connect(self.delete_task)
        self.delete_button.setShortcut("del")

        self.add_button = QPushButton("Add Task")
        self.add_button.clicked.connect(self.show_add)

        b_laout = QHBoxLayout()
        b_laout.addWidget(self.add_button)
        b_laout.addWidget(self.delete_button)

        list_layout = QVBoxLayout()
        list_layout.addWidget(self.todo_list)
        list_layout.addLayout(b_laout)
        self.setLayout(list_layout)


    
    def show_add(self):
            self.w = Additem(self.todo_list,self.save_tasks)
            self.w.show()

        
    def delete_task(self):
        self.todo_list.takeItem(self.todo_list.currentRow())
        self.save_tasks()


    def save_tasks(self):
        tasks = []
        for index in range(self.todo_list.count()):
            item = self.todo_list.item(index)
            task_text = item.text()
            due_date = item.data(Qt.UserRole)
            tasks.append({"task": task_text, "due_date": due_date})
        with open("todo_list.json","w") as f:
            json.dump(tasks,f,indent=4)

    def load_tasks(self):
        if os.path.exists("todo_list.json"):
            with open("todo_list.json","r") as f:
                try:
                    tasks = json.load(f)
                    for task in tasks:
                        item = QListWidgetItem(task["task"])
                        item.setData(Qt.UserRole, task["due_date"])
                        self.apply_item_styles(item)
                        self.todo_list.addItem(item)
                except json.JSONDecodeError:
                    print("JSONDecodeError: The JSON file is empty or invalid.")
                    tasks = []
            

    def apply_item_styles(self,item):
        font = QFont()
        item.setBackground(Qt.darkBlue)
        item.setForeground(Qt.white)
        item.setFont(font)
        item.setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        item.setSizeHint(item.sizeHint() + QSize(0,20))



if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = TodoApp()
    window.show()
    sys.exit(app.exec())