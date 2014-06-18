"""subroutine"""

def main():
	@gpu
	float def mysub(x,y):
		float x
		float y
		return x-y

	#@gpu.returns.vec4
	@gpu.main
	def myfunc(a):
		float* a
		return mysub( 1.1 * a[_id_], 2.2 )


	A = [1.3 for i in range(64)]
	res = myfunc( A )
	print(res)