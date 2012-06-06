#!/usr/bin/env python
from Tkinter import *
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
c.pack()

z = zipfile.ZipFile("axe.cbz", "r")

t = z.read(z.namelist()[0])

img=base64.encodestring(t)
pimg=PhotoImage(img)

c.create_image(100, 100, image=pimg)

root.mainloop()

    

    
    
