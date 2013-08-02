#!/usr/bin/env python

'''
Written By: Kyle Robinson
Comic Viewer

Features to add:
1) Add the ability to remember last page by using sqlite
'''

import sys, zipfile, rarfile
import Utility
from PySide import QtGui, QtCore

class ComicViewer(QtGui.QMainWindow):
    def __init__(self):
        super(ComicViewer, self).__init__()
        self.initUI()
        #self.createDB()
        #self.insertDB("test.cbz", self.currentPage)
    
    def initUI(self): 
        pixmap = QtGui.QPixmap()

        #Create a label to show the pixmap (comic)
        self.lbl = QtGui.QLabel(self)
        self.lbl.setPixmap(pixmap)
        self.lbl.setSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Ignored)
        self.lbl.setScaledContents(True)
        
        self.createActions()
        self.createMenu()

        #Create a scrollbar for the label
        self.scrollArea = QtGui.QScrollArea()
        self.scrollArea.setBackgroundRole(QtGui.QPalette.Dark)
        self.scrollArea.setWidget(self.lbl)
        self.setCentralWidget(self.scrollArea)

        #Find the resolution of the screen
        height = QtGui.QDesktopWidget().availableGeometry().height()
        width = QtGui.QDesktopWidget().availableGeometry().width()
        self.resize(width, height) #Set the window to native resolution

        self.center()
        self.setWindowTitle('Comic Viewer')
        self.show()

    def openFile(self):
        '''
        Open a file stream to either a rar/cbr or zip/cbz file
        '''
        inFile, _ = QtGui.QFileDialog.getOpenFileName(self, 'Open file',
                    QtCore.QDir.currentPath())

        self.currentPage = 0

        if zipfile.is_zipfile(inFile) == True:      #Check if its a zip file (.zip, .cbz)
            self.z = zipfile.ZipFile(inFile, "r")    
        elif rarfile.is_rarfile(inFile) == True:    #Check if its a rar file (.rar, .cbr)
            self.z = rarfile.RarFile(inFile)
        else:
            msgBox = QtGui.QMessageBox()
            msgBox.setText("This is not a valid CBZ or CBR file!")
            msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
            msgBox.setDefaultButton(QtGui.QMessageBox.Ok)
            ret = msgBox.exec_()

            #if statement is probably unecessary
            if ret == QtGui.QMessageBox.Ok:
                self.openFile()

        self.showImage(self.createPixmap(self.currentPage))

        #Make the label clickable to go forward pages
        Utility.clickable(self.lbl).connect(self.changePage)

        self.scaleFactor = 1.0
        self.scaleImage(self.scaleFactor)
        self.updateActions()

    def createMenu(self):
        self.fileMenu = QtGui.QMenu("&File", self)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.closeAct)

        self.viewMenu = QtGui.QMenu("&View", self)
        self.viewMenu.addAction(self.zoomInAct)
        self.viewMenu.addAction(self.zoomOutAct)

        self.menuBar().addMenu(self.fileMenu)
        self.menuBar().addMenu(self.viewMenu)

    def createActions(self):
        self.openAct = QtGui.QAction('Open', self, shortcut='Ctrl+O',
            triggered=self.openFile)

        self.closeAct = QtGui.QAction("&Quit", self, shortcut='Ctrl+Q',
            triggered = self.close)

        self.zoomInAct = QtGui.QAction("Zoom &In (25%)", self,
            shortcut="Ctrl++", enabled=False, triggered=self.zoomIn)

        self.zoomOutAct = QtGui.QAction("Zoom &Out (25%)", self,
            shortcut="Ctrl+-", enabled=False, triggered=self.zoomOut)

    def scaleImage(self, factor):
        self.scaleFactor *= factor
        self.lbl.resize(self.scaleFactor * self.lbl.pixmap().size())

        self.adjustScrollBar(self.scrollArea.horizontalScrollBar(), factor)
        self.adjustScrollBar(self.scrollArea.verticalScrollBar(), factor)

        self.zoomInAct.setEnabled(self.scaleFactor < 5.0)
        self.zoomOutAct.setEnabled(self.scaleFactor > 0.1)

    def adjustScrollBar(self, scrollBar, factor):
        scrollBar.setValue(int(factor * scrollBar.value() 
            + ((factor - 1) * scrollBar.pageStep()/2)))

    def zoomIn(self):
        self.scaleImage(1.25)

    def zoomOut(self):
        self.scaleImage(0.8)

    def close(self):
        sys.exit(1)

    def updateActions(self):
        self.zoomInAct.setEnabled(True)
        self.zoomOutAct.setEnabled(True)

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

    def getNumPages(self):
        '''
        Length of the current open comic book in pages
        ''' 
        return len(self.z.namelist())
        
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    ex = ComicViewer()
    sys.exit(app.exec_())