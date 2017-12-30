import re
from pattern.en import pluralize, singularize



def checkVow(val):
	return val == "o" or val == "i" or val == "e" or val == "a" or val == "u"




def check_this(Knowledge_Base,x,y):
	straight = {}
	reverse = {}
	if bool(Knowledge_Base[x]) == False:
		for fact in Knowledge_Base:
			backwardInfer(fact,fact,Knowledge_Base,x,reverse)
		return reverse.has_key(y)
	else:
		forwardInfer(1,Knowledge_Base,x,straight)
		for fact in Knowledge_Base:
			backwardInfer(fact,fact,Knowledge_Base,x,reverse)
		return straight.has_key(y) or reverse.has_key(y)


def forwardInfer(checker,Knowledge_Base,match,container):
	if bool(Knowledge_Base[match]):
		for fact in Knowledge_Base[match]:
			if container.has_key(fact) == False:
				if Knowledge_Base[match][fact]:
					container[fact] = Knowledge_Base[match][fact]
					forwardInfer(-1,Knowledge_Base,fact,container)
				elif Knowledge_Base[match][fact] == False  and checker == 1:
					container[fact] = Knowledge_Base[match][fact]
	


def backwardInfer(prev,next_val,Knowledge_Base,match,container):
	if bool(Knowledge_Base[next_val]):
		for fact in Knowledge_Base[next_val]:
			if Knowledge_Base[next_val][fact] == True and fact != match:
				backwardInfer(prev,fact,Knowledge_Base,match,container)
			elif fact == match:
				if container.has_key(prev) == False:
					container[prev] = Knowledge_Base[next_val][fact]






def generation(Knowledge_Base,x,y,bol):
	if checkPlurality(Knowledge_Base,x) == 1:
		ans = x.title()
		if bol:
			ans +=" are"
		else:
			ans += " are not"
	elif checkPlurality(Knowledge_Base,x) == 2:
		ans = x.title()
		if bol:
			ans +=" is"
		else:
			ans +=" is not"
		if checkPlurality(Knowledge_Base,y) == 1:
			y = extract(1,Knowledge_Base,y)[0]
	elif checkPlurality(Knowledge_Base,x) == 3:
		if checkVow(x[0]):
			ans = "An "+x
		else:
			ans = "A "+x
		if bol:
			ans +=" is"
		else:
			ans +=" is not"
	if checkPlurality(Knowledge_Base,y) == 3:
		if checkVow(y[0]):
			ans +=" an "
			ans += y
		else:
			ans +=" a "
			ans += y
	else:
		ans += " "
		ans +=y
	return ans







def checkPlurality(Knowledge_Base,i):
	for fact in Knowledge_Base:
		if fact[0] != i and fact[1] == i:
			return 1
		elif fact[0] == i and fact[1] == i:
			return 2
		elif fact[1] != i and fact[0] == i:
			return 3
	return None



def extract(num,Knowledge_Base,match):
	for fact in Knowledge_Base:
		if fact[num] == match:
			return fact
	return None



def store_Knowledge_Base(Knowledge_Base,text1,knowledge):
	case_enter_in = re.compile("(A |An )?([A-z]+) (is|are)+ (not )?(a |an )?([A-z]+)")
	match_enter_in = re.search(case_enter_in,text1)


	if match_enter_in:
		c_val = 1
		check = 0

		x = match_enter_in.group(2).lower()
		knowledge += c_val
		y = match_enter_in.group(6).lower()
			
		if match_enter_in.group(3) == "are":
			c_val+=1
			x_val = extract(1,Knowledge_Base,x)
			y_val = extract(1,Knowledge_Base,y)

			if x_val != None and y_val != None:
				if bool(Knowledge_Base[x_val]) == False:
					print ("Ok.")
				elif Knowledge_Base[x_val].has_key(y_val) or check_this(Knowledge_Base,x_val,y_val):
					print ("I know.")
				else:
					print ("Ok.")

			if x_val == None:
				insert_input = 'What is the singular form of '+match_enter_in.group(2)+ "?" +'\n'
				s_output_b = raw_input(insert_input).lower()
				if s_output_b == "na":	
					x_val = (x,x)
				else:
					x_val = (s_output_b,x)
			if y_val == None:
				insert_input = 'What is the singular form of '+match_enter_in.group(6)+ "?" +'\n'
				s_output_a = raw_input(insert_input).lower()
				if s_output_a == "na":
					y_val = (y,y)
				else:
					y_val = (s_output_a,y)  
			

		elif match_enter_in.group(3) == "is":
			x_val = extract(0,Knowledge_Base,x)
			y_val = extract(0,Knowledge_Base,y)

			if x_val != None and y_val != None:
				if bool(Knowledge_Base[x_val]) == False:
					print ("Ok.")
				elif Knowledge_Base[x_val].has_key(y_val) or check_this(Knowledge_Base,x_val,y_val):
					print ("I know.")
				else:
					print ("Ok.")


			if x_val == None:
				insert_input = 'What is the plural form of '+match_enter_in.group(2)+"?" +'\n'
				p_output_a = pluralize(match_enter_in.group(2))
				print("Test: " + p_output_a )
				if p_output_a == "na":
					p_output_a = x
				x_val = (x,p_output_a)
			if y_val == None:
				insert_input = 'What is the plural form of '+match_enter_in.group(6)+"?" +'\n'
				p_output_b = pluralize(match_enter_in.group(6))
				print("Test: " + p_output_b )
				if p_output_b == "na":
					p_output_b = y
				y_val = (y,p_output_b)
			
			
		if Knowledge_Base.has_key(x_val) == False:
			Knowledge_Base[x_val] = {}
		if Knowledge_Base.has_key(y_val) == False:
			Knowledge_Base[y_val] = {}
		if match_enter_in.group(4) == None:
			Knowledge_Base[x_val][y_val] = True
		else :
			Knowledge_Base[x_val][y_val] = False
	return Knowledge_Base








def run(User_Input,Knowledge_Base):

	case_what = re.compile("What do you know about ([A-z]+)?")
	match_what = re.search(case_what,User_Input)
	searcher = {}
	searcherRev = {}
	res="Got it!"
	if match_what:
		c = 0
		check = 1
		check_what = 1
		x = match_what.group(1).lower()
		x_val = extract(0,Knowledge_Base,x)
		num = checkPlurality(Knowledge_Base,x)
		if x_val == None:
			x_val = extract(1,Knowledge_Base,x)

		if x_val != None:
			forwardInfer(1,Knowledge_Base,x_val,searcher)
			for fact in Knowledge_Base:
				backwardInfer(fact,fact,Knowledge_Base,x_val,searcherRev)
			if bool(Knowledge_Base[x_val]):
				regList = searcher.items()
				revList = searcherRev.items()
				ans = match_what.group(1)

				y = regList[0]

				
				if checkPlurality(Knowledge_Base,x):
					res = generation(Knowledge_Base,x.lower(),y[0][1],y[1])
					c = c + 1
				else:
					res = generation(Knowledge_Base,x.lower(),y[0][0],y[1])
					c = c + 1
			else:
				check_what = 3
				revList = searcherRev.items()
				ans = match_what.group(1)
				y = revList[0]
				if checkPlurality(Knowledge_Base,x):
					res = generation(Knowledge_Base,y[0][1],x.lower(),y[1])
					c = c + 1
				else:
					res = generation(Knowledge_Base,y[0][0],x.lower(),y[1])
					c = c + 1				
		else:
			res = "I don't know anything about " + x+"."



	case_else = re.compile("Anything else?")
	match_else = re.search(case_else,User_Input)

	if match_else and check == 1:
		if check_what == 1:
			length = len(regList)-1
			if c <= length:
				y = regList[c]
				if checkPlurality(Knowledge_Base,x):
					res = generation(Knowledge_Base,x.lower(),y[0][1],y[1])
					c = c + 1
				else:
					res = generation(Knowledge_Base,x.lower(),y[0][0],y[1])
					c = c + 1
			elif c-length-1 < len(revList):
				y = revList[c - length-1]
				if checkPlurality(Knowledge_Base,x):
					res = generation(Knowledge_Base,y[0][1],x.lower(),y[1])
					c = c + 1
				else:
					res = generation(Knowledge_Base,y[0][0],x.lower(),y[1])
					c = c + 1
			else:
				res = "I don't know anything else about "+x+"."
				res = res
		else:
			length = len(revList)-1
			if c <= length:
				y = revList[c]
				if checkPlurality(Knowledge_Base,x):
					res = generation(Knowledge_Base,y[0][1],x.lower(),y[1])
					c = c + 1
				else:
					res = generation(Knowledge_Base,y[0][0],x.lower(),y[1])
					c = c + 1
			else:
				res = "I don't know anything else about "+x +"."
				res = res



	case_answer = re.compile("(Is|Are)+ (a |an )?([A-z]+) (a |an )?([A-z]+)\?")
	match_answer = re.search(case_answer,User_Input)
	if match_answer:
		check = 0
		x = match_answer.group(3).lower()
		y = match_answer.group(5).lower()
		num = match_answer.group(1).lower()
		if num == "is":
			x_val = extract(0,Knowledge_Base,x)
			y_val = extract(0,Knowledge_Base,y)
		else:
			x_val = extract(1,Knowledge_Base,x)
			y_val = extract(1,Knowledge_Base,y)

		if x_val == None or y_val == None or (Knowledge_Base[x_val].has_key(y_val) == False and check_this(Knowledge_Base,x_val,y_val) == False):
			res = "I'm not sure given what you've told me so far"
		elif check_this(Knowledge_Base,x_val,y_val) or Knowledge_Base[x_val][y_val] == True:
			res = ("Yes.")
		elif Knowledge_Base[x_val][y_val] == False:
			res = ("No.")
	case_enter_in = re.compile("(A |An )?([A-z]+) (is|are)+ (not )?(a |an )?([A-z]+)")
	match_enter_in = re.search(case_enter_in,User_Input)
	if match_enter_in:
		Knowledge_Base = store_Knowledge_Base(Knowledge_Base,User_Input,1)
	

	if match_answer == None and match_enter_in == None and match_what == None and match_else == None:
		res = ("I don't understand.")
	return res









