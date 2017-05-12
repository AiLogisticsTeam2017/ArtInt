from DataGenerator import DataGenerator
from LogisticsSystem import LogisticsSystem
import datetime
import os

#initialisation
dataGen = DataGenerator(200) #argument specifies how many street numbers exists per street 200 = 1-200
logistics = LogisticsSystem()

clear = lambda: os.system('cls') # clears console


LOOP_SPEED = 2
loopNr = 0
time = datetime.datetime.now()
#main loop    
while True:
    currentTime = datetime.datetime.now()
    deltaTime = currentTime - time
    if deltaTime > datetime.timedelta(seconds=LOOP_SPEED):
        time = currentTime
        print("Loop: " + str(loopNr))
        loopNr += 1
        
        dataGen.GenerateData(20, 20, 10, 'alteredData.csv') #Parameters: NumberOfLetters, ErrorPercentage, SafeErrorPercentage, FileName
        logistics.LoadLetters('alteredData.csv')
        logistics.SimulateLogistics('deliveries.csv', 50) #Parameters: saveFileName, errorChance
        
        #only for debugging
        """print("Delivered Letters")
        for letter in logistics.deliveredLetters:
            print("Letter: ", letter.letter.zipCode, "StartPos: ", letter.startPos.zipCode, "endPos: ", letter.endPos.zipCode)

        print("Letters In system")
        lettersInSystem = 0
        for centre in logistics.sortingCentres:
            for letter in centre.letters:
                print("Letter: ", letter.zipCode, "Location: ", centre.address.zipCode)"""
                lettersInSystem += 1
    if(loopNr == 1): #number of loops
        print('LoopNr met!')
        break