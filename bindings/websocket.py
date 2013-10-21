def on_open_default():
	print 'websocket open'

def on_close_default():
	print 'websocket close'



class websocket:
	def __init__(self, addr='ws://localhost:8080/websocket', on_open=None, on_close=None, on_json_message=None, on_binary_message=None):
		if not on_open:
			on_open = on_open_default
		if not on_close:
			on_close = on_close_default

		with javascript:
			ws = new( WebSocket(addr) )
			ws.binaryType = 'arraybuffer'
			ws.onmessage = lambda evt: self.__class__.__dict__.on_message([self,evt])
			ws.onopen = on_open
			ws.onclose = on_close
			self[...] = ws

		self.on_json_message = on_json_message
		self.on_binary_message = on_binary_message

	def on_message(self, event):
		bin = None
		ob = None

		with javascript:
			print 'on message', event
			if instanceof(event.data, ArrayBuffer):
				print 'got binary bytes', event.data.byteLength
				bin = new(Uint8Array(event.data))
			else:
				print 'got text'
				print event.data
				ob = JSON.parse( event.data )

		if bin:
			self.on_binary_message( bin )
		elif ob:
			self.on_json_message( ob )


	def send_json_message(self, ob):
		with javascript:
			self[...].send( JSON.stringify(ob) )