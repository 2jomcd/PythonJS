#!/usr/bin/env python
# PythonJS to JavaScript Translator
# by Amirouche Boubekki and Brett Hartshorn - copyright 2013
# License: "New BSD"


import os, sys
from types import GeneratorType

import ast
from ast import Str
from ast import Name
from ast import Tuple
from ast import parse
from ast import Attribute
from ast import NodeVisitor

#import inline_function
#import code_writer

class JSGenerator(NodeVisitor): #, inline_function.Inliner):
	def __init__(self, requirejs=True, insert_runtime=True, webworker=False, function_expressions=False):
		#writer = code_writer.Writer()
		#self.setup_inliner( writer )
		self._func_expressions = function_expressions
		self._indent = 0
		self._global_functions = {}
		self._function_stack = []
		self._requirejs = requirejs
		self._insert_runtime = insert_runtime
		self._webworker = webworker
		self._exports = set()

		self.special_decorators = set(['__typedef__', '__glsl__'])
		self._glsl = False
		self._has_glsl = False
		self._typed_vars = dict()

	def indent(self): return '  ' * self._indent
	def push(self): self._indent += 1
	def pull(self):
		if self._indent > 0: self._indent -= 1


	def visit_Assign(self, node):
		# XXX: I'm not sure why it is a list since, mutiple targets are inside a tuple
		target = node.targets[0]
		if isinstance(target, Tuple):
			raise NotImplementedError
		else:
			target = self.visit(target)
			value = self.visit(node.value)
			## visit_BinOp checks for `numpy.float32` and changes the operands from `a*a` to `a[id]*a[id]`
			if self._glsl and value.startswith('numpy.'):
				self._typed_vars[ target ] = value
				return ''
			else:
				code = '%s = %s;' % (target, value)
				if self._requirejs and target not in self._exports and self._indent == 0 and '.' not in target:
					self._exports.add( target )
				return code

	def visit_AugAssign(self, node):
		## n++ and n-- are slightly faster than n+=1 and n-=1
		target = self.visit(node.target)
		op = self.visit(node.op)
		value = self.visit(node.value)
		if op=='+' and isinstance(node.value, ast.Num) and node.value.n == 1:
			a = '%s ++;' %target
		if op=='-' and isinstance(node.value, ast.Num) and node.value.n == 1:
			a = '%s --;' %target
		else:
			a = '%s %s= %s;' %(target, op, value)
		return a

	def visit_Module(self, node):
		header = []
		lines = []

		if self._requirejs and not self._webworker:
			header.extend([
				'define( function(){',
				'__module__ = {}'
			])


		if self._insert_runtime:
			dirname = os.path.dirname(os.path.abspath(__file__))
			runtime = open( os.path.join(dirname, 'pythonjs.js') ).read()
			lines.append( runtime )  #.replace('\n', ';') )

		for b in node.body:
			line = self.visit(b)
			if line: lines.append( line )
			else:
				#raise b
				pass

		if self._requirejs and not self._webworker:
			for name in self._exports:
				if name.startswith('__'): continue
				lines.append( '__module__.%s = %s' %(name,name))

			lines.append( 'return __module__')
			lines.append('}) //end requirejs define')

		if self._has_glsl:
			header.append( 'var __shader_header__ = []' )
			header.append( 'var __shader__ = []' )

		lines = header + lines
		if False:
			for line in lines:
				assert isinstance(line, str)
			return '\n'.join(lines)
		else:
			## fixed by Foxboron
			return '\n'.join(l if isinstance(l,str) else l.encode("utf-8") for l in lines)

	def visit_Expr(self, node):
		# XXX: this is UGLY
		s = self.visit(node.value)
		if s.strip() and not s.endswith(';'):
			s += ';'
		return s


	def visit_In(self, node):
		return ' in '

	def visit_Tuple(self, node):
		return '[%s]' % ', '.join(map(self.visit, node.elts))

	def visit_List(self, node):
		return '[%s]' % ', '.join(map(self.visit, node.elts))

	def visit_TryExcept(self, node):
		out = []
		out.append( self.indent() + 'try {' )
		self.push()
		out.extend(
			list( map(self.visit, node.body) )
		)
		self.pull()
		out.append( self.indent() + '} catch(__exception__) {' )
		self.push()
		out.extend(
			list( map(self.visit, node.handlers) )
		)
		self.pull()
		out.append( '}' )
		return '\n'.join( out )

	def visit_Raise(self, node):
		return 'throw new %s;' % self.visit(node.type)

	def visit_Yield(self, node):
		return 'yield %s' % self.visit(node.value)

	def visit_ImportFrom(self, node):
		# print node.module
		# print node.names[0].name
		# print node.level
		return ''

	def visit_ExceptHandler(self, node):
		out = ''
		if node.type:
			out = 'if (__exception__ == %s || __exception__ instanceof %s) {\n' % (self.visit(node.type), self.visit(node.type))
		if node.name:
			out += 'var %s = __exception__;\n' % self.visit(node.name)
		out += '\n'.join(map(self.visit, node.body)) + '\n'
		if node.type:
			out += '}\n'
		return out

	def visit_Lambda(self, node):
		args = [self.visit(a) for a in node.args.args]
		return '(function (%s) {return %s;})' %(','.join(args), self.visit(node.body))



	def visit_FunctionDef(self, node):
		self._function_stack.append( node )
		node._local_vars = set()
		buffer = self._visit_function( node )

		if node == self._function_stack[0]:  ## could do something special here with global function
			#buffer += 'pythonjs.%s = %s' %(node.name, node.name)  ## this is no longer needed
			self._global_functions[ node.name ] = node

		self._function_stack.pop()
		return buffer

	def _visit_call_helper_var_glsl(self, node):
		lines = []
		for key in node.keywords:
			lines.append( '%s %s' %(key.value.id, key.arg))

		return ';'.join(lines)


	def _visit_function(self, node):
		is_main = node.name == 'main'
		return_type = None
		glsl = False
		glsl_wrapper_name = False
		gpu_return_types = {}
		gpu_vectorize = False
		args_typedefs = {}
		for decor in node.decorator_list:
			if isinstance(decor, ast.Name) and decor.id == '__glsl__':
				glsl = True
			elif isinstance(decor, ast.Attribute) and isinstance(decor.value, ast.Name) and decor.value.id == '__glsl__':
				glsl_wrapper_name = decor.attr
			elif isinstance(decor, ast.Call) and isinstance(decor.func, ast.Name) and decor.func.id == '__typedef__':
				for key in decor.keywords:
					args_typedefs[ key.arg ] = key.value.id
			elif isinstance(decor, ast.Call) and isinstance(decor.func, ast.Name) and decor.func.id == 'returns':
				if decor.keywords:
					for k in decor.keywords:
						key = k.arg
						assert key == 'array' or key == 'vec4'
						gpu_return_types[ key ] = self.visit(k.value)

				else:
					return_type = decor.args[0].id

			elif isinstance(decor, Attribute) and isinstance(decor.value, Name) and decor.value.id == 'gpu':
				if decor.attr == 'vectorize':
					gpu_vectorize = True
				elif decor.attr == 'main':
					is_main = True


		args = self.visit(node.args)

		if glsl:
			self._has_glsl = True  ## writes `__shader__ = []` in header
			lines = []
			x = []
			for i,arg in enumerate(args):
				if gpu_vectorize and arg not in args_typedefs:
					x.append( 'float* %s' %arg )
				else:
					if arg in args_typedefs:
						x.append( '%s %s' %(args_typedefs[arg].replace('POINTER', '*'), arg) )
					else:
						x.append( 'float* %s' %arg )

			if is_main:
				lines.append( '__shader__.push("void main( %s ) {");' %', '.join(x) )
			elif return_type:
				lines.append( '__shader_header__.push("%s %s( %s ) {");' %(return_type, node.name, ', '.join(x)) )
			else:
				lines.append( '__shader_header__.push("void %s( %s ) {");' %(node.name, ', '.join(x)) )

			self.push()
			# `_id_` always write out an array of floats or array of vec4floats
			if is_main:
				lines.append( '__shader__.push("vec2 _id_ = get_global_id();");')
			else:
				lines.append( '__shader_header__.push("vec2 _id_ = get_global_id();");')

			self._glsl = True
			for child in node.body:
				if isinstance(child, Str):
					continue
				else:
					for sub in self.visit(child).splitlines():
						if is_main:
							lines.append( '__shader__.push("%s");' %(self.indent()+sub) )
						else:
							lines.append( '__shader_header__.push("%s");' %(self.indent()+sub) )
			self._glsl = False
			#buffer += '\n'.join(body)
			self.pull()
			if is_main:
				lines.append('__shader__.push("%s}");' %self.indent())
			else:
				lines.append('__shader_header__.push("%s}");' %self.indent())

			lines.append(';')

			if is_main:
				if not glsl_wrapper_name:
					glsl_wrapper_name = node.name

				if args:
					lines.append('function %s( %s, __offset ) {' %(glsl_wrapper_name, ','.join(args)) )
				else:
					lines.append('function %s( __offset ) {' %glsl_wrapper_name )

				lines.append('	__offset =  __offset || 0')  ## note by default: 0 allows 0-1.0 ## TODO this needs to be set per-buffer

				lines.append('  var __webclgl = new WebCLGL()')
				lines.append('	var header = "\\n".join(__shader_header__)')
				lines.append('	var shader = "\\n".join(__shader__)')
				lines.append('  var __kernel = __webclgl.createKernel( shader, header );')

				if gpu_return_types:
					if 'array' in gpu_return_types:
						w,h = gpu_return_types['array'][1:-1].split(',')
					elif 'vec4' in gpu_return_types:
						w,h = gpu_return_types['vec4'][1:-1].split(',')
					else:
						raise NotImplementedError
					lines.append('  var __return_length = %s * %s' %(w,h))
				else:
					lines.append('  var __return_length = 64')  ## minimum size is 64

				for i,arg in enumerate(args):
					lines.append('  if (%s instanceof Array) {' %arg)
					#lines.append('    __return_length = %s.length==2 ? %s : %s.length' %(arg,arg, arg) )
					lines.append('    var %s_buffer = __webclgl.createBuffer(%s.length, "FLOAT", %s.scale || __offset)' %(arg,arg,arg))
					lines.append('    __webclgl.enqueueWriteBuffer(%s_buffer, %s)' %(arg, arg))
					lines.append('  __kernel.setKernelArg(%s, %s_buffer)' %(i, arg))
					lines.append('  } else { __kernel.setKernelArg(%s, %s) }' %(i, arg))

				#lines.append('	console.log("kernel.compile...")')
				lines.append('	__kernel.compile()')
				#lines.append('	console.log("kernel.compile OK")')

				if gpu_return_types:
					if 'array' in gpu_return_types:
						dim = gpu_return_types[ 'array' ]
						lines.append('	var rbuffer_array = __webclgl.createBuffer(%s, "FLOAT", __offset)' %dim)
						lines.append('	__webclgl.enqueueNDRangeKernel(__kernel, rbuffer_array)')
						lines.append('  var _raw_array_res = __webclgl.enqueueReadBuffer_Float( rbuffer_array )')
					else:
						dim = gpu_return_types[ 'vec4' ]
						lines.append('	var rbuffer_vec4 = __webclgl.createBuffer(%s, "FLOAT4", __offset)' %dim)
						lines.append('	__webclgl.enqueueNDRangeKernel(__kernel, rbuffer_vec4)')
						lines.append('  var _raw_vec4_res = __webclgl.enqueueReadBuffer_Float4( rbuffer_vec4 )')

					if 'array' in gpu_return_types and 'vec4' in gpu_return_types:
						adim = gpu_return_types['array']
						vdim = gpu_return_types['vec4']
						lines.append('	return [__unpack_array2d(_raw_array_res, %s),__unpack_vec4(_raw_vec4_res, %s)]' %(adim, vdim))
					elif 'vec4' in gpu_return_types:
						lines.append('	return __unpack_vec4(_raw_vec4_res, %s)' %gpu_return_types['vec4'])
					else:
						lines.append('	return __unpack_array2d(_raw_array_res, %s)' %gpu_return_types['array'])

				else:
					lines.append('  var __return = __webclgl.createBuffer(__return_length, "FLOAT", __offset)')
					lines.append('	__webclgl.enqueueNDRangeKernel(__kernel, __return)')
					lines.append('	return __webclgl.enqueueReadBuffer_Float( __return )')

				lines.append('} // end of wrapper')


			return '\n'.join(lines)

		elif len(node.decorator_list)==1 and not ( isinstance(node.decorator_list[0], ast.Call) and node.decorator_list[0].func.id not in self.special_decorators ):
			dec = self.visit(node.decorator_list[0])
			buffer = self.indent() + '%s.%s = function(%s) {\n' % (dec,node.name, ', '.join(args))

		elif len(self._function_stack) == 1:
			## this style will not make function global to the eval context in NodeJS ##
			#buffer = self.indent() + 'function %s(%s) {\n' % (node.name, ', '.join(args))
			## this is required for eval to be able to work in NodeJS, note there is no var keyword.

			if self._func_expressions:
				buffer = self.indent() + '%s = function(%s) {\n' % (node.name, ', '.join(args))
			else:
				buffer = self.indent() + 'function %s(%s) {\n' % (node.name, ', '.join(args))

			if self._requirejs and node.name not in self._exports:
				self._exports.add( node.name )

		else:

			if self._func_expressions:
				buffer = self.indent() + 'var %s = function(%s) {\n' % (node.name, ', '.join(args))
			else:
				buffer = self.indent() + 'function %s(%s) {\n' % (node.name, ', '.join(args))

		self.push()
		body = list()
		for child in node.body:
			if isinstance(child, Str):
				continue

			if isinstance(child, GeneratorType):  ## not tested
				for sub in child:
					body.append( self.indent()+self.visit(sub))
			else:
				body.append( self.indent()+self.visit(child))

		buffer += '\n'.join(body)
		self.pull()
		buffer += '\n%s}\n' %self.indent()
		return buffer

	def _visit_subscript_ellipsis(self, node):
		name = self.visit(node.value)
		return '%s["$wrapped"]' %name


	def visit_Subscript(self, node):
		if isinstance(node.slice, ast.Ellipsis):
			return self._visit_subscript_ellipsis( node )
		else:
			return '%s[%s]' % (self.visit(node.value), self.visit(node.slice))

	def visit_Index(self, node):
		return self.visit(node.value)

	def visit_Slice(self, node):
		#print(node.lower)
		#print(node.upper)
		#print(node.step)
		raise SyntaxError(node)  ## slicing not allowed here at js level

	def visit_arguments(self, node):
		out = []
		for name in [self.visit(arg) for arg in node.args]:
			out.append(name)
		return out

	def visit_Name(self, node):
		if node.id == 'None':
			return 'null'
		elif node.id == 'True':
			return 'true'
		elif node.id == 'False':
			return 'false'
		elif node.id == 'null':
			return 'null'
		return node.id

	def visit_Attribute(self, node):
		name = self.visit(node.value)
		attr = node.attr
		return '%s.%s' % (name, attr)

	def visit_Print(self, node):
		args = [self.visit(e) for e in node.values]
		s = 'console.log(%s);' % ', '.join(args)
		return s

	def visit_keyword(self, node):
		if isinstance(node.arg, basestring):
			return node.arg, self.visit(node.value)
		return self.visit(node.arg), self.visit(node.value)

	def _visit_call_helper_instanceof(self, node):
		args = map(self.visit, node.args)
		if len(args) == 2:
			return '%s instanceof %s' %tuple(args)
		else:
			raise SyntaxError( args )

	def _visit_call_helper_new(self, node):
		args = map(self.visit, node.args)
		if len(args) == 1:
			return ' new %s' %args[0]
		else:
			raise SyntaxError( args )

	def visit_Call(self, node):
		name = self.visit(node.func)
		if name == 'instanceof':  ## this gets used by "with javascript:" blocks to test if an instance is a JavaScript type
			return self._visit_call_helper_instanceof( node )

		elif name == 'new':
			return self._visit_call_helper_new( node )

		elif name == '__ternary_operator__':
			args = map(self.visit, node.args)
			if len(args) == 2:
				return '((%s) ? %s : %s)' %(args[0], args[0], args[1])
			elif len(args) == 3:
				return '((%s) ? %s : %s)' %(args[0], args[1], args[2])
			else:
				raise SyntaxError( args )

		elif name == 'numpy.array':
			return self._visit_call_helper_numpy_array(node)

		elif name == 'JSObject':
			return self._visit_call_helper_JSObject( node )

		elif name == 'var':
			if self._glsl:
				return self._visit_call_helper_var_glsl( node )
			else:
				return self._visit_call_helper_var( node )

		elif name == 'JSArray':
			return self._visit_call_helper_JSArray( node )

		elif name == 'inline' or name == 'JS':
			assert len(node.args)==1 and isinstance(node.args[0], ast.Str)
			return self._inline_code_helper( node.args[0].s )

		elif name == 'dart_import':
			if len(node.args) == 1:
				return 'import "%s";' %node.args[0].s
			elif len(node.args) == 2:
				return 'import "%s" as %s;' %(node.args[0].s, node.args[1].s)
			else:
				raise SyntaxError
		elif name == 'list':
			return self._visit_call_helper_list( node )

		elif name == '__get__' and len(node.args)==2 and isinstance(node.args[1], ast.Str) and node.args[1].s=='__call__':
			return self._visit_call_helper_get_call_special( node )

		#elif name in self._global_functions:
		#	return_id = self.inline_function( node )
		#	code = self.writer.getvalue()
		#	return '\n'.join([code, return_id])

		else:
			return self._visit_call_helper(node)

	def _visit_call_helper(self, node):
		if node.args:
			args = [self.visit(e) for e in node.args]
			args = ', '.join([e for e in args if e])
		else:
			args = ''
		return '%s(%s)' % (self.visit(node.func), args)

	def inline_helper_remap_names(self, remap):
		return "var %s;" %','.join(remap.values())

	def inline_helper_return_id(self, return_id):
		return "var __returns__%s = null;"%return_id

	def _visit_call_helper_numpy_array(self, node):
		if self._glsl:
			return self.visit(node.keywords[0].value)
		else:
			return self.visit(node.args[0])

	def _visit_call_helper_list(self, node):
		name = self.visit(node.func)
		if node.args:
			args = [self.visit(e) for e in node.args]
			args = ', '.join([e for e in args if e])
		else:
			args = ''
		return '%s(%s)' % (name, args)

	def _visit_call_helper_get_call_special(self, node):
		name = self.visit(node.func)
		if node.args:
			args = [self.visit(e) for e in node.args]
			args = ', '.join([e for e in args if e])
		else:
			args = ''
		return '%s(%s)' % (name, args)


	def _visit_call_helper_JSArray(self, node):
		if node.args:
			args = map(self.visit, node.args)
			out = ', '.join(args)
			#return '__create_array__(%s)' % out
			return '[%s]' % out

		else:
			return '[]'


	def _visit_call_helper_JSObject(self, node):
		if node.keywords:
			kwargs = map(self.visit, node.keywords)
			f = lambda x: '"%s": %s' % (x[0], x[1])
			out = ', '.join(map(f, kwargs))
			return '{%s}' % out
		else:
			return '{}'

	def _visit_call_helper_var(self, node):
		args = [ self.visit(a) for a in node.args ]
		if self._function_stack:
			fnode = self._function_stack[-1]
			rem = []
			for arg in args:
				if arg in fnode._local_vars:
					rem.append( arg )
				else:
					fnode._local_vars.add( arg )
			for arg in rem:
				args.remove( arg )

		out = []

		if args:
			out.append( 'var ' + ','.join(args) )
		if node.keywords:
			out.append( 'var ' + ','.join([key.arg for key in node.keywords]) )

		return ';'.join(out)

	def _inline_code_helper(self, s):
		s = s.replace('\n', '\\n').replace('\0', '\\0')  ## AttributeError: 'BinOp' object has no attribute 's' - this is caused by bad quotes
		if s.strip().startswith('#'): s = '/*%s*/'%s
		if '"' in s or "'" in s:  ## can not trust direct-replace hacks
			pass
		else:
			if ' or ' in s:
				s = s.replace(' or ', ' || ')
			if ' not ' in s:
				s = s.replace(' not ', ' ! ')
			if ' and ' in s:
				s = s.replace(' and ', ' && ')
		return s

	def visit_While(self, node):
		body = [ 'while (%s) {' %self.visit(node.test)]
		self.push()
		for line in list( map(self.visit, node.body) ):
			body.append( self.indent()+line )
		self.pull()
		body.append( self.indent() + '}' )
		return '\n'.join( body )

	def visit_Str(self, node):
		s = node.s.replace("\\", "\\\\").replace('\n', '\\n').replace('\r', '\\r').replace('"', '\\"')
		#if '"' in s:
		#	return "'%s'" % s
		return '"%s"' % s

	def visit_BinOp(self, node):
		left = self.visit(node.left)
		op = self.visit(node.op)
		right = self.visit(node.right)

		if left in self._typed_vars and self._typed_vars[left] == 'numpy.float32':
			left += '[_id_]'
		if right in self._typed_vars and self._typed_vars[right] == 'numpy.float32':
			right += '[_id_]'

		return '(%s %s %s)' % (left, op, right)

	def visit_Mult(self, node):
		return '*'

	def visit_Add(self, node):
		return '+'

	def visit_Sub(self, node):
		return '-'

	def visit_Div(self, node):
		return '/'

	def visit_Mod(self, node):
		return '%'

	def visit_Lt(self, node):
		return '<'

	def visit_Gt(self, node):
		return '>'

	def visit_GtE(self, node):
		return '>='

	def visit_LtE(self, node):
		return '<='

	def visit_LShift(self, node):
		return '<<'
	def visit_RShift(self, node):
		return '>>'
	def visit_BitXor(self, node):
		return '^'
	def visit_BitOr(self, node):
		return '|'
	def visit_BitAnd(self, node):
		return '&'

	def visit_Return(self, node):
		if isinstance(node.value, Tuple):
			return 'return [%s];' % ', '.join(map(self.visit, node.value.elts))
		if node.value:
			return 'return %s;' % self.visit(node.value)
		return 'return undefined;'

	def visit_Pass(self, node):
		return '/*pass*/'

	def visit_Eq(self, node):
		return '=='

	def visit_NotEq(self, node):
		return '!='

	def visit_Num(self, node):
		return str(node.n)

	def visit_Is(self, node):
		return '==='

	def visit_Compare(self, node):
		comp = [ '(']
		comp.append( self.visit(node.left) )
		comp.append( ')' )

		for i in range( len(node.ops) ):
			comp.append( self.visit(node.ops[i]) )

			if isinstance(node.comparators[i], ast.BinOp):
				comp.append('(')
				comp.append( self.visit(node.comparators[i]) )
				comp.append(')')
			else:
				comp.append( self.visit(node.comparators[i]) )

		return ' '.join( comp )

	def visit_Not(self, node):
		return '!'

	def visit_IsNot(self, node):
		return '!=='

	def visit_UnaryOp(self, node):
		#return self.visit(node.op) + self.visit(node.operand)
		return '%s (%s)' %(self.visit(node.op),self.visit(node.operand))

	def visit_USub(self, node):
		return '-'
		
	def visit_And(self, node):
		return ' && '

	def visit_Or(self, node):
		return ' || '

	def visit_BoolOp(self, node):
		op = self.visit(node.op)
		return op.join( [self.visit(v) for v in node.values] )

	def visit_If(self, node):
		out = []
		out.append( 'if (%s) {' %self.visit(node.test) )
		self.push()

		for line in list(map(self.visit, node.body)):
			if line is None: continue
			out.append( self.indent() + line )

		orelse = []
		for line in list(map(self.visit, node.orelse)):
			orelse.append( self.indent() + line )

		self.pull()

		if orelse:
			out.append( self.indent() + '} else {')
			out.extend( orelse )
		out.append( self.indent() + '}' )

		return '\n'.join( out )


	def visit_Dict(self, node):
		a = []
		for i in range( len(node.keys) ):
			k = self.visit( node.keys[ i ] )
			v = self.visit( node.values[i] )
			a.append( '%s:%s'%(k,v) )
		b = ','.join( a )
		return '{ %s }' %b


	def _visit_for_prep_iter_helper(self, node, out, iter_name):
		## support "for key in JSObject" ##
		#out.append( self.indent() + 'if (! (iter instanceof Array) ) { iter = Object.keys(iter) }' )
		## new style - Object.keys only works for normal JS-objects, not ones created with `Object.create(null)`
		out.append(
			self.indent() + 'if (! (%s instanceof Array || typeof %s == "string" || __is_typed_array(%s)) ) { %s = __object_keys__(%s) }' %(iter_name, iter_name, iter_name, iter_name, iter_name)
		)


	_iter_id = 0
	def visit_For(self, node):
		'''
		for loops inside a `with javascript:` block will produce this faster for loop.

		note that the rules are python-style, even though we are inside a `with javascript:` block:
			. an Array is like a list, `for x in Array` gives you the value (not the index as you would get in pure javascript)
			. an Object is like a dict, `for v in Object` gives you the key (not the value as you would get in pure javascript)

		if your are trying to opitmize looping over a PythonJS list, you can do this:
			for v in mylist[...]:
				print v
		above works because [...] returns the internal Array of mylist

		'''
		if self._glsl:
			target = self.visit(node.target)
			iter = self.visit(node.iter.args[0])
			lines = ['for (int %s=0; %s < %s; %s++) {' %(target, target, iter, target)]
			for b in node.body:
				lines.append( self.visit(b) )
			lines.append( '}' )
			return '\n'.join(lines)


		self._iter_id += 1
		iname = '__iter%s' %self._iter_id
		index = '__idx%s' %self._iter_id

		target = node.target.id
		iter = self.visit(node.iter) # iter is the python iterator

		out = []
		out.append( self.indent() + 'var %s = %s;' % (iname, iter) )
		#out.append( self.indent() + 'var %s = 0;' % index )

		self._visit_for_prep_iter_helper(node, out, iname)

		out.append( self.indent() + 'for (var %s=0; %s < %s.length; %s++) {' % (index, index, iname, index) )
		self.push()

		body = []
		# backup iterator and affect value of the next element to the target
		#pre = 'var backup = %s; %s = iter[%s];' % (target, target, target)
		body.append( self.indent() + 'var %s = %s[ %s ];' %(target, iname, index) )

		for line in list(map(self.visit, node.body)):
			body.append( self.indent() + line )

		# replace the replace target with the javascript iterator
		#post = '%s = backup;' % target
		#body.append( self.indent() + post )

		self.pull()
		out.extend( body )
		out.append( self.indent() + '}' )

		return '\n'.join( out )

	def visit_Continue(self, node):
		return 'continue'

	def visit_Break(self, node):
		return 'break;'



def generate_runtime():
	from python_to_pythonjs import main as py2pyjs
	lines = [
		main( open('runtime/pythonpythonjs.py', 'rb').read(), requirejs=False, insert_runtime=False, function_expressions=True ), ## lowlevel pythonjs
		main( py2pyjs(open('runtime/builtins.py', 'rb').read()), requirejs=False, insert_runtime=False, function_expressions=True )
	]
	return '\n'.join( lines )

def main(script, requirejs=True, insert_runtime=True, webworker=False, function_expressions=False):
	tree = ast.parse( script )
	return JSGenerator( requirejs=requirejs, insert_runtime=insert_runtime, webworker=webworker, function_expressions=function_expressions ).visit(tree)


def command():
	scripts = []
	if len(sys.argv) > 1:
		for arg in sys.argv[1:]:
			if arg.endswith('.py'):
				scripts.append( arg )

	if len(scripts):
		a = []
		for script in scripts:
			a.append( open(script, 'rb').read() )
		data = '\n'.join( a )
	else:
		data = sys.stdin.read()

	js = main( data )
	print( js )


if __name__ == '__main__':
	if '--runtime' in sys.argv:
		print('creating new runtime: pythonjs.js')
		open('pythonjs.js', 'wb').write( generate_runtime() )
	else:
		command()
