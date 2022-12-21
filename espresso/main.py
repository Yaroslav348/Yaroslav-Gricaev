import sqlite3
import sys
from PyQt5 import uic  
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QDialog


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('UI/UI.ui', self)
        self.connection = sqlite3.connect("data/coffee.sqlite")
        self.select_data()
        self.btn.clicked.connect(self.select_data)
        self.btn_2.clicked.connect(self.addEditForm)
        
    def select_data(self):
        cur = self.connection.cursor()
        res = cur.execute(""" 
                SELECT * FROM coffee
                """).fetchall()
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(0)
        self.names = list(map(lambda x: x[0], cur.description))
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.setHorizontalHeaderLabels(self.names)
    
    def addEditForm(self):
        form = addEditCoffee()
        form.exec()


class addEditCoffee(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        uic.loadUi('UI/addEditCoffeeForm.ui', self)
        self.isAdd= True
        self.lineEdits = ['lineEdit_' + str(i) for i in range(1, 7)]
        self.id = ex.tableWidget.rowCount() + 1
        self.label_edit.setVisible(False)
        self.lineEdit_edit.setVisible(False)
        self.btn_2.setVisible(False)
        self.btn.clicked.connect(self.add)
        self.btn_2.clicked.connect(self.findByTitle)
        self.comboBox.currentTextChanged.connect(self.change)

    def add(self):
        text = list()
        self.id += 1
        if self.isAdd:
            text.append(self.id)
            for line in self.lineEdits:
                string = eval('self.{}.text()'.format(line))
                eval('self.{}.setText("")'.format(line))
                if string == '':
                    text.append(None)
                else:
                    text.append(string)
            text = tuple(text)
            cur = ex.connection.cursor()
            cur.execute(""" 
                INSERT INTO coffee VALUES(?,?,?,?,?,?,?)
                """, text)
            ex.connection.commit()
        else:
            for line in self.lineEdits:
                string = eval('self.{}.text()'.format(line))
                eval('self.{}.setText("")'.format(line))
                if string == '':
                    text.append(None)
                else:
                    text.append(string)
            text.append(self.lineEdit_edit.text().capitalize())
            text = tuple(text)
            cur = ex.connection.cursor()
            cur.execute(""" 
                UPDATE coffee
                SET title = ?,
                roast = ?,
                'ground/in grains' = ?,
                description = ?,
                price = ?,
                'serving size (oz)' = ?
                WHERE title = ?
                """, text)
            ex.connection.commit()

    def change(self):
        if self.comboBox.currentText() == 'Add':
            self.isAdd= True
            self.label_edit.setVisible(False)
            self.lineEdit_edit.setVisible(False)
            self.btn_2.setVisible(False)
            self.btn.setText('Add')
        else:
            self.isAdd= False
            self.label_edit.setVisible(True)
            self.lineEdit_edit.setVisible(True)
            self.btn_2.setVisible(True)
            self.btn.setText('Edit')

    def findByTitle(self):
        title = self.lineEdit_edit.text().capitalize()
        cur = ex.connection.cursor()
        res = cur.execute(""" 
                    SELECT * FROM coffee
                    WHERE title = ?
                """, (title,)).fetchone()
        for i in range(6):
            eval('self.{}.setText("{}")'.format(self.lineEdits[i], res[i + 1]))



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())