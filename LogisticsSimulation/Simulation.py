from DataGenerator import DataGenerator
from LogisticsSystem import LogisticsSystem
import datetime
import os

#initialisation
dataGen = DataGenerator(200) #argument specifies how many street numbers exists per street 200 = 1-200
logistics = LogisticsSystem()

clear = lambda: os.system('cls') # clears console


LOOP_SPEED = 2 # determines the loop speed in seconds
loopNr = 0
numberOfLoops = 1
time = datetime.datetime.now()

#main loop    
while True:
    currentTime = datetime.datetime.now()
    deltaTime = currentTime - time
    if deltaTime > datetime.timedelta(seconds=LOOP_SPEED):
        time = currentTime
        print("Loop: " + str(loopNr))
        loopNr += 1
        
        dataGen.GenerateData(100000, 20, 10, 'alteredData.csv') #Parameters: NumberOfLetters, ErrorPercentage, SafeErrorPercentage, FileName
        logistics.LoadLetters('alteredData.csv')
        #logistics.SimulateLogistics('deliveries1M.csv', 20) #Parameters: saveFileName, errorChance
        #logistics.SimulateLogistics('deliveries1M2.0.csv', 20) #Parameters: saveFileName, errorChance
        #logistics.SimulateLogistics('deliveries1M3.0.csv', 20) #Parameters: saveFileName, errorChance
        #logistics.SimulateLogistics('deliveries10k.csv', 20) #Parameters: saveFileName, errorChance
        logistics.SimulateLogistics('deliveries100k.csv', 20) #Parameters: saveFileName, errorChance
        
        #only for debugging
        """print("Delivered Letters")
        for letter in logistics.deliveredLetters:
            print("Letter: ", letter.letter.zipCode, "StartPos: ", letter.startPos.zipCode, "endPos: ", letter.endPos.zipCode)

        print("Letters In system")
        lettersInSystem = 0
        for centre in logistics.sortingCentres:
            for letter in centre.letters:
                print("Letter: ", letter.zipCode, "Location: ", centre.address.zipCode)
                lettersInSystem += 1"""
    if(loopNr == numberOfLoops): #number of loops
        print('LoopNr met!')
        break