import sys
from PySide6 import QtWidgets
from widget import TodoApp


app = QtWidgets.QApplication(sys.argv)

window = TodoApp()
window.show()
app.exec()