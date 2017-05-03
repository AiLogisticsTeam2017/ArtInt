from DataGenerator import DataGenerator
import LogisticsSystem

#Generate data
dataGen = DataGenerator(200) #argument specifies how many street numbers exists per street 200 = 1-200
dataGen.GenerateData(10, 20, 'alteredData.csv')

#Simulate data
