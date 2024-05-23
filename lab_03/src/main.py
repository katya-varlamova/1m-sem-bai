import sys
import form
import numpy as np

from Bezier import Bezier
from numpy import array as a

from PyQt5 import QtCore, QtGui
from PyQt5 import QtWidgets
from PyQt5.QtGui import QImage
from PyQt5.QtCore import Qt

from genetic import RunGA
from swarm import RunSwarm
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import time
wind = None
pointt = []
class Scene(QtWidgets.QGraphicsScene):
    def mousePressEvent(self, QMouseEvent):
        if (QMouseEvent.button() == Qt.LeftButton):
            add_point(QMouseEvent.scenePos())

            self.update()

class Visual(QtWidgets.QMainWindow, form.Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.graphicsView_2.scale(1, 1)
        self.h = self.graphicsView_2.height()
        self.w = self.graphicsView_2.width()
        self.scene = Scene(0, 0, self.w - 2, self.h - 2)
        self.scene.win = self
        self.graphicsView_2.setScene(self.scene)
        self.image = QImage(561, 581, QImage.Format_ARGB32_Premultiplied)
        self.image.fill(Qt.white)
        self.pen_point = QtGui.QPen(QtCore.Qt.black)
        self.pen_rest = QtGui.QPen(QtCore.Qt.blue)
        self.pen_genetic = QtGui.QPen(QtCore.Qt.red)
        self.pen_pso = QtGui.QPen(QtCore.Qt.green)
        self.pen_point.setWidth(5)
        self.pen_rest.setWidth(3)
        self.pen_genetic.setWidth(3)
        self.pen_pso.setWidth(3)

        self.besier_x = []
        self.besier_y = []

        self.pushButton.clicked.connect(self.besier)
        self.pushButton_2.clicked.connect(self.genetic)
        self.pushButton_3.clicked.connect(self.PSO)
        self.pushButton_4.clicked.connect(self.stat)
        self.pushButton_5.clicked.connect(self.clear)
        self.draw_axis()
    def draw_axis(self):
        w = self.w
        h = self.h
        self.scene.addLine(5, 5,
                           w - 5, 5, QtGui.QPen(QtCore.Qt.black))
        self.scene.addLine(w - 5, 5,
                           w - 20, 10, QtGui.QPen(QtCore.Qt.black))
        self.scene.addLine(w - 5, 5,
                           w - 20, 0, QtGui.QPen(QtCore.Qt.black))

        self.scene.addLine(5, 5,
                           5, h - 5, QtGui.QPen(QtCore.Qt.black))
        self.scene.addLine(5, h - 5,
                           10, h - 20, QtGui.QPen(QtCore.Qt.black))
        self.scene.addLine(5, h - 5,
                           0, h - 20, QtGui.QPen(QtCore.Qt.black))
    def draw_line(self, x, y, pen):
        for i in range(len(x) - 1):
            wind.scene.addLine(x[i], y[i],
                               x[i + 1], y[i + 1], pen)
    def besier(self):
        besier = Bezier.Curve(np.arange(0, 1.01, 0.01), np.array(pointt))
        
        self.besier_x = np.array(besier[:, 0])
        self.besier_y = np.array(besier[:, 1])
        self.draw_line(self.besier_x, self.besier_y, wind.pen_rest)
        
    def genetic(self):
        coeffs = RunGA(self.besier_x / 100, self.besier_y / 100, min(5, len(pointt)))
        y_pred = np.polyval(coeffs, self.besier_x / 100) * 100
        self.draw_line(self.besier_x, y_pred, wind.pen_genetic)
    def PSO(self):
        coeffs = RunSwarm(self.besier_x / 100, self.besier_y / 100, min(5, len(pointt)))
        y_pred = np.polyval(coeffs, self.besier_x / 100) * 100
        self.draw_line(self.besier_x, y_pred, wind.pen_pso)
 
    def stat(self):
        iterations = list(map(int, np.linspace(10, 500, 50)))
        skos = [[], []]
        times = [[], []]
        for it in iterations:
            sko_mean = [[], []]
            time_mean = [[], []]
            for c in range(10):
                start = time.time()
                coeffs = RunGA(self.besier_x / 100, self.besier_y / 100, min(5, len(pointt)), it)
                t = time.time() - start
                y_pred = np.polyval(coeffs, self.besier_x / 100) * 100
                sko_mean[0].append(np.sqrt(np.std(self.besier_y - y_pred)))
                time_mean[0].append(t)
            
                start = time.time()
                coeffs = RunSwarm(self.besier_x / 100, self.besier_y / 100, min(5, len(pointt)), it)
                t = time.time() - start
                y_pred = np.polyval(coeffs, self.besier_x / 100) * 100
                sko_mean[1].append(np.sqrt(np.std(self.besier_y - y_pred)))
                time_mean[1].append(t)
                
            skos[0].append(np.mean(sko_mean[0]))
            times[0].append(np.mean(time_mean[0]))
            skos[1].append(np.mean(sko_mean[1]))
            times[1].append(np.mean(time_mean[1]))
            
        fig = plt.figure(figsize=(10, 6))
        plt.plot(iterations, skos[0], label='генетический')
        plt.plot(iterations, skos[1], label='рой частиц')
        plt.grid()
        plt.xlabel("количество итераций")
        plt.ylabel("СКО")
        plt.legend()
        pdf = PdfPages('img/' + "result_std.pdf")
        pdf.savefig(fig)
        pdf.close()
        plt.clf()

        plt.plot(iterations, times[0], label='генетический')
        plt.plot(iterations, times[1], label='рой частиц')
        plt.grid()
        plt.xlabel("количество итераций")
        plt.ylabel("время, с")
        plt.legend()
        pdf = PdfPages('img/' + "result_time.pdf")
        pdf.savefig(fig)
        pdf.close()
        plt.clf()
    
        
    def clear(self):
        self.scene.clear()
        self.draw_axis()
        self.besier_x = []
        self.besier_y = []
def add_point(point):
    x = point.x()
    y = point.y()
    pointt.append([x, y])
    wind.scene.addLine(x, y, x, y, wind.pen_point)


def main():
    global wind
    app = QtWidgets.QApplication(sys.argv)
    wind = Visual()
    wind.show()
    app.exec_()


if __name__ == "__main__":
    main()
