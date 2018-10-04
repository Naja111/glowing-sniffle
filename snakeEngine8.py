import random
import pickle
import math

build = True
bluePrint = []
blueAngle = []

def valAbs(x):
	if x < 0:
		x = -x
	return x

def up(nbPoint,angle,xy,var):
	#print(angle)
	angle = math.radians(float(angle))
	for i in range(nbPoint):
		last = xy[-1]
		Cx = last[0]+(float(var.get('step'))*math.cos(angle))
		Cy = last[1]+(float(var.get('step'))*math.sin(angle))
		C = (Cx,Cy)
		xy.append(C)

		if i ==nbPoint-1:
			bluePrint.append(xy[-1])
			blueAngle.append(angle)


def hor(nbPoint,xy,var):
	for i in range(nbPoint):

		last = xy[-1]

		x = last[0] + float(var.get('step'))
		y = last[1]
		xy.append((x,y))

		if i ==nbPoint-1:
			bluePrint.append(xy[-1])
			blueAngle.append(0)
	return 0

def transition(xy,var):
	for i in range(0,int(var.get('transDuration'))):

		last = xy[-1]

		x = last[0] + float(var.get('step'))
		y = last[1]
		xy.append((x,y))

		if i ==int(var.get('transDuration'))-1:
			bluePrint.append(xy[-1])
			blueAngle.append(0)



def purge(lst):
	fresh = []
	dic = {}

	for i in lst:
		if i[:1] == '#' or i[:1] == '':
			pass
		else:
			fresh.append(i)

	for i in fresh:
		ii = i.split('=')
		dic[ii[0]] = ii[1]
	return dic

def setProfile(file):

	with open('{}.conf'.format(file),'r') as profile:
		settings = profile.read()
		sett = settings.split('\n')
	var = purge(sett)
	return var

def buildBasique(xy=[(0,0)]):
	bluePrint.append(xy[-1])

	var = setProfile('sn')

	seed=var.get('seed')
	if seed != '':
		random.seed(int(seed))

	step=float(var.get('step'))
	nbSect=int(var.get('nbSect'))
	nbPointLineMin=int(var.get('nbPointLineMin'))
	nbPointLineMax=int(var.get('nbPointLineMax'))
	nbPointSlopeMin=int(var.get('nbPointSlopeMin'))
	nbPointSlopeMax=int(var.get('nbPointSlopeMax'))
	angleMin=int(var.get('angleMin'))
	angleMax=int(var.get('angleMax'))

	transition(xy,var)

	for i in range(nbSect):

		nbPointSlope = random.randint(nbPointSlopeMin,nbPointSlopeMax)
		angle = random.randint(angleMin,angleMax)
		signe = random.randint(0,1)
		if signe == 0:
			angle = -angle
		up(nbPointSlope,angle,xy,var)

		nbPointLine = random.randint(nbPointLineMin,nbPointLineMax)
		hor(nbPointLine,xy,var)
		
	nbPointSlope = random.randint(nbPointSlopeMin,nbPointSlopeMax)
	angle = random.randint(angleMin,angleMax)
	signe = random.randint(0,1)
	if signe == 0:
		angle = -angle
	up(nbPointSlope,angle,xy,var)

	transition(xy,var)

	return xy

def buildFile(xy):
	with open('snake8.csv','w') as file:
		for i in xy:
			file.write('{},{}\n'.format(i[0],i[1]))

	with open('snake8.b','wb') as file:
		myPick = pickle.Pickler(file)
		myPick.dump(xy)



	if build:
		with open('snake8.build','wb') as file:
			myPick = pickle.Pickler(file)
			myPick.dump([bluePrint,blueAngle])
		with open('snake8Build.csv','w') as file:
			for i in bluePrint:
				file.write('{},{}\n'.format(i[0],i[1]))

#EXEMPLE:
if __name__ == '__main__':
	build = True
	buildFile(buildBasique())

