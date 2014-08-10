#!/usr/bin/env python
# PythonJS to Go Translator
# by Brett Hartshorn - copyright 2014
# License: "New BSD"
import os, sys
import ast
import pythonjs



class GoGenerator( pythonjs.JSGenerator ):

	def __init__(self, requirejs=False, insert_runtime=False):
		pythonjs.JSGenerator.__init__(self, requirejs=False, insert_runtime=False)
		#self._classes = dict()
		#self._class_props = dict()
		self._vars = set()
		self._kwargs_type_ = dict()

	def visit_Print(self, node):
		r = [ 'fmt.Println(%s);' %self.visit(e) for e in node.values]
		return ''.join(r)

	def visit_Expr(self, node):
		return self.visit(node.value)

	def visit_Import(self, node):
		r = [alias.name for alias in node.names]
		if r:
			return 'import "%s"' %';'.join(r)
		else:
			return ''

	def visit_Module(self, node):
		header = [
			'package main',
			'import "fmt"'
		]
		lines = []

		for b in node.body:
			line = self.visit(b)

			if line:
				for sub in line.splitlines():
					if sub==';':
						raise SyntaxError(line)
					else:
						lines.append( sub )
			else:
				raise SyntaxError(line)

		lines.append('type _kwargs_type_ struct {')
		for name in self._kwargs_type_:
			type = self._kwargs_type_[name]
			lines.append( '  %s %s' %(name,type))
		lines.append('}')

		lines = header + lines
		return '\n'.join( lines )


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

	def visit_For(self, node):
		target = self.visit(node.target)
		lines = []
		if isinstance(node.iter, ast.Call) and isinstance(node.iter.func, ast.Name):
			iter = self.visit(node.iter.args[0])

			if node.iter.func.id == 'range':
				lines.append('for %s := 0; %s < %s; %s++ {' %(target, target, iter, target))
			elif node.iter.func.id == 'enumerate':
				idx = self.visit(node.target.elts[0])
				tar = self.visit(node.target.elts[1])
				lines.append('for %s,%s := range %s {' %(idx,tar, iter))

			else:
				raise SyntaxError('invalid for loop - bad iterator')

		elif isinstance(node.target, ast.List) or isinstance(node.target, ast.Tuple):
			iter = self.visit( node.iter )
			key = self.visit(node.target.elts[0])
			val = self.visit(node.target.elts[1])
			lines.append('for %s,%s := range %s {' %(key,val, iter))

		else:
			iter = self.visit( node.iter )
			lines.append('for _,%s := range %s {' %(target, iter))

		self.push()
		for b in node.body:
			lines.append( self.indent()+self.visit(b) )
		self.pull()
		lines.append( self.indent()+'}' )  ## end of for loop
		return '\n'.join(lines)


	def _visit_call_helper(self, node):
		if node.args:
			args = [self.visit(e) for e in node.args]
			args = ', '.join([e for e in args if e])
		else:
			args = ''
		fname = self.visit(node.func)
		if fname=='__DOLLAR__': fname = '$'

		if node.keywords:
			if args: args += ','
			args += '_kwargs_type_{'
			args += ','.join( ['%s:%s' %(kw.arg,self.visit(kw.value)) for kw in node.keywords] )
			args += '}'

		return '%s(%s)' % (fname, args)

	def _visit_call_helper_go(self, node):
		name = self.visit(node.func)
		if name == '__go__':
			return 'go %s' %self.visit(node.args[0])
		elif name == '__gomake__':
			return 'make(%s)' %self.visit(node.args[0])
		else:
			return SyntaxError('invalid special go call')

	def _visit_function(self, node):
		if self._function_stack[0] is node:
			self._vars = set()

		args_typedefs = {}
		return_type = None
		for decor in node.decorator_list:
			if isinstance(decor, ast.Call) and isinstance(decor.func, ast.Name) and decor.func.id == '__typedef__':
				for key in decor.keywords:
					args_typedefs[ key.arg ] = key.value.id
			elif isinstance(decor, ast.Call) and isinstance(decor.func, ast.Name) and decor.func.id == 'returns':
				if decor.keywords:
					raise SyntaxError('invalid go return type')
				else:
					return_type = decor.args[0].id


		#args = self.visit(node.args)
		args = []
		oargs = []
		offset = len(node.args.args) - len(node.args.defaults)
		varargs = False
		varargs_name = None
		for i, arg in enumerate(node.args.args):
			arg_name = arg.id
			if arg_name not in args_typedefs:
				err = 'error in function: %s' %node.name
				err += '\n  missing typedef: %s' %arg.id
				raise SyntaxError(err)

			arg_type = args_typedefs[arg_name]
			a = '%s %s' %(arg_name, arg_type)
			dindex = i - offset

			if a.startswith('__variable_args__'): ## TODO support go `...` varargs
				#varargs_name = a.split('__')[-1]
				#varargs = ['_vararg_%s'%n for n in range(16) ]
				#args.append( '[%s]'%','.join(varargs) )
				raise SyntaxError('TODO *args')

			elif dindex >= 0 and node.args.defaults:
				default_value = self.visit( node.args.defaults[dindex] )
				self._kwargs_type_[ arg_name ] = arg_type
				oargs.append( (arg_name, default_value) )
			else:
				args.append( a )

		if oargs:
			#args.append( '[%s]' % ','.join(oargs) )
			#args.append( '{%s}' % ','.join(oargs) )
			args.append( '__kwargs _kwargs_type_')

		####
		out = []
		if return_type:
			out.append( self.indent() + 'func %s(%s) %s {\n' % (node.name, ', '.join(args), return_type) )
		else:
			out.append( self.indent() + 'func %s(%s) {\n' % (node.name, ', '.join(args)) )
		self.push()

		if oargs:
			for n,v in oargs:
				out.append('%s := __kwargs.%s | %s' %(n,n,v))

		for b in node.body:
			v = self.visit(b)
			if v:
				out.append( self.indent() + v )

		self.pull()
		out.append( self.indent()+'}' )
		return '\n'.join(out)

	def _visit_call_helper_var(self, node):
		args = [ self.visit(a) for a in node.args ]
		#if args:
		#	out.append( 'var ' + ','.join(args) )
		if node.keywords:
			for key in node.keywords:
				args.append( key.arg )

		for name in args:
			if name not in self._vars:
				self._vars.add( name )

		#out = []
		#for v in args:
		#	out.append( self.indent() + 'var ' + v + ' int')

		#return '\n'.join(out)
		return ''

	def visit_Assign(self, node):
		target = node.targets[0]
		if isinstance(target, ast.Tuple):
			raise NotImplementedError('TODO')

		elif isinstance(node.value, ast.BinOp) and self.visit(node.value.op)=='<<' and isinstance(node.value.left, ast.Name) and node.value.left.id=='__go__send__':
			target = self.visit(target)
			value = self.visit(node.value.right)
			return 'var %s <- %s;' % (target, value)

		elif not self._function_stack:
			target = self.visit(target)
			value = self.visit(node.value)
			return 'var %s = %s;' % (target, value)

		elif isinstance(node.targets[0], ast.Name) and target.id in self._vars:
			target = self.visit(target)
			value = self.visit(node.value)
			self._vars.remove( target )
			return '%s := %s;' % (target, value)

		else:
			target = self.visit(target)
			value = self.visit(node.value)
			return '%s = %s;' % (target, value)

	def visit_While(self, node):
		body = [ 'for %s {' %self.visit(node.test)]
		self.push()
		for line in list( map(self.visit, node.body) ):
			body.append( self.indent()+line )
		self.pull()
		body.append( self.indent() + '}' )
		return '\n'.join( body )

	def _inline_code_helper(self, s):
		return s

def main(script, insert_runtime=True):
	if insert_runtime:
		dirname = os.path.dirname(os.path.abspath(__file__))
		dirname = os.path.join(dirname, 'runtime')
		runtime = open( os.path.join(dirname, 'go_builtins.py') ).read()
		script = runtime + '\n' + script

	tree = ast.parse(script)
	try:
		return GoGenerator().visit(tree)
	except SyntaxError as err:
		sys.stderr.write(script)
		raise err



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

	out = main( data )
	print( out )


if __name__ == '__main__':
	command()
