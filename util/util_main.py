import util
import bge

def subStuff(gameObj, sheet):
    objType = sheet['Discription']['type']
    objType = getattr(util.stuff, objType)
    return objType(gameObj, sheet)
    
def subOtherStuff(gameObj, objType):
    objType = getattr(util.stuff, objType)
    return objType(gameObj)

def subWidget(gameObj, objType):
    objType = getattr(util.widgets, objType)
    return objType(gameObj)

def subGM(gameObj, objType):
    objType = getattr(util.gm, objType)
    return objType(gameObj)



##################
" Image to Array "
##################
def image2Array(path):
    path = bge.logic.expandPath(path)
    
    import os
    if not os.path.isfile(path):    print(path,'Not Found')
    
    image = bge.texture.ImageFFmpeg(path)
    imageBuffer = bge.texture.imageToArray(image, 'RGBA')
    
    import numpy as np
    outArray = np.array(imageBuffer, np.uint8).reshape(image.size[0], image.size[1], 4)
    
    return outArray




##################
" Array to Image "
##################
#This code was taken from Stack Exchange without regard for liceing or acridation.
#It has minor changes to make it more compatable with the BGE.
#I dont realy understand exactly what the majority of this dose.
def buff2PNG(imageBuffer, imageName):
    imageHight = imageBuffer.shape[0]
    imageWith = imageBuffer.shape[1]
    
    def write_png(buf, width, height):
        """ buf: must be bytes or a bytearray in py3, a regular string in py2. formatted RGBARGBA... """
        import zlib, struct

        # reverse the vertical line order and add null bytes at the start
        width_byte_4 = width * 4
        raw_data = b''.join(b'\x00' + buf[span:span + width_byte_4]
                            for span in range((height - 1) * width * 4, -1, - width_byte_4))

        def png_pack(png_tag, data):
            chunk_head = png_tag + data
            return (struct.pack("!I", len(data)) +
                    chunk_head +
                    struct.pack("!I", 0xFFFFFFFF & zlib.crc32(chunk_head)))

        return b''.join([
            b'\x89PNG\r\n\x1a\n',
            png_pack(b'IHDR', struct.pack("!2I5B", width, height, 8, 6, 0, 0, 0)),
            png_pack(b'IDAT', zlib.compress(raw_data, 9)),
            png_pack(b'IEND', b'')])


    buf = bytearray(imageBuffer)
    data = write_png(buf, imageHight, imageWith)
    with open(imageName, 'wb') as fd:
        fd.write(data)





##################
" Texture Change "
##################
def textureChange(self, ffObj, matId = 0, textuId = 0):
    name = 'newTextu'+';'+str(matId)+','+str(textuId)
    try:
        if ffObj == None:    del self[name]
        else:
            self[name] = bge.texture.Texture(self, matId, textuId)
            try:    self[name].source = ffObj
            except TypeError:
                self[name].source = bge.texture.ImageBuff()
                self[name].source.filter = bge.texture.FilterRGBA32()
                buf = bytearray(ffObj)
                self[name].source.load(buf, ffObj.shape[0], ffObj.shape[1])
            self[name].refresh(False)
    except KeyError:    pass


def dtime2secs(dtime, tempo, ticks):
    #dtime = time measured in "ticks", 0 to 268435455
    #tempo = microseconds per crochet (quarter-note), 0 to 16777215
    #ticks = the number of ticks per crochet (quarter-note)
    
    #microseconds_per_tick = tempo / ticks
    #song_time_in_microseconds = dtime * microseconds_per_tick
    #song_time_in_seconds = song_time_in_microseconds * 0.000001
    #all_together = (tempo/ticks) * dtime * 1/1,000,000 or (tempo * dtime) / (ticks * 1000000)
    
    return (tempo * dtime) / (ticks * 1000000)




def scaleUV(object, u=1, v=1):
    #This acts on the refrence mesh, thus requiering libNew.
    for mesh in object.meshes:
       for m_index in range(len(mesh.materials)):
          for v_index in range(mesh.getVertexArrayLength(m_index)):
             vertex = mesh.getVertex(m_index, v_index)
             vertex.u *= u
             vertex.v *= v
 
 
 
def capValu(valu, min, max):
    if valu < min:    valu = min
    elif valu > max:    valu = max
    return valu


def getAttrSheet(sheet, section, item):
    return sheet[section][item]




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



def child_getter(gameObj, child):
    name = gameObj.name.split('.')
    try:    suffix = '.'+name[1]
    except IndexError: suffix = ''
    return gameObj.childrenRecursive[name[0] +' '+child+ suffix]



##################
" Texture Change "
##################
#If the Embeded Player resolution is not square then the image will be stretched.
def capThumb(camera, path):
    ir = bge.texture.ImageRender(camera.scene, camera)
    ir.capsize = 128,128
    ir.background = [127, 127, 127, 255]
    import numpy as np
    outArray = np.array(ir, np.uint8).reshape(ir.size[0], ir.size[1], 4)
    buff2PNG(outArray, path)


def getScene(sceneName):
    for scene in bge.logic.getSceneList():
        if scene.name == sceneName:
            return scene



def sortByDistance(gameObj, list):
    def getDist(other):
        return gameObj.getDistanceTo(other)
    
    return sorted(list, key=getDist)



