"""inline def"""

def test( callback=None ):
	return callback

def main():
	f = test( callback=def cb(x,y):
		return x+y
	)
	TestError( f(1,2) == 3 )

