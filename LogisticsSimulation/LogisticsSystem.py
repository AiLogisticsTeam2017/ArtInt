import csv
#class describing the end locations for the letters
class Home:
    def __init__(self, names, city, address, addressNr, zipCode):
        self.names = names
        self.city = city
        self.address = address
        self.addressNr = addressNr
        self.zipCode = zipCode
#The data class
class Letter:
    def __init__(self, name, surName, address, addressNr, zipCode, city, correct):
        self.name = name
        self.surName = surName
        self.address = address
        self.addressNr = addressNr
        self.zipCode = zipCode
        self.city = city
        self.correct = correct

class SortingCentre:
    def __init__(self, city, zipCode):
        self.city = city
        self.zipCode = zipCode
        self.letters = []
        self.linkedCenters = []
        self.linkedAddresses = []
                
    def SendLetters(self):
        if (len(self.letters) > 0):
            pass
            
class LogisticsSystem:
    def __init__(self):
        self.locations = []
        self.centreLinks = {}
        self.addressLinks = {}
        self.sortingCetres = []
        self.letters = []
        
    #Load Cities from Locations.csv file
    def GetLocations(self, fileName):
        with open(fileName) as csvfile:
            reader = csv.reader(csvfile, delimiter = ' ', quotechar = '|')
            for row in reader:
                self.locations.append(row)
    #loads the sorting centres from locations
    def GetSortingCentres(self):
        i = 1
        while i < len(self.locations):
            city = self.locations[i][0].split(',')[0]
            zipCode = self.locations[i][0].split(',')[1] + '222'
            sortCentre = SortingCentre(city, zipCode)
            self.sortingCetres.append(sortCentre)
            i += 1
    #load shipping links from PostCentreLinks.csv
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
                firstSplit = (row[0].split(','))
                key = firstSplit[0]
                value = firstSplit[1].split('|')
                tempList = []
                for n in value:
                    tempList.append(n.split('-'))
                value = tempList
                self.addressLinks[key] = value
    #load the letters
    def LoadLetters(self, fileName):
        with open(fileName) as csvfile:
            reader = csv.reader(csvfile, delimiter = ' ', quotechar = '|')
            first = True
            for row in reader:
                if(first):
                    first = False
                    continue
                #print(row)
                if(len(row) > 0):   
                    splitRow = row[0].split(',')
                    letter = Letter(splitRow[0], splitRow[1], splitRow[2], splitRow[3],
                                    splitRow[4], splitRow[5], splitRow[6])
                    self.letters.append(letter)
    #remove Letters with missing information
    def RemoveBrokenLetters(self):
        tempLetters = []
        if (len(self.letters) > 0):
            i = 0
            while i < len(self.letters):
                if (len(self.letters[i].zipCode) != 5):
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
        
    #Distribute letters to the right post centre               
    def DistributeLetters(self):
        for letter in self.letters:
            #First Sort
            self.FirstPostalCodeSort(letter.zipCode)
            #Second sort
            self.SecondPostalCodeSort(letter.zipCode)

    def FirstPostalCodeSort(self, zipCode):
        firstNum = zipCode[:3]
        print(firstNum)

    def SecondPostalCodeSort(self, zipCode):
        secondNum = zipCode[3:]
        print(secondNum)

#Code for debugging
logistics = LogisticsSystem()
logistics.GetLocations('Locations.csv')
logistics.GetSortingCentres()
logistics.GetCentreLinks('PostCentreLinks.csv')
logistics.GetAddressDic('AddressDic.csv')
logistics.LoadLetters('alteredData.csv')
logistics.RemoveBrokenLetters()
logistics.DistributeLetters()





























