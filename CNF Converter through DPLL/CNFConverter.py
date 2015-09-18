# your code goes 
import sys

#Tree structure in which every node's data contains an operator(logical connective)
#as a singletion list and the left and the right children are nodes with data 
#as the operands(literals/sentences)
class Tree(object):
    def __init__(self):
        self.left = None
        self.right = None
        self.data = None
        self.parent = None

#Method to visualize the tree representation by printing the nodes indented in different levels
def printNodes(node,level):
	display = ""
	for i in range(0,level):
		display += "\t"
	print(display+" "+str(node.data))
	level += 1
	if(node.left is not None):
		printNodes(node.left,level)
	if(node.right is not None):
		printNodes(node.right,level)
	level -= 1
		
#Method to create a tree structure. Given the parent node 'node', that has its data
#element set with a list(list of sentences as in the input file), this method recursively
#creates a set of nodes, each having its data as a logical connective and the left and 
#right children as either literals or sentences
def createNodes(node):
	if isinstance(node.data, list):
		if(len(node.data) > 1):
			value = node.data[1]
			del node.data[1]
			node.left = Tree()
			node.left.data = value
			node.left.parent = node
			createNodes(node.left)
		if(len(node.data) > 1):
			value = node.data[1]
			del node.data[1]
			node.right = Tree()
			node.right.data = value
			node.right.parent = node
			createNodes(node.right)
            
#Method that cleans up the tree by recursively traversing the tree from the 'node' and 
#sets the 'parent' element of each node to the parent node of the node
def resetParents(node):
	if(node.left is not None):
		node.left.parent = node
		resetParents(node.left)
	if(node.right is not None):
		node.right.parent = node
		resetParents(node.right)
	
#Method that copies the tree structure in node1 to node2
def copyNodes(node1,node2):
	if node1 is None:
		return node2
	node2.data = node1.data
	if (node1.left is not None):
		node2.left = Tree()
		node2.left.data = node1.left.data
		node2.left.parent = node1.left.parent
		copyNodes(node1.left,node2.left)
	if (node1.right is not None):
		node2.right = Tree()
		node2.right.data = node1.right.data
		node2.right.parent = node1.right.parent
		copyNodes(node1.right,node2.right)
	return node2

#Method that creates and returns a tree root node
def createTree(element):
	root = Tree()
	root.data = element
	return root

#Flag that if true, indicates that a CNF conversion step has been executed
stepflag = False

#Method that converts a tree that represents a sentence into its equivalent CNF format
def convertToCNF(node):
	global stepflag
    #Flag that if true, indicates that the distributive law can be applied to simplify the sentence
	global simplifiedFlag
	if(node is not None):
		connective = node
		leftNode = None
		rightNode = None
		if(node.left is not None):
			convertToCNF(node.left)
			leftNode = node.left
		if(node.right is not None):
			convertToCNF(node.right)
			rightNode = node.right
		if stepflag is True:
			return
		if( node.left is not None or node.right is not None ):
			if node.data[0]=="iff":			#Biconditional elimination
				node.data[0] = "and"
				leftNode = Tree()
				leftNode = copyNodes(node.left,leftNode)
				node.left.data = ["implies"]
				node.left.left = Tree()
				node.left.left = leftNode
				rightNode = Tree()
				rightNode = copyNodes(node.right,rightNode)
				node.left.right = Tree()
				node.left.right = rightNode
				node.right.data = ["implies"]
				node.right.left = Tree()
				node.right.left = rightNode
				node.right.right = Tree()
				node.right.right = leftNode
				stepflag = True
				return 
			if node.data[0]=="implies":		#Implication elimination
				leftNode = Tree()
				leftNode = copyNodes(node.left,leftNode)
				rightNode = Tree()
				rightNode = copyNodes(node.right,rightNode)
				node.data[0] = "or"
				node.left = Tree()
				node.left.data = ["not"]
				node.left.left = Tree()
				node.left.left = leftNode
				node.left.right = None
				node.right = Tree()
				node.right = rightNode
				stepflag = True
				return
			if node.data[0]=="not":
				if node.left.data is not None and node.left.data[0] == "not":#Double negation elimination
					leftNode = Tree()
					leftNode = copyNodes(node.left.left,leftNode)
					if node.parent is not None:
						if node.parent.left is node:
							node.parent.left = Tree()
							node = copyNodes(leftNode,node.parent.left)
						else:
							node.parent.right = Tree()
							node = copyNodes(leftNode,node.parent.right)
					stepflag = True
					return
				if node.left.data is not None and node.left.data[0] == "and":#De Morgan's Law - not of and
					node.data[0] = "or"
					node.left.data = ["not"]
					node.right = Tree()
					node.right.data = ["not"]
					leftNode = Tree()
					leftNode = copyNodes(node.left.left,leftNode)
					rightNode = Tree()
					rightNode = copyNodes(node.left.right,rightNode)
					node.left.left = Tree()
					node.left.left = leftNode
					node.left.right = None
					node.right.left = Tree()
					node.right.left = rightNode
					node.right.right = None
					stepflag = True
					return
				if node.left.data is not None and node.left.data[0] == "or":#De Morgan's Law - not of or
					node.data[0] = "and"
					node.left.data = ["not"]
					node.right = Tree()
					node.right.data = ["not"]
					leftNode = Tree()
					leftNode = copyNodes(node.left.left,leftNode)
					rightNode = Tree()
					rightNode = copyNodes(node.left.right,rightNode)
					node.left.left = Tree()
					node.left.left = leftNode
					node.left.right = None
					node.right.left = Tree()
					node.right.left = rightNode
					node.right.right = None
					stepflag = True
					return
			if node.data[0] == "or" and simplifiedFlag==1:	#Distributive Law
				isleftand = False
				isrightand = False
				if node.right.data is not None and node.right.data[0] == "and":
					isrightand = True
				if node.left.data is not None and node.left.data[0] == "and":
					isleftand = True
				if isrightand and isleftand:
					node.data[0] = "and"
					leftleftNode = Tree()
					leftrightNode = Tree()
					rightleftNode = Tree()
					rightrightNode = Tree()
					leftleftNode = copyNodes(node.left.left,leftleftNode)
					leftrightNode = copyNodes(node.left.right,leftrightNode)
					rightleftNode = copyNodes(node.right.left,rightleftNode)
					rightrightNode = copyNodes(node.right.right,rightrightNode)
					node.left.left = Tree()
					node.left.left.data = ["or"]
					node.left.right = Tree()
					node.left.right.data = ["or"]
					node.right.left = Tree()
					node.right.left.data = ["or"]
					node.right.right = Tree()
					node.right.right.data = ["or"]
					node.left.left.left = Tree()
					node.left.left.left = leftleftNode
					node.left.left.right = Tree()
					node.left.left.right = rightleftNode
					node.left.right.left = Tree()
					node.left.right.left = leftrightNode
					node.left.right.right = Tree()
					node.left.right.right = rightleftNode
					node.right.left.left = Tree()
					node.right.left.left = leftleftNode
					node.right.left.right = Tree()
					node.right.left.right = rightrightNode
					node.right.right.left = Tree()
					node.right.right.left = leftrightNode
					node.right.right.right = Tree()
					node.right.right.right = rightrightNode
					stepflag = True
					return
				if isrightand:
					node.data[0] = "and"
					orLeftNode = Tree()
					orLeftNode = copyNodes(node.left,orLeftNode)
					node.left = Tree()
					leftNode = Tree()
					leftNode = copyNodes(node.right.left,leftNode)
					rightNode = Tree()
					rightNode = copyNodes(node.right.right,rightNode)
					node.left.data = ["or"]
					node.left.left = Tree()
					node.left.left = orLeftNode
					node.left.right = Tree()
					node.left.right = leftNode
					node.right = Tree()
					node.right.data = ["or"]
					node.right.left = Tree()
					node.right.left = orLeftNode
					node.right.right = Tree()
					node.right.right = rightNode
					stepflag = True
					return
				if isleftand:
					orRightNode = Tree()
					leftNode = Tree()
					rightNode = Tree()
					node.data[0] = "and"
					orRightNode = copyNodes(node.right,orRightNode)
					leftNode = copyNodes(node.left.left,leftNode)
					rightNode = copyNodes(node.left.right,rightNode)
					node.left.data = ["or"]
					node.left.left = Tree()
					node.left.left = leftNode
					node.left.right = Tree()
					node.left.right = orRightNode
					node.right = Tree()
					node.right.data = ["or"]
					node.right.left = Tree()
					node.right.left = rightNode
					node.right.right = Tree()
					node.right.right = orRightNode
					stepflag = True
					return

#Method that splits more than 2 operands for an operator into sub trees
def formatSentence(sentence):
	if len(sentence)>3:
		while len(sentence)>3:
			sen = [sentence[0],sentence[1],sentence[2]]
			del sentence[1]
			del sentence[1]
			sentence.insert(1,sen)
	return sentence
	
nodeStr = ""
	
#Method that checks if the simplified sentence consists of any "iff" or "implies" operators
def containsCorrectConnectives(node):
	global nodeStr
	if node.data is not None:
		nodeStr += (str(node.data)+" , ")
	if(node.left is not None):
		containsCorrectConnectives(node.left)
	if(node.right is not None):
		containsCorrectConnectives(node.right)

isCNF = True

#Method that checks if the simplified sentence follows the CNF format
def isInCNF(node):
	global isCNF
	
	if node.left is not None and isinstance(node.left.data, list):
		isInCNF(node.left)
	if node.right is not None and isinstance(node.right.data, list):
		isInCNF(node.right)
	if isCNF is False:
		return
	if isinstance(node.data, list):
		if node.data[0] is "or":
			if isinstance(node.left.data, list):
				if node.left.data[0] is "and":
					isCNF = False
			if isinstance(node.right.data, list):
				if node.right.data[0] is "and":
					isCNF = False
		if node.data[0] is "not":
			if isinstance(node.left.data, list):
				if node.left.data[0] is "and":
					isCNF = False
				if node.left.data[0] is "or":
					isCNF = False
				if node.left.data[0] is "not":
					isCNF = False
	return

listStr = ""

#Method that reformats the tree each node in the tree consists of maximum 2 children
#and each child is either a sentence except for the leaf nodes which are literals
def reformatTree(node):
	if isinstance(node.data, list) and node.left is not None and node.right is not None:
		return [node.data[0],reformatTree(node.left),reformatTree(node.right)]
	if isinstance(node.data, list) and node.left is not None:
		return [node.data[0],reformatTree(node.left)]
	if node.data is not None and node.left is None and node.right is None:
		return node.data
		
#Method that formats the sentences in such a way that combines more than one OR/AND sentences
#in the same level into one OR/AND sentence with several operands
def reformatSentence(sentence):
	if isinstance(sentence, list) and len(sentence)>=3 and sentence[1] is not None and sentence[2] is not None:
		if(sentence[0] is sentence[1][0] and sentence[0] is sentence[2][0]):
			return reformatSentence([reformatSentence(sentence[0]),reformatSentence(sentence[1][1]),reformatSentence(sentence[1][2]),reformatSentence(sentence[2][1]),reformatSentence(sentence[2][2])])
		elif(sentence[0] is sentence[1][0]):
			l = reformatSentence([reformatSentence(sentence[0]),reformatSentence(sentence[1][1]),reformatSentence(sentence[1][2])])
			for i in range(2,len(sentence)):
				l.insert(i+1,reformatSentence(sentence[i]))
			return l
		elif(sentence[0] is sentence[2][0]):
			return reformatSentence([reformatSentence(sentence[0]),reformatSentence(sentence[1]),reformatSentence(sentence[2][1]),reformatSentence(sentence[2][2])])
		else:
			l = [reformatSentence(sentence[0]),reformatSentence(sentence[1])]
			for i in range(2,len(sentence)):
				l.insert(i,reformatSentence(sentence[i]))
			return l
	return sentence

#Method that removes duplicate literals within the same connective
def removeDuplicates(sentence):
	for i in sentence:
		indices = [j for j, x in enumerate(sentence) if x == i]
		if len(indices)>1:
			del indices[0]
			for k in indices:
				sentence.pop(k)
			
	for i in sentence:
		if isinstance(i, list):
			for j in i:
				indices = [k for k, x in enumerate(i) if x == j]
				#print j
				#print indices
				if len(indices)>1:
					del indices[0]
					for m in indices:
						i.pop(m)
	return sentence

#Reading the filename
fname = sys.argv[2]

#Reading the file
with open(fname) as f:
    input = f.read().splitlines()

output= ""
currentStatement = 0
if input:
	noOfSentences = len(input)
	for sentence in input:
		if currentStatement == 0:
			noOfSentences = int(sentence)
			currentStatement += 1
		else:
			currentStatement += 1
			l = eval(sentence)
			l = formatSentence(l)
			#print l
			root = createTree(l)
			createNodes(root)
			containsCorrectConnectives(root)
			isInCNF(root)
			while "iff" in nodeStr or "implies" in nodeStr or not isCNF:
				try:
					stepflag = False
					l = eval(sentence)
					l = formatSentence(l)
					root = createTree(l)
					createNodes(root)
					simplifiedFlag = 0
					convertToCNF(root)	#Performs biconditional/implication/double-negation eliminations and De Morgan's
					simplifiedFlag = 1
					convertToCNF(root)	#Performs distributive law
					root.parent = None
					resetParents(root)
					listStr = ""
					nodeStr = ""
					isCNF = True
					containsCorrectConnectives(root)
					isInCNF(root)
					formattedSentence = reformatTree(root)
					outputSentence = reformatSentence(formattedSentence)
					outputSentence = removeDuplicates(outputSentence)
					sentence = str(outputSentence)
				except AttributeError:
					pass
		output += sentence+"\n"
        output = '\n'.join(output.split('\n')[1:])
        f = open('sentences_CNF.txt', 'w')
        f.write(output)	#Write output to file