##Comic Viewer
A, work in progress, python .cbr and .cbz reader.
Currently requires PIL (Python Imaging Library), Qt, PyQt and Python 2.7, rarfile.

#Getting Started
Once the previous requirements are met you simply type in the console:
./ComicViewer path/to/your/comic

The file axe.cbz has been provided for testing purposes but it only contains 1 image.
In this case you would use ./ComicViewer axe.cbz
Currently when going back and forth through pages you won't run into any errors but if you keep pressing next page or previous page when you're on the first or last pages respectively, then you will have to go in the opposite direction to get back to the other pages of the comic (ie. you pressed next page 5 times after you hit the last page then you'll have to press previous page 6 times to get to the SECOND LAST page). Of course when you reopen a file with this program it will always start on the first page.

#Hotkeys
Good News! Although the interface is just a label currently, you can now actually go back and forth through the pages by using a few hotkeys. 

Next Page: Spacebar or Enter

Previous Page: Backspace
