#!/usr/bin/env python

'''
Written By: Kyle Robinson
Comic Viewer

Features to add:
1) Bounds checking on next and previous pages
2) Add the ability to remember last page by using sqlite
3) Once everything else is completed go back and work on the mainwindow
version so everything is GUI based.
'''

import sys, zipfile
import rarfile
from PIL import Image
from PyQt4 import QtGui, QtCore
from StringIO import StringIO

class ComicViewer(QtGui.QWidget):
    def __init__(self, inFile):
        super(ComicViewer, self).__init__()
        self.currentPage = 0
        self.openFile(inFile)
        self.initUI()
        self.showImage(self.createPixmap(self.currentPage))
        
        
    def initUI(self): 
        hbox = QtGui.QHBoxLayout(self)
        pixmap = QtGui.QPixmap()

        self.lbl = QtGui.QLabel(self)
        self.lbl.setPixmap(pixmap)
        
        #This makes the label clickable and calls nextPage
        #self.lbl.mouseReleaseEvent = self.changePage(e, 1)

        scrollArea = QtGui.QScrollArea(self)
        scrollArea.setBackgroundRole(QtGui.QPalette.Dark)
        scrollArea.setWidget(self.lbl)
        scrollArea.setWidgetResizable(True)
        
        hbox.addWidget(scrollArea)
        
        self.setLayout(hbox)
        self.setGeometry(1800, 1800,1800, 1800)
        self.move(300, 200)
        self.setWindowTitle('Comic Viewer')
        self.show() 
    
    def keyPressEvent(self, e):
        nextPage = 1
        lastPage = -1

        if e.key() == QtCore.Qt.Key_Space or e.key() == QtCore.Qt.Key_Return:
            self.changePage(e, nextPage)
            
        if e.key() == QtCore.Qt.Key_Backspace:
            self.changePage(e, lastPage)
      
    '''
    Change the nextpage previous page to 1 func that takes a +1 or -1.
    Will allow for a large page step func later
    '''      
    def changePage(self, event, nextOrPrev):
        '''
        Bring up the next or previous page in the comic archive
        
        WARNING: This does NO BOUNDS CHECKING
        '''
        self.currentPage = self.currentPage + nextOrPrev
        self.showImage(self.createPixmap(self.currentPage))
        
    def showImage(self, pixmap):
        '''
        Sets the label to the pixmap (Qt container meant
        for displaying images) provided.
        '''
        self.lbl.setPixmap(pixmap) 
        self.show()
    
    def openFile(self, inFile):
        '''
        Open a file stream to either a rar/cbr or zip/cbz file
        '''
        if zipfile.is_zipfile(inFile) == True:      #Check if its a zip file (.zip, .cbz)
            self.z = zipfile.ZipFile(inFile, "r")    
        elif rarfile.is_rarfile(inFile) == True:    #Check if its a rar file (.rar, .cbr)
            self.z = rarfile.RarFile(inFile, "r")
        else:
            print "Unknown Comic Archive Type"
            sys.exit(1)
        
    def createPixmap(self, pageNum):
        '''
        Returns a Pixmap of the image file in the archive
        where pageNum corresponds to the position in archive
        starting at 0.
        '''
        data = self.z.read(self.z.namelist()[pageNum])
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
        print "USAGE: ./ComicViewer.py <path to your comic file>"
        sys.exit(1)
            
    inFile = sys.argv[1]	
    app = QtGui.QApplication(sys.argv)
    ex = ComicViewer(inFile)
    sys.exit(app.exec_())
