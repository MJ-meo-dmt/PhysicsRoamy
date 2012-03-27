
#		2D -.-

#  create a very small and simple rpg game (2d)
#
#



# Main class

from pandac.PandaModules import loadPrcFileData
loadPrcFileData("",
"""	
	window-title Project - 2D
	fullscreen 0
	win-size 1024 768
	cursor-hidden 0
	sync-video 1
	frame-rate-meter-update-interval 0.5
	show-frame-rate-meter 1
"""
)
from panda3d.core import TextNode
from direct.gui.OnscreenText import OnscreenText

from player import *
from world import *
from colHandler import *
# For Showbase (main class)
from direct.showbase.ShowBase import ShowBase

# For Login state

# For MainMenu state

# For Pregame state

# For Preround state

# For Round state


# For starting the server from within the game
from subprocess import *
# For exit function
import sys

# Use to display text on screen.
def genLabelText(text, i):
  return OnscreenText(text = text, pos = (-1.3, .95-.05*i), fg=(1,1,0,1),
					  align = TextNode.ALeft, scale = .05)

class Main(ShowBase):
	
	def __init__(self):
		ShowBase.__init__(self)
		
		# Starting the main menu.
		self.start_mainmenu()
		self.start_round()
	
	def start_mainmenu(self):
		
		# TO display some text onscreen.
		self.title = OnscreenText(text="Project Roamy",
							  style=1, fg=(1,1,0,1),
							  pos=(0.8,-0.95), scale = .07)
		self.escapeText =   genLabelText("ESC: Quit", 0)
		self.leftkeyText =  genLabelText("[Left Arrow]: Turn Left (CCW)", 1)
		self.rightkeyText = genLabelText("[Right Arrow]: Turn Right (CW)", 2)
		self.upkeyText =	genLabelText("[Up Arrow]: Accelerate", 3)
		# This should change to Mousebutton.(1)
		self.spacekeyText = genLabelText("[Space Bar]: Jump", 4)
		
		#------>
		
		# Maybe add a gui here like start game or something instead of the simple text.
	
	def start_pregame(self):
		pass
	
	def start_round(self):
		print "start_round() !"
	
		w=World()
		stage1 = Level("Stage 1", "assets/levels/stage1")
		w.addLevel(1, stage1)
		
		
		p=Player()
		self.player = MakeActor('Player')
		p.addActor('Player', self.player)
		print "2nd Active print ", ACTIVE_ACTORS
		self.pInput=PlayerInput()
		
		
		
	def host_game(self,params):
		#pid = Popen(["python", "server_inst.py", params]).pid
		pass
		
	def quit(self):
		sys.exit()

game = Main()
game.run()


