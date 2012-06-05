#!/usr/bin/env python
from Tkinter import *
import Image            #PIL
import ImageTk          #PIL
import sys
import getopt

try:
    if len(sys.argv) == 1:
        raise ValueError, "No image filename specified"
except Exception, e:
    print >>sys.stderr, e
    print "USAGE: ./ComicViewer.py <comic filename>"
    sys.exit(1)
    
root = Tk()
file = sys.argv[1]

'''
Possibly use frombuffer or fromstring to deal with what you get back from zipfile. 
seen at http://www.pythonware.com/library/pil/handbook/image.htm
'''
img = Image.open(file) #problem here
    
canvas = Canvas(root, height=img.size[1]+20, width=img.size[0]+20)
canvas.pack(side=LEFT,fill=BOTH,expand=1)
photo = ImageTk.PhotoImage(img)
item = canvas.create_image(10,10,anchor=NW, image=photo)
mainloop()