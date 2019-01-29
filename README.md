# ddlc
ddlc programming language interpreter

Note: The (default) interactive mode is not fully functional due to recently changed language features (specifically statement demarcation).

See `examples/` for example scripts.

# Purpose
The purpose of this language is to have a ddlc-themed programming language that tries to keep true to the various themes found in ddlc.  The choice of Python as the host language was chosen primarily due to previous projects using PLY (Python-Lex-Yacc).  It is important to note that the language is not meant to be fast nor efficient.

# Comments
Comments are denoted by # like in Python, or quoted text. For example,

```
# This is a comment
"This is also a comment
that spans many lines"
```

# Assignments and Comparisons
Your standard assignment syntax and comparison operators used.  Namely,

`= == != > < >= <=`

# If - Elif - Else
I tried my best (with some help) to come up with good keywords here.

```
if    = desire
elif  = love me
else  = stab
endif = seppuku
```

There is no THEN keyword or a colon like in Python.

Example:

```
x = 3
y = 2
desire x == y + 1
    writeln "hooray"
love me x == y
    writeln "ok"
stab
    writeln "bad"
seppuku
```

# While Loops
These are just like if-statements in their format.

```
while    = just monika
break    = stop it
continue = keep writing
```

Example:

```
# prints numbers [10, 5] except 8 and 7
x = 10
just monika x >= 0
	desire x < 5
		stop it
	love me x == 8
		x = x - 2
		keep writing
	stab
	    writeln x
	    x = x - 1
	seppuku
delete
```

There is a consideration to make "just monika" indicate an infinite loop.

# Functions
All function are poems, so the return type is always a poem.

The keyword

`sayonara`

indicates a return statement.

Example of the Ackermann function in ddlc:

```
poem ack(x, y)
    desire x == 0
        sayonara y + 1
    love me y == 0
        sayonara ack(x-1, 1)
    stab
        sayonara ack(x-1, ack(x, y-1))
    seppuku
goodbye
```

It can be called thusly:

`ack(4, 0)`

They can also be assigned to a variable or directly printed.

# IO
Input is done with the following:

`read var`

It literally reads a value from the console and stores it in var.

Output is done with the following:

```
write   - print without '\n'
writeln - print with '\n'
```

You can combine Strings, ints, and floats like normal.

# Running
You need python2 and the ply module.

```
$ python -m pip install ply
$ python parser.py -h
```

# Todo
- Fix interactive mode
- ~~Add user input support~~
- Better error reporting
- Varargs and kwargs
- Arrays
- Include directive
- Library functions
- ~~Modulo support~~
