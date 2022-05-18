from enum import Enum
from GenerateKeywords import GenerateKeywordsFromImage, GenerateKeywordsFromText, GenerateKeywordsFromTextBis, UploadPicture, RemoveUselessKeywords
from os.path import exists

#Type of file
class DataType(Enum):
    TEXT = 1
    PICTURE = 2
    AUDIO = 3
    VIDEO = 4

#Each data (image and texts) are represented by this class
class MediaData():
    def __init__(self, path: str):
        self.path = str(path)
        self.type = None
        self.keyWords = None
        self.date = None
        self.loc = None
        if exists(path):
            if path.endswith('.txt'):
                self.type = DataType.TEXT
                f = open(path, "r")
                content = f.read()
                f.close()
                self.keyWords = GenerateKeywordsFromTextBis(content) #get keywords from API
                # self.keyWords = GenerateKeywordsFromText(content)  #old API used 
                self.keyWords = RemoveUselessKeywords(self.keyWords) #remove some keywords
            elif path.endswith('.png') or path.endswith('.jpg') or path.endswith('.jpeg') or path.endswith('.webp'):
                self.type = DataType.PICTURE
                link = UploadPicture(path)
                self.keyWords = GenerateKeywordsFromImage(link) #get keywords from API
                self.keyWords = RemoveUselessKeywords(self.keyWords) #remove some keywords
    
    #getter and setter
    def getType(self):
        return self.type
    
    def getKeyWords(self):
        return self.keyWords
    
    def getPath(self):
        return self.path

    def getDate(self):
        return self.date

    def getLocation(self):
        return self.loc

    def setDate(self, date):
        self.date = date

    def setLocation(self, long, lat):
        self.loc = [long, lat]