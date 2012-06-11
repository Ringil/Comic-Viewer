#!/usr/bin/env python
from Tkinter import *
from StringIO import StringIO
from PIL import Image, ImageTk
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
<<<<<<< HEAD
file = sys.argv[1]

'''
This has to change. Connect image to frame then add scrollbar
'''
frame = Frame(root, bd=2, relief=SUNKEN)
frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)

yscrollbar = Scrollbar(frame) 
yscrollbar.grid(row=0, column=1, sticky=N+S)
=======

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
>>>>>>> ziplfile

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
