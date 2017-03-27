import util
import bge

def collisionRegister(dynObj, hitObj, point, normal):
    hitPoint = util.classes.CollisionPoint(hitObj, point, normal, dynObj.lvlGround.worldPosition.z)
    dynObj.coliSet.add(hitPoint)

def coliFlush(coliSet):
    for coliPoint in coliSet.copy():
        if coliPoint.delMe:
            coliSet.remove(coliPoint)
        else:
            coliPoint.delMe = True


def dynRotate(dynObj, angle, axis='z', orin=True, velo=True):
    from mathutils import Euler
    angle *= util.turn
    if axis == 'z':    eul = Euler((0.0, 0.0, angle))
    elif axis == 'x':    eul = Euler((angle, 0.0, 0.0))
    elif axis == 'y':    eul = Euler((0.0, angle, 0.0))
    if orin:    dynObj.localOrientation.rotate(eul)
    if velo:    dynObj.localLinearVelocity.rotate(eul)



def onGround(dynObj):
    for coli in dynObj.coliSet:
        if coli.ground:
            return True
    return False

def onWall(dynObj):
    for coli in dynObj.coliSet:
        if not coli.ground:
            return True
    return False

def alin2Normal(dynObj, normal):
    dynObj.worldLinearVelocity = dynObj.wLV
    dynObj.onVertB = dynObj.wLV
    agl = dynObj.wLV.copy()
    agl.resize(2)
    normal.resize(2)
    agl = agl.angle_signed(normal)
    if agl >0:    agl = 1/4 *util.turn -agl
    else:    agl = -(agl + 1/4 *util.turn)
    
    from mathutils import Euler
    eul = Euler((abs(agl), 0.0, agl))
    dynObj.localLinearVelocity.rotate(eul)
    print(agl)
    dynObj.onVertA = agl
    dynObj.vertRetrn = dynObj.wLV.copy()
    dynObj.vertRetrn.rotate(Euler( (0.0, 0.0, 2*agl) ))




def skateLand(dynObj):
    dynObj.worldLinearVelocity = dynObj.wLV
    agl = 1/4 *util.turn
    from mathutils import Euler
    eul = Euler((-agl, 0.0, 0.0))
    print(dynObj.localLinearVelocity)
    dynObj.localLinearVelocity.rotate(eul)
    print(dynObj.localLinearVelocity)
    print('-')



def vehicleDrive(car, pedal):
    force = car.forcePerWheel *pedal *50
    for wheel in car.driveTrain:
        car.wrapper.applyEngineForce(-force, wheel.num)
    force = car.jet *pedal *50
    car.applyForce([0.0, force, 0.0],  True)


def vehicleTurn(car, pedal):
    for wheel in car.steering:
        turn = wheel.turnAngle * pedal
        car.wrapper.setSteeringValue(-turn, wheel.num)
    if car.lean:
        #turn = car.leanAngle *pedal *(abs(car.speed)/100)
        turn = car.leanAngle *pedal
        car.localAngularVelocity.z -= turn
        lean = pedal* 1/8 *util.turn
        from mathutils import Euler
        lean = Euler((0.0, lean, 0.0))
        car.body.localOrientation = lean
    
def vehicleBreak(car, pedal):
    pedal = (pedal + 1)/2
    force = car.breakForce *pedal *50 / len(car.wheels)
    for wheel in car.wheels:
        car.wrapper.applyBraking(force, wheel.num)
    resist = car.pResistance *(pedal)
    resist += car.resistance
    stab = car.pStability *(pedal)
    stab += car.stability
    car.setDamping(resist, stab)
    
    
    
def speedMps2Kph(dynObj):
    velo = dynObj.localLinearVelocity
    if velo.y >= 0:    return velo.magnitude * 3.6
    else:    return velo.magnitude * -3.6


def updateTraction(car, pedalDrive, pedalTurn,  pedalBreak):
    #traction = (1 - abs(pedalDrive) * abs(pedalTurn)) *wheel.traction
    pedalDrive = abs(pedalDrive)
    pedalTurn = abs(pedalTurn)
    pedalBreak = (pedalBreak + 1)/2
    tracBreak = pedalBreak /2
    for wheel in car.wheels:
        traction = 1
        if wheel.drive:
            traction -= pedalDrive * pedalTurn
            traction += len(car.driveTrain)/8
            traction -= tracBreak
        if wheel.steer:
            traction += tracBreak
            
        if traction < 0:    traction = 0
        traction *= wheel.traction
        car.wrapper.setTyreFriction(traction, wheel.num)


#  LOOK AT ME
#  Check camera methods for pointing to an object on the hud
#  FOV cyber?
def cameraShake(camera):
    if not camera['shaking']:
        from random import randint
        start = randint(1, 500000-12)
        act = camera.actuators['Shake']
        act.frameStart = start
        act.frameEnd = start + 12
        camera['shaking'] = True
    



def propDuration_setter(gameObj, value):
    gameObj['duration'] = value

def propDuration_getter(gameObj):
    return gameObj['duration']
    
def timerRemaing_getter(timer):
    return (bge.logic.getFrameTime() - timer.startTime) / bge.logic.getTimeScale()
