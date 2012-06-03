#!/usr/bin/env python
from Tkinter import *
import Image            #PIL
import ImageTk          #PIL
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
    
z = zipfile.ZipFile(sys.argv[1], "r")

for file in z.namelist():
    print file
    bytes = z.read(file)
    z.extract(file)

    '''Extract the files. Make the folder hidden (by putting a . infront of it).
    Concat the folder name with the next name in namelist and send it to Image.open'''
    img = Image.open(file) #problem here
    
    canvas = Canvas(root, height=img.size[1]+20, width=img.size[0]+20)
    canvas.pack(side=LEFT,fill=BOTH,expand=1)
    photo = ImageTk.PhotoImage("Batman and Robin 09 (2012) (Minutemen-DosHalos)/"+img)
    item = canvas.create_image(10,10,anchor=NW, image=photo)
    mainloop()

    

    
    
