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
        self.linnkedCenters = []
        self.linnkedAddresses = []
        
class LogisticsSystem:
    def __init__(self):
        self.sortingCetres = []
        self.letters = []