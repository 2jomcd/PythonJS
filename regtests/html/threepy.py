# Three.js HTML UI Generator
# by Brett Hartshorn - copyright 2014
# You may destribute this file using the "New BSD" or MIT license

pythonjs.configure(javascript=True)
from dddom import *  ## provides Window3D and SelectManager


class Editor( Window3D ):
	def __init__(self, engine, position=None):
		element = document.createElement( 'div' )
		Window3D.__init__(self, element, engine.scene, engine.scene2, engine.scene3, position, [1,1,1] )
		element.setAttribute('class', 'well')
		self.engine = engine

		b = document.createElement('button')
		b.appendChild(document.createTextNode('run script'))
		b.setAttribute('class', 'btn btn-inverse btn-small')
		element.appendChild(b)

		opts = ['javascript', 'python']
		element.appendChild(document.createTextNode(' mode:'))
		element.appendChild( self.create_select_dropdown(opts) )

		element.appendChild(document.createElement('br'))

		con = document.createElement('div')
		element.appendChild(con)
		ta = create_textarea()
		con.appendChild( ta )

		def ondrop(evt):
			print(evt)
			evt.preventDefault()
			if evt.dataTransfer.files.length==0:
				url = evt.dataTransfer.getData("text/plain")
				iframe = self.create_iframe( url, self.engine.renderer3.domElement )
				self.element.appendChild(iframe)
			else:
				self.handle_drop_event(evt.dataTransfer.files)

		element.ondrop = ondrop.bind( self )
		element.ondragover = lambda evt: evt.preventDefault()


		def onclick(evt):
			eval( ta.value )
		b.onclick = onclick.bind(self)




	def _gen_ui_multi(self, arr): pass

	def _gen_ui_single(self, o): pass

	def _gen_ui(self, o):

		if instanceof(o, Array):
			return self._gen_ui_multi(o)
		elif instanceof(o, THREE.Object3D):
			return self._gen_ui_single(o)
		else:
			raise RuntimeError('can not generate ui for type:'+o)



	def handle_drop_event(self, files):
		images = []
		videos = []
		for file in files:
			## note: `file.path` is only available in NodeWebkit,
			## for simple testing we will fake it here.
			file.path = '/home/brett/Desktop/'+file.name

			if file.path.endswith('.dae'):
				loader = new THREE.ColladaLoader();
				loader.options.convertUpAxis = true;
				#def on_load(collada):
				#	print(collada)
				#	element3D.root.add( collada.scene )
				#loader.load( 'http://localhost:8000'+file.path, on_load )
		
				def onload(evt):
					parser = new DOMParser()
					collada = loader.parse( parser.parseFromString(evt.target.result, "application/xml") )
					print(collada.scene)
					collada.scene.scale.set(0.25, 0.25, 0.25)
					collada.scene.position.set(0, -100, 200)
					element3D.root.add( collada.scene )
					element3D.collada = collada.scene

					menu = element3D.create_tab_menu()
					container.appendChild( menu.root )


					for i,model in enumerate(collada.scene.children):
						print(model)
						page = menu.add_tab( model.name )
						div = document.createElement('div')
						div.setAttribute('class', 'well')
						page.appendChild( div )
						#div.id = element3D.newid()

						h3 = document.createElement('h3')
						h3.appendChild( document.createTextNode(model.name) )
						div.appendChild( h3 )

						if hasattr(model, 'material'): ## could be THREE.Mesh or THREE.SkinnedMesh
							print(model.material)
							ui = gen_material_ui(model)
							div.appendChild( ui )

				reader = new FileReader()
				reader.onload = onload
				reader.readAsText( file )

			elif file.path.endswith('.html'):
				iframe = element3D.create_iframe( file.path, renderer3.domElement )
				container.appendChild(iframe)

			elif file.path.endswith('.css'):
				print( 'TODO css' )
			elif file.path.endswith('.js'):
				print( 'TODO js' )
			elif file.path.endswith('.jpg') or file.path.endswith('.png'):

				li = document.createElement('li')
				images.append(li)
				img = document.createElement('img')
				img.setAttribute('src', file.path)
				img.setAttribute('class', 'well img-rounded')
				li.appendChild( img )


			elif file.path.endswith('.mp4'):
				li = document.createElement('li')
				video = element3D.create_video( mp4=file.path )
				li.appendChild( video )
				videos.append( li )

			elif file.path.endswith('.ogv'):
				#li = document.createElement('li')
				video = element3D.create_video( ogv=file.path )
				container.appendChild(video)
				#li.appendChild( video )
				#videos.append( li )

			elif file.path.endswith('.py'):
				def on_load(event):
					contents = event.target.result
					py_body_editor.setValue( contents )

				Reader.onload = on_load
				Reader.readAsText( file )

		if images:
			print('loading images')
			ul = document.createElement('ul')
			container.appendChild(ul)
			for li in images:
				ul.appendChild(li)

		if videos:
			print('loading videos')
			ul = document.createElement('ul')
			container.appendChild(ul)
			for li in videos:
				ul.appendChild(li)

if False:
	camera = scene = renderer = None
	geometry = material = mesh = None
	scene2 = renderer2 = renderer3 = None
	controls = gizmo = composer = None
	Elements = []

class Engine:
	def Editor(self, **kw):
		e = Editor(self, **kw)
		self.windows.append( e )
		return e

	#def create_editor(self, position=None):
	#	return Editor(self, position=position)


	def __init__(self):
		self.windows = []

		SCREEN_WIDTH = window.innerWidth
		SCREEN_HEIGHT = window.innerHeight

		self.camera = camera = new THREE.PerspectiveCamera( 35, window.innerWidth / window.innerHeight, 1, 10000 );
		camera.position.set( 200, 150, 800 );

		self._selectman = SelectManager(self.camera)

		self.controls = controls = new THREE.TrackballControls( camera );
		camera.smooth_target = controls.target.clone()

		controls.rotateSpeed = 1.0;
		controls.zoomSpeed = 1.2;
		controls.panSpeed = 0.8;

		controls.noZoom = false;
		controls.noPan = false;

		controls.staticMoving = false;
		controls.dynamicDampingFactor = 0.3;

		controls.keys = [ 65, 83, 68 ];

		self.scene = scene = new THREE.Scene();
		self.scene3 = scene3 = new THREE.Scene();



		geometry = new THREE.BoxGeometry( 800, 400, 3800 );
		material = new THREE.MeshPhongMaterial( color=0xc1c1c1, transparent=true, opacity=0.27 );
		mesh = new THREE.Mesh( geometry, material );
		mesh.position.z = -400
		mesh.position.y = -220
		scene.add( mesh );
		mesh.receiveShadow = true;

		self.renderer = renderer = new THREE.WebGLRenderer(alpha=True);
		renderer.shadowMapEnabled = true
		renderer.shadowMapType = THREE.PCFSoftShadowMap
		renderer.shadowMapSoft = true


		renderer.setSize( window.innerWidth, window.innerHeight );
		renderer.domElement.style.position = 'absolute';
		renderer.domElement.style.top = 0;
		renderer.domElement.style.zIndex = 1;

		self.gizmo = new THREE.TransformControls( camera, renderer.domElement )
		scene.add( self.gizmo )

		self.spotlight = light = new(
			THREE.SpotLight( 0xffffff, 1, 0, Math.PI / 2, 1 )
		)
		light.position.set( 0, 1400, 400 )
		light.target.position.set( 0, 0, 0 )

		light.castShadow = True
		light.shadowCameraNear = 400
		light.shadowCameraFar = 1900
		light.shadowCameraFov = 64
		light.shadowCameraVisible = True

		light.shadowBias = 0.0001
		light.shadowDarkness = 0.4

		light.shadowMapWidth = 512
		light.shadowMapHeight = 512

		scene.add( light );

		self.pointlight = pointlight = new( THREE.PointLight(0xffffff, 2, 500) )
		pointlight.position.set( 10, 100, 300 )
		scene.add( pointlight )

		renderer.sortObjects = false
		renderer.autoClear = false

		renderTarget = new(
			THREE.WebGLRenderTarget(
				SCREEN_WIDTH, 
				SCREEN_HEIGHT, 
				minFilter = THREE.LinearFilter, 
				magFilter = THREE.LinearFilter, 
				format = THREE.RGBAFormat,  ## RGBA format is required to composite over css3d render
				stencilBuffer = false
			)
		)


		hblur = new(THREE.ShaderPass( THREE.HorizontalTiltShiftShader ))
		vblur = new(THREE.ShaderPass( THREE.VerticalTiltShiftShader ))

		bluriness = 1.7;
		hblur.uniforms[ 'h' ].value = bluriness / SCREEN_WIDTH;
		vblur.uniforms[ 'v' ].value = bluriness / SCREEN_HEIGHT;

		hblur.uniforms[ 'r' ].value = 0.1
		vblur.uniforms[ 'r' ].value = 0.1


		self.composer = composer = new(THREE.EffectComposer( renderer, renderTarget ))

		renderModel = new(THREE.RenderPass( scene, camera ))

		vblur.renderToScreen = true;
		composer.addPass( renderModel );
		composer.addPass( hblur );
		composer.addPass( vblur );


		self.scene2 = scene2 = new THREE.Scene();


		self.renderer2 = renderer2 = new THREE.CSS3DRenderer();
		renderer2.setSize( window.innerWidth, window.innerHeight );
		renderer2.domElement.style.position = 'absolute';
		renderer2.domElement.style.top = 0;
		renderer2.domElement.style.zIndex = 0;
		document.body.appendChild( renderer2.domElement );

		self.renderer3 = renderer3 = new THREE.CSS3DRenderer();
		renderer3.setSize( window.innerWidth, window.innerHeight );
		renderer3.domElement.style.position = 'absolute';
		renderer3.domElement.style.top = 0;
		renderer3.domElement.style.opacity = 0.1;
		renderer3.domElement.style.zIndex=4;

		document.body.appendChild( renderer2.domElement );
		document.body.appendChild( renderer.domElement );
		document.body.appendChild( renderer3.domElement );



	def gen_material_ui(model):
		print('gen material ui')
		def onchange(val):
			model.material.opacity = val
		slider = create_slider( model.material.opacity, onchange=onchange )
		return slider

	def animate(self):
		requestAnimationFrame( self.animate.bind(self) );
		self.gizmo.update()

		d = self.camera.smooth_target.clone()
		d.sub(self.controls.target)
		self.controls.target.add( d.multiplyScalar(0.03) )
		self.controls.update()

		for win in self.windows: win.update()
		self.renderer2.render( self.scene2, self.camera )
		self.renderer.clear()
		self.composer.render( self.scene, self.camera )
		self.renderer3.render( self.scene3, self.camera )

	def run(self):
		self.animate()

threepy = {
	'Engine' : lambda : Engine(),
}

#pythonjs.configure(javascript=False)
#threepy.Editor = lambda **kw: Engine(**kw)
