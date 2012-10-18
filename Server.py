from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base

class Server:
    def __init__(self):
        self.engine = create_engine('sqlite:///bookmarks.db', echo = False)
        
        Base = declarative_base()
        Base.metadata.create_all(self.engine)

    def insertDB(self, fileName, pageNum):
        #create a Session
        Session = sessionmaker(bind=self.engine)
        session = Session()
    
        #create new bookmarks
        newBookmark = Tables.Bookmark(fileName, pageNum)
        session.add(newBookmark)
    
        session.commit()

    class Bookmark(declarative_base()):
        __tablename__ = "bookmarks"
        id = Column(Integer, primary_key=True)
        fileName = Column(String(100))
        pageNum = Column(Integer)

        def __init__(self, fileName, pageNum):
            self.fileName = fileName
            self.pageNum = pageNum
        
    

