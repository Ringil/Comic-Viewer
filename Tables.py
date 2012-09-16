from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import *
from sqlalchemy import *

class Bookmark(declarative_base()):
    __tablename__ = "bookmarks"
    id = Column(Integer, primary_key=True)
    fileName = Column(String(100))
    pageNum = Column(Integer)

    def __init__(self, fileName, pageNum):
        self.fileName = fileName
        self.pageNum = pageNum
