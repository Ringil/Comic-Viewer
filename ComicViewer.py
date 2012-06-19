#!/usr/bin/python

'''
Rewritten in Qt4 instead of Tkinter
Missing functionality:

Scrollbar
Ability to read through multiple images
Relative positioning of widgets instead of exact
'''
import sys, zipfile, 
from PyQt4 import QtGui, QtCore
from StringIO import StringIO

class ComicViewer(QtGui.QWidget):
    
    def __init__(self):
        super(ComicViewer, self).__init__()
        
        self.initUI()
        
    def initUI(self):      

        hbox = QtGui.QHBoxLayout(self)
        pixmap = QtGui.QPixmap("axe.gif") #this will have to change

        lbl = QtGui.QLabel(self)
        lbl.setPixmap(pixmap)

        hbox.addWidget(lbl)
        self.setLayout(hbox)
        
        self.move(300, 200)
        self.setWindowTitle('Comic Viewer')
        self.show() 
        
    def readZip(self, inFile):
    		'''
    		This actually read and encodes the first file in a zipfile
    		NEEDS TO CHANGE
    		'''
    		z = zipfile.ZipFile(inFile,"r")
    		data = z.read(z.namelist()[0])
    		self.dataEnc = StringIO(data)       
        
if __name__ == '__main__':
	try:
    		if len(sys.argv) == 1:
        		raise ValueError, "No image filename specified"
	except Exception, e:
    		print >>sys.stderr, e
    		print "USAGE: ./ComicViewer.py <comic filename>"
    		sys.exit(1)
    		
    	inFile = sys.argv[1]	
	app = QtGui.QApplication(sys.argv)
	ex = ComicViewer()
	sys.exit(app.exec_())
