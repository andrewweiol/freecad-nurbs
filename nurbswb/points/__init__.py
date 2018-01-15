import FreeCAD,FreeCADGui,Sketcher,Part

App = FreeCAD
Gui = FreeCADGui

import numpy as np
import time


import Draft, Part
import Mesh
Gui=FreeCADGui


import numpy as np
import random
import time

# point limbach oberfrohna
# http://www.landesvermessung.sachsen.de/inhalt/produkte/dhm/dgm/dgm_download.html

# utm 56.373500, 34.32500 
# lat lon 50.865968,12.772980

def toUVMesh(bs, uf=5, vf=5):
		print "los"
		uc=uf*bs.NbUPoles
		vc=vf*bs.NbVPoles
		ss=[]
		for x in range(uc+1): 
			for y in range(vc+1): 
				ss.append(bs.value(1.0/uc*x,1.0/vc*y))

		randfaces=[]
		for x in [0,uc]:
			for y in range(vc+1): 
				randfaces += [(len(ss),len(ss)+1,len(ss)+2),(len(ss)+2,len(ss)+1,len(ss)+3)]
				vek=bs.value(1.0/uc*x,1.0/vc*y)
				ss.append (vek)
				veks=FreeCAD.Vector(vek.x,vek.y,-100)
				ss.append (veks)

		for y in [0,vc]:
			for x in range(uc+1): 
				randfaces += [(len(ss),len(ss)+1,len(ss)+2),(len(ss)+2,len(ss)+1,len(ss)+3)]
				vek=bs.value(1.0/uc*x,1.0/vc*y)
				ss.append (vek)
				veks=FreeCAD.Vector(vek.x,vek.y,-100)
				ss.append (veks)

		randfaces += [(len(ss),len(ss)+1,len(ss)+2),(len(ss)+2,len(ss)+1,len(ss)+3)]
		for x in [0,uc]:
			for y in [0,vc]:
				vek=bs.value(1.0/uc*x,1.0/vc*y)
				veks=FreeCAD.Vector(vek.x,vek.y,-100)
				ss.append (veks)

		scaler=1
		sst=[scaler*v for v in ss]
		ss=sst

		t=Mesh.Mesh((ss,randfaces[-2:]))
		faces1 = randfaces[:2*vc]+randfaces[2*vc+2:4*vc+2]+randfaces[4*vc+4:4*vc+2*uc+4]
		faces1 += randfaces[4*vc+2*uc+6:4*vc+4*uc+6] + randfaces[-2:]
		t=Mesh.Mesh((ss,faces1))
		Mesh.show(t)
		App.ActiveDocument.ActiveObject.ViewObject.Lighting="Two side"

		faces=[]
		for x in range(uc): 
			for y in range(vc): 
				#if max((vc+1)*x+y,(vc+1)*x+y+1,(vc+1)*(x+1)+y,(vc+1)*x+y+1,(vc+1)*(x+1)+y+1,(vc+1)*(x+1)+y)<50000: 
				#if len(faces)<100000:
					faces.append(((vc+1)*x+y,(vc+1)*x+y+1,(vc+1)*(x+1)+y))
					faces.append(((vc+1)*x+y+1,(vc+1)*(x+1)+y+1,(vc+1)*(x+1)+y))

		print "hu"
		# print ss
		# print faces
		FreeCAD.Console.PrintMessage(str(("size of the mesh:",uc,vc))+"\n")
		FreeCAD.Console.PrintMessage(str(("number of points" ,len(ss)))+"\n")
		FreeCAD.Console.PrintMessage(str(("faces:",len(faces)))+"\n")


		t=Mesh.Mesh((ss,faces+faces1))
		#t=Mesh.Mesh((ss,faces))
		Mesh.show(t)
		App.ActiveDocument.ActiveObject.ViewObject.Lighting="Two side"
		App.ActiveDocument.ActiveObject.ViewObject.DisplayMode = u"Wireframe"
		FreeCAD.Console.PrintMessage(str(t))


		print (uc,vc)
		return t


def PointarrayToMesh(par, uf=5, vf=5,h=1100):
		print "los"
		uc,vc,_=par.shape
		uc -= 1 
		vc -= 1
		print (uc,vc)
		ss=[]
		for x in range(uc+1): 
			for y in range(vc+1): 
				ss.append(FreeCAD.Vector(par[x,y]))

		randfaces=[]
		if 10:
			for x in [0,uc]:
				for y in range(vc+1): 
					randfaces += [(len(ss),len(ss)+1,len(ss)+2),(len(ss)+2,len(ss)+1,len(ss)+3)]
					vek=FreeCAD.Vector(par[x,y])
					ss.append (vek)
					veks=FreeCAD.Vector(vek[0],vek[1],h)
					ss.append (veks)

			for y in [0,vc]:
				for x in range(uc+1): 
					randfaces += [(len(ss),len(ss)+1,len(ss)+2),(len(ss)+2,len(ss)+1,len(ss)+3)]
					vek=par[x,y]
					vek=FreeCAD.Vector(par[x,y])
					ss.append (vek)
					veks=FreeCAD.Vector(vek[0],vek[1],h)
					ss.append (veks)

			randfaces += [(len(ss),len(ss)+1,len(ss)+2),(len(ss)+2,len(ss)+1,len(ss)+3)]
			for x in [0,uc]:
				for y in [0,vc]:
					vek=par[x,y]
					vek=FreeCAD.Vector(par[x,y])
					veks=FreeCAD.Vector(vek[0],vek[1],h)
					ss.append (veks)

		scaler=1
		sst=[scaler*v for v in ss]
		ss=sst

		t=Mesh.Mesh((ss,randfaces[-2:]))
		faces1 = randfaces[:2*vc]+randfaces[2*vc+2:4*vc+2]+randfaces[4*vc+4:4*vc+2*uc+4]
		faces1 += randfaces[4*vc+2*uc+6:4*vc+4*uc+6] + randfaces[-2:]
		t=Mesh.Mesh((ss,faces1))
		#Mesh.show(t)
		# App.ActiveDocument.ActiveObject.ViewObject.Lighting="Two side"

		faces=[]
		for x in range(uc): 
			for y in range(vc): 
				#if max((vc+1)*x+y,(vc+1)*x+y+1,(vc+1)*(x+1)+y,(vc+1)*x+y+1,(vc+1)*(x+1)+y+1,(vc+1)*(x+1)+y)<50000: 
				#if len(faces)<100000:
					faces.append(((vc+1)*x+y,(vc+1)*x+y+1,(vc+1)*(x+1)+y))
					faces.append(((vc+1)*x+y+1,(vc+1)*(x+1)+y+1,(vc+1)*(x+1)+y))

		print "hu"
		# print ss
		# print faces
		FreeCAD.Console.PrintMessage(str(("size of the mesh:",uc,vc))+"\n")
		FreeCAD.Console.PrintMessage(str(("number of points" ,len(ss)))+"\n")
		FreeCAD.Console.PrintMessage(str(("faces:",len(faces)))+"\n")

		t=Mesh.Mesh((ss,faces+faces1))
		#t=Mesh.Mesh((ss,faces))
		Mesh.show(t)
		App.ActiveDocument.ActiveObject.ViewObject.Lighting="Two side"
		#App.ActiveDocument.ActiveObject.ViewObject.DisplayMode = u"Wireframe"
		FreeCAD.Console.PrintMessage(str(t))


		print (uc,vc)
		return t

if 0:
	bs=App.ActiveDocument.Nurbs.Shape.Face1.Surface

	# bs=App.ActiveDocument.Shape.Shape.Face1.Surface

	print bs

	t=toUVMesh(bs, uf=10, vf=10)


	print "dine"
	print t




def machFlaeche(psta,ku=None,objName="XXd",degree=3):
		NbVPoles,NbUPoles,_t1 =psta.shape


		ps=[[FreeCAD.Vector(psta[v,u,0],psta[v,u,1],psta[v,u,2]) for u in range(NbUPoles)] for v in range(NbVPoles)]

#		kv=[1.0/(NbVPoles-3)*i for i in range(NbVPoles-2)]
#		if ku==None: ku=[1.0/(NbUPoles-3)*i for i in range(NbUPoles-2)]


		kv=[1.0/(NbVPoles-degree)*i for i in range(NbVPoles-degree+1)]
		if ku==None: ku=[1.0/(NbUPoles-degree)*i for i in range(NbUPoles-degree+1)]


#		mv=[4] +[1]*(NbVPoles-4) +[4]
#		mu=[4]+[1]*(NbUPoles-4)+[4]

		mv=[degree+1] +[1]*(NbVPoles-degree-1) +[degree+1]
		mu=[degree+1] +[1]*(NbUPoles-degree-1) +[degree+1]

#		print len(ku)
#		print len(mu)
#		print mu


		bs=Part.BSplineSurface()
		bs.buildFromPolesMultsKnots(ps, mv, mu, kv, ku, False, False ,degree,degree)

		res=App.ActiveDocument.getObject(objName)

		# if res==None:
		res=App.ActiveDocument.addObject("Part::Spline",objName)
			# res.ViewObject.ControlPoints=True

		res.Shape=bs.toShape()

		return bs




def createAll(mode="all",obj=None,dimU=500,dimV=500,
				ua=10,sizeU=100,va=10,sizeV=100,
				socketheight=10,saxonyflag=True,rowselector='',center=False,scale=1,
				createpart=False,createsurface=True 
			):




#	obj=App.ActiveDocument.Points
	print obj.Points.BoundBox.Center
	# center=False

	if center:
		zmin=obj.Points.BoundBox.ZMin -obj.Points.BoundBox.Center.z
		zmax=obj.Points.BoundBox.ZMax -obj.Points.BoundBox.Center.z
	else:
		zmin=obj.Points.BoundBox.ZMin
		zmax=obj.Points.BoundBox.ZMax

	p=obj.Points.Points


	if center:
		p=np.array(obj.Points.Points)- obj.Points.BoundBox.Center

	assert dimU*dimV==len(p)
	if mode<>"all":
		return


	zmin *=scale
	zmax *=scale
	socketheight *= scale
	p=[pp*scale for pp in p]


	pa2=np.array(p).reshape(dimU,dimV,3)

#	pa3=[]
#	a=0
#	for i in range(dimU):
#		if pa2[i][0][0]<>a:
#			pa3 += [pa2[i]] 
#			print pa2[i][0][0]-a
#		
#		print pa2[i][0]
#		a= pa2[i][0][0]

	# andere variante
	
	if saxonyflag:
		pa3=[]
		pmin=[]
		pmax=[]
		for i in range(dimU):
			if i%4==1:
				pmin += [pa2[i]]
			if i%4==3:
				pmax += [pa2[i]]
			if i%2==0:
				pa3 += [pa2[i]] 
			

	else:
		p3=p2
	pa4=np.array(pa3)
	pa4.shape
	
	if 0: # auswertung der anderen baender
		pmin=np.array(pmin)
		print pmin.shape
		pmax=np.array(pmax)
		print pmax.shape
		comp=[]
		for i in range(124):
			for j in range(500):
				if i<4 and j<4:
					print [pmin[i+1],j,pmax[i,j]]
				a=FreeCAD.Vector(pmin[i+1,j])
				b=FreeCAD.Vector(pmax[i,j])
				if a<>b:
					if b.z<a.z: a,b=b,a
					comp += [ Part.makePolygon([a,a+(b-a)*10])]
					

		print len(comp)
		Part.show(Part.Compound(comp))


#	return

	import time

	if 0:
		ta=time.time()
		ss=PointarrayToMesh(pa4[60:70,60:70])

		siz=10
		tb=time.time()
		bc=Part.BSplineSurface()
		bc.interpolate(pa4[100:100+siz,100:100+2*siz])
		tc=time.time()
		Part.show(bc.toShape())
		td=time.time()
		tc-tb
		td-tc


	#ss=PointarrayToMesh(pa4)

	if 0:
		ta=time.time()
		ss=PointarrayToMesh(pa4,h=zmax)
		ss=PointarrayToMesh(pa4,h=zmin)

		tb=time.time()
		print "create meshes all", tb-ta
#	return

	ta=time.time()
	#ss=PointarrayToMesh(pa4)
	if 1:
		print ("!",zmax,zmin,socketheight)
		# ss=PointarrayToMesh(pa4[ua:ua+sizeU,va:va+2*sizeV],h=zmax+socketheight)
		ss=PointarrayToMesh(pa4[ua:ua+sizeU,va:va+2*sizeV],h=zmin-socketheight)

	tb=time.time()
	print "create meshes sub ", tb-ta

	if not createsurface: return

	#create nurbs face
	tb=time.time()
	bs=machFlaeche(pa4[ua:ua+sizeU,va:va+2*sizeV])
	tc=time.time()
	print "create surf 200 x 200 ", tc-tb

	if 0:
		tb=time.time()
		bs=machFlaeche(pa4,degree=3)
		tc=time.time()
		print "create surf all ", tc-tb

	if not createpart: return


	#create side faces
	ff=App.ActiveDocument.ActiveObject
	be=[]
	faces=[ff.Shape.Face1]
	for i,e in enumerate(ff.Shape.Face1.Edges):
		print e
		pa=e.Vertexes[0].Point
		pe=e.Vertexes[-1].Point

		h=zmin-socketheight
		pau=FreeCAD.Vector(pa.x,pa.y,h)
		peu=FreeCAD.Vector(pe.x,pe.y,h)

		e2=Part.makePolygon([pa,pau])
		e3=Part.makePolygon([peu,pe])
		e4=Part.makePolygon([pau,peu])

	#	Part.show(e2)
	#	Part.show(e3)
		Part.show(e4)
		App.activeDocument().recompute()
		eA=App.ActiveDocument.ActiveObject
		if i%2==0:
			be += [eA]

		Part.show(e)
		App.activeDocument().recompute()
		eB=App.ActiveDocument.ActiveObject
		
		rf=FreeCAD.ActiveDocument.addObject('Part::RuledSurface', 'Ruled Surface')
		rf.Curve1=(eA,['Edge1'])
		rf.Curve2=(eB,['Edge1'])
		App.activeDocument().recompute()
		faces += [rf.Shape.Face1]

	# create bottom face
	rf=FreeCAD.ActiveDocument.addObject('Part::RuledSurface', 'Ruled Surface')
	rf.Curve1=(be[0],['Edge1'])
	rf.Curve2=(be[1],['Edge1'])
	App.activeDocument().recompute()
	faces += [rf.Shape.Face1]


	#create shell and solid
	_=Part.Shell(faces)
	sh=App.ActiveDocument.addObject('Part::Feature','Shell2')
	sh.Shape=_.removeSplitter()
	del _
	App.activeDocument().recompute()

	shell=sh.Shape
	_=Part.Solid(shell)
	App.ActiveDocument.addObject('Part::Feature','Solid').Shape=_.removeSplitter()
	del _

	App.activeDocument().recompute()

	tc=time.time()

	# toUVMesh(bs)

	tc-tb


# createAll()



if 1:
		import nurbswb.miki
		reload(nurbswb.miki)
		rc=nurbswb.miki.runtest()
		


layout2='''
VerticalLayoutTab:
	setText:"HUHUWAS"
	id:'main'

	VerticalLayout:

		QtGui.QLabel:
			setText:"***   N U R B S  YYY XX  E D I T O R   ***"
'''


layout2='''
MainWindow:

	VerticalLayout:
		QtGui.QLabel:
			setText:"***   create a surface for a point cloud   ***"
#		QtGui.QLabel:
#			setText:"<hr>you have <hr>to select <hr>a point cloud<br>"

		HorizontalLayout:
			QtGui.QCheckBox:
				id: 'createpart' 
				setText: 'Create Part Solid'
				setChecked: False

			QtGui.QCheckBox:
				id: 'createsurface' 
				setText: 'Create Surface'
				setChecked: False

			QtGui.QCheckBox:
				id: 'center' 
				setText: 'Origin to Center Bound Box'
				setChecked: True
			QtGui.QCheckBox:
				id: 'saxony' 
				setText: 'Saxon data format'
				setChecked: True
			QtGui.QLabel:
				setText:"row filter"
			QtGui.QComboBox:
				id: 'row'
				addItem: "even"
				addItem: "odd"
				addItem: "0 % 4"
				addItem: "1 % 4"
				addItem: "2 % 4"
				addItem: "3 % 4"

			QtGui.QLabel:
				setText:"socket height"
			QtGui.QLineEdit:
				setText:"10"
				id: 'socketheight'


		HorizontalLayout:
			QtGui.QLabel:
				setText:"scale "
			QtGui.QLineEdit:
				setText:"1000"
				id: 'scale'

			QtGui.QLabel:
				setText:"u dim "
			QtGui.QLineEdit:
				setText:"500"
				id: 'ud'
			QtGui.QLabel:
				setText:"v dim "
			QtGui.QLineEdit:
				setText:"500"
				id: 'vd'


		HorizontalLayout:
			QtGui.QLabel:
				setText:"u start "
			QtGui.QLineEdit:
				setText:"50"
				id: 'ua'
			QtGui.QLabel:
				setText:"u size "
			QtGui.QLineEdit:
				setText:"20"
				id: 'us'

		HorizontalLayout:

			QtGui.QLabel:
				setText:"v start "
			QtGui.QLineEdit:
				setText:"50"
				id: 'va'
			QtGui.QLabel:
				setText:"v size "
			QtGui.QLineEdit:
				setText:"20"
				id: 'vs'

		HorizontalLayout:
#			QtGui.QPushButton:
#				setText: "Run Mesh Socket"
#				clicked.connect: app.run
#			QtGui.QPushButton:
#				setText: "Run Nurbs at Socket"
#				clicked.connect: app.run

#			QtGui.QPushButton:
#				setText: "Run planar Part at Socket"
#				clicked.connect: app.run

			QtGui.QPushButton:
				setText: "Run "
				clicked.connect: app.run

			QtGui.QPushButton:
				setText: "Close"
				clicked.connect: app.close

'''



class MyApp(object):

	def __init__(self):
		self.pole1=[1,5]
		self.pole2=[3,1]
		self.lock=False

	def updateDialog(self):
		pass
		#self.root.ids['ud'].setMaximum(self.obj.Object.nNodes_u-2)
		#self.root.ids['vd'].setMaximum(self.obj.Object.nNodes_v-2)

	def run(self):
		print self.obj.Label
		print self.root.ids['ua'].text()
		print self.root.ids['us'].text()
		print self.root.ids['saxony'].isChecked()
		print self.root.ids['row'].currentText()

		createAll(
			'all',
			self.obj,
			int(self.root.ids['ud'].text()),
			int(self.root.ids['vd'].text()),

			int(self.root.ids['ua'].text()),
			int(self.root.ids['us'].text()),
			int(self.root.ids['va'].text()),
			int(self.root.ids['vs'].text()),
			int(self.root.ids['socketheight'].text()),
			self.root.ids['saxony'].isChecked(),
			self.root.ids['row'].currentText(),
			self.root.ids['center'].isChecked(),
			int(self.root.ids['scale'].text()),
			self.root.ids['createpart'].isChecked(),
			self.root.ids['createsurface'].isChecked(),
		)







	def close(self):
		for w in FreeCAD.w5: w.hide()
		FreeCAD.w5=[]


def mydialog(obj):


	import nurbswb.miki as miki
	reload (nurbswb.miki)

	app=MyApp()
	miki=miki.Miki()

	miki.app=app
	app.root=miki
	app.obj=obj

	#miki.parse2(layout2)
	miki.run(layout2)

#	miki.ids['ud'].setMaximum(obj.Object.nNodes_u-2)
#	miki.ids['vd'].setMaximum(obj.Object.nNodes_v-2)

	return miki



def runA():
	try:
		obj=Gui.Selection.getSelection()[0]
	except:
		obj=App.ActiveDocument.Points
	mydialog(obj)

