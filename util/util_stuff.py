import util
import bge
############
" Settings "
############
class SystemSettings:
   
    def __repr__(self):
        return 'SystemSettings'
    
    def __init__(settings, sheet):
        settings.uId = sheet['Discription']['uId']
        settings.type = sheet['Discription']['type']
        #Path#
        settings.pathIni = sheet['Path']['ini']
        
        #Main#
        settings.songBufferTime = float(sheet['Main']['songBufferTime'])
        settings.songHitTime = float(sheet['Main']['songHitTime'])
        settings.songMissMod = float(sheet['Main']['songMissMod'])
        settings.songMissInc = float(sheet['Main']['songMissInc'])
        
        settings.timePause = float(sheet['Main']['timePause'])
        settings.timeFast = float(sheet['Main']['timeFast'])
        settings.timeSlow = float(sheet['Main']['timeSlow'])
        
        #Keybinds#
        settings.activate = getattr(bge.events, sheet['Keybinds']['activate'])
        settings.context = getattr(bge.events, sheet['Keybinds']['context'])
        settings.scrollUp = getattr(bge.events, sheet['Keybinds']['scrollUp'])
        settings.scrollDown = getattr(bge.events, sheet['Keybinds']['scrollDown'])
        settings.camera = getattr(bge.events, sheet['Keybinds']['camera'])
        settings.mode = getattr(bge.events, sheet['Keybinds']['mode'])
        settings.accept = getattr(bge.events, sheet['Keybinds']['accept'])
        settings.cancel = getattr(bge.events, sheet['Keybinds']['cancel'])
        
        settings.select = getattr(bge.events, sheet['Keybinds']['select'])
        settings.move = getattr(bge.events, sheet['Keybinds']['move'])
        
        
        settings.cam0 = getattr(bge.events, sheet['Keybinds']['cam0'])
        settings.cam1 = getattr(bge.events, sheet['Keybinds']['cam1'])
        settings.cam2 = getattr(bge.events, sheet['Keybinds']['cam2'])
        settings.cam3 = getattr(bge.events, sheet['Keybinds']['cam3'])
        settings.cam4 = getattr(bge.events, sheet['Keybinds']['cam4'])
        
        settings.openMap = getattr(bge.events, sheet['Keybinds']['openMap'])
        settings.forward = getattr(bge.events, sheet['Keybinds']['forward'])
        settings.backward = getattr(bge.events, sheet['Keybinds']['backward'])
        settings.leftward = getattr(bge.events, sheet['Keybinds']['leftward'])
        settings.rightward = getattr(bge.events, sheet['Keybinds']['rightward'])
        settings.runward = getattr(bge.events, sheet['Keybinds']['runward'])
        settings.spaceward = getattr(bge.events, sheet['Keybinds']['spaceward'])
        
        settings.pBreak = getattr(bge.events, sheet['Keybinds']['pBreak'])
        
        settings.fretA = getattr(bge.events, sheet['Keybinds']['fretA'])
        settings.fretB = getattr(bge.events, sheet['Keybinds']['fretB'])
        settings.fretC = getattr(bge.events, sheet['Keybinds']['fretC'])
        settings.fretD = getattr(bge.events, sheet['Keybinds']['fretD'])
        settings.fretE = getattr(bge.events, sheet['Keybinds']['fretE'])
        settings.strum = getattr(bge.events, sheet['Keybinds']['strum'])

        settings.speedPause = getattr(bge.events, sheet['Keybinds']['speedPause'])
        settings.speedSlow = getattr(bge.events, sheet['Keybinds']['speedSlow'])
        settings.speedNormal = getattr(bge.events, sheet['Keybinds']['speedNormal'])
        settings.speedFast = getattr(bge.events, sheet['Keybinds']['speedFast'])
        



    def saveIni(settings):
        import configparser
        config = configparser.ConfigParser()
        config.read(settings.pathIni)
        config['Test'] = {}
        config['Test']['test'] = bge.events.EventToString(settings.activate)
        
        with open(settings.pathIni, 'w') as configfile:
            config.write(configfile)



def camera_getter(gameObj):
    return gameObj._camera

def camera_setter(gameObj, num):
    cam = gameObj.cams[num]
    jib = gameObj.jibs[num]
    if gameObj.active:    gameObj.scene.active_camera = cam
    gameObj._cameraNum = num
    gameObj._camera = cam
    gameObj._jib = jib

def cameraNum_getter(gameObj):
    return gameObj._cameraNum

def jib_getter(gameObj):
    return gameObj._jib


def onLedge_getter(gameObj, lvl):
    sen = getattr(gameObj,  'lvl'+lvl).sensors['Ray']
    if sen.hitObject:
        return gameObj.getDistanceTo(sen.hitPosition)
    else:    return False




def charTarg_getter(char, targ, locScl, axis):
    bone = char.arma.channels[targ]
    vec = getattr(bone, locScl)
    return getattr(vec, axis)


def charTarg_setter(char, valu, targ, locScl, axis):
    bone = char.arma.channels[targ]
    vec = getattr(bone, locScl)
    setattr(vec, axis, valu)
    setattr(bone, locScl, vec)
    char.arma.update()
    
    
def charPheno_getter(char):
    return char._pheno

def charPheno_setter(char, uId):
    char.body.replaceMesh(uId+' Mesh')
    char._pheno = uId
    if uId == 'baseMixoF' or uId == 'baseMixoM':
        char.afro = 0.0
        char.asio = 0.0
        char.euro = 0.0
    if uId == 'baseAfroF' or uId == 'baseAfroM':
        char.afro = 1.0
        char.asio = 0.0
        char.euro = 0.0
    if uId == 'baseAsioF' or uId == 'baseAsioM':
        char.afro = 0.0
        char.asio = 1.0
        char.euro = 0.0
    if uId == 'baseEuroF' or uId == 'baseEuroM':
        char.afro = 0.0
        char.asio = 0.0
        char.euro = 1.0


def child_getter(gameObj, child):
    name = gameObj.name.split('.')
    try:    suffix = name[1]
    except IndexError: suffix = ''
    return gameObj.childrenRecursive[name[0] +' '+child+ suffix]

def camActive_getter(char):
    for jib in char.jibs:
        if jib['active']:
            return True
    return False

def camActive_setter(char, bool):
    for jib in char.jibs:
        if jib:
            jib['active'] = bool


def runJib(char):
    jib = char.jib
    cam = char.camera
    hit = jib.sensors['Ray'].hitPosition
    if hit == [0.0, 0.0, 0.0]:
        cam.localPosition.z = jib.sensors['Ray'].range
    else:
        cam.worldPosition = hit
        cam.localPosition.z -= 0.1






def charSlot_setter(char, uId, slot):
    sheet = util.sheets[uId]
    slot = char.child(slot.capitalize())
    #slot = char.children[char.name+' Arma'].children[char.name+' '+slot.capitalize()]
    slot = util.classes.Equipment(slot, sheet)
    util.load[slot.pathMeshFemale] += 1
    util.load.updateModules()
    slot.replaceMesh(slot.uId +' Mesh')

def charSlot_getter(char, slot):
    #return char.children[char.name+' Arma'].children[char.name+' '+slot.capitalize()]
    return char.child(slot.capitalize())



def charWepon_getter(char, hand):
    #return getattr(char, '_'+hand)
    return getattr(char, 'slot'+hand)['wepon']


def charWepon_setter(char, uId, hand):
#    oldObj = getattr(char, hand)
#    sheet = util.sheets[uId]
#    util.load[sheet['Path']['pathMesh']] +=1
#    try:    util.load[oldObj.pathMesh] -=1
#    except AttributeError:    pass
#    util.load.updateModules()
#    newObj = char.scene.addObject(uId, oldObj)
#    newObj.setParent(oldObj.parent)
#    oldObj.endObject()
#    char._left = util.classes.Wepon(newObj, sheet)
    
    slot = getattr(char, 'slot'+hand.capitalize())
    sheet = util.sheets[uId]
    util.load[sheet['Path']['pathMesh']] +=1
    
    try:
        oldObj = slot['wepon']
        util.load[oldObj.pathMesh] -=1
        oldObj.endObject()
    except KeyError:    pass
    util.load.updateModules()
    
    newObj = char.scene.addObject(uId, slot)
    newObj = util.classes.Wepon(newObj, sheet)
    newObj.setParent(slot)
    slot['wepon'] = newObj
    







def timerStart(timer, valu, storage):
    startStop = [bge.logic.getFrameTime(), valu]
    setattr(timer, storage, startStop)

def timerCurrent(timer, storage):
    return bge.logic.getFrameTime() - getattr(timer, storage)[0]

def timerRemaing(timer, storage):
    return getattr(timer, storage)[1] - (bge.logic.getFrameTime() - getattr(timer, storage)[0])




class Character_REAL(bge.types.KX_GameObject):
    speed = property(util.methods.speedMps2Kph)
    
    timeJump = property(
        util.partial(timerCurrent, storage = '_timeJump'),
        util.partial(timerStart, storage = '_timeJump'))
    timeAction = property(
        util.partial(timerCurrent, storage = '_timeAction'),
        util.partial(timerStart, storage = '_timeAction')) 
    
    
    
    
    child = util.child_getter
    sortDist = util.sortByDistance
    
    
    
    
    cameraNum = property(cameraNum_getter, camera_setter)
    camera = property(camera_getter, camera_setter)
    jib = property(jib_getter, camera_setter)
    camEnabled = property(camActive_getter, camActive_setter)
    runJib = runJib
    
    onGround = property(util.methods.onGround)
    onWall = property(util.methods.onWall)
    onLedge = property(util.partial(onLedge_getter, lvl='Ledge'))
    onMid = property(util.partial(onLedge_getter, lvl='Mid'))
    onLeg = property(util.partial(onLedge_getter, lvl='Leg'))
    
    hair = property(
        util.partial(charSlot_getter, slot='hair'),
        util.partial(charSlot_setter, slot='hair'))
    hands = property(
        util.partial(charSlot_getter, slot='hands'),
        util.partial(charSlot_setter, slot='hands'))
    torso = property(
        util.partial(charSlot_getter, slot='torso'),
        util.partial(charSlot_setter, slot='torso'))
    legs = property(
        util.partial(charSlot_getter, slot='legs'),
        util.partial(charSlot_setter, slot='legs'))
    feet = property(
        util.partial(charSlot_getter, slot='feet'),
        util.partial(charSlot_setter, slot='feet'))
    accessory = property(
        util.partial(charSlot_getter, slot='accessory'),
        util.partial(charSlot_setter, slot='accessory'))
    left = property(
        util.partial(charWepon_getter, hand='left'),
        util.partial(charWepon_setter, hand='left'))
    right = property(
        util.partial(charWepon_getter, hand='right'),
        util.partial(charWepon_setter, hand='right'))

    cheek = property(
        util.partial(charTarg_getter, targ='targ1', locScl='location', axis='x'),
        util.partial(charTarg_setter, targ='targ1', locScl='location', axis='x'))
    brow = property(
        util.partial(charTarg_getter, targ='targ1', locScl='location', axis='y'),
        util.partial(charTarg_setter, targ='targ1', locScl='location', axis='y'))
    ear = property(
        util.partial(charTarg_getter, targ='targ1', locScl='location', axis='z'),
        util.partial(charTarg_setter, targ='targ1', locScl='location', axis='z'))
    mouth = property(
        util.partial(charTarg_getter, targ='targ1', locScl='scale', axis='x'),
        util.partial(charTarg_setter, targ='targ1', locScl='scale', axis='x'))
    rotate = property(
        util.partial(charTarg_getter, targ='targ1', locScl='scale', axis='y'),
        util.partial(charTarg_setter, targ='targ1', locScl='scale', axis='y'))
    lid = property(
        util.partial(charTarg_getter, targ='targ1', locScl='scale', axis='z'),
        util.partial(charTarg_setter, targ='targ1', locScl='scale', axis='z'))
    greek = property(
        util.partial(charTarg_getter, targ='targ2', locScl='location', axis='x'),
        util.partial(charTarg_setter, targ='targ2', locScl='location', axis='x'))
    curve = property(
        util.partial(charTarg_getter, targ='targ2', locScl='location', axis='y'),
        util.partial(charTarg_setter, targ='targ2', locScl='location', axis='y'))
    size = property(
        util.partial(charTarg_getter, targ='targ2', locScl='location', axis='z'),
        util.partial(charTarg_setter, targ='targ2', locScl='location', axis='z'))
    width = property(
        util.partial(charTarg_getter, targ='targ2', locScl='scale', axis='x'),
        util.partial(charTarg_setter, targ='targ2', locScl='scale', axis='x'))
    volume = property(
        util.partial(charTarg_getter, targ='targ2', locScl='scale', axis='y'),
        util.partial(charTarg_setter, targ='targ2', locScl='scale', axis='y'))
    height = property(
        util.partial(charTarg_getter, targ='targ2', locScl='scale', axis='z'),
        util.partial(charTarg_setter, targ='targ2', locScl='scale', axis='z'))
    chin = property(
        util.partial(charTarg_getter, targ='targ3', locScl='location', axis='x'),
        util.partial(charTarg_setter, targ='targ3', locScl='location', axis='x'))
    jaw = property(
        util.partial(charTarg_getter, targ='targ3', locScl='location', axis='y'),
        util.partial(charTarg_setter, targ='targ3', locScl='location', axis='y'))
    afro = property(
        util.partial(charTarg_getter, targ='targ3', locScl='location', axis='z'),
        util.partial(charTarg_setter, targ='targ3', locScl='location', axis='z'))
    euro = property(
        util.partial(charTarg_getter, targ='targ3', locScl='scale', axis='x'),
        util.partial(charTarg_setter, targ='targ3', locScl='scale', axis='x'))
    asio = property(
        util.partial(charTarg_getter, targ='targ3', locScl='scale', axis='y'),
        util.partial(charTarg_setter, targ='targ3', locScl='scale', axis='y'))
    
    pheno = property(charPheno_getter, charPheno_setter)
    
    def __init__(char, DNU, sheet):
        
        #Discription#
        char.uId = sheet['Discription']['uId']
        char.nameProper = sheet['Discription']['nameProper']
        char.discription = sheet['Discription']['discription']
        char.type = sheet['Discription']['type']
        char.tags = set()
        for tag in sheet['Discription']['tags'].split(','):    char.tags.add(tag)
        
        #char.arma = char.children[char.name+' Arma']
        char.arma = char.child('Arma')
        char.jibs = []
        char.jibs.append(None)
        #char.jibs.append(char.children[char.name+' Jib1'])
        char.jibs.append(char.child('Jib1'))
        char.jibs.append(None)
        #char.jibs.append(char.children[char.name+' Jib3'])
        char.jibs.append(char.child('Jib3'))
        char.jibs.append(char.child('Jib4'))
        
        char.cams = []
        char.cams.append(None)
        #char.cams.append(char.jibs[1].children[char.name+' Cam1'])
        char.cams.append(char.child('Cam1'))
        char.cams.append(None)
        #char.cams.append(char.jibs[3].children[char.name+' Cam3'])
        char.cams.append(char.child('Cam3'))
        char.cams.append(char.child('Cam4'))
        
        char.active = True
        char.camera = 1
        char.camEnabled = False
        #util.input.select.add(char)
        util.input.select = char
        
        
        char.lvlLedge = char.child('lvlLedge')
        char.lvlMid = char.child('lvlMid')
        char.lvlLeg = char.child('lvlLeg')
        char.lvlGround = char.child('lvlGround')
        char.coliSet = set()
        char.coliFlush = util.Method(util.methods.coliFlush, char.coliSet)
        char.collisionCallbacks.append( util.Method(util.methods.collisionRegister, char) )
        
        #Path#
        char.pathThumbNail = sheet['Path']['pathThumbNail']
        
        #Equip#
        def setSlot(name):
            slotSheet = util.sheets[sheet['Equip'][name]]
            slot = char.children[char.name+' Arma'].children[char.name+' '+name.capitalize()]
            slot = util.classes.Equipment(slot, slotSheet)
            util.load[slot.pathMeshFemale] += 1
            util.load.updateModules()
            slot.replaceMesh(slot.uId +' Mesh')
            return slot
        char.body = char.child('Body')
        char.eyes = char.child('Eyes')
        char.body.visible = True
        char.eyes.visible = True
        
        
#        charSlot_setter(char, sheet['Equip']['hair'], 'hair')
#        char.hair = setSlot('hair')
#        char.hands = setSlot('hands')
#        char.torso = setSlot('torso')
#        char.legs = setSlot('legs')
#        char.feet = setSlot('feet')
#        char.accessory = setSlot('accessory')

        char.hair = sheet['Equip']['hair']
        char.hands = sheet['Equip']['hands']
        char.torso = sheet['Equip']['torso']
        char.legs = sheet['Equip']['legs']
        char.feet = sheet['Equip']['feet']
        char.accessory = sheet['Equip']['accessory']
        
        
        char.slotLeft = char.child('Wepon LeftHand')
        char.slotRight = char.child('Wepon RightHand')
        char.left = sheet['Equip']['weponL']
        char.right = sheet['Equip']['weponR']
        #Targets#
        char.cheek = float(sheet['Targets']['cheek'])
        char.brow = float(sheet['Targets']['brow'])
        char.ear = float(sheet['Targets']['ear'])
        char.mouth = float(sheet['Targets']['mouth'])
        char.rotate = float(sheet['Targets']['rotate'])
        char.lid = float(sheet['Targets']['lid'])
        char.greek = float(sheet['Targets']['greek'])
        char.curve = float(sheet['Targets']['curve'])
        char.size = float(sheet['Targets']['size'])
        char.width = float(sheet['Targets']['width'])
        char.volume = float(sheet['Targets']['volume'])
        char.height = float(sheet['Targets']['height'])
        char.chin = float(sheet['Targets']['chin'])
        char.jaw = float(sheet['Targets']['jaw'])
        #char.afro = float(sheet['Targets']['afro'])
        #char.euro = float(sheet['Targets']['euro'])
        #char.asio = float(sheet['Targets']['asio'])
        char.pheno = sheet['Targets']['pheno']
        
        
        #Attack#
        char.attks = []
        char.deffs = []
        char.stances = []
        
        def makeAttk(uId, storage):
            sheet = util.sheets[uId]
            attk = util.classes.Attack(sheet, char)
            storage.append(attk)
            util.load[attk.pathAniAttk] += 1
            util.load[attk.pathAniDeff] += 1
            
        for i in range(8):
            attk = sheet['Attack']['a'+str(i)]
            deff = sheet['Attack']['d'+str(i)]
            stan = sheet['Attack']['s'+str(i)]

            if attk != 'none':    makeAttk(attk, char.attks)
            if deff != 'none':    makeAttk(deff, char.deffs)
            if stan != 'none':    makeAttk(stan, char.stans)
        
        util.load.updateModules()

        
        
        
        
        
        
        char._timeJump = 0.0
        char.maxJump = 0.2
        
        
        
        
#        char.targ1 = char.arma.channels['targ1']
#        char.targ1 = char.arma.channels['targ2']
#        char.targ1 = char.arma.channels['targ3']

#        charTarg_setter(char, 'targ1', 'location', 'x', 1.0)
#        charTarg_setter(char, 'targ1', 'location', 'y', 1.0)
#        charTarg_setter(char, 'targ1', 'location', 'z', 1.0)









        char.scene.active_camera = char.scene.objects['Camera']
        char.move = char.child('Move')
        char.attkPost = char.child('AttkPost')
        
        
        
        
        
        
        
        char.hitPosts = set()
        for i in range(6):
            char.hitPosts.add(char.child('HitPost '+str(i)))
        
        char.gm = char.scene.objects['JinniGM']
        if char['team'] == 'red':
            char.teamColor = [1.0, 0.0, 0.0]
            char.allys = char.gm.red
            char.allys.add(char)
            char.enemys = char.gm.blue
        elif char['team'] == 'blue':
            char.teamColor = [0.0, 0.0, 1.0]
            char.allys = char.gm.blue
            char.allys.add(char)
            char.enemys = char.gm.red
        
        
        
        
        
        char.action = 'idel'
    
        
        
        
        
        
    
    
    

    def run(char):
        #coli = char.coliSet
        #print(len(char.coliSet))
        #print(char.getActionName())
        #print(char.isPlayingAction())
#        cont = bge.logic.getCurrentController()
#        hup = cont.actuators['Hup']
#        cont.deactivate(hup)
#        if char.getActionName()== 'Hup' and char.getActionFrame() < 95.0:
#            cont = bge.logic.getCurrentController()
#            hup = cont.actuators['Hup']
#            cont.deactivate(hup)
#            
#            char.stopAction()
#            print(char.getActionFrame())
        #char.stopAction()
        
#        char.coliFlush()
#        if not char.arma.isPlayingAction():
#            if char.onGround and char.action =='idel':
#                if -0.00001 < char.speed < 0.00001:
#                    #frame = char.arma.getActionFrame()
#                    #char.arma.playAction('walk', 1, 100, play_mode = bge.logic.KX_ACTION_MODE_LOOP, blendin=6)
#                    #char.arma.playAction('onLedge', 1, 1, blendin=6)
#                    #print(char.arma.getActionFrame())
#                    char.arma.playAction('walk', 1, 100)
#                    pass
#                else:
#                    pass
#                    #char.arma.playAction('walk', 1, 90, play_mode = bge.logic.KX_ACTION_MODE_LOOP, speed = abs(char.speed), blendin=6)
#
#            if char.onLedge and not char.onGround:
#                pass
#                #char.arma.playAction('onLedge', 1, 2, blendin=1)
        
        
        if char.onGround or char.onLedge:
            force = -char.scene.gravity.z * char.mass
            char.applyForce((0, 0, force))
            char.localLinearVelocity = 0, 0, 0
            char.timeJump = 0.0
        
        
#        postChar = char.scene.active_camera.getScreenPosition(char)
#        postMouse = bge.logic.mouse.position
#        #print(postChar, postMouse)
#        
#        from mathutils import Vector, Euler
#        from math import atan, pi
#        #vec = char.worldOrientation.
#        x = postChar[0] - postMouse[0]
#        y = postChar[1] - postMouse[1]
#        #x = 2
#        #y = 0
#        #z = -1
#        #z = char.worldOrientation.z
#        #char.worldOrientation = x, y, z
#        agl = atan(x/y)
#        if y < 0:
#            agl = agl + pi
#        #print(agl /util.turn)
#        eul = Euler((0.0, 0.0, agl))
#        #vec = Vector((x, y, z))
#        #char.alignAxisToVect(vec, 1)
#        char.worldOrientation = eul
        
        
        
        
#    def runJib(char):
#        jib = char.jib
#        cam = char.camera
#        hit = jib.sensors['Ray'].hitPosition
#        if hit == [0.0, 0.0, 0.0]:
#            cam.localPosition.z = jib.sensors['Ray'].range
#        else:
#            cam.worldPosition = hit
#            cam.localPosition.z -= 0.1
    
    def getNearTarget(char):
        from random import choice
        attk = char.attkPost
        enemy = char.sortDist(list(char.enemys))[0]
        
        hitSet = set()
        for hit in enemy.hitPosts:
            if attk.rayCastTo(hit) == enemy:
                hitSet.add(hit)
        return enemy, choice(tuple(hitSet))
        
    
    
    def ai(char):
        
        if char.action == 'idel':
            
            
        
        
            
            enemy, hit = char.getNearTarget()
#            attk = char.attkPost
#            vec = attk.getVectTo(hit)[1]
#            vec.magnitude = attk.getVectTo(hit)[0]
#            from mathutils import Euler
#            accuY = 0.05     #up down, about 0.1 - 0.01
#            accuZ = 0.05     #left right, low is better
#            from random import gauss
#            eul = Euler((0.0, gauss(0, accuY), gauss(0, accuZ)))
#            vec.rotate(eul)
#            vec = vec + attk.worldPosition
#            import Rasterizer
#            Rasterizer.drawLine(attk.worldPosition, vec, char.teamColor)
            
            
            char.action = char.attks[2]
            char.action.target = enemy
            char.action.aim = hit
            char.timeAction = char.action.proc[2]
            char.actionStage = 0
            char.arma.playAction(char.action.aniAttk, char.action.proc[0], char.action.proc[2])
            
            
        if char.action.type == 'Attack':
            if char.actionStage == 0:
                print('start')
                char.actionStage = 1
            if char.actionStage == 1 and char.timeAction > char.action.proc[1]/24:
                char.action.run(char.action.target)
                char.actionStage = 2
            if char.actionStage == 2 and char.timeAction > char.action.proc[2]/24:
                print('fin')
                char.action = 'idel'
            
            
    
    
    
    
    
    def input(char):
        keys = util.settings
        Click = util.input.Click
        reClick = util.input.reClick
        # 1.5-2.5 mps walk, 12 mps run, 60 fps, about 0.03 * 5
        speed = 0.0746 *25
        from mathutils import Vector
#        moveVec = Vector((0.0, 0.0, 0.0))
        moveVec = char.localLinearVelocity.copy()
        
        if keys.accept in Click:
            char.arma.playAction('walk', 1, 100, play_mode = bge.logic.KX_ACTION_MODE_LOOP, blendin=6)
        
        if char.active:
            
            
            if keys.move in Click:
                char.move.removeParent()
                char.move.worldPosition = util.input.hitWorld
                cont = bge.logic.getCurrentController()
                cont.activate(cont.actuators['Steering'])
                char.move.visible = True
            #elif {keys.forward, keys.backward, keys.leftward, keys.rightward} <= Click:
            elif not {keys.forward, keys.backward, keys.leftward, keys.rightward}.isdisjoint(reClick):
                cont = bge.logic.getCurrentController()
                cont.deactivate(cont.actuators['Steering'])
                char.move.visible = False
            
            
            if char.onGround:
                
                moveVec.x = 0
                moveVec.y = 0
                if keys.runward in reClick:
                    speed *= 3
                if keys.forward in reClick:
                    moveVec.y += speed
                if keys.backward in reClick:
                    moveVec.y -= speed
                if keys.leftward in reClick:
                    moveVec.x -= speed
                if keys.rightward in reClick:
                    moveVec.x += speed
                
                if char.timeJump < char.maxJump:
                    if not char.onLedge and not char.onMid and not char.onLeg:
                        if keys.spaceward in reClick:
                            moveVec.z = 4
                            if char.onWall:
                                moveVec.z *=2
                            
                
            
            if char.onLedge:
                if not char.onGround:
                    if keys.leftward in reClick:
                        moveVec.x -= speed
                    if keys.rightward in reClick:
                        moveVec.x += speed
                    
                    if keys.spaceward in Click:
                        cont = bge.logic.getCurrentController()
                        hup = cont.actuators['Up']
                        hup.frameEnd = (char.onLedge+0.1)*10
                        cont.activate(hup)
                    
                    if keys.backward in reClick:
                        moveVec.y -= speed
            
            
            
            if char.onLeg:
                if char.onGround:
                    if keys.spaceward in Click:
                        cont = bge.logic.getCurrentController()
                        hup = cont.actuators['Up']
                        hup.frameEnd = (char.onLeg+0.1)*10
                        cont.activate(hup)
            
            
            if char.onMid:
                if char.onGround:
                    if keys.spaceward in Click:
                        cont = bge.logic.getCurrentController()
                        hup = cont.actuators['Up']
                        hup.frameEnd = (char.onMid+0.1)*10
                        cont.activate(hup)
            
            
            
            
                        
            if char.onGround:
#                if keys.runward in reClick:
#                    speed *= 3
#                if keys.forward in reClick:
#                    moveVec.y += speed
#                if keys.backward in reClick:
#                    moveVec.y -= speed
#                if keys.leftward in reClick:
#                    moveVec.x -= speed
#                if keys.rightward in reClick:
#                    moveVec.x += speed
                
#                if char.onWall:
#                    if keys.spaceward in reClick:
#                        moveVec.z += speed *2
#                else:
#                    if keys.spaceward in reClick:
#                        moveVec.z += speed
                
                
                
                
                
                
                
                
                if moveVec == Vector((0.0, 0.0, 0.0)):
                    pass
                    #char.arma.playAction('Idel', 1, 100, play_mode = bge.logic.KX_ACTION_MODE_LOOP, blendin=6)
                elif not util.input.p3:
                    char.jib.removeParent()
                    orin = char.jib.worldOrientation.to_euler()
                    orin.x = 0.0
                    orin.y = 0.0
                    char.worldOrientation = orin
                    char.jib.setParent(char)
                    #char.arma.playAction('Female ArmaAction Second', 1, 90, play_mode = bge.logic.KX_ACTION_MODE_LOOP, speed = speed*2, blendin=6)
                elif {keys.leftward, keys.rightward}.isdisjoint(reClick):
                    postChar = char.scene.active_camera.getScreenPosition(char)
                    postMouse = bge.logic.mouse.position
                    
                    from mathutils import Euler
                    from math import atan, pi
                    x = postChar[0] - postMouse[0]
                    y = postChar[1] - postMouse[1]
                    agl = atan(x/y)
                    if y < 0:    agl = agl + pi
                    eul = Euler((0.0, 0.0, agl))
                    char.worldOrientation = eul

            
            
            
            
            
            char.localLinearVelocity = moveVec
                    
                    
#            print(char.timeJump, char.maxJump)
#            if char.timeJump < char.maxJump and keys.spaceward in reClick:
#                char.localLinearVelocity.z = 1

        
        
        
        
        
        
        
        
        
        
        if keys.mode in Click:
            if char.active:
                char.active = False
                char.camEnabled = False
                bge.logic.mouse.visible = True
                bge.logic.addScene('InfoWindow')
                bge.logic.getCurrentScene().objects['ThumbMoniter'].active = True
                
            else:
                char.active = True
                char.camEnabled = True
                bge.logic.mouse.position = 0.5, 0.5
                bge.logic.mouse.visible = False
                util.getScene('InfoWindow').end()
                bge.logic.getCurrentScene().objects['ThumbMoniter'].active = False
        
        if keys.cam1 in Click:    char.camera = 1
        elif keys.cam3 in Click:    char.camera = 3
        elif keys.cam4 in Click:    char.camera = 4
        
        if keys.accept in Click:
            print('ground, wall, ledge')
            print(char.onGround, char.onWall, char.onLedge)
            print(char.onMid, char.onLeg)
            print(len(char.coliSet))
            for coli in char.coliSet:
                print(coli.point, char.lvlGround.worldPosition)
    
    
    
    def save(char, thumb=False):
        import configparser
        sheet = configparser.ConfigParser()
        sheet['Discription'] = {
            'uId' : char.uId,
            'nameProper' : char.nameProper,
            'discription' : char.discription,
            'type' : char.type}
        
        tags = ''
        for tag in char.tags:
            tags += ','+tag
        sheet['Discription']['tags'] = tags.lstrip(',')
        
        sheet['Path'] = {}
        sheet['Path']['pathThumbNail'] = '//stuff/system/NoImage.png'
        
        sheet['Equip'] = {
            'hair' : char.hair.uId,
            'hands' : char.hands.uId,
            'torso' : char.torso.uId,
            'legs' : char.legs.uId,
            'feet' : char.feet.uId,
            'accessory' : char.accessory.uId}
        
        sheet['Targets'] = {
            'cheek' : char.cheek,
            'brow' : char.brow,
            'ear' : char.ear,
            'mouth' : char.mouth,
            'rotate' : char.rotate,
            'lid' : char.lid,
            'greek' : char.greek,
            'curve' : char.curve,
            'size' : char.size,
            'width' : char.width,
            'volume' : char.volume,
            'height' : char.height,
            'chin' : char.chin,
            'jaw' : char.jaw,
            'afro' : char.afro,
            'euro' : char.euro,
            'asio' : char.asio}
            
            
        if char.uId.startswith('custom'):
            path = '//stuff/char/custom/'+char.uId+'.png'
            sheet['Path']['pathThumbNail'] = path
            path = bge.logic.expandPath(path)
            char.pathThumbNail = path
            cam = char.camera
            camNum = char.cameraNum
            char.camera = 1
            util.capThumb(cam, path)
            char.camera = camNum
            
            
            path = bge.logic.expandPath('//stuff/char/custom/'+char.uId+'.ini')
            with open(path, 'w') as configfile:
                sheet.write(configfile)
                for tag in sheet['Discription']['tags'].split(','):
                    try:    util.tags[tag].append(sheet)
                    except KeyError:
                        util.tags[tag] = []
                        util.tags[tag].append(sheet)
        else:    raise Exception("My hovercraft is full of eels")

    
    





class Sk8r(bge.types.KX_GameObject):
    turn = util.methods.dynRotate
    onGround = property(util.methods.onGround)
    onWall = property(util.methods.onWall)
    speed = property(util.methods.speedMps2Kph)
    
    def __init__(skater, DNU, sheet):
        scene = bge.logic.getCurrentScene()
        objs = scene.objects
        
        #Discription#
        skater.uId = sheet['Discription']['uId']
        skater.type = sheet['Discription']['type']
        skater.tags = set()
        for tag in sheet['Discription']['tags'].split(','):    skater.tags.add(tag)
        
        skater.lvlGround = objs[skater.name+' LvlGround']
        skater.collisionCallbacks.append( util.Method(util.methods.collisionRegister, skater) )
        skater.coliSet = set()
        skater.coliFlush = util.Method(util.methods.coliFlush, skater.coliSet)
        
        skater.body = skater.children[skater.name+' Body']
        
        skater.onVert = False
        skater.off = False
    
    
    def run(skater):
        skater.coliFlush()
        skater.body.alignAxisToVect(skater.worldLinearVelocity,  1)
        #print(skater.speed)
        if skater.onVert:
            if skater.onGround:
                skater.worldLinearVelocity = skater.vertRetrn
                skater.onVert = False
            if skater.onGround and 1==2:
                velo = skater.onVertB
                skater.worldLinearVelocity = velo
                velo = skater.localLinearVelocity
                
                print(skater.onVertA *util.turnPercent)
                quarter = 1/4*util.turn
                half = 1/2*util.turn
                
                agl = skater.onVertA
                print(agl *util.turnPercent,  skater.onVertA *util.turnPercent)
                    
                x = 0.0
                y = 0.0
                z =  2*agl
                print(z *util.turnPercent)
                from mathutils import Euler
                eul = Euler( (x, y, z) )
                velo.rotate(eul)
                """
                if velo.x > 0:
                    eul = Euler( (0.0, 0.0, 1/4 *util.turn) )
                else:
                    eul = Euler( (0.0, 0.0, -1/4 *util.turn) )
                velo.rotate(eul)
                """
                print(velo)
                skater.onVert = False
                
            
            
            
            
            if skater.onGround and 1==2:
                #speed = abs(skater.speed)
                velo = skater.onVertB
                #velo.magnitude = speed
                skater.worldLinearVelocity = velo
                
                print(velo)
                velo = skater.localLinearVelocity
                
                #velo.y = -velo.y
                print(skater.onVertA *util.turnPercent)
                quarter = 1/4*util.turn
                half = 1/2*util.turn
                
                agl = quarter - abs(skater.onVertA)
                print(agl *util.turnPercent,  skater.onVertA *util.turnPercent)
                #if skater.onVertA < 0:
                #    agl *= -1
                    
                x = 0.0
                y = 0.0
                z =  half + -agl
                print(z *util.turnPercent)
                from mathutils import Euler
                eul = Euler( (x, y, 2*agl) )
                velo.rotate(eul)
                """
                if velo.x > 0:
                    eul = Euler( (0.0, 0.0, 1/4 *util.turn) )
                else:
                    eul = Euler( (0.0, 0.0, -1/4 *util.turn) )
                velo.rotate(eul)
                """
                print(velo)
                skater.onVert = False
                
            if skater.onGround and 1==2:
                skater.worldLinearVelocity = skater.wLV
                from mathutils import Euler
                agl = skater.onVertA
                
                print(agl *util.turnPercent)
                x = 0.0
                y = 0.0
                z = -agl
#                   if agl > 0:
#                        eul = Euler( (-abs(agl), 0.0, -agl) )
#                    else:
#                        eul = Euler( (-abs(agl), 0.0, -agl) )
                #quart = -1/4 *util.turn
                
                eul = Euler( (x, y, z) )
                print(skater.localLinearVelocity)
                skater.localLinearVelocity.rotate(eul)
                print(skater.localLinearVelocity)
                skater.onVert = False
        else:
            for coli in skater.coliSet:
                if not coli.ground and not skater.onVert and not skater.off:
                    #coli.hitObj.suspendDynamics(True)
                    util.methods.alin2Normal(skater, coli.normal)
                    skater.onVert = True
                    #skater.off=True
                    print('coli')
        
        
        
        
        skater.wLV = skater.worldLinearVelocity.copy()

    def input(skater):
        import util
        keys = util.settings
        Click, reClick, deClick = util.input.catch()
            
        force = 1000
        angle = 1/100
        if skater.onGround:
            if keys.forward in reClick:
                skater.applyForce([0, force, 0], True)
            if keys.backward in reClick:
                skater.applyForce([0, -force, 0], True)
            if keys.leftward in reClick:
                skater.turn(angle)
            if keys.rightward in reClick:
                skater.turn(-angle)
                
            if keys.spaceward in Click:
                velo = skater.localLinearVelocity
                
                
                x = 0.0
                y = 0.0
                z = 1/2 + 1/4
                from mathutils import Euler
                eul = Euler( (x*util.turn, y*util.turn, z*util.turn) )
                velo.rotate(eul)






class Vehicle(bge.types.KX_GameObject):
    
    child = util.child_getter
    
    cameraNum = property(cameraNum_getter, camera_setter)
    camera = property(camera_getter, camera_setter)
    jib = property(jib_getter, camera_setter)
    camEnabled = property(camActive_getter, camActive_setter)
    runJib = runJib
    
    
    drive = util.methods.vehicleDrive
    turn = util.methods.vehicleTurn
    pBreak = util.methods.vehicleBreak
    updateTraction = util.methods.updateTraction
    speed = property(util.methods.speedMps2Kph)
    
    def __init__(car, DNU, sheet):
        #Discription#
        car.uId = sheet['Discription']['uId']
        car.nameProper = sheet['Discription']['nameProper']
        car.discription = sheet['Discription']['discription']
        car.type = sheet['Discription']['type']
        car.tags = set()
        for tag in sheet['Discription']['tags'].split(','):
            car.tags.add(tag)
        
        #Main#
        car.activate = util.Method(getattr(util.actions, sheet['Main']['activate']), car)
        car.context = util.Method(getattr(util.actions, sheet['Main']['context']), car)
        
        #Path#
        car.pathThumbNail = sheet['Path']['pathThumbNail']
        
        
        #Stats#
        car.weight = float(sheet['Stats']['mass'])
        car.force = float(sheet['Stats']['force'])
        car.breakForce = float(sheet['Stats']['breakForce'])
        car.mass = car.weight
        car.resistance = float(sheet['Stats']['resistance'])
        car.stability = float(sheet['Stats']['stability'])
        car.setDamping(car.resistance, car.stability)
        
        car.leanAngle = float(sheet['Stats']['leanAngle'])
        car.lean = sheet['Stats'].getboolean('lean')
        car.jet = float(sheet['Stats']['jet'])
        car.body = car.children[car.name+' Body']
        
        car.pResistance = float(sheet['Stats']['pResistance'])
        car.pStability = float(sheet['Stats']['pStability'])
        car.skeg = float(sheet['Stats']['skeg'])
        
        car.wheels = []
        car.steering = set()
        car.driveTrain = set()
        wheelNum = 0
        for wheelId in sheet['Stats']['wheels'].split(','):
            wheelObj = car.children[car.name+' '+wheelId]
            wheel = util.classes.Wheel(sheet, wheelObj, wheelId, wheelNum)
            car.wheels.append(wheel)
            if wheel.steer:    car.steering.add(wheel)
            if wheel.drive:    car.driveTrain.add(wheel)
            wheelNum += 1
        try:    car.forcePerWheel = car.force / len(car.driveTrain)
        except ZeroDivisionError:    car.forcePerWheel = 0

        #Camera#
        car.jibs = []
        car.jibs.append(None)
        car.jibs.append(car.child('Jib1'))
        car.jibs.append(None)
        car.jibs.append(None)
        car.jibs.append(None)
        
        car.cams = []
        car.cams.append(None)
        car.cams.append(car.child('Cam1'))
        car.cams.append(None)
        car.cams.append(None)
        car.cams.append(None)
        
        car.active = False
        car.camEnabled = False
        car.camera = 1
        
        #Pysics#
        import PhysicsConstraints
        vehicleConstraint = PhysicsConstraints.createConstraint(car.getPhysicsId(), 0, 11)
        car.wrapper = PhysicsConstraints.getVehicleConstraint(vehicleConstraint.getConstraintId())
        
        for wheel in car.wheels:
            car.wrapper.addWheel(wheel.obj, wheel.obj.localPosition, wheel.camber, wheel.toe, wheel.hight, wheel.radius, wheel.steer)
            wheel.obj.removeParent()
            car.wrapper.setRollInfluence(wheel.roll, wheel.num)
            car.wrapper.setSuspensionDamping(wheel.damping, wheel.num)
            car.wrapper.setSuspensionStiffness(wheel.stiffness, wheel.num)
            car.wrapper.setTyreFriction(wheel.traction, wheel.num)
        



    def run(car):
        if car.uId == 'baseIshikawa':
            car.localLinearVelocity.x -= car.localLinearVelocity.x * (car.skeg / 60)
    
    def input(car):
        import util
        keys = util.settings
        
        Click, reClick, deClick = util.input.catch()
        if car.active:
            if keys.accept in Click:
                car.active = False
                util.input.select.active = True
                util.input.select.camEnabled = True
                util.input.select.camera = 1
            
            
            
            pedalTurn = util.input.joy0
            pedalDrive = util.input.joy3
            if keys.pBreak in reClick:    pedalBreak = 1.0
            else:    pedalBreak = -1.0
        else:
            pedalTurn = 0.0
            pedalDrive = 0.0
            pedalBreak = -1.0
            
        
        car.drive(pedalDrive)
        car.turn(pedalTurn)
        car.pBreak(pedalBreak)
        
        car.updateTraction(pedalDrive, pedalTurn, pedalBreak)
        
        



        
        
        
        
        
class Song:
    def __init__(song, sheet, fretBoard):
        #Discription#
        song.uId = sheet['Discription']['uId']
        song.nameProper = sheet['Discription']['nameProper']
        song.discription = sheet['Discription']['discription']
        song.type = sheet['Discription']['type']
        song.tags = set()
        for tag in sheet['Discription']['tags'].split(','):
            song.tags.add(tag)
        
        #Path#
        song.pathImage = sheet['Path']['pathImage']
        song.pathTrack = sheet['Path']['pathTrack']
        song.pathMidi = sheet['Path']['pathMidi']
        
        song.fretBoard = fretBoard
        
        with open(song.pathMidi, 'rb') as midiFile:
            song.score = util.midi.midi2score(midiFile.read())
        song.ticks = song.score[0]
        song.tempo = None
        for note in song.score[1]:
            if note[0] == 'set_tempo':
                if not song.tempo:    song.tempo = note[2]
                else:    print('Changing tempo not curently implemented.')
        from collections import deque
        song.notes = deque()
        for note in song.score[2][1:len(song.score[2])]:
            if 96 <= note[4] <= 100:
                note = util.classes.SongNote(note, song.tempo, song.ticks, song, fretBoard)
                song.notes.append(note)



def timerRemaing_getter(timer):
    return (bge.logic.getFrameTime() - timer.startTime) / bge.logic.getTimeScale()



class TemporalControler(bge.types.KX_GameObject):
    duration = property(util.methods.propDuration_getter, util.methods.propDuration_setter)
    remaining = property(util.methods.timerRemaing_getter)
    
    def __init__(timer, DNU):
        timer.startTime = 0.0
    
    def run(timer):
        if timer.remaining >= timer.duration:
            timer.duration = 0.0
            timer.resume()
    
    
    def resume(timer):
        bge.logic.setTimeScale(1.0)
    
    def pause(timer, duration):
        timer.startTime = bge.logic.getFrameTime()
        bge.logic.setTimeScale(util.settings.timePause)
        timer.duration = duration

    def fast(timer, duration):
        timer.startTime = bge.logic.getFrameTime()
        bge.logic.setTimeScale(util.settings.timeFast)
        timer.duration = duration

    def slow(timer, duration):
        timer.startTime = bge.logic.getFrameTime()
        bge.logic.setTimeScale(util.settings.timeSlow)
        timer.duration = duration
    
    def input(timer):
        Click = util.input.Click
        keys = util.settings
        
        if keys.speedPause in Click:    timer.pause(5)
        elif keys.speedSlow in Click:    timer.slow(5)
        elif keys.speedNormal in Click:    timer.resume()
        elif keys.speedFast in Click:    timer.fast(5)
        




class Thing(bge.types.KX_GameObject):
    def __init__(thing, DNU, sheet):
        #Discription#
        thing.uId = sheet['Discription']['uId']
        thing.nameProper = sheet['Discription']['nameProper']
        thing.discription = sheet['Discription']['discription']
        thing.type = sheet['Discription']['type']
        thing.tags = set()
        for tag in sheet['Discription']['tags'].split(','):    thing.tags.add(tag)
        
        #Path#
        thing.pathThumbNail = sheet['Path']['pathThumbNail']
        
        #Main#
        thing.activate = util.Method(getattr(util.actions, sheet['Main']['activate']), thing)
        thing.context = util.Method(getattr(util.actions, sheet['Main']['context']), thing)















class JinniGM(bge.types.KX_GameObject):
    def __init__(jinni, DNU):
        jinni.red = set()
        jinni.blue = set()
        
        jinni.scene.active_camera = jinni.scene.objects['Camera']
        util.input.p3 = True
        char = util.input.select
        try:
            for jib in char.jibs:
                if jib:
                    jib['active'] = False
        except:    pass
    
    
    
    def input(jinni):
        input = util.input
        Click = input.Click
        keys = util.settings
        
        if keys.select in Click:
            if input.select:
                input.select.select = False
            if input.window:
                input.window.select = True
                
        if keys.move in Click:
            pass
            #input.select.moveObj.worldPosition = input.hitWorld
    
    def run(jinni):
        pass
    
    def message(jinni):
        pass






def selected_getter(thing):
    return thing.selectObj.visible

def selected_setter(thing, bool):
    if bool:
        util.input.select = thing
    else:
        util.input.select = None
    thing.selectObj.visible = bool


def sortByDistance(gameObj, list):
    def getDist(other):
        return gameObj.getDistanceTo(other)
    
    return sorted(list, key=getDist)









class MovingThingy(bge.types.KX_GameObject):
    child = util.child_getter
    
    select = property(selected_getter, selected_setter)
    sortDist = util.sortByDistance
    
    timeAction = property(
        util.partial(timerCurrent, storage = '_timeAction'),
        util.partial(timerStart, storage = '_timeAction'))
    
    timeActionRemaing = property(util.partial(timerRemaing, storage = '_timeAction'))
    
    
    
    
    
    
    def __init__(thing, DNU):
        thing.selectObj = thing.child('Select')
        thing.moveObj = thing.child('Move')
        thing.moveObj.removeParent()
        thing.attkPost = thing.child('AttkPost')
        
        
        
        thing.gm = thing.scene.objects['JinniGM']
        if thing['team'] == 'red':
            thing.teamColor = [1.0, 0.0, 0.0]
            thing.allys = thing.gm.red
            thing.allys.add(thing)
            thing.enemys = thing.gm.blue
        elif thing['team'] == 'blue':
            thing.teamColor = [0.0, 0.0, 1.0]
            thing.allys = thing.gm.blue
            thing.allys.add(thing)
            thing.enemys = thing.gm.red
        
        
        
        thing.hitPosts = set()
        for i in range(9):
            thing.hitPosts.add(thing.child('HitPost '+str(i)))

    
    def input(thing):
        pass
    
    def run(thing):
        pass
        
    def message(thing):
        pass
    
    
    def ai(thing):
        
        #import Rasterizer
        from random import choice, gauss
        attk = thing.attkPost
        enemys = list(thing.enemys)
        enemys = thing.sortDist(enemys)
        enemy = enemys[0]
        hitSet = set()
        for hit in enemy.hitPosts:
            if attk.rayCastTo(hit) == enemy:
                hitSet.add(hit)
            
            
        hit = choice(tuple(hitSet))
        #hit = thing.scene.objects['Dood HitPost 0']
        #for hit in hitSet:
        vec = attk.getVectTo(hit)[1]
        vec.magnitude = attk.getVectTo(hit)[0]
        #vec.z += 0
    
        #vec = vec + attk.worldPosition
        from mathutils import Euler
        accuY = 0.05     #up down, about 0.1 - 0.01
        accuZ = 0.05     #left right, low is better
        eul = Euler((0.0, gauss(0, accuY), gauss(0, accuZ)))
        #x = 0#1/4 *util.turn
        #y = 1/8 *util.turn
        #z = 0#1/4 *util.turn
        #eul = Euler((x, y, z))
        vec.rotate(eul)
        #vec.z += 1.0
        vec = vec + attk.worldPosition
        
        
        import Rasterizer
        Rasterizer.drawLine(attk.worldPosition, vec, thing.teamColor)
            
        
        
        
        #for enemy in thing.enemys:
        #    thing.getDistanceTo(enemy)
#            for hit in enemy.hitPosts:
#                attk = thing.attkPost
#                attk.rayCastTo(other, dist, prop)
            
        
        #enemy = choice(tuple(thing.enemys))
        
        
        
        #enemyHit = choice(tuple(enemy.hitPosts))
        
        
        
        
        #print(thing.enemys)
        #print(enemy)
#        for hitPost in thing.hitPosts:
#            start = hitPost.worldPosition
#            end = enemyHit.worldPosition
#            color = [ 1.0, 0.0, 0.0]
#            Rasterizer.drawLine( start, end, color)
        
        
        



class testThingy(bge.types.KX_GameObject):
    child = util.child_getter
    
    def __init__(thing, DNU):
        arma = thing.child('Arma')
        arma.playAction('walk', 1, 100, play_mode = bge.logic.KX_ACTION_MODE_LOOP, blendin=6)








def attr2dict_getter(obj, slot):
    return obj[slot]

def attr2dict_setter(obj, value, slot):
    obj[slot] = value

def attr2dict(slot):
    return property(
        util.partial(attr2dict_getter, slot=slot),
        util.partial(attr2dict_setter, slot=slot))


def charTarget_getter(obj, slot):
    return obj.body[slot]

def charTarget_setter(obj, value, slot):
    obj.body[slot] = value

def charTarget(slot):
    return property(
        util.partial(charTarget_getter, slot=slot),
        util.partial(charTarget_setter, slot=slot))

#brow = property(
#    util.partial(attr2dict_getter, slot='brow'),
#    util.partial(attr2dict_setter, slot='brow'))

#brow = target('brow')


#cheek = property(
#    util.partial(attr2dict_getter, slot='cheek'),
#    util.partial(attr2dict_setter, slot='cheek'))
#
#chin = property(
#    util.partial(attr2dict_getter, slot='chin'),
#    util.partial(attr2dict_setter, slot='chin'))
#    
#ear = property(
#    util.partial(attr2dict_getter, slot='ear'),
#    util.partial(attr2dict_setter, slot='ear'))
#    
#eyeInner = property(
#    util.partial(attr2dict_getter, slot='eyeInner'),
#    util.partial(attr2dict_setter, slot='eyeInner'))
#    
#eyeMid = property(
#    util.partial(attr2dict_getter, slot='eyeMid'),
#    util.partial(attr2dict_setter, slot='eyeMid'))
#    
#eyeOuter = property(
#    util.partial(attr2dict_getter, slot='eyeOuter'),
#    util.partial(attr2dict_setter, slot='eyeOuter'))
#    
#jaw = property(
#    util.partial(attr2dict_getter, slot='jaw'),
#    util.partial(attr2dict_setter, slot='jaw'))
#
#lips = property(
#    util.partial(attr2dict_getter, slot='lips'),
#    util.partial(attr2dict_setter, slot='lips'))
#
#noseBridge = property(
#    util.partial(attr2dict_getter, slot='noseBridge'),
#    util.partial(attr2dict_setter, slot='noseBridge'))
#
#noseHight = property(
#    util.partial(attr2dict_getter, slot='noseHight'),
#    util.partial(attr2dict_setter, slot='noseHight'))
#
#noseLength = property(
#    util.partial(attr2dict_getter, slot='noseLength'),
#    util.partial(attr2dict_setter, slot='noseLength'))
#
#noseRidge = property(
#    util.partial(attr2dict_getter, slot='noseRidge'),
#    util.partial(attr2dict_setter, slot='noseRidge'))
#
#noseWidth = property(
#    util.partial(attr2dict_getter, slot='noseWidth'),
#    util.partial(attr2dict_setter, slot='noseWidth'))



def charSlot_getter(char, slot):
    return char.child(slot.capitalize())

def charSlot_setter(char, uId, slot):
    sheet = util.sheets[uId]
    slot = char.child(slot.capitalize())
    slot = util.classes.Equipment(slot, sheet, char)
#    try:
#        ary = util.image2Array(slot.pathMask)
#        util.textureChange(char.body, ary, textuId = 0)
#    except AttributeError:
#        print(uId)
        
    
def charSlot(slot):
    return property(
        util.partial(charSlot_getter, slot=slot),
        util.partial(charSlot_setter, slot=slot))


def charPheno_setter(char, uId):
    sheet = util.sheets[uId]
    slot = char.child('Body')
    slot = util.classes.Equipment(slot, sheet, char)
    char.body['update'] = True
    char.gender = sheet['Stats']['gender']
    try:
        char.torso = char.torso.uId
        char.legs = char.legs.uId
    except AttributeError:
        pass

def charWepon_setter(char, uId, slot):
    sheet = util.sheets[uId]
    
    try:
        if '2h' in sheet['Discription']['tags'].split(','):
            sheetNon = util.sheets['baseNonEquipment']
            slotNon = char.child('Left')
            slotNon = util.classes.Equipment(slotNon, sheetNon, char)
        
        elif '2h' in char.right.tags:
            sheetNon = util.sheets['baseNonEquipment']
            slotNon = char.child('Right')
            slotNon = util.classes.Equipment(slotNon, sheetNon, char)
    except AttributeError:
        pass
    
    slot = char.child(slot.capitalize())
    slot = util.classes.Equipment(slot, sheet, char)

def charWepon(slot):
    return property(
        util.partial(charSlot_getter, slot=slot),
        util.partial(charWepon_setter, slot=slot))



body = property(
    util.partial(charSlot_getter, slot='body'),
    util.partial(charPheno_setter))


#body = property(
#    util.partial(charSlot_getter, slot='body'),
#    util.partial(charSlot_setter, slot='body'))
#
#eyes = property(
#    util.partial(charSlot_getter, slot='eyes'),
#    util.partial(charSlot_setter, slot='eyes'))
#
#hair = property(
#    util.partial(charSlot_getter, slot='hair'),
#    util.partial(charSlot_setter, slot='hair'))
#
#hands = property(
#    util.partial(charSlot_getter, slot='hands'),
#    util.partial(charSlot_setter, slot='hands'))
#
#torso = property(
#    util.partial(charSlot_getter, slot='torso'),
#    util.partial(charSlot_setter, slot='torso'))
#
#legs = property(
#    util.partial(charSlot_getter, slot='legs'),
#    util.partial(charSlot_setter, slot='legs'))
#
#feet = property(
#    util.partial(charSlot_getter, slot='feet'),
#    util.partial(charSlot_setter, slot='feet'))
#
#accessory = property(
#    util.partial(charSlot_getter, slot='accessory'),
#    util.partial(charSlot_setter, slot='accessory'))




class Character(bge.types.KX_GameObject):
    
    child = util.child_getter
    
    body = body
    eyes = charSlot('eyes')
    hair = charSlot('hair')
    hands = charSlot('hands')
    torso = charSlot('torso')
    legs = charSlot('legs')
    feet = charSlot('feet')
    accessory = charSlot('accessory')
    left = charWepon('left')
    right = charWepon('right')
    
    brow = charTarget('brow')
    cheek = charTarget('cheek')
    chin = charTarget('chin')
    ear = charTarget('ear')
    eyeInner = charTarget('eye_inner')
    eyeMid = charTarget('eye_mid')
    eyeOuter = charTarget('eye_outer')
    jaw = charTarget('jaw')
    lips = charTarget('lips')
    noseBridge = charTarget('nose_bridge')
    noseHight = charTarget('nose_hight')
    noseLength = charTarget('nose_length')
    noseRidge = charTarget('nose_ridge')
    noseWidth = charTarget('nose_width')

    
    def __init__(char, DNU, sheet):
        
        #Discription#
        char.uId = sheet['Discription']['uId']
        char.nameProper = sheet['Discription']['nameProper']
        char.discription = sheet['Discription']['discription']
        char.type = sheet['Discription']['type']
        char.tags = set()
        for tag in sheet['Discription']['tags'].split(','):    char.tags.add(tag)
        
        char.pathThumbNail = sheet['Path']['pathThumbNail']
        
        
        char.arma = char.child('Arma')
        char.gender = sheet['Stats']['gender']
        
        char.body = sheet['Equip']['pheno']
        char.eyes = sheet['Equip']['eyes']
        char.hair = sheet['Equip']['hair']
        char.hands = sheet['Equip']['hands']
        char.torso = sheet['Equip']['torso']
        char.legs = sheet['Equip']['legs']
        char.feet = sheet['Equip']['feet']
        char.accessory = sheet['Equip']['accessory']
        char.left = sheet['Equip']['left']
        char.right = sheet['Equip']['right']
        
        
        
        char.brow = float(sheet['Targets']['brow'])
        char.cheek = float(sheet['Targets']['cheek'])
        char.chin = float(sheet['Targets']['chin'])
        char.ear = float(sheet['Targets']['ear'])
        char.eyeInner = float(sheet['Targets']['eyeInner'])
        char.eyeMid = float(sheet['Targets']['eyeMid'])
        char.eyeOuter = float(sheet['Targets']['eyeOuter'])
        char.jaw = float(sheet['Targets']['jaw'])
        char.lips = float(sheet['Targets']['lips'])
        char.noseBridge = float(sheet['Targets']['noseBridge'])
        char.noseHight = float(sheet['Targets']['noseHight'])
        char.noseLength = float(sheet['Targets']['noseLength'])
        char.noseRidge = float(sheet['Targets']['noseRidge'])
        char.noseWidth = float(sheet['Targets']['noseWidth'])
        
    
    
    
    def save(char):
        import configparser
        sheet = configparser.ConfigParser()
        sheet['Discription'] = {
            'uId' : char.uId,
            'nameProper' : char.nameProper,
            'discription' : char.discription,
            'type' : char.type}
        
        tags = ''
        for tag in char.tags:
            tags += ','+tag
        sheet['Discription']['tags'] = tags.lstrip(',')
        
        sheet['Path'] = {}
        sheet['Path']['pathThumbNail'] = '//stuff/system/NoImage.png'
        
        sheet['Equip'] = {
            'pheno' : char.body.uId,
            'eyes' : char.eyes.uId,
            'hair' : char.hair.uId,
            'hands' : char.hands.uId,
            'torso' : char.torso.uId,
            'legs' : char.legs.uId,
            'feet' : char.feet.uId,
            'accessory' : char.accessory.uId, 
            'left' : char.left.uId, 
            'right' : char.right.uId}
        
#        sheet['Targets'] = {
#            'cheek' : char.cheek,
#            'brow' : char.brow,
#            'ear' : char.ear,
#            'mouth' : char.mouth,
#            'rotate' : char.rotate,
#            'lid' : char.lid,
#            'greek' : char.greek,
#            'curve' : char.curve,
#            'size' : char.size,
#            'width' : char.width,
#            'volume' : char.volume,
#            'height' : char.height,
#            'chin' : char.chin,
#            'jaw' : char.jaw,
#            'afro' : char.afro,
#            'euro' : char.euro,
#            'asio' : char.asio}
            
            
        sheet['Targets'] = {
            'brow' : char.brow,
            'cheek' : char.cheek,
            'chin' : char.chin,
            'ear' : char.ear,
            'eyeInner' : char.eyeInner,
            'eyeMid' : char.eyeMid,
            'eyeOuter' : char.eyeOuter,
            'jaw' : char.jaw,
            'lips' : char.lips,
            'noseBridge' : char.noseBridge,
            'noseHight' : char.noseHight,
            'noseLength' : char.noseLength,
            'noseRidge' : char.noseRidge,
            'noseWidth' : char.noseWidth}
        
        sheet['Stats'] = {
            'gender' : char.gender}
            
            
            
        if char.uId.startswith('custom'):
            path = '//stuff/char/custom/'+char.uId+'.png'
            sheet['Path']['pathThumbNail'] = path
            path = bge.logic.expandPath(path)
            char.pathThumbNail = path
            cam = char.scene.active_camera
            cam = char.scene.cameras['Char CamThumb']
            util.capThumb(cam, path)
            
            path = bge.logic.expandPath('//stuff/char/custom/'+char.uId+'.ini')
            with open(path, 'w') as configfile:
                sheet.write(configfile)
            
            uId = sheet['Discription']['uId']
            util.sheets[uId] = sheet
            for tag in sheet['Discription']['tags'].split(','):
                try:    util.tags[tag].append(sheet)
                except KeyError:
                    util.tags[tag] = []
                    util.tags[tag].append(sheet)
        
        else:    raise Exception("My hovercraft is full of eels")














