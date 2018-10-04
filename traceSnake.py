from bge import *
from snakeEngine8 import *
import pickle
import math

def load():
	with open('snake8.build','rb') as tileFile:
		myDePick = pickle.Unpickler(tileFile)
		data,ang = myDePick.load()
	return data,ang

def makeMesh():
	cont = logic.getCurrentController()
	own = cont.owner
	sc = logic.getCurrentScene()
	obl = sc.objects

	data,ang = load()

	ID = own['n']+1
	if ID <= 9:
		ID = '0'+str(ID)
	else:
		ID = str(ID)

	if own['n'] < len(data)-1:
		wip = 'Plane.0'+ID
		print('build',ID,'/',len(data)-1)

		wip = sc.addObject(wip,own)

		go = data[own['n']]
		angle = ang[own['n']]
		wip.worldPosition.xyz = (go[0],go[1],0)

		msh = wip.meshes[-1]

		vrt0 = msh.getVertex(0,0)
		vrt1 = msh.getVertex(0,1)
		vrt2 = msh.getVertex(0,2)
		vrt3 = msh.getVertex(0,3)

		pos0 = vrt0.getXYZ()
		pos1 = vrt1.getXYZ()
		pos2 = vrt2.getXYZ()
		pos3 = vrt3.getXYZ()
		rot = [0.0,0.0,angle]

		dat = data[own['n']+1]
		x = dat[0] - wip.worldPosition.x
		y = dat[1] - wip.worldPosition.y
		d = math.sqrt(x**2+y**2)

		wip.worldPosition.xyz = (go[0]+x/2,go[1]+y/2,0)

		pos0 = ((pos0[0]-d/2)/100,-0.001,-0.001)
		pos1 = ((pos1[0]+d/2)/100,-0.001,-0.001)
		pos2 = ((pos2[0]+d/2)/100,0.001,-0.001)
		pos3 = ((pos3[0]-d/2)/100,0.001,-0.001)

		vrt0.setXYZ(pos0)
		vrt1.setXYZ(pos1)
		vrt2.setXYZ(pos2)
		vrt3.setXYZ(pos3)
		wip.applyRotation(rot)
		own['n'] = own['n']+1
		#sc=[2,2,2]
		#wip.worldScale = sc
		#wip.reinstancePhysicsMesh()
		#own.setParent(obl['visi'],True,False)
	else:
		pass

def do():
	cont = logic.getCurrentController()
	own = cont.owner

	if own['buildNewFile']:
		buildFile(buildBasique())
		own['buildNewFile'] = False

	makeMesh()



