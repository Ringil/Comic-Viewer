#!/usr/bin/env python

'''
Written By: Kyle Robinson
Comic Viewer

Features to add:
1) Add the ability to remember last page by using sqlite
2) Once everything else is completed go back and work on the mainwindow
version so everything is GUI based.
'''

import sys, zipfile, rarfile
import Utility
from PySide import QtGui, QtCore
from StringIO import StringIO

class ComicViewer(QtGui.QWidget):
    def __init__(self, inFile):
        super(ComicViewer, self).__init__()
        self.openFile(inFile)
        self.initUI()
        #self.createDB()
        #self.insertDB("test.cbz", self.currentPage)
        self.showImage(self.createPixmap(self.currentPage))
    
    def initUI(self): 
        hbox = QtGui.QHBoxLayout(self)
        pixmap = QtGui.QPixmap()

        self.lbl = QtGui.QLabel(self)
        self.lbl.setPixmap(pixmap)
        
        Utility.clickable(self.lbl).connect(self.changePage)

        #Create a scrollbar for the label
        scrollArea = QtGui.QScrollArea(self)
        scrollArea.setBackgroundRole(QtGui.QPalette.Dark)
        scrollArea.setWidget(self.lbl)
        scrollArea.setWidgetResizable(True)
        
        hbox.addWidget(scrollArea)
        
        self.setLayout(hbox)

        #Find the resolution of the screen
        height = QtGui.QDesktopWidget().availableGeometry().height()
        width = QtGui.QDesktopWidget().availableGeometry().width()
        self.resize(width, height) #Set the window to native resolution

        self.center()
        self.setWindowTitle('Comic Viewer')
        self.show()

    def center(self):
        #Can use this if user doesn't want the screen to be filled at start
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    
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
        maxPages = self.getNumPages()

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
        # elif rarfile.is_rarfile(inFile) == True:    #Check if its a rar file (.rar, .cbr)
        #     self.z = rarfile.RarFile(inFile, "r")
        else:
            print("Unknown Comic Archive Type")
            sys.exit(1)

    def getNumPages(self):
        '''
        Length of the current open comic book in pages
        ''' 
        return len(self.z.namelist())
            
    def createPixmap(self, pageNum):
        '''
        Returns a Pixmap of the image file in the archive
        where pageNum corresponds to the position in archive
        starting at 0.
        '''
        data = self.z.read(self.z.namelist()[pageNum])
        qimg = QtGui.QImage.fromData(data)
        pix = QtGui.QPixmap.fromImage(qimg)
    
        return pix
        
if __name__ == '__main__':
    try:
        if len(sys.argv) == 1:
            raise ValueError("No image filename specified")
    except Exception(e):
        print >> sys.stderr, e
        print("USAGE: ./ComicViewer.py <path to your comic file>")
        sys.exit(1)
            
    inFile = sys.argv[1]	
    app = QtGui.QApplication(sys.argv)
    ex = ComicViewer(inFile)
    sys.exit(app.exec_())
