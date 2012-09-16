#!/usr/bin/env python

'''
Written By: Kyle Robinson
Comic Viewer

Features to add:
1) Add the ability to remember last page by using sqlite
2) Once everything else is completed go back and work on the mainwindow
version so everything is GUI based.
'''

import sys, zipfile
import rarfile, Tables
from PIL import Image
from PyQt4 import QtGui, QtCore
from StringIO import StringIO

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import *


class ComicViewer(QtGui.QWidget):
    def __init__(self, inFile):
        super(ComicViewer, self).__init__()
        self.openFile(inFile)
        self.initUI()
        self.createDB()
        #self.insertDB("test.cbz", self.currentPage)
        self.showImage(self.createPixmap(self.currentPage))
       

    def createDB(self):
        #Might have to make db a global var dont know yet
        self.engine = create_engine('sqlite:///bookmarks.db', echo = False)
        
        Base = declarative_base()
        
        Base.metadata.create_all(self.engine)
    
    def insertDB(self, fileName, pageNum):
        #create a Session
        Session = sessionmaker(bind=self.engine)
        session = Session()
    
        #create new bookmarks
        newBookmark = Tables.Bookmark(fileName, pageNum)
        session.add(newBookmark)
    
        session.commit()
    
    def initUI(self): 
        hbox = QtGui.QHBoxLayout(self)
        pixmap = QtGui.QPixmap()

        self.lbl = QtGui.QLabel(self)
        self.lbl.setPixmap(pixmap)
        
        #For some reason this works but if you use changePage(1) it 
        #has a problem saying connect needs a slot or callable
        clickable(self.lbl).connect(self.changePage)

        #Create a scrollbar for the label
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
            self.changePage(nextPage)
            
        if e.key() == QtCore.Qt.Key_Backspace:
            self.changePage(lastPage)
    
    def changePage(self, nextOrPrev = 1):
        '''
        Bring up the next or previous page in the comic archive
        '''
        maxPages = self.getMaxPages()

        chosenPage = self.currentPage + nextOrPrev

        #Do bounds checking to make sure you don't try to display a 
        #page that doesn't exist
        if (chosenPage <= maxPages - 1) and (chosenPage >= 0):
            self.showImage(self.createPixmap(chosenPage))
            self.currentPage = chosenPage
        
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
        self.currentPage = 0
        if zipfile.is_zipfile(inFile) == True:      #Check if its a zip file (.zip, .cbz)
            self.z = zipfile.ZipFile(inFile, "r")    
        elif rarfile.is_rarfile(inFile) == True:    #Check if its a rar file (.rar, .cbr)
            self.z = rarfile.RarFile(inFile, "r")
        else:
            print "Unknown Comic Archive Type"
            sys.exit(1)

    def getMaxPages(self):
        '''
        Gotta be a better way than this
        '''
        counter = 0

        for count in self.z.namelist():
            counter = counter + 1 

        return counter
            
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

'''
Code from pyqt wiki to make unclickable objects clickable
'''
def clickable(widget):
    class Filter(QtCore.QObject):     

        clicked = QtCore.pyqtSignal()

        def eventFilter(self, obj, event):
            
            if obj == widget:
                if event.type() == QtCore.QEvent.MouseButtonRelease:
                    self.clicked.emit()
                    return True
            return False

    filter = Filter(widget)
    widget.installEventFilter(filter)
    return filter.clicked
        
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
