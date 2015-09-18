import sys
import collections
from itertools import *
import itertools	

#Reading the filename
fname = sys.argv[2]
output = ""	
inputArr = []
indices = []
cpt = dict()
cptDic = dict()

possibleValues = dict()
possibleValues['income'] = [0,25001,50001,75001]
possibleValues['bmi'] = ['underweight','normal','overweight','obese']
possibleValues['exercise'] = ['yes','no']
possibleValues['bp'] = ['yes','no']
possibleValues['smoke'] = ['yes','no']
possibleValues['cholesterol'] = ['yes','no']
possibleValues['diabetes'] = ['yes','no']
possibleValues['stroke'] = ['yes','no']
possibleValues['attack'] = ['yes','no']
possibleValues['angina'] = ['yes','no']

cptDic['bmi'] = ['income','exercise']
cptDic['exercise'] = ['income']
cptDic['bp'] = ['income','exercise','smoke']
cptDic['smoke'] = ['income']
cptDic['cholesterol'] = ['income','exercise','smoke']
cptDic['diabetes'] = ['bmi']
cptDic['stroke'] = ['bmi','bp','cholesterol']
cptDic['attack'] = ['bmi','bp','cholesterol']
cptDic['angina'] = ['bmi','bp','cholesterol']

prob = dict()

#Method that returns the lower bound of the range in which the input no falls
def getInputRange(num):
	global possibleValues
	range = 75001
	prev = 0
	for i in possibleValues['income']:
		if num < i:
			return prev
		prev = i
	return 75001
			

#Method that returns the no. of elements given the various categories and their values
def findNoOfElements(index):
	index = index[1:-1]
	global inputArr
	global indices
	count = 0
	conditions = index.split(",")
	for j in inputArr:
		testFlag = True
		for condition in conditions:	
			values = condition.split(":")
			ind = indices.index(values[0]);
			testStr = "'"+str(j[ind])+"'"
			if testStr != values[1]:
				testFlag = False
				break;
		if testFlag:
			count = count + 1
	return count

def findCombinations(comboArr,parents):
	product = list(itertools.product(*comboArr))
	comboListStr = "[";
	for combination in product:
		comboListStr = comboListStr + "\"[";
		index = 0
		for par in parents:
			comboListStr = comboListStr + str(parents[index]) +  ":'"+ str(combination[index]) +"'," 
			index = index + 1
		comboListStr = comboListStr[:-1]
		comboListStr = comboListStr + "]\",";
	comboListStr = comboListStr[:-1]
	comboListStr = comboListStr + "]"
	return comboListStr

#def enumerateAll(vars,evidences):
	

#Reading the file
i = 0
inputArr = []
with open(fname) as f:
	input = f.read().splitlines()
	for line in input:
		if i == 0:
			indices = line.split("\t");
			print "INDICES : "+str(indices)
		else:
			#print i
			inputArr.append(line.split("\t"))
			for j in range(0,len(inputArr[i-1])):
				if inputArr[i-1][j].isdigit():
					inputArr[i-1][j] = getInputRange(int(inputArr[i-1][j]))
		i = i+1
totalNoOfInputs = i-1
output = ""
for node in indices:
	keys = cptDic.keys()
	if node in keys:
		comboArr = []
		parents = cptDic[node]
		print node
		for parent in parents:
			#print parent
			comboArr.append(possibleValues[parent]);
		#print comboArr
		denominatorCombo = findCombinations(comboArr,parents)
		comboArr.insert(0,possibleValues[node]);
		parents.insert(0,node);
		#print comboArr
		numeratorCombo = findCombinations(comboArr,parents)
		#print numeratorCombo
		#output = output+str(numeratorCombo)+"\n"
		numList = eval(numeratorCombo)
		denList = eval(denominatorCombo)
		prob1 = dict()
		dens = dict()
		for denEl in denList:
			probabilityDenominator = findNoOfElements(denEl)
			dens[denEl] = probabilityDenominator
			#print denEl
			output = output + "DEN : "+str(denEl)+"\n"
			#print probabilityDenominator
			output = output+str(probabilityDenominator)+"\n"
		noOfDens = len(denList)
		denindex = 0
		for numEl in numList:
			probabilityNumerator = findNoOfElements(numEl)
			firstPost = numEl.index(',')
			query = numEl[1:firstPost]
			given = numEl[firstPost+1:len(numEl)-1]
			probabilityDenominator = dens["["+given+"]"]
			pr = float(probabilityNumerator)/probabilityDenominator
			prob1[query+" | "+given] = '{0:.4f}'.format(round(pr,4))
			#print numEl
			output = output + "NUM : "+str(numEl)+"\n"
			#print probabilityNumerator
			output = output+str(probabilityNumerator)+"\n"
		dens.update((x, float(y)/totalNoOfInputs) for x, y in dens.items())
		dens.update((x, round(y,4)) for x, y in dens.items())
		cpt.update(dens)
		#print prob1
		output = output +str(prob1)+"\n"
		output = output + str(len(prob1.keys()))
		cpt.update(prob1)
		#break
	else:
		for value in possibleValues[node]:
			index = ["["+node+":'"+str(value)+"']"]
			probability = float(findNoOfElements(index[0]))/totalNoOfInputs
			prob[index[0]] = '{0:.4f}'.format(round(probability,4))
			cpt.update(prob)
print len(cpt.keys())
query = "[{'stroke':'yes'}, {'income':51000, 'smoke':'no', 'exercise':'no'}]"

f = open('test_output.txt', 'w')
f.write(output+"\n\n"+str(cpt))	#Write output to file
	