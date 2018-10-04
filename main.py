from bge import *
import random
import math
import datetime
import pickle

def IA(): #WIP, UNUSED
	####### PARAM #######
	fps = 2
	#####################

	cont = logic.getCurrentController()
	own = cont.owner
	sc = logic.getCurrentScene()
	obl = sc.objects

	loco = obl['Loco']
	track = cont.actuators['track']
	shoot = cont.actuators['shoot']

	##### TIR ######
	if own['look'] == 0:
		r = random.randint(1,4)
		target = 'cible{}'.format(r)
		track.object = obl[target]
		own['targ'] = target
		own['look'] = 1

	if own['time'] >= fps:
		cont.activate(shoot)
		own['time'] = 0

	# color = [256,0,0]
	# render.drawLine(own.worldPosition,obl[own['targ']].worldPosition,color)
	################

	####### MOVE #########

def gun(ID): #When called, this fct juste return the variables associate to a gun ID. Can get them from a config file ?
	var = {}
		#list of parameter
	if ID == 0:
		var['cd'] = 0.2
		var['bullet'] = 0
	elif ID == 1:
		var['cd'] = 1
		var['bullet'] = 0
	elif ID == 2:
		var['cd'] = 2
		var['bullet'] = 0
	return var

def gunning(): #Just get the parameter of a gun from gun(), apply them, and shoot one time.
	cont = logic.getCurrentController()
	own = cont.owner
	sc = logic.getCurrentScene()
	obl = sc.objects
	ID = own['id']
	clic = cont.sensors['clic']
	shoot = cont.actuators['shoot']

	var = gun(ID)

	if clic.positive and own['cd'] >= var.get('cd') and own['act'] == 1:
		shoot.object = 'bullet{}'.format(var.get('bullet'))
		cont.activate(shoot)
		own['cd'] = 0


def wheel(): #Select the active turret ID depending of the player inputs
	cont = logic.getCurrentController()
	own = cont.owner
	sc = logic.getCurrentScene()
	obl = sc.objects
		#list of inputs
	up = cont.sensors['up']
	dw = cont.sensors['down']
	un = cont.sensors['un']
	deux = cont.sensors['deux']
	trois = cont.sensors['trois']
	quatre = cont.sensors['quatre']
	cinq = cont.sensors['cinq']
	chng = cont.sensors['chng']

	if chng.positive:
		own['fx'] = 1

	if up.positive: #use mouse wheel to change
		own['wheel'] = own['wheel'] +1
	elif dw.positive:
		own['wheel'] = own['wheel'] -1

	if un.positive: #use keyboard
		own['wheel'] = 0
	elif deux.positive and own['nbTurret'] >=2:
		own['wheel'] = 1
	elif deux.positive and own['nbTurret'] >=3:
		own['wheel'] = 2
	elif deux.positive and own['nbTurret'] >=4:
		own['wheel'] = 3
	elif deux.positive and own['nbTurret'] >=5:
		own['wheel'] = 4
			 #make wheel id loop in between min an max
	if own['wheel'] >= own['nbTurret']:
		own['wheel'] = 0
	elif own['wheel'] < 0:
		own['wheel'] = own['nbTurret'] -1

	i = 0
	while i != int(own['nbTurret']):
		if i == own['wheel']:
			obl['t{}'.format(own['wheel'])]['active'] = 1
			obl['gun{}'.format(own['wheel'])]['act'] = 1
			obl['puff{}'.format(own['wheel'])]['act'] = 1

		else:
			obl['t{}'.format(i)]['active'] = 0
			obl['gun{}'.format(i)]['act'] = 0
			obl['puff{}'.format(i)]['act'] = 0
		i = i+1

def wagon(): #generate wagon route

	cont = logic.getCurrentController()
	own = cont.owner
	sc = logic.getCurrentScene()
	obl = sc.objects
	track = cont.actuators['track']
	track.object = obl[own['follow']]

	own['mvID'] = obl[own['follow']]['mvID'] -25

	with open('snake8.b','rb') as tileFile:
		myDePick = pickle.Unpickler(tileFile)
		data = myDePick.load()

	own.worldPosition.xy = data[own['mvID']]

def puff2():
	cont = logic.getCurrentController() # get the object that uses the controller
	own = cont.owner

	if own['act'] == 1:
		if own['n'] <= 7:
			own.setVisible(True)
			# Image orginale de la texture
			ID = texture.materialID(own, "IMf0.png")
			object_texture = texture.Texture(own, ID)
			own.attrDict["tex1"] = object_texture
			# Chemin de l'image
			url = '/home/eliott/Desktop/Train/Assets/FX/Puff/Frames/f{}.png'.format(own['n'])
			new_source = texture.ImageFFmpeg(url)
			object_texture.source = new_source
			object_texture.refresh(False)
			own['n'] = own['n']+1
		elif own['n'] >= 8:
			own.setVisible(False)
			own['fx'] = 0

			#play anim

		else:
			own.setVisible(False)
			pass
	elif own['act'] == 0:
		own.setVisible(False)
		own['n'] = 0

def ray():
	cont = logic.getCurrentController()
	own = cont.owner
	sc = logic.getCurrentScene()
	obl = sc.objects
	loco = obl['Loco']
	rR = obl['RayR']
	rL = obl['RayL']

	rayR = cont.sensors['rayR']
	posR = rayR.hitPosition
	rayL = cont.sensors['rayL']
	posL = rayL.hitPosition

	# print(posR[0],'/',loco.worldPosition.x)
	# color = [256,0,0]
	# render.drawLine(rR.worldPosition,posR,color)

	if loco.worldPosition.x >= posR[0]:
		loco['max'] = 1
	elif loco.worldPosition.x <= posL[0]:
		loco['max'] = -1
	else:
		loco['max'] = 0

def scroll():
	cont = logic.getCurrentController()
	own = cont.owner
	sc = logic.getCurrentScene()
	obl = sc.objects
	loco = obl['Loco']

	with open('snake8.b','rb') as tileFile:
		myDePick = pickle.Unpickler(tileFile)
		data = myDePick.load()

	if own['scroll']:
		if loco['max'] == 0:
			loco['mvID'] = loco['mvID'] +1
		elif loco['max'] == -1:
			loco['mvID'] = loco['mvID'] +2
		else:
			pass

		own['scrollID'] = own['scrollID'] +1
		own['scrollID'] = loop(own['scrollID'],data)

	try:
		pos = data[own['scrollID']]
	except:
		pos = data[-1]
		
	own.worldPosition.x = pos[0]

	own.worldPosition.y = pos[1]

def loop(posID,data):
	if posID >= (len(data)-1)-350: ####change 350 to transDuration/2 from conf file later
		podID = 0
	return posID

def move2():
	cont = logic.getCurrentController()
	own = cont.owner
	sc = logic.getCurrentScene()
	obl = sc.objects
	cam = obl['Camera']

	x = own.worldPosition.x

	with open('snake8.b','rb') as tileFile:
		myDePick = pickle.Unpickler(tileFile)
		data = myDePick.load()

	left = cont.sensors['left']
	right = cont.sensors['right']

	if left.positive and own['max'] != -1:
		own['mvID'] = own['mvID'] -4
		
	if right.positive and own['max'] != 1:
		own['mvID'] = own['mvID'] +4
	
	own['mvID'] = loop(own['mvID'],data)

	try:
		pos = data[own['mvID']]
		#print('time:',cam['time'])
		#print('x:',pos[0],'y:',pos[1])
	except:
		pos = data[-1]
		own['mvID'] = len(data)
	own.worldPosition.x = pos[0]
	own.worldPosition.y = pos[1]

def velocity():
	cont = logic.getCurrentController()
	own = cont.owner

	vel = own.getLinearVelocity(True)
	own['vel'] = vel[1]

def mob():
	cont = logic.getCurrentController()
	own = cont.owner
	sc = logic.getCurrentScene()
	obl = sc.objects
	wall = obl['wall']

	if own.worldPosition.x <= wall.worldPosition.x:
		act1 = cont.actuators['mail']
		act2 = cont.actuators['end']
		cont.activate(act1)
		cont.activate(act2)

def tracker():
	cont = logic.getCurrentController()
	own = cont.owner
	sc = logic.getCurrentScene()
	obl = sc.objects

	cursor = obl['cursor']
	mouse_over = cont.sensors['mouse_over']

	if mouse_over.positive:
		cursor.worldPosition.x = mouse_over.hitPosition.x
		cursor.worldPosition.y = mouse_over.hitPosition.y
		cursor.worldPosition.z = 0

def spawn():
	cont = logic.getCurrentController()
	own = cont.owner
	sc = logic.getCurrentScene()
	obl = sc.objects

	if own['time'] >= 2:
		own['time'] = 0

		r = random.randint(1,5)

		x = 'sp{}'.format(r)

		act = cont.actuators['{}'.format(x)]
		cont.activate(act)

def finish():
	cont = logic.getCurrentController()
	own = cont.owner
	sc = logic.getCurrentScene()
	obl = sc.objects
	loco = obl['Loco']
	end = obl['finishLine']
	cam = obl['Camera']

	if loco.worldPosition.x >= end.worldPosition.x:
		print(cam['score'])
		act = cont.actuators['end']
		cont.activate(act)

def log():
	cont = logic.getCurrentController()
	own = cont.owner
	sc = logic.getCurrentScene()
	obl = sc.objects
	cam = obl['Camera']
	loco = obl['Loco']
	end = obl['finishLine']

	if own['logStart'] == 0:
		with open('game.log','a') as log:
			now = datetime.datetime.now()
			intro = '##########\nNEW GAME\n' + str(now) + '\n##########\n'
			log.write(intro)
			own['logStart'] = 1
			#get inputs, kills, hp and wagon loss, final score, victory and game over

	elif own['logStart'] == 1:
		with open('game.log','a') as log:

			left = cont.sensors['left']
			right = cont.sensors['right']
			if left.positive:
				log.write('>left\n')
			if right.positive:
				log.write('>right\n')

			kill = cont.sensors['kill']
			hp = cont.sensors['hp-1']
			wagon = cont.sensors['w-1']
			if kill.positive:
				log.write('kill +1\n')
			if hp.positive:
				log.write('@hp -1\n')
			if wagon.positive:
				log.write('@wg -1\n')

			if cam['hp'] <= 0:
				log.write('DEATH BY 0 HP\n')
				s = str(cam['score'])
				sc = 'score is : '+s+'\n\n\n'
				log.write(sc)
			if cam['wagon'] <= 0:
				log.write('DEATH BY 0 WG\n')
				s = str(cam['score'])
				sc = 'score is : '+s+'\n\n\n'
				log.write(sc)

			if loco.worldPosition.x >= end.worldPosition.x:
				log.write('VICTORY\n')
				s = str(cam['score'])
				sc = 'score is : '+s+'\n\n\n'
				log.write(sc)