from DataGenerator import DataGenerator
import LogisticsSystem

#Generate data
dataGen = DataGenerator(200) #argument specifies how many street numbers exists per street 200 = 1-200
dataGen.GenerateData(1000000, 20, 10, 'alteredData.csv1M') #Parameters: NumberOfLetters, ErrorPercentage, SafeErrorPercentage, FileName

#Simulate data
