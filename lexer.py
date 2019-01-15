import ply.lex as lex

reserved = {
	'desire'	:	'IF',
	'love'		:	'ELIF1',
	'me'		:	'ELIF2',
	'stab'		:	'ELSE',
	'seppuku'	:	'ENDIF',

	'just'		:	'WHILE1',
	'monika'	:	'WHILE2',
	'delete'	:	'ENDWHILE',

	'sayonara'	:	'RETURN',

	'stop'		:	'BREAK1',
	'it'		:	'BREAK2',

	'keep'		:	'CONTINUE1',
	'writing'	:	'CONTINUE2',


	'write'		:	'PRINT',
	'writeln'	:	'PRINTLN',

	'poem'		:	'FUNC',
	'goodbye'	:	'ENDFUNC',

	'read'		:	'READ',
}


tokens = [ 'NAME', 'INT', 'FLOAT', 'PLUS', 'MINUS', 'TIMES', 
			'DIVIDE', 'MODULO', 'LPAREN', 'RPAREN', 'EQUALS', 
			'STRING', 'NEWLINE', 'LESSTHAN', 'GREATERTHAN', 'COMPARE',
			'LTEQUAL', 'GTEQUAL', 'NOTEQUAL', 'COMMA'] + list(reserved.values())


t_ignore = ' \t'

t_PLUS        = r'\+'
t_MINUS       = r'-'
t_TIMES       = r'\*'
t_DIVIDE      = r'/'
t_MODULO      = r'\%'
t_LPAREN      = r'\('
t_RPAREN      = r'\)'
t_EQUALS      = r'\='
t_COMPARE     = r'=='
t_LESSTHAN    = r'\<'
t_GREATERTHAN = r'\>'
t_LTEQUAL     = r'<='
t_GTEQUAL     = r'>='
t_NOTEQUAL    = r'!='
t_COMMA       = r'\,'

# change this
t_STRING = '("(?:[^"\\\\]|\\\\.)*"|'+"'(?:[^'\\\\]|\\\\.)*')"


def t_NEWLINE(t):
	r'\n'
	t.lexer.lineno += len(t.value)
	t.value = '\n'
	return t


def t_COMMENT(t):
	r'\#.*'
	pass


def t_FLOAT(t):
	r'((\d+\.\d+|\.\d+|\d+\.)([eE]-?\d+)?)|\d+[eE]-?\d+'
	t.value = float(t.value)
	return t

def t_INT(t):
	r'\d+'
	t.value = int(t.value)
	return t


def t_NAME(t):
	r'[a-zA-Z_][a-zA-Z_0-9]*'

	# Syntax: Dict.get(key, default=None)
	t.type = reserved.get(t.value, 'NAME')
	t.value = t.value if t.type == 'NAME' else t.type
	return t


def t_error(t):
	# No raise so we can keep debugging
	print("Illegal character '%s'" % t.value[0])
	t.lexer.skip(1)



lexer = lex.lex()

if __name__ == '__main__':
	lex.input(raw_input('lex > '))
	while True:
		tok = lex.token()
		if not tok: break
		print tok