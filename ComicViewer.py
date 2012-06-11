#!/usr/bin/env python
from Tkinter import *
from StringIO import StringIO
from PIL import Image, ImageTk
import sys
import getopt
import zipfile
import base64

try:
    if len(sys.argv) == 1:
        raise ValueError, "No image filename specified"
except Exception, e:
    print >>sys.stderr, e
    print "USAGE: ./ComicViewer.py <comic filename>"
    sys.exit(1)

root = Tk()

c = Canvas(root)
c.pack()                                                #TODO: check what this does

z = zipfile.ZipFile(sys.argv[1], "r")

data = z.read(z.namelist()[0])                          #Read in the image data
dataEnc=StringIO(data)                                  #Encode the raw data to be used by Image.open()

####jpegs display in the tk window but gif doesnt####
img = Image.open(dataEnc)                               #Open the image
pimg= ImageTk.PhotoImage(img)                           #Make tk compatible image
#img.show()                                              #shows image in preview
#################

c.create_image(img.size[0], img.size[1], image=pimg)    #TODO: check what this does
root.mainloop()

    

    
    
