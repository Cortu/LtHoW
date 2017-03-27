import util
import bge

def non(thing):
    print('non'+thing.name)



def jukeBox(thing):
    print('juke')
    

    bge.logic.addScene('FoF')
    char = util.input.select
    char.camera = 3
    char.active = False
    char.arma.playAction('Idel', 1, 100, play_mode=1)
    
#    for char in util.input.select:
#        char.camera = 3
#        char.active = False



def enterVehicle(car):
    car.active = True
    util.input.select.active = False
    util.input.select.camEnabled = False
    car.camera = 1


def attkRanged(attk, attkr, deffr):
    attkObj = attkr.attkPost
    vec = attkObj.getVectTo(attk.aim)[1]
    vec.magnitude = attkObj.getVectTo(attk.aim)[0]
    from mathutils import Euler
    accuY = 0.02     #up down, about 0.1 - 0.01
    accuZ = 0.02     #left right, low is better
    from random import gauss
    eul = Euler((0.0, gauss(0, accuY), gauss(0, accuZ)))
    vec.rotate(eul)
    vec.magnitude += 10
    vec = vec + attkObj.worldPosition
    import Rasterizer
    Rasterizer.drawLine(attkObj.worldPosition, vec, attkr.teamColor)
    #attkr.worldPosition = vec
    hitObj = attkObj.rayCastTo(vec)
    try:
        hitName = hitObj.nameProper
    except AttributeError:
        hitName = str(hitObj)
    
    print(attkr.nameProper+' '+attk.nameProper+'s '+deffr.nameProper+' and hits '+hitName)


