"""list slice set"""


def main():
	a = list(range(10))
	a[ 2:4 ] = 'XXXY'

	TestError( a[0]==0 )
	TestError( a[1]==1 )

	TestError( a[2]=='X' )
	TestError( a[3]=='X' )
	TestError( a[4]=='X' )
	TestError( a[5]=='Y' )

	TestError( a[6]==4 )
	TestError( a[7]==5 )
	TestError( a[8]==6 )
	TestError( a[9]==7 )
	TestError( a[10]==8 )
	TestError( a[11]==9 )

	b = list(range(3))
	c = b [ :2 ]
	TestError( c[0]==0 )
	TestError( c[1]==1 )

	b[ :2 ] = 'ABC'
	TestError( len(b)==4 )
	TestError( b[0]=='A' )