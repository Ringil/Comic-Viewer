#!/usr/bin/python

import sys
from PyQt4 import QtGui, QtCore

class Example(QtGui.QWidget):
    
    def __init__(self):
        super(Example, self).__init__()
        
        self.initUI()
        
    def initUI(self):      

        hbox = QtGui.QHBoxLayout(self)
        pixmap = QtGui.QPixmap("batman.jpg")

        lbl = QtGui.QLabel(self)
        lbl.setPixmap(pixmap)

        scrollArea = QtGui.QScrollArea(self)
        hbox.addWidget(scrollArea)
        scrollArea.setBackgroundRole(QtGui.QPalette.Dark)
        scrollArea.setWidget(lbl)
        scrollArea.setWidgetResizable(True)
        
        #hbox.addWidget(lbl)
        
        self.setLayout(hbox)
        self.setGeometry(800, 800, 600, 600)
        self.move(300, 200)
        self.setWindowTitle('Batman')
        self.show()        

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
