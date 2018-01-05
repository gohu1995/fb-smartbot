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



def updateKB(knowledgeBase,x,y,relationship):
	if getScenario(knowledgeBase,x) == 1:
		response = x.title()
		if relationship:
			response +=" are"
		else:
			response += " are not"
	elif getScenario(knowledgeBase,x) == 2:
		response = x.title()
		if relationship:
			response +=" is"
		else:
			response +=" is not"
		if getScenario(knowledgeBase,y) == 1:
			y = extract(1,knowledgeBase,y)[0]
	elif getScenario(knowledgeBase,x) == 3:
		if isVowel(x[0]):
			response = "An "+x
		else:
			response = "A "+x
		if relationship:
			response +=" is"
		else:
			response +=" is not"
	if getScenario(knowledgeBase,y) == 3:
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



def getScenario(knowledgeBase,fact):
	for fact in knowledgeBase:
		if fact[0] != fact and fact[1] == fact:
			return 1
		elif fact[0] == fact and fact[1] == fact:
			return 2
		elif fact[1] != fact and fact[0] == fact:
			return 3
	return None



def extract(input,knowledgeBase,fact):
	for fact in knowledgeBase:
		if fact[input] == fact:
			return fact
	return None





def submitFact(knowledgeBase,input):
	template = re.compile("(A |An )?([A-z]+) (is|are)+ (not )?(a |an )?([A-z]+)")
	statement = re.search(template,input)

	if statement:
		x = statement.group(2).lower()
		y = statement.group(6).lower()		
		if statement.group(3) == "are":
			subject = extract(1,knowledgeBase,x)
			target = extract(1,knowledgeBase,y)
			if subject != None and target != None:
				if bool(knowledgeBase[subject]) == False:
					print ("Ok.")
				elif knowledgeBase[subject].has_key(target) or verifyStatement(knowledgeBase,subject,target):
					print ("I know.")
				else:
					print ("Ok.")
			if subject == None:
				question = 'What is the singular form of '+statement.group(2)+ "?" +'\n'
				singular = singularize(statement.group(2))
				if singular == "na":	
					subject = (x,x)
				else:
					subject = (singular,x)
			if target == None:
				question = 'What is the singular form of '+statement.group(6)+ "?" +'\n'
				singularNegative = singularize(statement.group(6))
				if singularNegative == "na":
					target = (y,y)
				else:
					target = (singularNegative,y)  
		elif statement.group(3) == "is":
			subject = extract(0,knowledgeBase,x)
			target = extract(0,knowledgeBase,y)
			if subject != None and target != None:
				if bool(knowledgeBase[subject]) == False:
					print ("Ok.")
				elif knowledgeBase[subject].has_key(target) or verifyStatement(knowledgeBase,subject,target):
					print ("I know.")
				else:
					print ("Ok.")
			if subject == None:
				question = 'What is the plural form of '+statement.group(2)+"?" +'\n'
				plural = pluralize(statement.group(2))
				print("Test: " + plural )
				if plural == "na":
					plural = x
				subject = (x,plural)
			if target == None:
				question = 'What is the plural form of '+statement.group(6)+"?" +'\n'
				pluralNegative = pluralize(statement.group(6))
				print("Test: " + pluralNegative )
				if pluralNegative == "na":
					pluralNegative = y
				target = (y,pluralNegative)
			
		if knowledgeBase.has_key(subject) == False:
			knowledgeBase[subject] = {}
		if knowledgeBase.has_key(target) == False:
			knowledgeBase[target] = {}
		if statement.group(4) == None:
			knowledgeBase[subject][target] = True
		else :
			knowledgeBase[subject][target] = False
	return knowledgeBase








def run(input,knowledgeBase):

	template = re.compile("What do you know about ([A-z]+)?")
	statement = re.search(template,input)
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
		num = getScenario(knowledgeBase,x)
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

				
				if getScenario(knowledgeBase,x):
					response = updateKB(knowledgeBase,x.lower(),y[0][1],y[1])
					counter = counter + 1
				else:
					response = updateKB(knowledgeBase,x.lower(),y[0][0],y[1])
					counter = counter + 1
			else:
				isNew = False
				revList = reverseGraph.items()
				ans = statement.group(1)
				y = revList[0]
				if getScenario(knowledgeBase,x):
					response = updateKB(knowledgeBase,y[0][1],x.lower(),y[1])
					counter = counter + 1
				else:
					response = updateKB(knowledgeBase,y[0][0],x.lower(),y[1])
					counter = counter + 1				
		else:
			response = "I don't know anything about " + x+"."



	templateElse = re.compile("Anything else?")
	statementElse = re.search(templateElse,input)

	if statementElse and statementExists == True:
		if isNew == True:
			length = len(regList)-1
			if counter <= length:
				y = regList[c]
				if getScenario(knowledgeBase,x):
					response = updateKB(knowledgeBase,x.lower(),y[0][1],y[1])
					counter = counter + 1
				else:
					response = updateKB(knowledgeBase,x.lower(),y[0][0],y[1])
					counter = counter + 1
			elif c-length-1 < len(revList):
				y = revList[counter - length-1]
				if getScenario(knowledgeBase,x):
					response = updateKB(knowledgeBase,y[0][1],x.lower(),y[1])
					counter = counter + 1
				else:
					response = updateKB(knowledgeBase,y[0][0],x.lower(),y[1])
					counter = counter + 1
			else:
				response = "I don't know anything else about "+x+"."
				response = response
		else:
			length = len(revList)-1
			if counter <= length:
				y = revList[c]
				if getScenario(knowledgeBase,x):
					response = updateKB(knowledgeBase,y[0][1],x.lower(),y[1])
					counter = counter + 1
				else:
					response = updateKB(knowledgeBase,y[0][0],x.lower(),y[1])
					counter = counter + 1
			else:
				response = "I don't know anything else about "+x +"."
				response = response



	templateAnswer = re.compile("(Is|Are)+ (a |an )?([A-z]+) (a |an )?([A-z]+)\?")
	statementAnswer = re.search(templateAnswer,input)
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
	statement = re.search(fact,input)
	if statement:
		knowledgeBase = submitFact(knowledgeBase,input)
	

	if statementAnswer == None and statement == None and statement == None and statementElse == None:
		response = ("I don't understand.")
	return response