CONTINUE = object()
BREAK = object()
RETURN = type('Return Value', (), {})

class Node(object):
	def __init__(self, *children):
		self.children = tuple(children)

	def eval(self):
		pass
	
	def append_child(self, child):
		self.children = self.children + (child,)

class Unary(Node):
	def eval(self):
		### print with no '\n'
		if callable(self.children[0]): 
			if self.children[0].__name__=='print' and len(self.children)==3:
				return self.children[0](self.children[1].eval(), end='')
			elif self.children[0].__name__=='raw_input':
				return raw_input()	

		return self.children[0](self.children[1].eval())

class Binary(Node):
	def eval(self):
		return self.children[0](self.children[1].eval(), self.children[2].eval())

class Block(Node):
	def eval(self):
		for child in self.children:
			val = child.eval()
			if val==CONTINUE or val==BREAK or isinstance(val, RETURN):
				return val

class Literal(Node):
	def eval(self):
		return self.children[0]

class Symbol_Lookup(Node):
	def eval(self):
		return env[self.children[0]]

class Assign(Node):
	def eval(self):
		env[self.children[0]]=self.children[1].eval()

class Setitem(Node):
	def eval(self):
		self.children[0].eval()[self.children[1].eval()]=self.children[2].eval()

class While(Node):
	def eval(self):
		while self.children[0].eval():
			val = self.children[1].eval()
			if val==BREAK:
				break
			if isinstance(val, RETURN):
				return val

class If_Chain(Node):
	def eval(self):
		for clause in self.children:
			if clause[0].eval():
				return clause[1].eval()

class Compare(Node):
	def eval(self):
		if self.children[2]=='==':
			return self.children[0].eval()==self.children[1].eval()
		elif self.children[2]=='>':
			return self.children[0].eval()>self.children[1].eval()
		elif self.children[2]=='<':
			return self.children[0].eval()<self.children[1].eval()
		elif self.children[2]=='>=':
			return self.children[0].eval()>=self.children[1].eval()
		elif self.children[2]=='<=':
			return self.children[0].eval()<=self.children[1].eval()
		elif self.children[2]=='!=':
			return self.children[0].eval()!=self.children[1].eval()

class Funcdef(Node):
	def eval(self):
		def defined_func(vals):
			global env

			old_env = env.copy()
			env.update(dict(zip(self.children[1], vals)))

			v = self.children[2].eval()

			env = old_env

			if isinstance(v, RETURN):
				return v.value

		env[self.children[0]]=defined_func

class Call(Node):
	def eval(self):
		return self.children[0].eval()([i.eval() for i in self.children[1]])

class Return(Node):
	def eval(self):
		v = RETURN()
		v.value = self.children[0].eval()
		return v