import util
import bge

#########################
" Initilal Inialazation "
#########################
def iniIni(path, extention='ini'):
    import glob
    import configparser
    import os.path
    
    path = bge.logic.expandPath(path)
    path = path+'/**/*.'+extention
    pathList = glob.glob(path, recursive = True)

    #'//' = working directory of the blend.
    #'' = working directory of the ini.
    #'~' = user path.
    #'/' = absolute path.
    #'none' = special case
    for pathIni in pathList:
        sheet = configparser.ConfigParser()
        #print(pathIni)
        sheet.read(pathIni)
        pathDir = os.path.dirname(pathIni)
        try:
            for key, path in sheet['Path'].items():
                if path != 'none':
                    os.path.expanduser(path)
                    if path.startswith('//'):
                        path = bge.logic.expandPath('//'+path)
                    if not os.path.isabs(path):
                        path = pathDir+'/'+path
                sheet['Path'][key] = path
        except KeyError:    pass
        try:    sheet['Path']['ini'] = pathIni
        except KeyError:    sheet['Path'] = {'ini':pathIni}
        
        uId = sheet['Discription']['uId']
        util.sheets[uId] = sheet
        for tag in sheet['Discription']['tags'].split(','):
            try:    util.tags[tag].append(sheet)
            except KeyError:
                util.tags[tag] = []
                util.tags[tag].append(sheet)

#########
" Timer "
#########
class Timer():
    
    def __init__(self):
        from timeit import default_timer
        self.timer = default_timer
        self.start()
        
    def start(self):
        self.startTime = self.timer()
        self.stopTime = False
            
    def stop(self):
        self.stopTime = self.timer()
    
    def time(self):
        if self.stopTime:    print(self.stopTime - self.startTime)
        else:    print(self.timer() - self.startTime)



#################
" Input Catcher "
#################
# Sensors #
#anyKey
#mouseOver <- must have non empty property comand
#mouseLeft
#mouseMiddle
#mouseRight
#mouseUp
#mouseDown
def Click_getter(catcher):
        catcher.catch()
        return catcher._Click
def reClick_getter(catcher):
        catcher.catch()
        return catcher._reClick
def deClick_getter(catcher):
        catcher.catch()
        return catcher._deClick

class InputCatcher:
    Click = property(Click_getter)
    reClick = property(reClick_getter)
    deClick = property(deClick_getter)
    
    def __init__(self):
        self.button = None
        self.window = None
        self.hitPost = None
        self.cmd = [None]
        self.hitNode = None
        self.winOpened = False
        self.frameTime = None
        
        self._Click = set()
        self._reClick = set()
        self._deClick = set()
        
        self.joy0 = 0
        self.joy1 = 0
        self.joy2 = 0
        self.joy3 = 0
        
        self.select = None
        self.selectSet = set()
        self.p3 = False
        
        
    def catch(self):


#        cont = bge.logic.getCurrentController()
#        sens = cont.sensors
#        mouseOver = sens['mouseOver']
#        hitObj = mouseOver.hitObject
#        
#        self.hitWorld = mouseOver.hitPosition
#        #self.hitNode = [round(self.hitWorld.x), round(self.hitWorld.y)]
    
    
        if self.frameTime != bge.logic.getFrameTime():
            self.frameTime = bge.logic.getFrameTime()
            
            Click = set()
            reClick = set()
            deClick = set()
            
            joy = bge.logic.joysticks[0]
            try:
                self.joy0 = joy.axisValues[0]
                self.joy1 = -joy.axisValues[1]
                self.joy2 = joy.axisValues[2]
                self.joy3 = -joy.axisValues[3]
            except AttributeError:    pass
            
            try:
                for button in joy.activeButtons:
                    button += 1000
                    reClick.add(button)
                    if button >= 1000 and button not in self._Click and button not in self._reClick:
                        Click.add(button)
                for button in self._reClick:
                    try:
                        if button >=1000 and button -1000 not in joy.activeButtons:
                            deClick.add(button)
                    except TypeError:    pass
            except AttributeError:    pass
            
            self._Click = Click
            self._reClick = reClick
            self._deClick = deClick

        
          
#        camera = bge.logic.getCurrentScene().active_camera
#        mousePost = bge.logic.mouse.position
#        camera.getScreenRay(mousePost[0], mousePost[1], 0)
#        print(camera, mousePost)
        
        mouseOver = bge.logic.getCurrentController().owner.sensors['mouseOver']
        self.button = mouseOver.hitObject
        self.window = None
        self.hitWorld = mouseOver.hitPosition
        self.hitLocal = None
        
        if self.button:
            window = self.button
            count = 0
            while window.parent != None and count < 10:
                window = window.parent
                count += 1
            self.window = window
            self.hitLocal = self.hitWorld - window.worldPosition
            if self.button[mouseOver.propName]:
                self.cmd = self.button[mouseOver.propName].split(',')
            else:
                self.cmd = [False]
        
            
        for key,status in bge.logic.keyboard.active_events.items():
            if status == bge.logic.KX_INPUT_JUST_ACTIVATED:
                self._Click.add(key)
                self._reClick.add(key)
            if status == bge.logic.KX_INPUT_ACTIVE:
                self._reClick.add(key)
            if status == bge.logic.KX_INPUT_JUST_RELEASED:
                self._deClick.add(key)
        
        for key,status in bge.logic.mouse.active_events.items():
            if status == bge.logic.KX_INPUT_JUST_ACTIVATED:
                self._Click.add(key)
                self._reClick.add(key)
                if self.button:
                   for command in self.cmd:
                       self._Click.add(command)
                       self._reClick.add(command)
            if status == bge.logic.KX_INPUT_ACTIVE:
                self._reClick.add(key)
                if self.button:
                   for command in self.cmd:
                       self._reClick.add(command)
            if status == bge.logic.KX_INPUT_JUST_RELEASED:
                self._deClick.add(key)
                if self.button:
                   for command in self.cmd:
                       self._deClick.add(command)

        
        
        return self._Click, self._reClick, self._deClick




from collections import Counter
class LoadCounter(Counter):
    
    def updateModules(self):
        import bge 
        libList = bge.logic.LibList()
        
        for module,count in self.items():
            
            if count > 0 and module not in libList:
                bge.logic.LibLoad(module, 'Scene', load_actions=True)
            elif count == 0 and module in libList:
                bge.logic.LibFree(module)
            elif count < 0:
                bge.logic.LibFree(module)
                print(str(module)+' has a '+str(count)+' count!')
        self += Counter()
    
    def flush(self):
        for module, count in self.items():
            bge.logic.LibFree(module)
        self.clear()
