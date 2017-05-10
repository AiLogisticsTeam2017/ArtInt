import csv
import random
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
        
class Address:
    def __init__(self, address,addressNr,zipCode,city):
        self.address = address
        self.addressNr = addressNr
        self.zipCode = zipCode
        self.city = city
        
class SentLetter:
    def __init__(self, letter):
        self.letter = letter
        self.startPos = Address("","","","")
        self.endPos = Address("","","","")
        self.correctEndPos = Address("","","","")

class SortingCentre:
    def __init__(self, address):
        self.address = address
        self.letters = []
        self.linkedCentres = []
        self.linkedAddresses = []
        self.sentLetters = []
        
    def SortLetters(self):
        for letter in self.letters:
            sentLetter = SentLetter(letter)
            sentLetter.startPos = Address(self.address.address, self.address.addressNr, self.address.zipCode, self.address.city)
            #sets the correct end position can be without specified city
            if(sentLetter.startPos.zipCode[:2] == letter.zipCode[:2]):
                sentLetter.correctEndPos = Address(letter.address, letter.addressNr, letter.zipCode, letter.city)
            else:
                sentLetter.correctEndPos = Address("SortingStreet", "1", letter.zipCode[:2] + "222", letter.city)#ALERT temp solution for postal centres address
            sentLetter.endPos = sentLetter.correctEndPos #ALERT this shall not always be right!
            self.sentLetters.append(sentLetter)
        self.letters = []

class LogisticsSystem:
    def __init__(self):
        self.locations = [] #A list containing the cities with their first two postal Code numbers
        self.locationsDic = {} #the key is the first 2 zipCode numbers, value is the city
        self.centreLinks = {} #the key is a city and the value is the connected cities
        self.addressLinks = {} #the key is a city and the value is the connected addresses
        self.sortingCentres = [] #A list containing the sorting Centres
        self.letters = [] #A list containing the letters (data)
        self.deliveredLetters = [] #Letters that are delivered to thier end address
        
        self.GetLocations('Locations.csv')
        self.GetSortingCentres()
        self.GetCentreLinks('PostCentreLinks.csv')
        self.GetAddressDic('AddressDic.csv')
        
    #Load Cities from Locations.csv file
    def GetLocations(self, fileName):
        with open(fileName) as csvfile:
            reader = csv.reader(csvfile, delimiter = ' ', quotechar = '|')
            for row in reader:
                self.locations.append(row)
        first = True
        #creates a dictionary with the first two zip code numbers as key and the city as value
        for location in self.locations:
            if(first):
                first = False
                continue
            self.locationsDic[location[0].split(',')[1]] = location[0].split(',')[0]
    #loads the sorting centres from locations
    def GetSortingCentres(self):
        i = 1
        while i < len(self.locations):
            city = self.locations[i][0].split(',')[0]
            zipCode = self.locations[i][0].split(',')[1] + '222' #ALERT temp solution to postal centres zipCode
            address = Address("SortingStreet", "1", zipCode, city)#ALERT temp solution to postal centres address
            sortCentre = SortingCentre(address)
            self.sortingCentres.append(sortCentre)
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
                
        for centre in self.sortingCentres:
            centre.linkedCentres = self.centreLinks[centre.address.city]
        
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
            randIdx = random.randrange(0, len(self.sortingCentres), 1)
            self.sortingCentres[randIdx].letters.append(letter)
            self.letters = []
            
    def SortAndSendLetters(self):
        #sort the letters
        for centre in self.sortingCentres:
            centre.SortLetters()
        #send the letters
        for centre in self.sortingCentres:
            for letter in centre.sentLetters:
                if(letter.endPos.zipCode[:2] == centre.address.zipCode[:2]):
                    self.deliveredLetters.append(letter)
                    #introduce an error! for example the wrong end adressNr
                    continue
                for linked in self.sortingCentres:
                    if(letter.endPos.zipCode == linked.address.zipCode):
                        #send letter to postal centre
                        linked.letters.append(letter)
                        #introduce an error! for example sent to the wrong sorting centre
                        break
        
        

#Code for debugging
#initialisation
logistics = LogisticsSystem()

#load letters (data) to the system
logistics.LoadLetters('alteredData.csv')
#remove letters with missing information
logistics.RemoveBrokenLetters()
#distribute letters to post cetres
logistics.DistributeLetters()
#sort letters and send them to the right post centre / to the right address
logistics.SortAndSendLetters()

print("Delivered Letters")
for letter in logistics.deliveredLetters:
    print("Letter: ", letter.letter.address, letter.letter.zipCode, "StartPos: ", letter.startPos.address, letter.startPos.zipCode, "endPos: ", letter.endPos.address, letter.endPos.zipCode)

print("Letters In system")
for centre in logistics.sortingCentres:
    for letter in centre.letters:
        pass





























