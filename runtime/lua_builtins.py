JS("""
__NULL_OBJECT__ = {}

__concat_tables_array = function(t1, t2)
	for i=1,#t2 do
		t1[ #t1+1 ] = t2[i]
	end
	return t1
end

__concat_tables = function(t1, t2)
	for k,v in pairs(t2) do
		t1[k] = v
	end
	return t1
end

__test_if_true__ = function( x )
	if x == 0 then
		return false
	elseif x == nil then
		return false
	else
		return true
	end
end

__get__ = function(ob, name)
	if name == '__call__' then
		if type(ob)=='function' then
			return ob
		else
			return ob.__call__
		end
	elseif type(ob)=='string' then
		return __get__helper_string(ob,name)
	else
		return ob[ name ]
	end
end

__sprintf = function(s, args)
	return string.format(s, unpack(args))
end

function string:to_array()
	local i = 1
	local t = {}
	for c in self:gmatch('.') do
		t[ i ] = c
		i = i + 1
	end
	return t
end

function string:split(sSeparator, nMax, bRegexp)
	assert(sSeparator ~= '')
	assert(nMax == nil or nMax >= 1)
	if sSeparator == nil then
		sSeparator = ' '
	end

	local aRecord = {}

	if self:len() > 0 then
		local bPlain = not bRegexp
		nMax = nMax or -1

		local nField=1 nStart=1
		local nFirst,nLast = self:find(sSeparator, nStart, bPlain)
		while nFirst and nMax ~= 0 do
			aRecord[nField] = self:sub(nStart, nFirst-1)
			nField = nField+1
			nStart = nLast+1
			nFirst,nLast = self:find(sSeparator, nStart, bPlain)
			nMax = nMax-1
		end
		aRecord[nField] = self:sub(nStart)
	end
	return aRecord
end

__create_class__ = function(class_name, parents, attrs, props)
	local class = {
		__bases__ = parents,
		__name__ = class_name,
		__properties__ = props,
		__attributes__ = attrs
	}
	function class.__call__( args, kwargs )
		local object = {
			__class__ = class,
			__dict__ = 'TODO'
		}
		for k,v in pairs(attrs) do
			if type(v)=='function' then
				object[ k ] = function(_args, _kwargs)
					a = {object}
					if _args then
						return v(__concat_tables_array(a, _args), _kwargs)
					else
						return v(a, _kwargs)
					end
				end
			else
				object[ k ] = v
			end
		end
		a = {object}
		if args then
			attrs.__init__( __concat_tables_array(a, args), kwargs )
		else
			attrs.__init__( a, kwargs or {} )
		end
		return object
	end
	return class
end


__add_op = function(a,b)
	if type(a) == 'string' then
		return a .. b
	else
		return a + b
	end
end

__add__ = function(a,b)
	if type(a) == 'string' then
		return a .. b
	else
		return a + b
	end
end

""")

def str(ob):
	with lowlevel:
		return tostring(ob)

def int(ob):
	with lowlevel:
		return tonumber(ob)

def float(ob):
	with lowlevel:
		return tonumber(ob)

def len(ob):
	with lowlevel:
		if type(ob) == 'string':
			return string.len(ob)
		else:
			return ob.length

def chr(a):
	with lowlevel:
		return string.char(a)

def ord(a):
	with lowlevel:
		return string.byte(a)

class __iterator_string:
	def __init__(self, obj, index):
		with lowlevel:
			self.obj = obj
			self.index = index
			self.length = string.len(obj)

	def next_fast(self):
		with lowlevel:
			index = self.index
			self.index += 1
			return string.sub( self.obj, index+1, index+1 )

class __iterator_list:
	def __init__(self, obj, index):
		self.obj = obj
		self.index = index
		self.length = len(obj)

	def next_fast(self):
		with lowlevel:
			index = self.index
			self.index += 1
			return self.obj[...][index+1]


class list:
	'''
	Array length in Lua must be manually tracked, because a normal for loop will not
	properly loop over a sparse Array with nil holes.
	'''
	def __init__(self, items, pointer=None, length=0):
		with lowlevel:
			self.length = length
			if type(items)=='string':
				self[...] = string.to_array( items )
				self.length = string.len(items)
			elif pointer:
				self[...] = pointer
			else:
				self[...] = {}

	def __getitem__(self, index):
		with lowlevel:
			if index < 0:
				index = self.length + index
			return self[...][index+1]

	def __setitem__(self, index, value):
		with lowlevel:
			if index < 0:
				index = self.length + index
			self[...][index+1] = value

	def __getslice__(self, start, stop, step):
		if stop == null and step == null:
			return self[...].sublist( start )
		elif stop < 0:
			stop = self[...].length + stop
			return self[...].sublist(start, stop)

	def __iter__(self):
		return __iterator_list(self, 0)

	def __add__(self, other):
		for item in other:
			self.append( item )

	def append(self, item):
		with lowlevel:
			self.length += 1
			self[...][ self.length ] = item

	def index(self, obj):
		with lowlevel:
			i = 0
			while i < self.length:
				if self[...][i+1] == obj:
					return i
				i += 1

## this must come after list because list.__call__ is used directly,
## and the lua compiler can not use forward references.
JS('''
__get__helper_string = function(s, name)
	local wrapper
	if name == '__getitem__' then
		wrapper = function(args, kwargs)
			return string.sub(s, args[1]+1, args[1]+1)
		end
	elseif name == '__iter__' then
		wrapper = function(args, kwargs)
			return __iterator_string.__call__( {s, 0} )
		end

	elseif name == 'upper' then
		wrapper = function(args, kwargs)
			return string.upper(s)
		end
	elseif name == 'lower' then
		wrapper = function(args, kwargs)
			return string.lower(s)
		end
	elseif name == 'split' then
		wrapper = function(args, kwargs)
			local a
			if args then
				a = s:split( args[1] )
			else
				a = s:split()
			end
			return list.__call__( {}, {pointer=a, length=#a} )
		end
	else
		print('ERROR: NotImplemented')
	end

	return wrapper
end
''')