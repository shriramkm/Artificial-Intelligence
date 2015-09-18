import sys
import collections

#Method that implements the DPLL algorithm. This method runs recursively, each time 
#trying to execute either a unit clause step or a pure symbol step. 
#If both do not return relevant results, then the method runs the splitting step
def DPLL():
	global clauses
	global symbols
	global model
	global isFirstSplit
	global clausesBeforeSplit
	#print "NEXT : "+str(clauses)
	index = 0
	for clause in clauses:
		if isinstance(clause,list):
			if len(clause)==2:
				if(clause[0]=="or"):
					clauses[index] = clause[1]
		index += 1
	if len(clauses)==0:
		return True
	if [] in clauses:
		return False
	#Find Unit Clause and remove the complement of unit clauses from the remaining clauses
	unitClause = findUnitClause()
	if unitClause==False:
		return False
	if len(unitClause)>0:
		#print "UNIT : "+str(unitClause)
		return DPLL()
	#Find Pure Symbol
	pureSymbol = findPureSymbol()

	if len(pureSymbol)>0:
      	#Add the value of the pure symbol to the model
		#print "PURE : "+str(pureSymbol)
		if isinstance(pureSymbol,list):
			#print "REMOVING "+pureSymbol[1]+" FROM "+str(symbols)
			if pureSymbol[1] not in symbols:
				return False;
			symbols.remove(pureSymbol[1])
			value = pureSymbol[1]+"=false"
		else:
			#print "REMOVING "+pureSymbol+" FROM "+str(symbols)
			if pureSymbol not in symbols:
				return False;
			symbols.remove(pureSymbol)
			value = pureSymbol+"=true"
		clausesToDelete = []
        #Remove the clauses the contain the pure symbol from the list of all clauses
		for clause in clauses:
			if pureSymbol in clause or pureSymbol==clause:
				clausesToDelete.append(clause)
		for toDelete in clausesToDelete:
			clauses.remove(toDelete)
		model.append(value)
		#print model
		return DPLL()
	if len(pureSymbol)==0 and len(unitClause)==0:
		P = symbols[0]
		#del symbols[0]
		if(isFirstSplit == False):
			clausesBeforeSplit = clauses
			clauses.append(P)
			firstSplit = True
			firstSplit = DPLL()
		if firstSplit:
			#print "SPLIT : "+str(P)
			return firstSplit
		else:
			#clauses.remove(P)
			clauses = clausesBeforeSplit
			#print "SPLIT : "+str(["not",P])
			clauses.append(["not",P])
			return DPLL()
	
#Method that returns a list of all the literals that are present in all the clauses in the input
def findClauseLiterals():
	global clauses
	global symbols
	global model
	clauseLiterals = []
	for clause in clauses:
		if isinstance(clause,list):
			for part in clause:
				if isinstance(part,list) and part[0]=="not":
					clauseLiterals.append(part)
				elif part=="not":
					clauseLiterals.append(clause)
					break
				elif part!="or" and part!="and":
					clauseLiterals.append(part)
		else:
			if clause!="or" and clause!="and" and clause!="not":
				clauseLiterals.append(clause)
	return clauseLiterals
	
#Method that finds a unit clause from the list of all clauses and removes this clause from the list
#of all clauses. It also removes the complement of the unit clause from all the other clauses.
def findUnitClause():
	global symbols
	global clauses
	global model
	unitClause = []
	complement = None
	symbol = None
	chosenClause = None
	for clause in clauses:
      	#Find the unit clause and adding the value of the unit clause to model
		if len(clause)==1:
			if isinstance(clause[0],list):
				#print "REMOVING "+clause[0][1]+" FROM "+str(symbols)
				if clause[0][1] not in symbols:
					return False
				symbols.remove(clause[0][1])
				value = clause[0][1]+"=false"
				complement = clause[0][1]
			else:
				#print "REMOVING "+clause[0]+" FROM "+str(symbols)
				if clause[0] not in symbols:
					return False
				symbols.remove(clause[0])
				value = clause[0]+"=true"
				complement = ["not",clause[0]]
			chosenClause = clause
			symbol = clause[0]
			if(chosenClause in clauses and complement in clauses):
				return False
			clauses.remove(clause)
			model.append(value)
			unitClause.append(clause)
			break
	clausesToDelete = []
	#Removing the clauses that contain the unit clause
	if(len(unitClause)>0):
		for clause in clauses:
			if unitClause[0] in clause or unitClause[0]==clause:
				clausesToDelete.append(clause)
		for toDelete in clausesToDelete:
			clauses.remove(toDelete)
	#Removing the complement of the unit clause from the remaining clauses
	if complement is not None:
		for clause in clauses:
			if complement in clause:
				#print "REMOVING COMPLEMENTARY CLAUSE 1"
				clause.remove(complement)
	return unitClause
	
#Method that finds a pure symbol from a list of clauses
def findPureSymbol():
	global symbols
	global clauses
	global model
	clauseLiterals = findClauseLiterals()
	for clauseLiteral in clauseLiterals:
		if isinstance(clauseLiteral,list) and clauseLiteral[1] not in clauseLiterals:
			return clauseLiteral
		elif not isinstance(clauseLiteral,list) and ["not",clauseLiteral] not in clauseLiterals:
			return clauseLiteral
	return []
	
#Method that returns a list of clauses in a given string
def findClauses(sentence):
	clauses = []
	if sentence[0] == "and":
		for i in range(1,len(sentence)):
			clauses.append(sentence[i])
	else:
		clauses.append(sentence)
	return clauses
	
#Method that finds all the symbols present in a list of clauses
def findSymbols(clauses):
	symbols = []
	for clause in clauses:
		if isinstance(clause,list):
			for part in clause:
				if isinstance(part,list):
					for subpart in part:
						if subpart!="or" and subpart!="and" and subpart!="not":
							symbols.append(subpart)
				elif part!="or" and part!="and" and part!="not":
					symbols.append(part)
		else:
			if clause!="or" and clause!="and" and clause!="not":
				symbols.append(clause)
	symbols = list(set(symbols))
	return symbols

#Reading the filename
fname = sys.argv[2]

#Reading the file
with open(fname) as f:
	input = f.read().splitlines()
	print input
output = ""
for sentence in input[1:]:
	sentence = eval(sentence)
	clauses = findClauses(sentence)
	symbols = findSymbols(clauses)
	model = []
	isFirstSplit = False
	if(DPLL()):
		for symbol in symbols:
			model.append(symbol+"=true")
		model.insert(0, "true") 
	else:
		model = ["false"]
	output += str(model)+"\n"
	#print "OUTPUT : "+str(model)
f = open('CNF_satisfiability.txt', 'w')
f.write(output)	#Write output to file