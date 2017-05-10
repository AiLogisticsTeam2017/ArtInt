import csv
import random
from math import pow
import LogisticsSystem

#data generator class takes three arguments, first is the number of letters to be generated, the second
# is the number of adress numbers 200 means 1-200. The thrd is the percantage of errors in the data.
class DataGenerator:
    def __init__(self, nrOfAddressNrs):
        #Initialising variables
        self.homes = []
        #self.numberOfLetters = numberOfLetters
        self.nrOfAddressNrs = nrOfAddressNrs
        self.locations = []
        self.addressDic = {}
        self.nameList = []
        self.letters = []
        self.loadedLetters = []
        
        #reading files for all initialisation
        self.GetLocations()
        self.GetAddressDic()
        self.GetNamesList()
        self.GenerateHomes()
        self.AssignOwners()
        
    #Load Cities from Locations.csv file
    def GetLocations(self):
        with open('Locations.csv') as csvfile:
            reader = csv.reader(csvfile, delimiter = ' ', quotechar = '|')
            for row in reader:
                self.locations.append(row)
    #Load City Address from AddressDic.csv file
    def GetAddressDic(self):
        with open('AddressDic.csv') as csvfile:
            reader = csv.reader(csvfile, delimiter = ' ', quotechar = '|')
            for row in reader:
                firstSplit = (row[0].split(","))
                key = firstSplit[0]
                value = firstSplit[1].split("|")
                self.addressDic[key] = value
    #Load names from ListOfNames.csv file
    def GetNamesList(self):
        with open('ListOfNames.csv') as csvfile:
            reader = csv.reader(csvfile, delimiter = ' ', quotechar = '|')
            for row in reader:
                self.nameList.append(row)
                
    def GenerateHome(self, names, city, address, addressNr, zipCode):
        home = LogisticsSystem.Home(names, city, address, addressNr, zipCode)
        self.homes.append(home)

    def GenerateHomes(self):
        for loc in self.locations[1:]:
            locSplit = loc[0].split(',')
            
            for address in self.addressDic[locSplit[0]]:
                addressSplit = address.split('-')
                i = 0
                while i < self.nrOfAddressNrs:
                    self.GenerateHome([], locSplit[0], addressSplit[0], i, (locSplit[1]+addressSplit[1]))
                    i += 1
                    
    #generates random name
    def GenerateName(self):
        randomIdx = random.randrange(0, len(self.nameList), 1)
        name = self.nameList[randomIdx] #[0] + ' ' + self.nameList[randomIdx][1]
        return name

    #assign people to the homes
    def AssignOwners(self):
       i = 0
       while i < len(self.homes):
           nameNr = random.randrange(1, 5, 1)
           j = 0
           while j < nameNr:
               name = self.GenerateName()
               self.homes[i].names.append(name)
               j += 1
           i += 1
           
    #letter generator
    def GenerateLetter(self):
        randomHomeIdx = random.randrange(0, len(self.homes),1)
        home = self.homes[randomHomeIdx]
        if(len(home.names) > 1):
            reciever = home.names[random.randrange(0, len(home.names), 1)]
        else:
            reciever = home.names[0]
        return LogisticsSystem.Letter(reciever[0].split(',')[0], reciever[0].split(',')[1], home.address, home.addressNr, home.zipCode, home.city, 'True')
        
    def GenerateLetters(self, numLetters):
        i = 0
        while i < numLetters:
            self.letters.append(self.GenerateLetter())
            i += 1
            
    def SaveData(self, fileName):
        with open(fileName, 'w') as csvfile:
            fieldnames = ['Name', 'SurName', 'Street', 'StreetNr', 'ZipCode', 'City', 'Legitimate']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
            writer.writeheader()
            i = 0
            while i < len(self.letters):
                writer.writerow({'Name': self.letters[i].name, 'SurName': self.letters[i].surName, 'Street': self.letters[i].address, 'StreetNr': self.letters[i].addressNr,
                             'ZipCode': self.letters[i].zipCode, 'City': self.letters[i].city, 'Legitimate': self.letters[i].correct})
                i += 1
                
    def RemoveCriticalData(self, dataType):
        removed = False
        while not removed:
            randIdx = random.randrange(1, len(self.letters), 1)
            if(dataType == 'name' and self.letters[randIdx].name != ''):
                self.letters[randIdx].name = ''
                removed = True
            if(dataType == 'surName' and self.letters[randIdx].surName != ''):
                self.letters[randIdx].surName = ''
                removed = True
            if(dataType == 'city' and self.letters[randIdx].city != ''):
                self.letters[randIdx].city = ''
                removed = True
            if(dataType == 'address' and self.letters[randIdx].address != ''):
                self.letters[randIdx].address = ''
                self.letters[randIdx].correct = False
                removed = True
            if(dataType == 'addressNr' and self.letters[randIdx].addressNr != ''):
                self.letters[randIdx].address = ''
                self.letters[randIdx].correct = False
                removed = True
            if(dataType == 'zipCode' and self.letters[randIdx].zipCode != ''):
                self.letters[randIdx].zipCode = ''
                self.letters[randIdx].correct = False
                removed = True
                
    def RemoveData(self, dataType, times):
        i = 0
        while i < times:
            self.RemoveCriticalData(dataType)
            i += 1
        return
    
    def AlterData(self, dataType, times):
        i = 0
        while i < times:  
            removed = False
            while not removed:
                randIdx = random.randrange(1, len(self.letters), 1)
                if(dataType == 'zipCode' and len([self.letters[randIdx].zipCode]) > 0):
                    self.letters[randIdx].zipCode = self.letters[randIdx].zipCode[:len(self.letters[randIdx].zipCode)-1]
                    self.letters[randIdx].correct = False
                    removed = True
            i += 1
            
    def LoadData(self, fileName):
        with open(fileName) as csvfile:
            reader = csv.reader(csvfile, delimiter = ' ', quotechar = '|')
            for row in reader:
                self.loadedLetters.append(row)
        return
    
    def PrintLetters(self):
        i = 0
        while i < len(self.loadedLetters):
            print(self.loadedLetters[i])
            i += 1
            
    def RemoveAndAlterData(self, errorRate, safeErrorRate):
        self.RemoveData('name', safeErrorRate)
        self.RemoveData('surName', safeErrorRate)
        self.RemoveData('city', safeErrorRate)
        self.RemoveData('address', errorRate)
        self.RemoveData('addressNr', errorRate)
        self.RemoveData('zipCode', errorRate)
        self.AlterData('zipCode', errorRate)
        
    def GenerateData(self, numLetters, errorPercentage, safeErrorPercentage, fileName):
        errorSize = numLetters * ((errorPercentage)*pow(10,-2))
        errorTypes = 4 #hard coded number of error types
        safeErrorTypes = 3 #hard coded number of error types
        errorRate = int(errorSize/errorTypes)
        safeErrorRate = int(errorSize/safeErrorTypes)
        
        self.GenerateLetters(numLetters)
        self.RemoveAndAlterData(errorRate, safeErrorRate)
        self.SaveData(fileName)