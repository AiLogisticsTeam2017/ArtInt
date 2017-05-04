import csv

class Home:
    def __init__(self, names, city, address, addressNr, zipCode):
        self.names = names
        self.city = city
        self.address = address
        self.addressNr = addressNr
        self.zipCode = zipCode
        
class Letter:
    def __init__(self, name, city, address, addressNr, zipCode, correct):
        self.name = name
        self.city = city
        self.address = address
        self.addressNr = addressNr
        self.zipCode = zipCode
        self.correct = correct
        
class SortingCentre:
    def __init__(self, city, zipCode):
        self.city = city
        self.zipCode = zipCode
        self.letters = []
        self.linkedCenters = []
        self.linkedAddresses = []
        
    def RemoveBrokenLetters(self):
        tempLetters = []
        if (len(self.letters) > 0):
            i = 0
            while i < len(self.letters):
                if (len(self.letters[i].zipCode) != 6):
                    i += 1
                    continue
                if (len(self.letters[i].address) == 0):
                    i += 1
                    continue
                if (len(self.letters[i].addressNr) == 0):
                    i += 1
                    continue
                tempLetters.append(self.letters[i])
                i += 1
            self.letters = tempLetters
                
    def SendLetters(self):
        if (len(self.letters) > 0):
            pass
            
class LogisticsSystem:
    def __init__(self):
        self.locations = []
        self.centreLinks = {}
        self.addressLinks = {}
        self.sortingCetres = []
        #self.letters = []
        
    #Load Cities from Locations.csv file
    def GetLocations(self, fileName):
        with open(fileName) as csvfile:
            reader = csv.reader(csvfile, delimiter = ' ', quotechar = '|')
            for row in reader:
                self.locations.append(row)
                
    def GetSortingCentres(self):
        i = 1
        while i < len(self.locations):
            city = self.locations[i][0].split(',')[0]
            zipCode = self.locations[i][0].split(',')[1] + '222'
            sortCentre = SortingCentre(city, zipCode)
            self.sortingCetres.append(sortCentre)
            i += 1
            
    def GetCentreLinks(self, fileName):
        with open(fileName) as csvfile:
            reader = csv.reader(csvfile, delimiter = ' ', quotechar = '|')
            for row in reader:
                toString = row[0]
                key = toString.split(',')[0]
                value = toString.split(',')[1].split('|')
                self.centreLinks[key] = value
                
        for centre in self.sortingCetres:
            centre.linkedCenters = self.centreLinks[centre.city]
        
    #Load City Address from AddressDic.csv file
    def GetAddressDic(self, fileName):
        with open(fileName) as csvfile:
            reader = csv.reader(csvfile, delimiter = ' ', quotechar = '|')
            for row in reader:
                firstSplit = (row[0].split(","))
                key = firstSplit[0]
                value = firstSplit[1].split("|")
                self.addressLinks[key] = value
                print(self.addressLinks[key])
        






#Code for testing
logistics = LogisticsSystem()
logistics.GetLocations('Locations.csv')
logistics.GetSortingCentres()
logistics.GetCentreLinks('PostCentreLinks.csv')
logistics.GetAddressDic('AddressDic.csv')





























