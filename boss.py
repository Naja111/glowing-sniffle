from bge import *
import random
import pickle

cont = logic.getCurrentController
own = cont.owner

with open('snake8.b','rb') as file:

bossID = own['bossID']

def anim1(): #goes around the screen
  frame = 0
  own.worldPosition.x = data'[bossID'] + frame
  own.worldPostion.y = data[
