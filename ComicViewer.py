#!/usr/bin/python

'''
Written By: Kyle Robinson
Rewritten in Qt4 instead of Tkinter
Missing functionality:

Scrollbar
Ability to read through multiple images
Relative positioning of widgets instead of exact
'''

import sys, zipfile
from PIL import Image
from PyQt4 import QtGui, QtCore
from StringIO import StringIO

class ComicViewer(QtGui.QWidget):
    def __init__(self, inFile):
        super(ComicViewer, self).__init__()
        self.initUI()
        self.openFile(inFile)
        self.showImage(self.encodeImg())
        
    def initUI(self): 
        hbox = QtGui.QHBoxLayout(self)
        pixmap = QtGui.QPixmap()

        self.lbl = QtGui.QLabel(self)
        self.lbl.setPixmap(pixmap)

        scrollArea = QtGui.QScrollArea(self)
        scrollArea.setBackgroundRole(QtGui.QPalette.Dark)
        scrollArea.setWidget(self.lbl)
        scrollArea.setWidgetResizable(True)
        
        hbox.addWidget(scrollArea)
        
        self.setLayout(hbox)
        self.setGeometry(800, 800, 600, 600)
        self.move(300, 200)
        self.setWindowTitle('Batman')
        self.show() 
        
    def showImage(self, imgData):
        self.lbl.setPixmap(imgData) 
        self.show()
    
    def openFile(self, inFile):
        self.z = zipfile.ZipFile(inFile, "r")
        
    def encodeImg(self):
        '''
        Returns a QPixmap of the first image in an archive
        '''
        
        data = self.z.read(self.z.namelist()[0])
        enc = StringIO(data) 
        img = Image.open(enc)
        data = img.tostring()
        qimg = QtGui.QImage(data, img.size[0], img.size[1], QtGui.QImage.Format_RGB32)
        pix = QtGui.QPixmap.fromImage(qimg)
    
        return pix
        
if __name__ == '__main__':
    try:
        if len(sys.argv) == 1:
            raise ValueError, "No image filename specified"
    except Exception, e:
        print >> sys.stderr, e
        print "USAGE: ./ComicViewer.py <comic filename>"
        sys.exit(1)
            
    inFile = sys.argv[1]	
    app = QtGui.QApplication(sys.argv)
    ex = ComicViewer(inFile)
    sys.exit(app.exec_())
