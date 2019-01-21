import ply.yacc as yacc
import lexer
import argparse
from nodes import *
import nodes
from funcs import *
import sys

tokens = lexer.tokens

precedence = (
	('nonassoc', 'LESSTHAN', 'GREATERTHAN', 'COMPARE',
		'LTEQUAL', 'GTEQUAL', 'NOTEQUAL'),
	('left', 'PLUS', 'MINUS'),
	('left', 'TIMES', 'DIVIDE', 'MODULO'),
	('right', 'UMINUS'),
	('left', 'LPAREN'),
)

### blocks and statements ###
def p_block(p):
	'''block : block statement
			| statement'''
	if len(p)==3:
		p[1].append_child(p[2])
		p[0] = p[1]
	else:
		p[0] = Block(p[1])

def p_statement(p):
	'''statement : assign newline
			| expr newline
			| print newline
			| read newline
			| if newline
			| continue newline
			| break newline
			| while newline
			| return newline
			| funcdef newline'''
	p[0] = p[1]

### if - elif - else ###
def p_if_chain(p):
	'''if_chain : if_chain ELIF1 ELIF2 expr newline block
			| IF expr newline block'''
	if len(p)==5:
		p[0] = If_Chain((p[2], p[4]))

	else:
		p[1].append_child((p[4], p[6]))
		p[0] = p[1]

def p_else(p):
	'''else : ELSE newline block ENDIF'''
	p[0] = (Literal(True), p[3])

def p_if(p):
	'''if : if_chain ENDIF
		| if_chain else'''
	if p[2]!='ENDIF':
		p[1].append_child(p[2])
	p[0] = p[1]

### while and loop controls ###
def p_while(p):
	'''while : WHILE1 WHILE2 expr newline block ENDWHILE'''
	p[0] = While(p[3], p[5])

def p_return(p):
	'''return : RETURN expr'''
	p[0] = Return(p[2])

def p_break(p):
	'''break : BREAK1 BREAK2'''
	p[0] = Literal(BREAK)

def p_continue(p):
	'''continue : CONTINUE1 CONTINUE2'''
	p[0] = Literal(CONTINUE)

### assignments and IO ###
def p_assign(p):
	'''assign : NAME EQUALS expr'''
	p[0] = Assign(p[1], p[3])

def p_print(p):
	'''print : PRINT expr
		| PRINTLN expr'''
	if p[1] == 'PRINT':
		p[0] = Unary(operators[p[1]], p[2], "")
	else:
		p[0] = Unary(operators[p[1]], p[2])

def p_read(p):
	'''read : READ NAME'''
	x = Unary(operators[p[1]])
	p[0] = Assign(p[2], x)

### numbers and data ###
def p_expr_uminus(p):
	'''expr : MINUS expr %prec UMINUS'''
	p[0] = -p[2].eval()
	p[0] = Literal(p[0])

def p_binary_expression(p):
	'''expr : expr PLUS expr
		| expr MINUS expr
		| expr TIMES expr
		| expr DIVIDE expr
		| expr MODULO expr'''
	p[0] = Binary(operators[p[2]], p[1], p[3])

def p_parens(p):
	'''expr : LPAREN expr RPAREN'''
	p[0] = p[2]

def p_name(p):
	'''expr : NAME'''
	p[0] = Symbol_Lookup(p[1])

def p_compare(p):
	'''expr : expr COMPARE expr
		| expr LESSTHAN expr
		| expr GREATERTHAN expr
		| expr LTEQUAL expr
		| expr GTEQUAL expr
		| expr NOTEQUAL expr'''
	p[0] = Compare(p[1], p[3], p[2])

def p_factor(p):
	'''expr : INT
		| FLOAT
		| STRING'''
	p[0] = Literal(p[1][1:-1]if isinstance(p[1], str) else p[1])

### functions ###
def p_val_seq(p):
	'''valseq : valseq COMMA expr
		| expr'''
	if len(p)==2:
		p[0] = p[1],
	else:
		p[1] += p[3],
		p[0] = p[1]

def p_name_seq(p):
	'''nameseq : nameseq COMMA NAME
		| NAME'''
	if len(p)==2:
		p[0] = p[1],
	else:
		p[1] += p[3],
		p[0] = p[1]

def p_funcdef(p):
	'''funcdef : FUNC NAME LPAREN nameseq RPAREN newline block ENDFUNC'''
	p[0] = Funcdef(p[2], p[4], p[7])

def p_call(p):
	'''expr : expr LPAREN valseq RPAREN'''
	p[0] = Call(p[1], p[3])


def p_newline(p):
	'''newline : NEWLINE
		| newline NEWLINE'''
	pass

def p_error(p):
	# no raise to aid in debugging
	print p
	print SyntaxError("Invalid Syntax")

def run(code):
	parser = yacc.yacc()

	t = parser.parse(code)

	sys.setrecursionlimit(30000)

	return t.eval()


if __name__=='__main__':
	argparser = argparse.ArgumentParser(description = 'parser.py')

	argparser.add_argument('--file', '-f', type=argparse.FileType('r'), help='input file with code to run.')
	argparser.add_argument('--version', '-v', action='version', version='%(prog)s 0.9')
	argparser.add_argument('--interactive', '-i', action="store_true", help='run in interactive mode (default)')

	args = argparser.parse_args()

	nodes.env = {}

	if args.file==None or args.interactive:
		while True:
			try:
				s = raw_input('ddlc > ')
			except EOFError:
				break
			if not s:
				continue
			try:
				if not s.startswith("#"):
					result = run(s + '\n')
					if result != None:
						print result
			except Exception as e:
				print 'Error: %s not defined' % e
				pass
	else:
		result = run(args.file.read().strip() + '\n')
		if result != None:
			print result