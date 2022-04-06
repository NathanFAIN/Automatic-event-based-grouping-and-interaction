from enum import Enum
from GenerateKeywords import GenerateKeywordsFromImage, GenerateKeywordsFromText, UploadPicture

class DataType(Enum):
    TEXT = 1
    PICTURE = 2
    AUDIO = 3
    VIDEO = 4

class MediaData():
    def __init__(self, path: str):
        self.path = path
        self.type = None
        self.keyWords = None
        if exists(path):
            if path.endswith('.txt'):
                self.type = TEXT
                f = open(path, "r")
                contest = f.read()
                self.keyWords = GenerateKeywordsFromText(contest)
            elif path.endswith('.png') or path.endswith('.jpg') or path.endswith('.jpeg'):
                self.type = PICTURE
                link = UploadPicture(path)
                self.keyWords = GenerateKeywordsFromImage(link)
    
    def getType(self):
        return self.type
    
    def getKeyWords(self):
        return self.keyWords