import util
import bge

def ini(cont):
    pass


def subSheet(cont):
    import util
    own = cont.owner
    sheet = util.sheets[own['type']]
    own = util.subStuff(own, sheet)

def subOther(cont):
    import util
    own = cont.owner
    own = util.subOtherStuff(own, own['type'])

def subWidget(cont):
    import util
    own = cont.owner
    own = util.subWidget(own, own['type'])

def subGM(cont):
    import util
    own = cont.owner
    own = util.subGM(own, own['type'])



def run(cont):
    cont.owner.run()
    
def input(cont):
    cont.owner.input()

def update(cont):
    cont.owner.update()


def message(cont):
    for num, subject in enumerate(cont.sensors['Message'].subjects):
        body = cont.sensors['Message'].bodies[num]
        cont.owner.message(subject, body)

def ai(cont):
    cont.owner.ai()




#Other#
def iniFret(cont):
    import util
    own = cont.owner
    own = util.classes.FretBoard(own)

def runNoteNova(cont):
    own = cont.owner
    if own.visible and not own.isPlayingAction():
        own.endObject()

def runJib(cont):
    cont.owner.parent.runJib()

def iniScene(cont):
    scene = cont.owner.scene
    util.scenes[scene.name] = scene


def iniMain(cont):
    bge.logic.addScene('Hud')

def iniKilnMenu(cont):
    bge.logic.addScene('Kiln', 0)
    #for char in util.input.select:    char.camera = 3

def subKiln(cont):
    own = cont.owner
    scene = util.getScene('Main')
    jinni = scene.objects['Main JinniGM']
    sheet = jinni.sheet
    
    
    own = util.subStuff(own, sheet)
    util.input.select = set([own])
    
    



def runTargJinniGM(cont):
    pass
#    for char in util.input.select:
#        objs = bge.logic.getCurrentScene
#        char.cheek = Scroller.CheekBrow['x']
#        char.brow = float(sheet['Targets']['brow'])
#        char.ear = float(sheet['Targets']['ear'])
#        char.mouth = float(sheet['Targets']['mouth'])
#        char.rotate = float(sheet['Targets']['rotate'])
#        char.lid = float(sheet['Targets']['lid'])
#        char.greek = float(sheet['Targets']['greek'])
#        char.curve = float(sheet['Targets']['curve'])
#        char.size = float(sheet['Targets']['size'])
#        char.width = float(sheet['Targets']['width'])
#        char.volume = float(sheet['Targets']['volume'])
#        char.height = float(sheet['Targets']['height'])
#        char.chin = float(sheet['Targets']['chin'])
#        char.jaw = float(sheet['Targets']['jaw'])
#        char.afro = float(sheet['Targets']['afro'])
#        char.euro = float(sheet['Targets']['euro'])
#        char.asio = float(sheet['Targets']['asio'])


def mouseMain(cont):
    import util
    util.input.catch()
    keys = util.settings
    Click = util.input.Click
    
    cursor = util.scenes['Hud'].objects['Cursor']
    hitObj = util.input.window
    
    if hitObj:
        cursor.color = [0.0, 0.0, 1.0, 0.5]
    else:
        cursor.color = [0.0, 1.0, 0.0, 0.5]
    
    if {keys.activate, 'activate'} <= Click:
        hitObj.activate()
    
    if {keys.context, 'context'} <= Click:
        hitObj.context()

#Widgets#
def scrollerY(cont):
    cont.owner.scrollY = cont.sensors['propY'].owner['y']
    
def scrollerX(cont):
    cont.owner.scrollX = cont.sensors['propX'].owner['x']



def testBloc(cont):
    own = cont.owner
    text = """
1...................
a...................
2...................
b...................
3...................
c...................
4...................
d...................
5...................
e...................
6...................
f...................
7...................
g...................
8...................
h...................
9...................
i...................
10..................
j...................
11..................
k...................
12..................
l...................
    """
    own.text = text

def testMani(cont):
    items = []
    #util.input.maniTags = 'equipment'
    for item in util.tags[util.input.maniTags]:
        items.append(item)
    cont.owner.text = items



def scrollUp(cont):
    cont.owner.y += 0.04
def scrollDown(cont):
    cont.owner.y -= 0.04
def scrollRight(cont):
    cont.owner.x += 0.04
def scrollLeft(cont):
    cont.owner.x -= 0.04

def testBloc4(cont):
    own = cont.owner
    sens = cont.sensors
    own.scroll = 1-sens['propY'].owner.y



def test2(cont):
    own = cont.owner
    own.source = '/media/porto/1Tb1/Code/JukeBox/stuff/equipment/accessory/Earphones/thumb.png'


def test3(cont):
    print('t3', cont.owner.state)

def test4(cont):
    print('t4', cont.owner.state)

def test5(cont):
    print('t5', cont.owner.state)






def setStateB(state, stateNum, opperation):
    state = list(format(state, 'b').rjust(30, '0'))
    stateNum = 30 -stateNum
    #print(state[stateNum])
    if opperation == 'on':
        state[stateNum] = '1'
    elif opperation == 'off':
        state[stateNum] = '0'
    elif opperation == 'toggle':
        if state[stateNum] == '1':
            state[stateNum] = '0'
        else:
            state[stateNum] = '1'
    else:
        raise
    #print(''.join(state))
    return int(''.join(state), 2)



def testB(cont):
    from math import sqrt
    state = cont.owner.state
    print('t1', cont.owner.state)
    prt = sqrt(state)
    prt = state
    prt = int('1000000000000000000000000000', 2)*2
    prt = '0'.ljust(30, '0')
    prt = ''.zfill(30)
    prt = bin(state)
    
    prt = format(state, 'b').rjust(30, '0')
    prt = list(prt)
    prt = ''.join(prt)
    
    #print(int(prt, 2), state)
    prt = setState(cont.owner.state, 1, 'off')
    #print(prt)
    #cont.owner.state = setState(cont.owner.state, 20, 'on')
    #cont.owner.state = setState(cont.owner.state, 13, 'on')
    #cont.owner.state = setState(cont.owner.state, 22, 'off')
    #cont.owner.state = setState(cont.owner.state, 1, 'off')
    
    #state = cont.owner.state
    #state = list(format(state, 'b').rjust(30, '0'))
    cont.owner.state = setState(cont.owner.state, 13, 'on')
    cont.owner.state = setState(cont.owner.state, 1, 'off')
    
    #print(state)
    #cont.owner.state = int(state, 2)
    
    #cont.owner.state = 528385
    #cont.owner.state = 524288
    #cont.owner.state = 513





def setState(state, stateNum, opperation):
    state = list(format(state, 'b').rjust(30, '0'))
    stateNum = 30 -stateNum
    
    if opperation == 'on':    state[stateNum] = '1'
    elif opperation == 'off':    state[stateNum] = '0'
    
    elif opperation == 'toggle':
        if state[stateNum] == '1':    state[stateNum] = '0'
        else:    state[stateNum] = '1'
    
    else:    raise Exception("My hovercraft is full of eels")
    
    return int(''.join(state), 2)








def test(cont):
    print('t1', cont.owner.state)
    cont.owner.state = util.setState(cont.owner.state, 13, 'on')
    cont.owner.state = util.setState(cont.owner.state, 20, 'on')
    cont.owner.state = util.setState(cont.owner.state, 1, 'off')








