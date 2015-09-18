import sys
import collections
from itertools import *
import itertools
		
#Method that subtracts each element from 1 and replaces the element 
#with this value and returns this array with new values
def getComplementArray(arr):
	arr2 = list(arr)
	arr2[:] = [1-x for x in arr2]
	return arr2

#Method that returns the index at which arr1 and arr2 have different values
def getIndexWithDifferentValue(arr1,arr2):
	for x in range(0,len(arr1)):
		if(arr1[x]!=arr2[x]):
			#print x
			return x

#Method that calculates the probabilty of X given A using Baye's Thorem.
#Here, A is composed of symptoms whose corresponding truth values are
#present in 'truthValues'. If the truth value of a symptom is T, then it
#is considered as part of A. If it is F, then the negation of the symptom
#is considered as part of A. X denotes the disease. This method uses
#4 global dictionaries that hold the different conditional probabilities
#required to compute probability of X given A
def bayesProbability(truthValues):
	global diseaseSymptomsGivenDisease
	global diseaseSymptomsGivenNoDisease
	global diseaseNoSymptomsGivenDisease
	global diseaseNoSymptomsGivenNoDisease
	num = 1.0
	falseDen = 1.0
	for j in range(0,len(truthValues)):
		if truthValues[j]=='T':
			num = num * diseaseSymptomsGivenDisease[disease][j]
			falseDen = falseDen * diseaseSymptomsGivenNoDisease[disease][j]
		elif truthValues[j]=='F':
			num = num * diseaseNoSymptomsGivenDisease[disease][j]
			falseDen = falseDen * diseaseNoSymptomsGivenNoDisease[disease][j]
			
	num = num*diseasePriorProbabilities[disease]
	falseDen = falseDen*(1-diseasePriorProbabilities[disease])
	if(num+falseDen==0):
		postProbability = float('inf')
	else:
		postProbability = num/(num+falseDen);
	return postProbability

#Reading the filename
fname = sys.argv[2]
output = ""

#Reading the file
with open(fname) as f:
	input = f.read().splitlines()
	noOfDiseases = int(input[0].split(" ")[0])
	noOfPatients = int(input[0].split(" ")[1])
	diseases = []
	diseasePriorProbabilities = dict()
	diseaseSymptoms = dict()
	diseaseSymptomsGivenDisease = dict()
	diseaseSymptomsGivenNoDisease = dict()
	diseaseNoSymptomsGivenDisease = dict()
	diseaseNoSymptomsGivenNoDisease = dict()
	count = 4*noOfDiseases+1;
	#For each disease, store the conditional probabilities related
	#to each symptom of a disease in 4 different dictionaries
	for i in range(0,noOfDiseases):
		diseaseLine = input[4*i+1].split(" ")
		disease = str(diseaseLine[0])
		diseases.append(disease)
		diseasePriorProbabilities[disease] = float(diseaseLine[2])
		diseaseSymptoms[disease] = eval(input[4*i+2])
		symptomsGivenDisease = eval(input[4*i+3])
		diseaseSymptomsGivenDisease[disease] = symptomsGivenDisease
		symptomsGivenNoDisease = eval(input[4*i+4])
		diseaseSymptomsGivenNoDisease[disease] = symptomsGivenNoDisease
		noSymptomsGivenDisease = getComplementArray(symptomsGivenDisease);
		diseaseNoSymptomsGivenDisease[disease] = noSymptomsGivenDisease
		noSymptomsGivenNoDisease = getComplementArray(symptomsGivenNoDisease);
		diseaseNoSymptomsGivenNoDisease[disease] = noSymptomsGivenNoDisease

	patientNo = 1
	#Read patient data(truth values of symptoms for each disease) and 
	#generate 3 lines of output for every patient
	while (count < len(input)):
		output += "Patient-"+str(patientNo)+":\n"
		line1dic = dict()
		line2dic = dict()
		line3dic = dict()
		for i in range(0,noOfDiseases):
			truthValues = eval(input[count])
			disease = diseases[i]
			symptoms = diseaseSymptoms[disease]
			
			noOfUnknowns = 0
			maxPostProb = 0.0
			minPostProb = 1.0
			for j in range(0,len(truthValues)):
				if truthValues[j]=='U':
					noOfUnknowns = noOfUnknowns + 1
			
			#Compute probability of disease given symptoms
			postProbability = bayesProbability(truthValues)
			
			line1dic[disease] = '{0:.4f}'.format(round(postProbability,4))

			#Generate different permutations of truth values that can be assigned to the any of the
			#(even more than one at a time) unknown symptoms
			truthValueList = ['T','F']
			unknownPermutations = [p for p in itertools.product(truthValueList, repeat=noOfUnknowns)]

			possibleTruthValues = []
		
			for unknownPerm in list(unknownPermutations):
				values = list(truthValues)
				index = 0
				for k in range(0,len(values)):
					if(values[k]=='U'):
						values[k] = unknownPerm[index]
						index = index+1
				possibleTruthValues.append(values)

			maxPostProb = 0.0
			minPostProb = 1.0
			#For each permutation, compute the probability and find the maximum and minimum probabilities
			for possibleTruthValue in possibleTruthValues:
				possiblePostProb = bayesProbability(possibleTruthValue)
				if(possiblePostProb > maxPostProb):
					maxPostProb = possiblePostProb
				if(possiblePostProb < minPostProb):
					minPostProb = possiblePostProb

			line2dic[disease] = ['{0:.4f}'.format(round(minPostProb,4)),'{0:.4f}'.format(round(maxPostProb,4))]

			possibleTruthValues1 = []
			alreadySubstitutedIndex = []
	
			#Generate different permutations of truth values that can be assigned to the exactly 
			#one of the unknown symptoms
			values = list(truthValues)
			for k in range(0,len(values)):
				if(values[k]=='U' and k not in alreadySubstitutedIndex):
					newValue = list(values)
					newValue[k] = 'T'
					possibleTruthValues1.append(newValue)
					newValue1 = list(values)
					newValue1[k] = 'F'
					possibleTruthValues1.append(newValue1)
					alreadySubstitutedIndex.append(k)	

			#Compute the truth values for the symptoms that have the highest and lowest probabilities
			maxPostProb = 0.0
			minPostProb = 1.0
			maxPostProbTruthValue = []
			minPostProbTruthValue = []
			#print possibleTruthValues1
			maxflag = False
			minflag = False
			probIncDec = dict()
			probIncDec['max'] = ['none','N']
			probIncDec['min'] = ['none','N']
			for possibleTruthValue in possibleTruthValues1:
				possiblePostProb = bayesProbability(possibleTruthValue)
				if(possiblePostProb > maxPostProb):
					maxPostProb = possiblePostProb
					changedMaxIndex = getIndexWithDifferentValue(possibleTruthValue,truthValues)
					maxflag = True
					probIncDec['max'] = [symptoms[changedMaxIndex],possibleTruthValue[changedMaxIndex]]
				elif(possiblePostProb == maxPostProb and maxflag):
					changedMaxIndex = getIndexWithDifferentValue(possibleTruthValue,truthValues)
					if (symptoms[changedMaxIndex] < probIncDec['max'][0]):
						probIncDec['max'] = [symptoms[changedMaxIndex],possibleTruthValue[changedMaxIndex]]
				if(possiblePostProb < minPostProb):
					minPostProb = possiblePostProb
					changedMinIndex = getIndexWithDifferentValue(possibleTruthValue,truthValues)
					minflag = True
					probIncDec['min'] = [symptoms[changedMinIndex],possibleTruthValue[changedMinIndex]]
				elif(possiblePostProb == minPostProb and minflag):
					changedMinIndex = getIndexWithDifferentValue(possibleTruthValue,truthValues)
					if (symptoms[changedMinIndex] < probIncDec['min'][0]):
						probIncDec['min'] = [symptoms[changedMinIndex],possibleTruthValue[changedMinIndex]]
			line3dic[disease] = [probIncDec['max'][0],probIncDec['max'][1],probIncDec['min'][0],probIncDec['min'][1]]
			count = count+1
		output +=  (str(line1dic)+"\n")
		output +=  (str(line2dic)+"\n")
		output +=  (str(line3dic)+"\n")
		patientNo = patientNo+1
	
	filenameparts = sys.argv[2].split("/");
	filename = filenameparts[len(filenameparts)-1].split(".")[0]
	f = open(filename+'_inference.txt', 'w')
	f.write(output)	#Write output to file