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
This has to change. Connect image to frame then add scrollbar
'''
frame = Frame(root, bd=2, relief=SUNKEN)
frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)

yscrollbar = Scrollbar(frame) 
yscrollbar.grid(row=0, column=1, sticky=N+S)

'''
Possibly use frombuffer or fromstring to deal with what you get back from zipfile. 
seen at http://www.pythonware.com/library/pil/handbook/image.htm
'''
img = Image.open(file) #problem here
    
#canvas = Canvas(root, height=img.size[1]-200, width=img.size[0]+20)
#canvas = Canvas(frame, height=800, width=img.size[0]+20)
canvas = Canvas(frame, height=800, width=img.size[0]+20,bd=0, yscrollcommand=yscrollbar.set)
canvas.grid(row=0, column=0, sticky=N+S+E+W)
canvas.config(scrollregion=canvas.bbox(ALL))

yscrollbar.config(command=canvas.yview)

frame.pack(side=LEFT,fill=BOTH,expand=1)
photo = ImageTk.PhotoImage(img)
item = canvas.create_image(10,10,anchor=NW, image=photo)
mainloop()