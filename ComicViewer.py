#!/usr/bin/python

'''
Written By: Kyle Robinson
Comic Viewer
'''

import sys, zipfile
import rarfile
from PIL import Image
from PyQt4 import QtGui, QtCore
from StringIO import StringIO

class ComicViewer(QtGui.QMainWindow):
    def __init__(self, inFile):
        super(ComicViewer, self).__init__()
        self.initUI()
        self.openFile(inFile)
        self.showImage(self.encodeImg())
        
    def initUI(self): 
        pixmap = QtGui.QPixmap()

        self.lbl = QtGui.QLabel(self)
        self.lbl.setPixmap(pixmap)
        
		'''
		I think this scrollarea is unneeded due to QMainWindow
		'''
        scrollArea = QtGui.QScrollArea(self)
        scrollArea.setBackgroundRole(QtGui.QPalette.Dark)
        scrollArea.setWidget(self.lbl)
        scrollArea.setWidgetResizable(True)
        
        self.setCentralWidget(self.lbl)
        
        self.statusBar()

        openFile = QtGui.QAction(QtGui.QIcon('open.png'), 'Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.showDialog)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)
        
		#FIXME: Find out how to set a specific initial height regardless of pic size
        #self.setGeometry(800, 800, 600, 600)
        self.setMaximumHeight(300)
        self.move(300, 200)
        self.setWindowTitle('Comic Viewer')
        self.show()
        
    def showDialog(self):
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file', 
                '/home')
        '''
		TODO: find out what open returns and hook it up to the
		current open file system
		'''
        f = open(fname, 'r')
        
        with f:        
            data = f.read() 
        
    def showImage(self, imgData):
        self.lbl.setPixmap(imgData) 
		#Possibly set size of window here before showing
        self.show()
    
    def openFile(self, inFile):
        if zipfile.is_zipfile(inFile) == True:      #Check if its a zip file (.zip, .cbz)
            self.z = zipfile.ZipFile(inFile, "r")    
        elif rarfile.is_rarfile(inFile) == True:    #Check if its a rar file (.rar, .cbr)
            self.z = rarfile.RarFile(inFile, "r")
        else:
            print "Unknown Comic Archive Type"
            sys.exit(1)
        
    def encodeImg(self):
        '''
        Returns a QPixmap of the first image in an archive
        '''
        data = self.z.read(self.z.namelist()[0])
        enc = StringIO(data) 
        img = Image.open(enc)
        data = img.convert("RGBA").tostring("raw", "BGRA")
        qimg = QtGui.QImage(data, img.size[0], img.size[1], QtGui.QImage.Format_ARGB32)
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
