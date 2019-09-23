class Error():
	def __init__(self, row, column, message):
		self.row = row
		self.column = column
		self.message = message

class Lexem():
	def __init__(self, row=0, column=0, code=0, Ltype ='', string =''):
		self.row = row
		self.column = column
		self.code = code
		self.type = Ltype
		self.string = string

class Lexer():
	def __init__(self,filetxt):
		self.currentRow = 1
		self.currentColumn = 0
		self.keywords = {}
		self.multiDelimiters = {}
		self.identifiers = {}
		self.constants = {}
		self.delimiters = {}
		self.State = dict(zip(['Start', 'Input', 'Identifier', 'Constant','Delimiter', 'BeginComment', 'Comment','EndComment', 'MultiDelimiter', 'Email', 'Phone'],range(11)))
		self.currentState = self.State['Start']
		# self.lexemList = []
		# self.errorList = []
		self.program = open(filetxt)
		self.currentLexem = Lexem()
		self.lastId = 400
		self.lastConst = 600
		self.LoadKeywords()
		self.LoadDelimiters()
		self.LoaduMultiDelimiters()

	def LoadKeywords(self):
		with open('keywords.txt') as k:
			for line in k:
				self.keywords[line.split(' ')[0]] = int(line.split(' ')[1])

	def LoaduMultiDelimiters(self):
		self.multiDelimiters = {':=': 501,'($': 502, '$)': 503}
	
	def LoadDelimiters(self):
		self.delimiters = {';': ord(';'),':': ord(':'),',':ord(','),'(':ord('('),')':ord(')')}


	def Analize(self):
		while True:
			current = self.GetChar()
			self.currentColumn +=1
			if current == '\n':
				self.currentColumn = 0
				self.currentRow += 1
			self.DefineState(current)
			if current == None:
				break

	def GetChar(self):
		char = self.program.read(1)
		if not char and self.currentState == self.State['Start']:
			print (Error(0,0,'File is empty'))
			return None
		elif not char:
			return None
		else:
			return char

	def IsWhiteSpace(self, current):
		ch = ord(current)
		if ch == 32 or ch == 13 or ch == 10 or ch == 9 or ch == 11 or ch==12:
			return True
		return False

	def IsDelimiter(self, current):
		if current in self.delimiters:
			return True
		return False

	def IsMultiDelimiter(self,current):
		for key,value in self.multiDelimiters.items():
				if current == key[0]:
					return True
		return False

	def DefineState(self,current):
		if current == None:
			if self.currentState == self.State['BeginComment'] or self.currentState == self.State['Comment'] or self.currentState == self.State['EndComment']:
				self.DefineError('eof')
			if len(self.currentLexem.string) > 0:
				self.DefineLexem()
			return
		if self.currentState == self.State['BeginComment']:
			if current == '*':
				self.currentState = self.State['Comment']
				self.currentLexem = Lexem()
				return
			if current == '$':
				self.currentState = self.State['MultiDelimiter']
				self.currentLexem.string += current
				self.DefineLexem()
				return
			self.currentState = self.State['Delimiter']
			self.DefineLexem()

		if self.currentState == self.State['Comment']:
			if current == '*':
				self.currentState = self.State['EndComment']
			return


		if self.currentState == self.State['EndComment']:
			if current == ')':
				self.currentState = self.State['Input']
				return
			if current == '*':
				return
			self.currentState = self.State['Comment']
			return

		if (self.currentState == self.State['Phone']) or current == '$':
			self.currentState = self.State['Phone']
			if current.isdigit() or current == '$':
				self.currentLexem.string += current
				return	

			phone = self.currentLexem.string.split('$')
			if len(phone) > 1 and current.isdigit():
				return

			if len(phone) > 1 and len(phone[1]) > 3 and  current.isdigit():
				self.DefineError(self.currentLexem.string)
				self.currentState = self.State['Input']
				return
			if not(current.isdigit() or current == '$') and not len(phone) == 3:
				self.DefineError(self.currentLexem.string)
				self.currentState = self.State['Input']
				return
			if len(phone) == 3 and len(phone[0]) == 0 and len(phone[1]) == 3:
				if len(phone[2].strip()) == 7 and phone[2].strip().isdigit():
					self.DefineLexem()
					return
				if len(phone[2].strip()) > 7:
					self.DefineError(self.currentLexem.string)
					self.currentState = self.State['Input']
					return
			

		if (self.currentState == self.State['Email']) or (current.isalpha() and not current.isupper()) or current == '@' or current == '.':
			self.currentState = self.State['Email']
			self.currentLexem.string += current
			if self.currentLexem.string == '@' or self.currentLexem.string == '.':
				self.DefineError(self.currentLexem.string)
				self.currentState = self.State['Input']
				return

			if len(self.currentLexem.string) > 1 and current == '@':
				return

			email = self.currentLexem.string.split('@')
			if len(email[0]) > 0 and len(email) == 2:
				email_second_part = email[1]
				if len(email_second_part) > 1 and current == '.':
					return
				if len(email_second_part) > 1:
					third_part = email_second_part.split('.')
					
					if len(third_part) == 2:	
						if len(third_part[1]) > 1:
						
							if not current.isalpha():
								if third_part[1].strip().isalpha():
									self.DefineLexem()
									return
								else:
									self.DefineError(self.currentLexem.string)
									self.currentState = self.State['Input']
									return
			if 	not current.isalpha() and len(email[0].strip()) > 0:
				self.DefineError(self.currentLexem.string)
				self.currentState = self.State['Input']
				return					
						
	

		if self.currentState == self.State['Start']:
			self.currentState = self.State['Input']


		if self.currentState == self.State['Input']:
			if current.isupper():
				self.currentLexem.row = self.currentRow
				self.currentLexem.column = self.currentColumn
				self.currentLexem.string += current
				self.currentState = self.State['Identifier']
				return
			if current.isdigit():
				self.currentLexem.row = self.currentRow
				self.currentLexem.column = self.currentColumn
				self.currentLexem.string += current
				self.currentState = self.State['Constant']
				return
			if current == '(':
				self.currentLexem.row = self.currentRow
				self.currentLexem.column = self.currentColumn
				self.currentLexem.string += current
				self.currentState = self.State['BeginComment']
				return
			for key,value in self.multiDelimiters.items():
				if current == key[0]:
					self.currentState = self.State['MultiDelimiter']
					self.currentLexem.string += current
					return
			if self.IsDelimiter(current):
				self.currentLexem.string += current
				self.currentState = self.State['Delimiter']
				self.DefineLexem()
				return
			if self.IsWhiteSpace(current):
				return
			self.DefineError(current)
			return

		if self.currentState == self.State['Identifier']:
			if current == '(':
				self.DefineLexem()
				self.currentLexem.row = self.currentRow
				self.currentLexem.column = self.currentColumn
				self.currentLexem.string += current
				self.currentState = self.State['BeginComment']
				return
			if current.isdigit() or current.isupper():
				self.currentLexem.string += current
				return
			if self.IsMultiDelimiter(current):
				self.DefineLexem()
				self.currentLexem.string += current
				self.currentState = self.State['MultiDelimiter']
				return
			if self.IsDelimiter(current):
				self.DefineLexem()
				self.currentLexem.string += current
				self.currentState = self.State['Delimiter']
				self.DefineLexem()
				return
			if self.IsWhiteSpace(current):
				self.DefineLexem()
				return

			self.DefineError(current)
			return
		if self.currentState == self.State['Constant']:
			if current =='(':
				self.DefineLexem()
				self.currentLexem.row = self.currentRow
				self.currentLexem.column = self.currentColumn
				self.currentLexem.string += current
				self.currentState = self.State['BeginComment']
				return
			if current.isdigit():
				self.currentLexem.string += current
				return
			if self.IsMultiDelimiter(current):
				self.DefineLexem()
				self.currentLexem.string += current
				self.currentState = self.State['MultiDelimiter']
				return
			if self.IsDelimiter(current):
				self.DefineLexem()
				self.currentLexem.string += current
				self.currentState = self.State['Delimiter']
				self.DefineLexem()
				return
			if self.IsWhiteSpace(current):
				self.DefineLexem()
				return

			self.DefineError(current)
			return

		if self.currentState == self.State['Delimiter']:
			if current =='(':
				self.DefineLexem()
				self.currentLexem.row = self.currentRow
				self.currentLexem.column = self.currentColumn
				self.currentLexem.string += current
				self.currentState = self.State['BeginComment']
				return
			else:
				self.currentLexem.string += current
				self.currentState = self.State['Delimiter']
				self.DefineLexem()
			return
		if self.currentState == self.State['MultiDelimiter']:
			if current =='(':
				self.DefineLexem()
				self.currentLexem.row = self.currentRow
				self.currentLexem.column = self.currentColumn
				self.currentLexem.string += current
				self.currentState = self.State['BeginComment']
				return
			if current.isupper():
				self.currentState = self.State['Delimiter']
				self.DefineLexem()
				self.currentLexem.string += current
				self.currentState = self.State['Identifier']
				return
			if current.isdigit():
				self.currentState = self.State['Delimiter']
				self.DefineLexem()
				self.currentLexem.string += current
				self.currentState = self.State['Constant']
				return
			for key,value in self.multiDelimiters.items():
				tmp = self.currentLexem.string + current
				if tmp == key:
					self.currentLexem.string = tmp
					self.DefineLexem()
					return
			if self.IsMultiDelimiter(current):
				self.currentState = self.State['Delimiter']
				if self.IsDelimiter(self.currentLexem.string):
					self.DefineLexem()
				else:
					self.DefineError(self.currentLexem.string)
				self.currentState = self.State['MultiDelimiter']
				self.currentLexem.string += current
				return
			if self.IsDelimiter(current):
				self.currentState = self.State['Delimiter']
				self.DefineLexem()
				self.currentState = self.State['Delimiter']
				self.currentLexem.string += current
				self.DefineLexem()
				return
			if self.IsWhiteSpace(current):
				self.currentState = self.State['Delimiter']
				self.DefineLexem()
				return
			self.DefineError(current)
			return

	def DefineError(self,current):
		error = 'Unresolved  symbol: {} \nline: {} column: {} \n'.format(current,self.currentRow, self.currentColumn)
		if self.currentState == self.State['Email'] or self.currentState == self.State['Phone']:
			self.currentLexem.string = ''	
		if self.currentState == self.State['Constant']:
			error += 'Constants should consist of numbers\n'	
		elif current == 'eof':
			error = 'Error. Unexpected end of file. Unclosed comment.'
		if self.currentState == self.State['Delimiter']:
			self.currentLexem.string = ''
		print Error(self.currentRow, self.currentColumn, error).message

	def DefineLexem(self):
		if self.currentState == self.State['Identifier']:
			if self.currentLexem.string in self.keywords:
				self.currentLexem.type = 'Keyword'
				self.currentLexem.code = self.keywords[self.currentLexem.string]
			elif self.currentLexem.string in self.identifiers:
				self.currentLexem.type = 'Identifier'
				self.currentLexem.code = self.identifiers[self.currentLexem.string]
			else:
				self.lastId +=1
				self.identifiers[self.currentLexem.string] = self.lastId
				self.currentLexem.type = 'Identifier'
				self.currentLexem.code = self.lastId
			self.OutputLexem()
			return
		if self.currentState == self.State['Constant']:
			if  not self.currentLexem.string in self.constants:
				self.lastConst += 1
				self.constants[self.currentLexem.string] = self.lastConst
			self.currentLexem.type = 'Constant'
			self.currentLexem.code = self.constants[self.currentLexem.string]
			self.OutputLexem()
			return
		if self.currentState == self.State['Email']:
			self.currentLexem.type = 'Email'
			self.currentLexem.code = 701
			self.currentLexem.column = int(self.currentColumn)-len(self.currentLexem.string)+1
			self.currentLexem.row = self.currentRow
			self.OutputLexem()
			return
		if self.currentState == self.State['Phone']:
			self.currentLexem.type = 'Phone'
			self.currentLexem.code = 702
			self.currentLexem.column = int(self.currentColumn)-len(self.currentLexem.string)+1
			self.currentLexem.row = self.currentRow
			self.OutputLexem()
			return	
		if self.currentState == self.State['Delimiter']:
			self.currentLexem.row = self.currentRow
			self.currentLexem.column = self.currentColumn
			self.currentLexem.code = self.delimiters[self.currentLexem.string]
			self.currentLexem.type = 'Delimiter'
			self.OutputLexem()
			return
		if self.currentState == self.State['MultiDelimiter']:
			if self.currentLexem.string in self.multiDelimiters.keys():
				self.currentLexem.type = 'MultiSymbolicDelimiter'
				self.currentLexem.code = self.multiDelimiters[self.currentLexem.string]
				self.currentLexem.row = self.currentRow
				self.currentLexem.column = self.currentColumn - len(self.currentLexem.string) + 1
				self.OutputLexem()
				return
			else:
				self.DefineError(self.currentLexem.string)
				return


	def OutputLexem(self):
		print( '{}  \t\t\t[{},{}] {} \t\t {}'.format(self.currentLexem.code,self.currentLexem.row,self.currentLexem.column,self.currentLexem.string,self.currentLexem.type))
		self.currentLexem = Lexem()
		self.currentState = self.State['Input']

	# def Display(self):
	# 	print ('Lexem string')
	# 	for index, l in enumerate(self.lexemList):
	# 		print( '{}  \t\t\t[{},{}] {} \t\t {}'.format(l.code,l.row,l.column,l.string,l.type))	
			
				
		


