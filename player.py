import sys, os, math, random
from panda3d.core import *
from pandac.PandaModules import *
from direct.actor.Actor import Actor
from direct.task import Task
from panda3d.core import CollisionTraverser,CollisionNode
from panda3d.core import CollisionHandlerQueue,CollisionRay
from direct.showbase.DirectObject import DirectObject
from colHandler import *
# The basic player class.

# GLOBAL for holding active players, bots and other actors.
ACTIVE_ACTORS = {}


class Player(DirectObject):
	"""
	Player Class:
	actorName = Type: player or bot1, bot2, bot3...
	"""
	
	def __init__(self):
		
		# Holds the active Actors.
		#self.activeActors = {}
		#print "activeActors 1st print = ", self.activeActors
		pass
		
	def addActor(self, actorKey, actorObject):
		#self.activeActors[actorKey] = actorObject
		ACTIVE_ACTORS[actorKey] = actorObject

	# Method for setting the player pos.
	# Should be Vec3()
	def setPlayerPos(self, actorName, pos=Vec3(0, 0, 0)):
		ACTIVE_ACTORS[actorName].setPos(pos)
		print "Player: Pos - " + str(pos)
		
	# Method for setting the player speed.
	def setPlayerSpeed(self, actorName, playerSpeed):
		ACTIVE_ACTORS[actorName] = playerSpeed
		print "Player: Speed - " + str(playerSpeed)
	
	# Method for adding items to bag.
	# This will need some re-Thinking.
	def addToBag(self, actorName, slot, items):
		for slot in items:
			ACTIVE_ACTORS[actorName].bag[slot] = items
			#print "Player: Items added - " + item +" "+ items
			print self.bag
			
	# Something maybe for destroying items in bag.
	# This will need redo later.
	# del self.bag[itemToDel]
	def removeFromBag(self, items):
		if items in self.bag:
			self.bag[items].remove #Destroy?
			#print "Player: Items removed - " + item +" "+ items
	
	# Method for adding to xp.
	def addXp(self, actorName, xp):
		ACTIVE_ACTORS[actorName].xp = ACTIVE_ACTORS[actorName].xp + xp
		print "Player: Player XP - " + ACTIVE_ACTORS[actorName].xp
	
	# Method for modifying the player gold.
	def modifyGold(self, actorName, addGold=None, removeGold=None):
		
		if removeGold != None:
			ACTIVE_ACTORS[actorName].playerGold = ACTIVE_ACTORS[actorName].playerGold - removeGold
			
		elif addGold != None:
			ACTIVE_ACTORS[actorName].playerGold = ACTIVE_ACTORS[actorName].playerGold + addGold
			
	# Method for modifying the players Hp.
	def modifyHp(self, actorName, addHp=None, removeHp=None):
		
		if removeHp != None:
			ACTIVE_ACTORS[actorName].hp = ACTIVE_ACTORS[actorName].hp - removeHp
			
		elif addHp != None:
			ACTIVE_ACTORS[actorName].hp = ACTIVE_ACTORS[actorName].hp + addHp
	
	# Method for modifying the players Mana. 
	def modifyMana(self, addMana=None, removeMana=None):
		
		if removeMana != None:
			ACTIVE_ACTORS[actorName].mana = ACTIVE_ACTORS[actorName].mana - removeMana
			
		elif addMana != None:
			ACTIVE_ACTORS[actorName].mana = ACTIVE_ACTORS[actorName].mana + addMana
			
class MakeActor():
	
	"""
	MakeActor Class:
	
	This class handels the creation of player_Actors also bot_Actors.
	"""

	def __init__(self, name):
		
		# Has to get the name from ^s
		# -- #
		self.playerName = name
		print "Player: "+self.playerName+" "+"created"
		
		self.playerSpeed = 25 # Default Speed
		self.isPlayerMoving = False # This should be used with PlayerInput.
		
		# -- #
		self.bag = {} # I thought keep this a dict. for specific sized bags.  Like 10 slot or 15-30.
		self.xp = 0.0 # xp start on 0
		self.playerGold = 0.0 # Gold starts on 0
		self.hp = 100.0 # Basic Hp start
		self.mana = 100.0 # Basic Mane start
		
		# Load the player model and the needed animations.
		self.playerActor = Actor("assets/models/ralph", 
										{"run":"assets/models/ralph-run",
										"walk":"assets/models/ralph-walk"})
		
		self.playerActor.reparentTo(render)
		self.playerActor.setScale(.2)
		self.playerActor.setPos(0, 0, 1) # This will point to the spawnLocation in the level.
		
class PlayerInput(DirectObject):
	
	"""
	PlayerInput Class:
	Handels all inputs.
	"""
	
	def __init__(self):
		
		# Should make a method to get active players.
		self.activePlayer = ACTIVE_ACTORS['Player'].playerActor
		self.activePlayerSpeed = ACTIVE_ACTORS['Player'].playerSpeed
		
		# Set the control maps.
		self.controlMap = {"left": 0, "right": 0, "forward": 0, "backward": 0, "jump": 0, "wheel-in": 0, "wheel-out": 0}  
		self.mousebtn = [0, 0, 0]
		
		# Create a floater object.  We use the "floater" as a temporary
		# variable in a variety of calculations.
		self.floater = NodePath(PandaNode("floater"))
		self.floater.reparentTo(render)
		
		### SETUP KEYBOARD ###
		# Setup the control [KEYS] for movement w,a,s,d.
		self.accept("escape", sys.exit)
		self.accept("w", self.setControl, ["forward", 1])
		self.accept("a", self.setControl, ["left", 1])
		self.accept("s", self.setControl, ["backward", 1])
		self.accept("d", self.setControl, ["right", 1])
		self.accept("space", self.setControl, ["jump", 1])
		
		self.accept("w-up", self.setControl, ["forward", 0])
		self.accept("a-up", self.setControl, ["left", 0])
		self.accept("s-up", self.setControl, ["backward", 0])
		self.accept("d-up", self.setControl, ["right", 0])
		self.accept("space-up", self.setControl, ["jump", 0])
		
		# Setup mouse [ZOOM].
		self.accept("wheel_up", self.setControl, ["wheel-in", 1])
		self.accept("wheel_down", self.setControl, ["wheel-out", 1])
		
		# Add the "moveTask"
		taskMgr.add(self.move, "moveTask")
		
		# Game State Variable.
		self.isMoving = False
		###>
		
		###  SETUP CAMERA  ###
		# Reparent the -main- Camera to playerActor.
		base.camera.reparentTo(self.activePlayer)
		self.cameraTargetHeight = 6.0
		self.cameraDistance = 30
		self.cameraPitch = 10 
		base.disableMouse()
		# This should be used together with a right click function, for the camera rotate. Like in wow.
		WinProps = WindowProperties()
		# Hide the cursor. | This will change with the rightClick function. 
		# Giving us the cursor when not rotating. If the player wants to rotate basic [KEYS] left/right can turn while cursor is active.
		WinProps.setCursorHidden(True) 
		base.win.requestProperties(WinProps)
		#base.camera.setPos(self.activePlayer.getX(),self.activePlayer.getY()+10,2)
		
		# FROM THE ROAMING RALPH TUT>
		# We will detect the height of the terrain by creating a collision
		# ray and casting it downward toward the terrain.  One ray will
		# start above ralph's head, and the other will start above the camera.
		# A ray may hit the terrain, or it may hit a rock or a tree.  If it
		# hits the terrain, we can detect the height.  If it hits anything
		# else, we rule that the move is illegal.

		#self.cTrav = CollisionTraverser()

		self.actorGroundRay = CollisionRay()
		self.actorGroundRay.setOrigin(0,0,1000)
		self.actorGroundRay.setDirection(0,0,-1)
		self.actorGroundCol = CollisionNode('actorRay')
		self.actorGroundCol.addSolid(self.actorGroundRay)
		self.actorGroundCol.setFromCollideMask(BitMask32.bit(0x2))
		self.actorGroundCol.setIntoCollideMask(BitMask32.bit(0x3))
		self.actorGroundColNp = self.activePlayer.attachNewNode(self.actorGroundCol)
		self.actorGroundHandler = CollisionHandlerQueue()
		cTrav.addCollider(self.actorGroundColNp, self.actorGroundHandler)

		# We will detect anything obstructing the camera's view of the player 
 
		self.cameraRay = CollisionSegment((0,0,self.cameraTargetHeight),(0,5,5)) 
		self.cameraCol = CollisionNode('cameraRay') 
		self.cameraCol.addSolid(self.cameraRay) 
		self.cameraCol.setFromCollideMask(BitMask32.bit(0)) 
		self.cameraCol.setIntoCollideMask(BitMask32.allOff()) 
		self.cameraColNp = self.activePlayer.attachNewNode(self.cameraCol) 
		self.cameraColHandler = CollisionHandlerQueue() 
		cTrav.addCollider(self.cameraColNp, self.cameraColHandler) 

		# Uncomment this line to see the collision rays
		self.actorGroundColNp.show()
		self.cameraColNp.show()
	   
		# Uncomment this line to show a visual representation of the 
		# collisions occuring
		cTrav.showCollisions(render)
		
		###>
		
	# Check the state of the KB.
	def setControl(self, key, value):
		self.controlMap[key] = value
		
	def move(self, task):
		
		self.actorPos = self.activePlayer.getPos()
		# Check if a-move key is pressed, if so move.
		# Forward.
		if (self.controlMap["forward"] != 0):
			self.activePlayer.setY(self.activePlayer, -self.activePlayerSpeed * globalClock.getDt())
		# Backward.
		if (self.controlMap["backward"] != 0):
			self.activePlayer.setY(self.activePlayer, self.activePlayerSpeed * globalClock.getDt())
		# Left.
		if (self.controlMap["left"] != 0):
			self.activePlayer.setX(self.activePlayer, self.activePlayerSpeed * globalClock.getDt())
		# Right.
		if (self.controlMap["right"] != 0):
			self.activePlayer.setX(self.activePlayer, -self.activePlayerSpeed * globalClock.getDt())
			
		if (self.controlMap["jump"] != 0):
			self.activePlayer.setZ(10)
		
		# Check for zooming and Do.
		if (self.controlMap["wheel-in"] != 0):
			self.cameraDistance -= 0.1 * self.cameraDistance
			if  (self.cameraDistance < 5):
				self.cameraDistance = 5
			self.controlMap["wheel-in"] = 0
		
		elif (self.controlMap["wheel-out"] != 0):
			self.cameraDistance += 0.1 * self.cameraDistance
			if (self.cameraDistance > 250):
				self.cameraDistance = 250
			self.controlMap["wheel-out"] = 0
			
		# Make use of mouse, to turn.
		if base.mouseWatcherNode.hasMouse():
			
			# get changes in mouse position
			md = base.win.getPointer(0)
			x = md.getX()
			y = md.getY()
			
			deltaX = md.getX() - 200
			deltaY = md.getY() - 200
			
			# reset mouse cursor position
			base.win.movePointer(0, 200, 200)
			
			# Mouse speed setting
			mouseSpeed = 0.3
			
			# alter the actor yaw by an amount proportionate to deltaX
			self.activePlayer.setH(self.activePlayer.getH() - mouseSpeed* deltaX)

			# find the new camera pitch and clamp it to a reasonable range
			self.cameraPitch = self.cameraPitch + 0.1 * deltaY
			if (self.cameraPitch < -60): self.cameraPitch = -60
			if (self.cameraPitch >  80): self.cameraPitch =  80
			base.camera.setHpr(0,self.cameraPitch,0)
			
			# set the camera at around middle of the ship
			# We should pivot around here instead of the view target which is noticebly higher
			base.camera.setPos(0,0,self.cameraTargetHeight/2)
			# back the camera out to its proper distance
			base.camera.setY(base.camera,self.cameraDistance)
		
		# point the camera at the view target 
		viewTarget = Point3(0,0,self.cameraTargetHeight) 
		base.camera.lookAt(viewTarget) 
		# reposition the end of the  camera's obstruction ray trace 
		self.cameraRay.setPointB(base.camera.getPos())
		
		# If ralph is moving, loop the run animation.
		# If he is standing still, stop the animation.

		if (self.controlMap["forward"]!=0) or (self.controlMap["left"]!=0) or (self.controlMap["right"]!=0):
			if self.isMoving is False:
				self.activePlayer.loop("run")
				self.isMoving = True
		else:
			if self.isMoving:
				self.activePlayer.stop()
				self.activePlayer.pose("walk",5)
				self.isMoving = False
		
		# Now check for collisions.

		cTrav.traverse(render)

		# Adjust ralph's Z coordinate.  If ralph's ray hit terrain,
		# update his Z. If it hit anything else, or didn't hit anything, put
		# him back where he was last frame.

		entries = []
		for i in range(self.actorGroundHandler.getNumEntries()):
			entry = self.actorGroundHandler.getEntry(i)
			entries.append(entry)
		entries.sort(lambda x,y: cmp(y.getSurfacePoint(render).getZ(),
									 x.getSurfacePoint(render).getZ()))
		if (len(entries)>0) and (entries[0].getIntoNode().getName() == "ground"):
			self.activePlayer.setZ(entries[0].getSurfacePoint(render).getZ())
		else:
			self.activePlayer.setPos(self.actorPos)

		# Keep the camera at one foot above the terrain,
		# or two feet above ralph, whichever is greater.
		
		entries = [] 
		for i in range(self.cameraColHandler.getNumEntries()): 
			entry = self.cameraColHandler.getEntry(i) 
			entries.append(entry) 
		entries.sort(lambda x,y: cmp(-y.getSurfacePoint(self.activePlayer).getY(), 
									 -x.getSurfacePoint(self.activePlayer).getY())) 
		if (len(entries)>0): 
			collisionPoint =  entries[0].getSurfacePoint(self.activePlayer) 
			collisionVec = ( viewTarget - collisionPoint) 
			if ( collisionVec.lengthSquared() < self.cameraDistance * self.cameraDistance ): 
				base.camera.setPos(collisionPoint) 
				if (entries[0].getIntoNode().getName() == "ground"): 
					base.camera.setZ(base.camera, 0.2) 
				base.camera.setY(base.camera, 0.3) 
				
		return task.cont   
		
	
###>   
