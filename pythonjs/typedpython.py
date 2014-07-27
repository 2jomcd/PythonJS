types = ['str', 'list', 'dict']

glsl_types = ['struct*', 'int*', 'float*', 'vec2', 'vec3', 'vec4', 'mat2', 'mat3', 'mat4']
glsl_xtypes = ['mat2x2', 'mat3x3', 'mat4x4']  ## others not supported in WebGLSL
glsl_types.extend( glsl_xtypes )
glsl_aliases = ['floatPOINTER', 'intPOINTER', 'structPOINTER']

types.extend( glsl_types )
types.extend( glsl_aliases )

native_number_types = ['int', 'float', 'double']  ## float and double are the same
simd_types = ['float32x4', 'int32x4']
vector_types = ['float32vec']
vector_types.extend( simd_types )
number_types = ['long']  ## requires https://github.com/dcodeIO/Long.js
number_types.extend( native_number_types )

types.extend( number_types)
types.extend( vector_types )


__whitespace = [' ', '\t']

def transform_source( source, strip=False ):
	output = []
	output_post = None

	for line in source.splitlines():
		a = []
		for i,char in enumerate(line):
			nextchar = None
			j = i+1
			while j < len(line):
				nextchar = line[j]
				if nextchar.strip(): break
				j += 1

			if a and char in __whitespace:
				b = ''.join(a)
				b = b.strip()
				if b in types and nextchar != '=':
					if strip:
						a = a[ : -len(b) ]
					else:
						if a[-1]=='*':
							a.pop()
							a.append('POINTER')
						a.append('=\t\t\t\t')
						#a.append( char )
				else:
					a.append( char )
			else:
				a.append( char )

		if not a:
			continue


		if a[-1]==';':
			a.pop()
		c = ''.join(a)
		cs = c.strip()

		if cs.startswith('//'):
			continue
		elif cs.startswith('inline(') or cs.startswith('JS('):
			output.append(c)
			continue


		if cs.startswith('var '):
			c = c.replace('var ', '')

		if '= function(' in c:
			k = '= function('
			a,b = c.split(k)
			output.append( '@expression(%s)' %a.strip())
			c = 'def __NAMELESS__(' + b

		if ' except ' in c:  ## PEP 463 - exception expressions
			s = c.split(' except ')
			if len(s) == 2 and '=' in s[0]:
				indent = []
				for char in s[0]:
					if char in __whitespace:
						indent.append( char )
					else:
						break
				indent = ''.join(indent)
				s0 = s[0].strip()
				output.append('%stry: %s' %(indent, s0) )
				exception, default = s[1].split(':')
				output.append('%sexcept %s: %s=%s' %(indent, exception, s0.split('=')[0], default) )
				c = ''

		if '=\t\t\t\tdef ' in c:
			x, c = c.split('=\t\t\t\tdef ')
			indent = []
			pre = []
			for char in x:
				if char in __whitespace:
					indent.append(char)
				else:
					pre.append( char )
			indent = ''.join(indent)
			pre = ''.join(pre)
			output.append( indent + '@returns(%s)' %pre)
			c = indent+'def '+c
		elif c.strip().startswith('def ') and '->' in c:  ## python3 syntax
			c, rtype = c.split('->')
			c += ':'
			rtype = rtype.strip()[:-1]
			indent = []
			for char in c:
				if char in __whitespace:
					indent.append(char)
				else:
					break
			indent = ''.join(indent)
			output.append( indent + '@returns(%s)' %rtype)
		elif c.startswith('import ') and '-' in c:
			c = c.replace('-', '__DASH__')
		elif ' new ' in c:
			c += ')' * c.count(' new ')
			c = c.replace(' new ', ' new(')

		## X.method.bind(X) shortcut `->`
		if '->' in c:
			a,b = c.split('->')
			this_name = a.split()[-1].split('=')[-1].split(':')[-1].split(',')[-1]
			method_name = b.split()[0].split('(')[0]
			c = c.replace('->'+method_name, '.'+method_name+'.bind(%s)'%this_name)

		## callback=def .. inline function ##
		if '=def ' in c or '= def ' in c or ': def ' in c or ':def ' in c:
			if '=def ' in  c:
				d = '=def '
			elif '= def ' in c:
				d = '= def '
			elif ': def ' in c:
				d = ': def '
			elif ':def ' in c:
				d = ':def '

			if 'def (' in c:
				c = c.replace('def (', 'def __NAMELESS__(')
			c, tail = c.split(d)

			#if d.startswith('='):
			#	if '(' in c:
			#		c += '=lambda __INLINE_FUNCTION__: %s )' %tail.strip().split(':')[0]
			#	else:
			#		c += '=lambda __INLINE_FUNCTION__: %s' %tail.strip().split(':')[0]
			#	output_post = 'def %s'%tail

			if d.startswith('='):
				c += '=lambda __INLINE_FUNCTION__: %s' %tail.strip().split(':')[0]

				if output_post:
					if output_post[-1][-1]==',':
						output_post[-1] = output_post[-1][:-1]
						output[-1] += ','
				else: output_post = list()

				output.append( c )

				c = 'def %s'%tail

			else:
				c += ':lambda __INLINE_FUNCTION__: %s,' %tail.strip().split(':')[0]
				output.append( c )
				if output_post:
					if output_post[-1][-1]==',':
						output_post[-1] = output_post[-1][:-1]
				else: output_post = list()
				c = 'def %s'%tail


		## jquery ##
		## TODO ensure this is not inside quoted text
		if '$(' in c:
			c = c.replace('$(', '__DOLLAR__(')
		if '$' in c and 'def ' in c:  ## $ as function parameter
			c = c.replace('$', '__DOLLAR__')
		if '$.' in c:
			c = c.replace('$.', '__DOLLAR__.')

		if c.strip().startswith('nonlocal '):  ## Python3 syntax
			c = c.replace('nonlocal ', 'global ')  ## fake nonlocal with global

		if type(output_post) is list:
			output_post.append( c )
		else:
			output.append( c )

		if type(output_post) is str:  ## DEPRECATED
			indent = 0
			for u in output[-1]:
				if u == ' ' or u == '\t':
					indent += 1
				else:
					break
			output.append( ('\t'*indent)+output_post)
			output_post = True
		elif output_post == True:  ## DEPRECATED
			if output[-1].strip()==')':
				output.pop()
				output_post = None

		elif type(output_post) is list:
			if output_post[-1].strip().endswith( ('}',')') ):
				output.append( output_post.pop() )
				indent = 0
				for u in output[-1]:
					if u == ' ' or u == '\t':
						indent += 1
					else:
						break
				for ln in output_post:
					output.append( ('\t'*indent)+ln )

				output_post = None

	r = '\n'.join(output)
	return r


test = '''
int a = 1
float b = 1.1
str c = "hi"
int d
int def xxx(): pass
if True:
	float* def Y():
		pass

A.callback = B->method
A.do_something( x,y,z, B->method )
A.do_something( x,y,z, callback=B->method )
A.do_something( x,y,z, callback=def cb(x):
	return x+y
)
A.do_something( x,y,z, callback=def (x,y,z):
	return x+y
)
a = {
	'cb1': def (x,y):
		return x+y
}
def xxx():
	b = {
		'cb1': def (x,y):
			return x+y,
		'cb2': def (x,y):
			return x+y
	}

X.func( cb1=def ():
		return 1,
	cb2=def ():
		return 2
)

c = function(x,y):
	return x+y
if True:
	d = a[ 'somekey' ] except KeyError: 'mydefault'

'''

if __name__ == '__main__':
	out = transform_source(test)
	print(out)
	import ast
	print( ast.parse(out) )