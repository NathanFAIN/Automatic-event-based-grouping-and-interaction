import datetime

class MediaEvent():
    def __init__(self):
        self.date = None
        self.loc = None
        self.keyWords = []
        self.mediaDatas = []
        self.title = None
    
    def getDate(self):
        return self.date
    
    def getLocation(self):
        return self.loc

    def getKeyWords(self):
        return self.keyWords

    def getMediaDatas(self):
        return self.mediaDatas

    def getTitle(self):
        return self.title

    def generateMissingData(self):
        if self.date is None:
            self.date = datetime.datetime.now()
        if self.title is None:
            keyWordsList = []
            for mediaData in self.mediaDatas:
                for word in mediaData.getKeyWords():
                    keyWordsList.append(word)
            self.title = max(set(keyWordsList), key = keyWordsList.count)

    def isSame(self, mediaData):
        if self.date is not None and mediaData.getDate() is not None and self.date == mediaData.getDate():
            return True
        if self.loc is not None and mediaData.getLocation() is not None and self.loc == mediaData.getLocation():
            return True
        for word1, word2 in ((w1, w2) for w1 in mediaData.getKeyWords() for w2 in self.keyWords):
            if word1 == word2:
                return True
        return False

    def addMediaData(self, mediaData):
        if self.date is None and mediaData.getDate() is not None:
            self.date = mediaData.getDate()
        if self.loc is None and mediaData.getLocation() is not None:
            self.loc = mediaData.getLocation()
        self.mediaDatas.append(mediaData)
        for word in mediaData.getKeyWords():
            if word not in self.keyWords:
                self.keyWords.append(word)
