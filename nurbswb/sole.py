# -*- coding: utf-8 -*-
#-------------------------------------------------
#-- create a shoe sole
#--
#-- microelly 2017 v 0.8
#--
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------

__version__ = '0.11'




import FreeCAD,FreeCADGui
App=FreeCAD
Gui=FreeCADGui

from PySide import QtGui
import Part,Mesh,Draft,Points


import numpy as np
import random

import os, nurbswb

global __dir__
__dir__ = os.path.dirname(nurbswb.__file__)
print __dir__
import numpy as np


# 12 divisions 


def ssa2npa(spreadsheet,c1,r1,c2,r2,default=None):
	''' create array from table'''

	c2 +=1
	r2 +=1

	ss=spreadsheet
	z=[]
	for r in range(r1,r2):
		for c in range(c1,c2):
			cn=cellname(c,r)
#			print cn
			try:
				v=ss.get(cn)
				z.append(ss.get(cn))
			except:
				z.append(default)


	z=np.array(z)
#	print z
	ps=np.array(z).reshape(r2-r1,c2-c1)
	return ps



def npa2ssa(arr,spreadsheet,c1,r1,color=None):
	''' write 2s array into spreadsheet '''
	ss=spreadsheet
	arr=np.array(arr)
	try:
		rla,cla=arr.shape
	except:
		rla=arr.shape[0]
		cla=0
	c2=c1+cla
	r2=r1+rla
	if cla==0:
		for r in range(r1,r2):
			cn=cellname(c1,r)
			ss.set(cn,str(arr[r-r1]))
			if color<>None: ss.setBackground(cn,color)
	else:
		for r in range(r1,r2):
			for c in range(c1,c2):
				cn=cellname(c,r)
	#			print (cn,c,r,)
				ss.set(cn,str(arr[r-r1,c-c1]))
				if color<>None: ss.setBackground(cn,color)



def cellname(col,row):
	#limit to 26
	if col>90-64:
		raise Exception("not implement")
	char=chr(col+64)
	cn=char+str(row)
	return cn


def runA():

	LL=244.0
	LS=LL+30

	div12=[round(LL/11*i,1) for i in range(12)]

	try: ss=App.ActiveDocument.Spreadsheet
	except: 
		ss=App.activeDocument().addObject('Spreadsheet::Sheet','Spreadsheet')

		ss.set("A1","Sohle")
		ss.set("C1","LL")
		ss.set("A8","Divisionen")
		npa2ssa(np.arange(1,13).reshape(1,12),ss,2,8)
		ss.set("A18","Spitze")
		ss.set("A19","  length -LL")
		ss.set("A20","  left/right")
		ss.set("A21","  height")
		
		ss.set("A23","Ferse")
		ss.set("A24","  length")
		ss.set("A25","  left/right")
		ss.set("A26","  height")


		#-------------------------------------------------------------------------------
		ss.set("D1",str(LL))

		# fussspitze
		h=14
		# normal
		if 0:

			tt=[[[LS-15,35,h],[LS-8,28,h],[LS-5,14,h],[LS,0,h],[LS-5,-15,h],[LS-8,-20,h],[LS-15,-35,h]]]

		# sehr gross 
		if 1:
			h=18
			LS=LL+70
			tt=[[[35,35,14],[40,28,h],[65,14,h],[70,0,h],[65,-15,h],[40,-15,h],[35,-20,14]]]

		npa2ssa(np.array(tt[0]).swapaxes(0,1),ss,2,19)

		#ferse
		h=30
		tf=[[[16,26,h],[8,18,h],[4,9,h],[0,0,h],[4,-7,h],[8,-14,h],[18,-22,h]]]
		npa2ssa(np.array(tf[0]).swapaxes(0,1),ss,2,24)

	#if 1:
		higha=[18,17,16,15, 11,10,8,5, 0,2,5,9,14]

		weia=[-15,-22,-28,-30,-32,	-33,-34,-39,-43,-42,	-37,-25,-23]
		weib=[15,26,25,22,20,			22,23,28,32,43,			45,42,15]

		ss.set("A9","Hight A")
		ss.set("A10","Length")
		ss.set("A14","Width right")
		ss.set("A15","Width left")

		npa2ssa(np.array(higha).reshape(1,13),ss,2,9)
		npa2ssa(np.array(weia).reshape(1,13),ss,2,14)
		npa2ssa(np.array(weib).reshape(1,13),ss,2,15)
		npa2ssa(np.array(div12).reshape(1,12),ss,2,10)

	highb=[17,17,16,15,11,10,8,4,2,1,2,5,9,14]
	highc=[17,17,16,15,25,35,35,15,5,1,2,5,9,14]

	App.activeDocument().recompute()

	tf=[ssa2npa(ss,2,24,8,26,default=None).swapaxes(0,1)]
	tt=np.array([ssa2npa(ss,2,19,8,21,default=None).swapaxes(0,1)])
	tt[0,:,0] += LL

	higha=ssa2npa(ss,2,9,2+12,9,default=None)[0]
	weia=ssa2npa(ss,2,14,2+12,14,default=None)[0]
	weib=ssa2npa(ss,2,15,2+12,15,default=None)[0]

	App.activeDocument().recompute()

	rand=True
	bh=0 # randhoehe
	bw=0.1 # randbreite


	sh=5 # sohlenhoehe


	# prgramm parameter
	# grad der flaechen
	du=3
	dv=3
	drawisolines=False
	drawwires=False

	#-----------------------------------------------------------------------------

	# hilfslinien
	la=[[div12[i],-100,higha[i]] for i in range(12)]
	lb=[[div12[i],100,highb[i]] for i in range(12)]
	lc=[[div12[i],80,highc[i]] for i in range(12)]

	try: App.getDocument("Unnamed")
	except: App.newDocument("Unnamed")
	
	App.setActiveDocument("Unnamed")
	App.ActiveDocument=App.getDocument("Unnamed")
	Gui.ActiveDocument=Gui.getDocument("Unnamed")

	if drawwires:
		import Draft
		wa=Draft.makeWire([FreeCAD.Vector(tuple(p)) for p in la])
		wa.ViewObject.LineColor=(.0,1.,.0)

		wb=Draft.makeWire([FreeCAD.Vector(tuple(p)) for p in lb])
		wb.ViewObject.LineColor=(1.,0.,.0)

		wc=Draft.makeWire([FreeCAD.Vector(tuple(p)) for p in lc])
		wc.ViewObject.LineColor=(1.,1.,.0)

	# siehe auch https://forum.freecadweb.org/viewtopic.php?f=3&t=20525&start=70#p165214


	pts2=[]
	print "Koordianten ..."
	for i in range(13):
		if i<>12:
			x=div12[i]
			h=higha[i]
			hc=highc[i]
		if i == 0:
			# fersenform
			#tf=[[[16,26,h],[8,18,h],[4,9,h],[0,0,h],[4,-7,h],[8,-14,h],[18,-22,h]]]
			pts2 += tf 
			print (i,tf)
		elif i == 12:
			# Spitze
			# spitzenform
			#tt=[[[LS-15,35,h],[LS-8,28,h],[LS-5,14,h],[LS,0,h],[LS-5,-15,h],[LS-8,-20,h],[LS-15,-35,h]]]
			# pts2 += tt 
			pts2.append(tt[0])
			print ("XX",i,tt)
		else:
			# mit innengewoelbe
			# pts2 += [[[x,weib[i]+1.0*(weia[i]-weib[i])*j/6,h if j<>0 else hc] for j in range(7)]]
			pts2 += [[[x,weib[i]+1.0*(weia[i]-weib[i])*j/6,h ] for j in range(7)]]
			print (i,round(x,1),h,weib[i],weia[i])


	pts2=np.array(pts2)
	print "--------------", pts2.shape

	cv=len(pts2)
	cu=len(pts2[0])
	#print pts2.round()
	print (cv,cu)

	kvs=[1.0/(cv-dv)*i for i in range(cv-dv+1)]
	kus=[1.0/(cu-du)*i for i in range(cu-du+1)]

	mv=[dv+1]+[1]*(cv-dv-1)+[dv+1]
	mu=[du+1]+[1]*(cu-du-1)+[du+1]

	bs=Part.BSplineSurface()

	bs.buildFromPolesMultsKnots(pts2,mv,mu,kvs,kus,
				False,False,
				dv,du,
			)

	try: fa=App.ActiveDocument.orig
	except: fa=App.ActiveDocument.addObject('Part::Spline','orig')

	fa.Shape=bs.toShape()
	fa.ViewObject.ControlPoints=True


	if rand:

		pts0=np.array(pts2).swapaxes(0,1)

		l=np.array(pts0[0])
		l[1:-1,1] += bw
		l[1:-1,2] += bh

		r=np.array(pts0[-1])
		r[1:-1,1] -= bw
		r[1:-1,2] += bh

		pts2=np.concatenate([[l],[pts0[0]],pts0[1:],[r]])



		pts0=np.array(pts2).swapaxes(0,1)

		l=np.array(pts0[0])
		l[:,0] -= bw
		l[:,2] += bh

		pts0[0,0,2] += bh
		pts0[0,0,0] -= bw

		pts0[0,-1,2] += bh
		pts0[0,-1,0] -= bw

		r=np.array(pts0[-1])

		r[:,0] += bw
		r[:,2] += bh

		pts0[-1,0,2] += bh
		pts0[-1,0,0] += bw

		pts0[-1,-1,2] += bh
		pts0[-1,-1,0] += bw

		pts2=np.concatenate([[l],[pts0[0]],pts0[1:],[r]])




	cv=len(pts2)
	cu=len(pts2[0])

	kvs=[1.0/(cv-dv)*i for i in range(cv-dv+1)]
	kus=[1.0/(cu-du)*i for i in range(cu-du+1)]

	mv=[dv+1]+[1]*(cv-dv-1)+[dv+1]
	mu=[du+1]+[1]*(cu-du-1)+[du+1]

	bs=Part.BSplineSurface()

	bs.buildFromPolesMultsKnots(pts2,mv,mu,kvs,kus,
				False,False,
				dv,du,
			)



	if 1:
		try: fa= App.ActiveDocument.up
		except: fa=App.ActiveDocument.addObject('Part::Spline','up')

		fa.Shape=bs.toShape()
		fa.ViewObject.ControlPoints=True


	if drawisolines:
		for k in kus:
			Part.show(bs.vIso(k).toShape())

		for k in kvs:
			Part.show(bs.uIso(k).toShape())



	if 1:


		pts2[:,:,2] -= sh

		pts3=pts2

		# fuess gewoelbe wieder runter
		'''
		pts3[4,-1,2]=14
		pts3[4,-2,2]=14

		pts3[5,-1,2]=10
		pts3[5,-2,2]=10

		pts3[6,-1,2]=6
		pts3[6,-2,2]=6
		'''


		cv=len(pts2)
		cu=len(pts2[0])

		kvs=[1.0/(cv-dv)*i for i in range(cv-dv+1)]
		kus=[1.0/(cu-du)*i for i in range(cu-du+1)]

		mv=[dv+1]+[1]*(cv-dv-1)+[dv+1]
		mu=[du+1]+[1]*(cu-du-1)+[du+1]

		bs=Part.BSplineSurface()

		bs.buildFromPolesMultsKnots(pts2,mv,mu,kvs,kus,
					False,False,
					dv,du,
				)



		try: fb= App.ActiveDocument.inner
		except: fb=App.ActiveDocument.addObject('Part::Spline','inner')

		fb.Shape=bs.toShape()
		fb.ViewObject.ControlPoints=True

		try:  loft=App.ActiveDocument.sole
		except: loft=App.ActiveDocument.addObject('Part::Loft','sole')

		loft.Sections=[fa,fb]
		loft.Solid=True
		loft.ViewObject.ShapeColor=(.0,1.,.0)
		App.activeDocument().recompute()

		for f in loft.Sections:
			f.ViewObject.hide()



def createheel():

		points=[FreeCAD.Vector(30.0, 11.0, 0.0), FreeCAD.Vector (65., 5., 0.0), 
			FreeCAD.Vector (60., -10., 0.0), FreeCAD.Vector (19., -13., 0.0)]
		spline = Draft.makeBSpline(points,closed=True,face=True,support=None)


		s=spline.Shape.Edge1
		f=App.ActiveDocument.orig.Shape.Face1

		p=f.makeParallelProjection(s, App.Vector(0,0,1))
		Part.show(p)
		proj=App.ActiveDocument.ActiveObject

		clone=Draft.clone(spline)
		clone.Placement.Base.z=-100
		clone.Scale=(0.4,0.5,1.)


		loft=App.ActiveDocument.addObject('Part::Loft','Loft')
		loft.Sections=[proj,clone]


		points = [FreeCAD.Vector(165.,-7.,-00.0),FreeCAD.Vector(208.,-25.,-00.0),FreeCAD.Vector(233.,20.,-00.0)]
		spline = Draft.makeBSpline(points,closed=True,face=True,support=None)


		s=spline.Shape.Edge1
		f=App.ActiveDocument.orig.Shape.Face1

		p=f.makeParallelProjection(s, App.Vector(0,0,1))
		Part.show(p)
		proj=App.ActiveDocument.ActiveObject

		clone=Draft.clone(spline)
		clone.Placement.Base.z=-100

		loft=App.ActiveDocument.addObject('Part::Loft','Loft')
		loft.Sections=[proj,clone]


		App.activeDocument().recompute()
		Gui.activeDocument().activeView().viewAxonometric()
		Gui.SendMsgToActiveView("ViewFit")


		print "okay"


def run():
	runA()
	#createheel()



if __name__=='__main__':
	run()

