import sys
from PyQt5 import uic
from PyQt5.QtCore import Qt, QPointF, QObject
from random import randint
from PyQt5.QtGui import QPainter, QColor, QPen, QPainterPath
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('UI.ui', self)
        self.do_paint = False
        self.btn.clicked.connect(self.paint)
    
    def paint(self):
        self.do_paint = True
        self.repaint()

    def paintEvent(self, event):
        if self.do_paint:
            qp = QPainter()
            qp.begin(self)
            for x in range(150, 800, 500):
                for y in range(100, 650, 200):
                    self.draw_circle(qp, x, y)
            for y in range(100, 501, 400):
                self.draw_circle(qp, 400, y)
            qp.end()

    def draw_circle(self, qp, x, y):
        qp.setBrush(QColor(255, 255, 0))
        length = min(x, y, randint(10, 60))
        center = QPointF(x, y)
        qp.drawEllipse(center, length, length)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())