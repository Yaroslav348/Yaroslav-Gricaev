import sqlite3
import sys
from PyQt5 import uic  
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('UI.ui', self)
        self.connection = sqlite3.connect("coffee.sqlite")
        self.btn.clicked.connect(self.select_data)
        
    def select_data(self):
        cur = self.connection.cursor()
        res = cur.execute(""" 
                SELECT * FROM coffee
                """).fetchall()
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setRowCount(0)
        names = list(map(lambda x: x[0], cur.description))
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.setHorizontalHeaderLabels(names)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())