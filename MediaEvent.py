import datetime
import math

#This class represents an event and contains 1 or more MediaData objects 
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

    #calculation of the distance between two long and lat
    def isInRadius(self, m1, m2):
        # approximate radius of earth in km
        R = 6373.0

        print(m1)
        print(m2)
        lat1 = math.radians(m1[0])
        lon1 = math.radians(m1[1])
        lat2 = math.radians(m2[0])
        lon2 = math.radians(m2[1])

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        distance = R * c

        print("Result:", distance)

        return distance < 20

    #compare a MediaData object with the event
    def isSame(self, mediaData):
        print(mediaData.getLocation())
        print(self.loc)
        print("----------")
        if self.date is not None and mediaData.getDate() is not None and self.date == mediaData.getDate():
            return True
        if self.loc is not None and mediaData.getLocation() is not None and self.isInRadius(self.loc, mediaData.getLocation()):
            return True
        if self.loc is not None and mediaData.getLocation() is not None and self.loc == mediaData.getLocation():
            return True
        for word1, word2 in ((w1, w2) for w1 in mediaData.getKeyWords() for w2 in self.keyWords):
            if word1 == word2:
                return True
        return False

    #add a MediaData object in the event
    def addMediaData(self, mediaData):
        if self.date is None and mediaData.getDate() is not None:
            self.date = mediaData.getDate()
        if self.loc is None and mediaData.getLocation() is not None:
            self.loc = mediaData.getLocation()
        self.mediaDatas.append(mediaData)
        for word in mediaData.getKeyWords():
            if word not in self.keyWords:
                self.keyWords.append(word)
