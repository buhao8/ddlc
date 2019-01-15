from __future__ import print_function

operators = {
	'+': lambda a, b: a+b if (isinstance(a, (int, float, long)) and 
							isinstance(b, (int, float, long))) 
							else str(a)+str(b),
	'-': lambda a, b: a-b,
	'*': lambda a, b: a*b,
	'/': lambda a, b: a/b,
	'%': lambda a, b: a%b,
	'PRINT': print,
	'PRINTLN': print
}
