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
        myLayout = QtGui.QHBoxLayout()
        self.lbl = QtGui.QLabel(self)
        
        self.setLayout(myLayout)
        
        sarea = QtGui.QScrollArea()
        sarea.setWidgetResizable(True)
        sarea.setEnabled(True)
        sarea.setMaximumSize(800, 600)
        sarea.setWidget(self.lbl)        
        self.addWidget(sarea)
        
        myLayout.addWidget(self.lbl)
        
        self.move(300, 200)
        self.setWindowTitle('Comic Viewer')
        '''     
        self.hbox = QtGui.QHBoxLayout(self)
        self.lbl = QtGui.QLabel(self)
        self.setLayout(self.hbox)
        
        self.sbar = QtGui.QScrollArea()
        self.sbar.setWidgetResizable(True)
        self.sbar.setEnabled(True)
        self.sbar.setMaximumSize(800,600)
        self.sbar.setWidget(self.lbl)

        self.hbox.addWidget(self.lbl)
        
        
        self.move(300, 200)
        self.setWindowTitle('Comic Viewer')
        #self.show() 
        '''
        
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
