from DataGenerator import DataGenerator
import LogisticsSystem

#Generate data
dataGen = DataGenerator(200) #argument specifies how many street numbers exists per street 200 = 1-200
dataGen.GenerateData(1000, 20, 'alteredData.csv') #Parameters: NumberOfLetters, ErrorPercentage, FileName

#Simulate data
