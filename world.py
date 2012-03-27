from pandac.PandaModules import *
from panda3d.core import *
from panda3d.core import CollisionTraverser,CollisionNode
from panda3d.core import CollisionHandlerQueue,CollisionRay
from direct.task import Task
from player import *
from direct.showbase.DirectObject import DirectObject

# Global Dict. for holding levels.
ACTIVE_LEVEL = {}

class World(DirectObject):
	
	"""
	World Class:
	"""
	
	def __init__(self):
		pass
		# Things go here that most levels would share.
		# Physics may go in here i think.
		
		# Loads the level model.
	def addLevel(self, levelId, levelObject):
		ACTIVE_LEVEL[levelId] = levelObject
		print "Level "+ str(levelId)+ " Created"

# Create a level
class Level(DirectObject):
	
	"""
	Level Class:
	"""
	
	def __init__(self, levelName, levelPath):
		
		# Name the Level.
		self.levelName = levelName
		# Point to the level Model.
		self.np = loader.loadModel(levelPath)
		self.np.reparentTo(render)
		self.np.setPos(0, 0, 0)
		
		self.obj1 = Ball()
		taskMgr.add(self.levelColCheck, "ballColCheck")
		
		self.obj1ballHandler = CollisionHandlerQueue()
		cTrav.addCollider(self.obj1.ballColNp, self.obj1ballHandler)
		base.messenger.toggleVerbose()
		### This is for testing. 
		self.levelTexture = loader.loadTexture("assets/levels/grass_d.png")
		self.levelTexture.WMRepeat
		self.np.setTexture(self.levelTexture)
		###
	
	def levelColCheck(self, task):

		#entry = self.obj1.ballHandler.getEntry()
		#if (entry.getIntoNode().getName() == "ground"):
		#	print "IT happend"
		
		for i in range(self.obj1ballHandler.getNumEntries()):
			entry = self.obj1ballHandler.getEntry(i)
			x = entry.getFrom()
			print entry, x
			
		#if (entries[1].getIntoNode() == 'actorRay'):
			#print "Now lets do stuff.."
		
	
		return task.cont


	
class Ball():
	
	def __init__(self):
		
		self.object1 = loader.loadModel("assets/models/collect_ball")
		self.object1.reparentTo(render)
		self.object1.setPos(6, 6, .5)
		
		
		self.ballSphere = CollisionSphere(0, 0, 0, .2)
		self.ballCol = CollisionNode('Ball')
		self.ballCol.addSolid(self.ballSphere)
		#self.ballCol.setFromCollideMask(BitMask32.bit(0x2))
		self.ballCol.setIntoCollideMask(BitMask32.bit(0x2))
		self.ballColNp = self.object1.attachNewNode(self.ballCol)
		






