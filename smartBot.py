import re
from pattern.en import pluralize, singularize

def isVowel(val):
	return val in ('a', 'e', 'i', 'o', 'u')


def verifyStatement(knowledgeBase,x,y):
	forwardSearch = {}
	reverseSearch = {}
	if bool(knowledgeBase[x]) == False:
		for fact in knowledgeBase:
			backwardInfer(fact,fact,knowledgeBase,x,reverseSearch)
		return reverseSearch.has_key(y)
	else:
		forwardInfer(True,knowledgeBase,x,forwardSearch)
		for fact in knowledgeBase:
			backwardInfer(fact,fact,knowledgeBase,x,reverseSearch)
		return forwardSearch.has_key(y) or reverseSearch.has_key(y)


def forwardInfer(isFoward,knowledgeBase,isMatch,statement):
	if bool(knowledgeBase[isMatch]):
		for fact in knowledgeBase[isMatch]:
			if statement.has_key(fact) == False:
				if knowledgeBase[isMatch][fact]:
					statement[fact] = knowledgeBase[isMatch][fact]
					forwardInfer(False,knowledgeBase,fact,statement)
				elif knowledgeBase[isMatch][fact] == False  and isFoward == True:
					statement[fact] = knowledgeBase[isMatch][fact]


def backwardInfer(previousVal,nextVal,knowledgeBase,isMatch,statement):
	if bool(knowledgeBase[nextVal]):
		for fact in knowledgeBase[nextVal]:
			if knowledgeBase[nextVal][fact] == True and fact != isMatch:
				backwardInfer(previousVal,fact,knowledgeBase,isMatch,statement)
			elif fact == isMatch:
				if statement.has_key(previousVal) == False:
					statement[previousVal] = knowledgeBase[nextVal][fact]


def retrieveStatement(knowledgeBase,x,y,relationship):
	response = x.title()
	if getProperGrammar(knowledgeBase,x) == 1:
		if relationship:
			response +=" are"
		else:
			response += " are not"
	elif getProperGrammar(knowledgeBase,x) == 2:
		response = x.title()
		if relationship:
			response +=" is"
		else:
			response +=" is not"
		if getProperGrammar(knowledgeBase,y) == 1:
			y = extract(1,knowledgeBase,y)[0]
	elif getProperGrammar(knowledgeBase,x) == 3:
		if isVowel(x[0]):
			response = "An "+x
		else:
			response = "A "+x
		if relationship:
			response +=" is"
		else:
			response +=" is not"
	if getProperGrammar(knowledgeBase,y) == 3:
		if isVowel(y[0]):
			response +=" an "
			response += y
		else:
			response +=" a "
			response += y
	else:
		response += " "
		response +=y
	return response


def getProperGrammar(knowledgeBase,entity):
	for fact in knowledgeBase:
		if fact[0] != entity and fact[1] == entity:
			return 1
		elif fact[0] == entity and fact[1] == entity:
			return 2
		elif fact[1] != entity and fact[0] == entity:
			return 3
	return None


def extract(userInput,knowledgeBase,userInputFact):
	for fact in knowledgeBase:
		if fact[userInput] == userInputFact:
			return fact
	return None


def submitFact(knowledgeBase,userInput):
	template = re.compile("(A |An )?([A-z]+) (is|are)+ (not )?(a |an )?([A-z]+)")
	statement = re.search(template,userInput)
	response = "Got it"

	if statement:
		x = statement.group(2).lower()
		y = statement.group(6).lower()		
		if statement.group(3) == "are":
			subject = extract(1,knowledgeBase,x)
			target = extract(1,knowledgeBase,y)
			if subject != None and target != None:
				if knowledgeBase[subject].has_key(target) or verifyStatement(knowledgeBase,subject,target):
					response = "I know."

			if subject == None:
				question = 'What is the singular form of '+statement.group(2)+ "?" +'\n'
				singular = singularize(statement.group(2)).lower()#raw_input(question).lower()
				#print("Test: " + singular )
				if singular == "na":	
					subject = (x,x)
				else:
					subject = (singular,x)
			if target == None:
				question = 'What is the singular form of '+statement.group(6)+ "?" +'\n'
				singularTarget = singularize(statement.group(6)).lower()#raw_input(question).lower()
				#print("Test: " + singularTarget )
				if singularTarget == "na":
					target = (y,y)
				else:
					target = (singularTarget,y)  

		elif statement.group(3) == "is":
			subject = extract(0,knowledgeBase,x)
			target = extract(0,knowledgeBase,y)
			if subject != None and target != None:
				if knowledgeBase[subject].has_key(target) or verifyStatement(knowledgeBase,subject,target):
					response ="I know."
			if subject == None:
				question = 'What is the plural form of '+statement.group(2)+"?" +'\n'
				plural = pluralize(statement.group(2)).lower()
				#print("Test: " + plural )
				if plural == "na":
					plural = x
				subject = (x,plural)
			if target == None:
				question = 'What is the plural form of '+statement.group(6)+"?" +'\n'
				pluralTarget = pluralize(statement.group(6)).lower()
				#print("Test: " + pluralTarget )
				if pluralTarget == "na":
					pluralTarget = y
				target = (y,pluralTarget)

		if knowledgeBase.has_key(subject) == False:
			knowledgeBase[subject] = {}
		if knowledgeBase.has_key(target) == False:
			knowledgeBase[target] = {}
		if statement.group(4) == None:
			knowledgeBase[subject][target] = True
		else :
			knowledgeBase[subject][target] = False
	return response


def run(userInput,knowledgeBase):
	template = re.compile("What do you know about ([A-z]+)?")
	statement = re.search(template,userInput)
	searchGraph = {}
	reverseGraph = {}
	response = "Got it!"
	statementExists = False
	if statement:
		counter = 0
		statementExists = True
		isNew = True
		x = statement.group(1).lower()
		subject = extract(0,knowledgeBase,x)
		num = getProperGrammar(knowledgeBase,x)
		if subject == None:
			subject = extract(1,knowledgeBase,x)

		if subject != None:
			forwardInfer(True,knowledgeBase,subject,searchGraph)
			for fact in knowledgeBase:
				backwardInfer(fact,fact,knowledgeBase,subject,reverseGraph)
			if bool(knowledgeBase[subject]):
				regList = searchGraph.items()
				revList = reverseGraph.items()
				ans = statement.group(1)

				y = regList[0]

				
				if getProperGrammar(knowledgeBase,x):
					response = retrieveStatement(knowledgeBase,x.lower(),y[0][1],y[1])
					counter = counter + 1
				else:
					response = retrieveStatement(knowledgeBase,x.lower(),y[0][0],y[1])
					counter = counter + 1
			else:
				isNew = False
				revList = reverseGraph.items()
				ans = statement.group(1)
				y = revList[0]
				if getProperGrammar(knowledgeBase,x):
					response = retrieveStatement(knowledgeBase,y[0][1],x.lower(),y[1])
					counter = counter + 1
				else:
					response = retrieveStatement(knowledgeBase,y[0][0],x.lower(),y[1])
					counter = counter + 1				
		else:
			response = "I don't know anything about " + x+"."

		# Traverse graph to attain all the facts
		regList = searchGraph.items()
		revList = reverseGraph.items()

		length = len(regList)-1

		if isNew ==True: 
			while counter <= length or counter-length-1 < len(revList):
				if counter <= length:
					y = regList[counter]
					if getProperGrammar(knowledgeBase,x):
						response += "\n" +retrieveStatement(knowledgeBase,x.lower(),y[0][1],y[1])
						counter = counter + 1
					else:
						response += "\n" +retrieveStatement(knowledgeBase,x.lower(),y[0][0],y[1])
						counter = counter + 1
				elif counter-length-1 < len(revList):
					y = revList[counter - length-1]
					if getProperGrammar(knowledgeBase,x):
						response += "\n" +retrieveStatement(knowledgeBase,y[0][1],x.lower(),y[1])
						counter = counter + 1
					else:
						response += "\n" +retrieveStatement(knowledgeBase,y[0][0],x.lower(),y[1])
						counter = counter + 1
				else:
					response += "I don't know anything else about "+x+"."
					response += response


		else:
			while counter <= length:
				if counter <= length:
					y = revList[counter]
					if getProperGrammar(knowledgeBase,x):
						response += "\n" +retrieveStatement(knowledgeBase,y[0][1],x.lower(),y[1])
						counter = counter + 1
					else:
						response += "\n" +retrieveStatement(knowledgeBase,y[0][0],x.lower(),y[1])
						counter = counter + 1
				else:
					response += "I don't know anything else about "+x +"."
					response += response	
	# End

	templateAnswer = re.compile("(Is|Are|is|are)+ (a |an )?([A-z]+) (a |an )?([A-z]+)(\?)?")
	statementAnswer = re.search(templateAnswer,userInput)
	if statementAnswer:
		statementExists = False
		x = statementAnswer.group(3).lower()
		y = statementAnswer.group(5).lower()
		num = statementAnswer.group(1).lower()
		if num == "is":
			subject = extract(0,knowledgeBase,x)
			target = extract(0,knowledgeBase,y)
		else:
			subject = extract(1,knowledgeBase,x)
			target = extract(1,knowledgeBase,y)

		if subject == None or target == None or (knowledgeBase[subject].has_key(target) == False and verifyStatement(knowledgeBase,subject,target) == False):
			response = "I'm not sure given what you've told me so far"
		elif verifyStatement(knowledgeBase,subject,target) or knowledgeBase[subject][target] == True:
			response = ("Yes.")
		elif knowledgeBase[subject][target] == False:
			response = ("No.")
	fact = re.compile("(A |An )?([A-z]+) (is|are)+ (not )?(a |an )?([A-z]+)")
	statementFact = re.search(fact,userInput)
	if statementFact:
		response = submitFact(knowledgeBase,userInput)
	

	if statementAnswer == None and statementFact == None and statement == None:
		response = ("I don't understand.")
	return response



