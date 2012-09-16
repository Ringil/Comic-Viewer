from PyQt4 import QtCore

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
