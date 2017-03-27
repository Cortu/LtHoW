import bge
bge.events.JOY0 = 1000
bge.events.JOY1 = 1001
bge.events.JOY2 = 1002
bge.events.JOY3 = 1003
bge.events.JOY4 = 1004
bge.events.JOY5 = 1005
bge.events.JOY6 = 1006
bge.events.JOY7 = 1007
bge.events.JOY8 = 1008
bge.events.JOY9 = 1009
bge.events.JOY10 = 1010
bge.events.JOY11 = 1011
bge.events.JOY12 = 1012
bge.events.JOY13 = 1013
bge.events.JOY14 = 1014



from types import MethodType as Method
from functools import partial
import util.lib_MIDI as midi

from util.util_main import *
import util.util_tools as tools
import util.util_methods as methods
import util.util_actions as actions
import util.util_classes as classes
import util.util_stuff as stuff
import util.util_widgets as widgets
import util.util_gm as gm


actions
classes
stuff
methods
widgets
midi
gm
Method
partial

from math import pi
turn = 2*pi
turnPercent = 100/turn

sheets = {}
tags = {}
scenes = {}
tools.iniIni('//stuff')
settings = stuff.SystemSettings(sheets['baseSettings'])

timer = tools.Timer()
input = tools.InputCatcher()
load = tools.LoadCounter()







#print(dir(bge.events))
#for event in dir(bge.events):
#    prt = getattr(bge.events, event)
#    print(prt)
