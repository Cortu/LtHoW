import util
import bge
class CollisionPoint():
    def __init__(coliPoint, hitObj, point, normal,  lvlGround):
        coliPoint.hitObj = hitObj
        coliPoint.point = point
        coliPoint.normal = normal
        coliPoint.delMe = False
        if point.z < lvlGround:    coliPoint.ground = True
        else:    coliPoint.ground = False


class Wheel():
    def __init__(wheel, sheet, wheelObj, wheelId, wheelNum):
        wheel.id = wheelId
        wheel.num = wheelNum
        wheel.obj = wheelObj
        wheel.camber = [0.0, 0.0, -1.0]
        wheel.toe = [ -1.0, 0.0, 0.0]
        
        wheel.radius = float(sheet[wheel.id]['radius'])
        wheel.hight = float(sheet[wheel.id]['hight'])
        wheel.stiffness = float(sheet[wheel.id]['stiffness'])
        wheel.damping = float(sheet[wheel.id]['damping'])
        wheel.roll = float(sheet[wheel.id]['roll'])
        wheel.traction = float(sheet[wheel.id]['traction'])
        wheel.drive = sheet[wheel.id].getboolean('drive')
        wheel.steer = sheet[wheel.id].getboolean('steer')
        wheel.turnAngle = float(sheet[wheel.id]['turnAngle']) *util.turn










class SongNote():
    def __init__(note, midi, tempo, ticks, song, fretBoard):
        import util
        note.spawn = util.dtime2secs(midi[1], tempo, ticks)
        note.hit = note.spawn + util.settings.songBufferTime
        note.deSpawn = note.hit + (util.settings.songHitTime / 2)
        note.sustain = util.dtime2secs(midi[2], tempo, ticks)
        note.sustaining = False
        note.fretBoard = fretBoard
        note.song = song
        
        if midi[4] == 96:    note.note = 'A'
        elif midi[4] == 97:    note.note = 'B'
        elif midi[4] == 98:    note.note = 'C'
        elif midi[4] == 99:    note.note = 'D'
        elif midi[4] == 100:    note.note = 'E'
        
        note.obj = None

    def run(note):
        songTime = note.fretBoard.sound.time
        timeTel = note.hit - songTime
        note.obj.localPosition.y = timeTel / util.settings.songBufferTime
        if note.sustaining:
            if songTime > note.deSpawn + note.sustain:
                note.deSpawnObj()
                
        elif songTime > note.deSpawn:
            note.fretBoard.targetVolume = util.settings.songMissMod
            note.deSpawnObj()
    
    def spawnObj(note):
        import bge
        scene = bge.logic.getCurrentScene()
        new = scene.addObject(note.fretBoard.notes[note.note], note.fretBoard.starts[note.note])
        new.worldScale = [1.0,1.0,1.0]
        new.setParent(note.fretBoard)
        new['note'] = note
        note.obj = new
        note.fretBoard.notesActive.add(note)
        note.nova = note.obj.children[note.obj.name+' Nova']
        note.tail = note.obj.children[note.obj.name+' Tail']
        note.cloud = note.obj.children[note.obj.name+' Cloud']
        scaleMulti = note.sustain * note.fretBoard.worldScale.y / util.settings.songBufferTime
        note.tail.localScale.y = scaleMulti
        #This requires a unique mesh, like libnew or something
        #util.scaleUV(note.tail, u=scaleMulti)
    
    def gotHit(note):
        note.nova.removeParent()
        note.nova.visible = True
        note.nova.playAction('Note Nova Action', 0, 24)
        
        if note.note == 'A':
            note.tail.color = [1.0, 0.0, 0.0, 0.666]
        elif note.note == 'B':
            note.tail.color = [0.0, 1.0, 0.133, 0.666]
        elif note.note == 'C':
            note.tail.color = [0.604, 0.0, 1.0, 0.666]
        elif note.note == 'D':
            note.tail.color = [0.604, 1.0, 0.0, 0.666]
        elif note.note == 'E':
            note.tail.color = [0.0, 0.133, 1.0, 0.666]
        
        note.obj.visible = False
        note.sustaining = True
        note.fretBoard.notesSustain.add(note)
        note.fretBoard.notesActive.remove(note)
        
        speed = ((note.song.tempo/1000000) *4)
        char = util.input.select.arma
        char.playAction('dance', 1, 96, play_mode=1, speed=speed, blendin=5)
        

    def deSpawnObj(note):
        note.obj.endObject()
        try:
            note.fretBoard.notesSustain.remove(note)
        except KeyError:
            char = util.input.select.arma
            char.playAction('Idel', 1, 100, play_mode=1, blendin=5)
            print('missNote '+note.note)






class FretBoard(bge.types.KX_GameObject):
    def __init__(fret, DNU):
        fret.sound = fret.actuators['Sound']
        from random import choice
        sheet = choice(util.tags['fof'])
        fret.song = util.stuff.Song(sheet, fret)
        print(fret.song.uId)
        fret.targetVolume = fret.sound.volume
        fret.camera = fret.children[fret.name +' Cam']
        fret.camera['shaking'] = False
        fret.cameraShake = util.Method(util.methods.cameraShake, fret.camera)
        
        fret.starts = {}
        fret.stops = {}
        fret.notes = {}
        
        fret.starts['A'] = fret.children[fret.name +' Start A']
        fret.starts['B'] = fret.children[fret.name +' Start B']
        fret.starts['C'] = fret.children[fret.name +' Start C']
        fret.starts['D'] = fret.children[fret.name +' Start D']
        fret.starts['E'] = fret.children[fret.name +' Start E']
        
        fret.stops['A'] = fret.children[fret.name +' Stop A']
        fret.stops['B'] = fret.children[fret.name +' Stop B']
        fret.stops['C'] = fret.children[fret.name +' Stop C']
        fret.stops['D'] = fret.children[fret.name +' Stop D']
        fret.stops['E'] = fret.children[fret.name +' Stop E']
        
        objsInact = bge.logic.getCurrentScene().objectsInactive
        fret.notes['A'] = objsInact[fret.name +' Note A']
        fret.notes['B'] = objsInact[fret.name +' Note B']
        fret.notes['C'] = objsInact[fret.name +' Note C']
        fret.notes['D'] = objsInact[fret.name +' Note D']
        fret.notes['E'] = objsInact[fret.name +' Note E']
        
        fret.notesActive = set()
        fret.notesSustain = set()
        
        import aud
        audFac = aud.Factory(fret.song.pathTrack)
        audFac = audFac.delay(4.0)
        fret.sound.sound = audFac
        cont = bge.logic.getCurrentController()
        cont.activate(fret.sound)
    
    
    
    def run(fret):
        try:
            next = fret.song.notes[0]
            if fret.sound.time > next.spawn:
                note = fret.song.notes.popleft()
                note.spawnObj()
                fret.notesActive.add(note)
        except IndexError:    pass
        
        import util
        inc = util.settings.songMissInc
        targetV = fret.targetVolume
        soundV = fret.sound.volume
        
        if abs(targetV - soundV) < inc:
            fret.sound.volume = targetV
        elif targetV > soundV:
            fret.sound.volume += inc
        else:
            fret.sound.volume -= inc
        
        #if fret.camera['shaking']:
        #    fret.cameraShake()
            


    
    def input(fret):
        import util
        keys = util.settings
        buffer = util.settings.songHitTime / 2
        Click, reClick, deClick = util.input.catch()
        
        heldFrets = set()
        if keys.fretA in reClick:
            heldFrets.add('A')
            #fret.stops['A'].color = [1.0, 0.0, 0.0, 1.0]
            fret.stops['A'].color = [1.0, 0.091, 0.091, 1.0]
        elif keys.fretA in deClick:
            fret.stops['A'].color = [1.0, 0.402, 0.402, 1.0]
        
        if keys.fretB in reClick:
            heldFrets.add('B')
            #fret.stops['B'].color = [0.0, 1.0, 0.133, 1.0]
            fret.stops['B'].color = [0.091, 1.0, 0.319, 1.0]
        elif keys.fretB in deClick:
            fret.stops['B'].color = [0.402, 1.0, 0.604, 1.0]
        
        if keys.fretC in reClick:
            heldFrets.add('C')
            #fret.stops['C'].color = [0.604, 0.0, 1.0, 1.0]
            fret.stops['C'].color = [0.723, 0.091, 1.0, 1.0]
        elif keys.fretC in deClick:
            fret.stops['C'].color = [0.855, 0.402, 1.0, 1.0]
            
        if keys.fretD in reClick:
            heldFrets.add('D')
            #fret.stops['D'].color = [0.604, 1.0, 0.0, 1.0]
            fret.stops['D'].color = [0.723, 1.0, 0.091, 1.0]
        elif keys.fretD in deClick:
            fret.stops['D'].color = [0.855, 1.0, 0.402, 1.0]        
        
        if keys.fretE in reClick:
            heldFrets.add('E')
            #fret.stops['E'].color = [0.0, 0.133, 1.0, 1.0]
            fret.stops['E'].color = [0.091, 0.319, 1.0, 1.0]
        elif keys.fretE in deClick:
            fret.stops['E'].color = [0.406, 0.607, 1.0, 1.0]        
        
        if keys.strum in Click:
            gotHit = set()
            for note in fret.notesActive.copy():
                timeTil = note.hit - fret.sound.time
                if -buffer < timeTil < buffer:
                    if note.note in heldFrets:
                        gotHit.add(note.note)
                        note.gotHit()
                        fret.targetVolume = 1.0
                        print('hit '+note.note)
            
            if len(gotHit) == 0:
                fret.cameraShake()
                print('openStrum')
            
            for fretLetter in heldFrets - gotHit:
                print('missStrum '+fretLetter)
        
        for note in fret.notesSustain.copy():
            if note.note not in heldFrets:
                note.deSpawnObj()
                
        
        
        if keys.accept in Click:
            char = util.input.select
            char.active = True
            char.camera = 1
            #char.scene.active_camera = char.scene.objects['Female Cam1']
            
            #char.arma.playAction('dance', 1, 96, play_mode=1)
            #print(char.arma.getActionName())
            bge.logic.getCurrentScene().end()
        
        
        
        
        
class EquipmentREAL(bge.types.KX_GameObject):
    
    def __init__(equip, DNU, sheet):
        #Discription#
        equip.uId = sheet['Discription']['uId']
        equip.nameProper = sheet['Discription']['nameProper']
        equip.discription = sheet['Discription']['discription']
        equip.type = sheet['Discription']['type']
        equip.tags = set()
        for tag in sheet['Discription']['tags'].split(','):    equip.tags.add(tag)
        
        #Path#
        equip.pathThumbNail = sheet['Path']['pathThumbNail']
        equip.pathMeshFemale = sheet['Path']['pathMeshFemale']
        equip.pathMeshMale = sheet['Path']['pathMeshMale']
        
        #Stats#
        equip.slot = sheet['Stats']['slot']


class Wepon(bge.types.KX_GameObject):
    
    def __init__(equip, DNU, sheet):
        #Discription#
        equip.uId = sheet['Discription']['uId']
        equip.nameProper = sheet['Discription']['nameProper']
        equip.discription = sheet['Discription']['discription']
        equip.type = sheet['Discription']['type']
        equip.tags = set()
        for tag in sheet['Discription']['tags'].split(','):    equip.tags.add(tag)
        
        #Path#
        equip.pathThumbNail = sheet['Path']['pathThumbNail']
        equip.pathMesh = sheet['Path']['pathMesh']


class Equipment(bge.types.KX_GameObject):
    
    def __init__(equip, DNU, sheet, char):
        equip.owner = char
        #Discription#
        equip.uId = sheet['Discription']['uId']
        equip.nameProper = sheet['Discription']['nameProper']
        equip.discription = sheet['Discription']['discription']
        equip.type = sheet['Discription']['type']
        equip.tags = set()
        for tag in sheet['Discription']['tags'].split(','):    equip.tags.add(tag)
        
        #Path#
        equip.pathThumbNail = sheet['Path']['pathThumbNail']
        #print(equip.uId)
        try:
            equip.pathMesh = sheet['Path']['pathMesh']
            equip.mesh = sheet['Stats']['mesh']
            #print('1')
        except KeyError:
            #print('2')
            if equip.owner.gender in {'female', 'feminine'}:
                equip.pathMesh = sheet['Path']['pathMeshF']
                equip.mesh = sheet['Stats']['meshF']
            else:
                equip.pathMesh = sheet['Path']['pathMeshM']
                equip.mesh = sheet['Stats']['meshM']
        
        
        util.load[equip.pathMesh] += 1
        util.load.updateModules()
        equip.replaceMesh(equip.mesh)
        









        
class Attack:
    def __init__(attk, sheet, owner):
        #Discription#
        attk.uId = sheet['Discription']['uId']
        attk.nameProper = sheet['Discription']['nameProper']
        attk.discription = sheet['Discription']['discription']
        attk.type = sheet['Discription']['type']
        attk.tags = set()
        for tag in sheet['Discription']['tags'].split(','):
            attk.tags.add(tag)
        
        #Path#
        attk.pathAniAttk = sheet['Path']['pathAniAttk']
        attk.pathAniDeff = sheet['Path']['pathAniDeff']
        attk.pathThumbNail = sheet['Path']['pathThumbNail']
        
        #Stats#
        attk.aniAttk = sheet['Stats']['aniAttk']
        attk.aniDeff = sheet['Stats']['aniDeff']
        attk.range = float(sheet['Stats']['range'])
        attk.proc = []
        for frame in sheet['Stats']['proc'].split(','):
            attk.proc.append(float(frame))
        attk.attkStat = sheet['Stats']['attkStat']
        attk.deffStat = sheet['Stats']['deffStat']
        
        attk.owner = owner
        attk.run = util.partial(getattr(util.actions, (sheet['Stats']['Action'])), attk, attk.owner)
        attk.target = None
        
        
        
