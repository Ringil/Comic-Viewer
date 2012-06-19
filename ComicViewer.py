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
from PyQt4 import QtGui, QtCore
from StringIO import StringIO

class ComicViewer(QtGui.QWidget):
    def __init__(self, inFile):
        super(ComicViewer, self).__init__()
        self.initUI()
        self.openFile(inFile)
        self.showImage(self.encodeImg())
        
    def initUI(self):      
        self.hbox = QtGui.QHBoxLayout(self)
        self.lbl = QtGui.QLabel(self)

        self.hbox.addWidget(self.lbl)
        self.setLayout(self.hbox)
        
        self.move(300, 200)
        self.setWindowTitle('Comic Viewer')
        self.show() 
        
    def showImage(self, imgData):
        self.pixmap = QtGui.QPixmap()
        self.pixmap.loadFromData(imgData)
         
        self.lbl.setPixmap(self.pixmap)
        
        self.show()
    
    def openFile(self, inFile):
        self.z = zipfile.ZipFile(inFile, "r")
        
    def encodeImg(self):
        '''
    	This actually encodes ONLY the first file in a zipfile
		NEEDS TO CHANGE
		'''
        #FIXME: NOT ENCODED THE WAY THAT LOADFROMDATA WANTS IT
        data = self.z.read(self.z.namelist()[0])
        return StringIO(data)       
        
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
