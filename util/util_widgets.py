import util
import bge




def imageSource_getter(thumb):
    return thumb._image

def imageSource_setter(thumb, image):
    try:    image = util.image2Array(image)
    except TypeError:    pass
    util.textureChange(thumb.display, image)
    thumb._image = image



class ThumbNail(bge.types.KX_GameObject):
    
    source = property(imageSource_getter, imageSource_setter)
    child = util.child_getter
    
    def __init__(thumb, DNU):
        #thumb.display = thumb.children[thumb.name+' Display']
        thumb.display = thumb.child('Display')
        thumb._image = None
    
    
    def input(thumb):
#        input = util.input
#        input.catch()
#        try:
#            thumbNum = input.button['thumbNum']
#            path = input.window.sheets[thumbNum]['Path']['pathThumbNail']
#            thumb.source = path
#            print(input.button['pathThumbNail'])
#        except (KeyError, TypeError):    pass
        try:    thumb.source = thumb.sensors['mouseOver'].hitObject['pathThumbNail']
        except TypeError:    pass
        #print(thumb.sensors['mouseOver'].hitObject['pathThumbNail'])
    
    def message(thumb, subject, body):
        if subject == 'pathThumbNail':
            thumb.source = body




def multiSceneTarg(mont):
    #if not mont._target:
    for scene in bge.logic.getSceneList():
        try:
            if str(scene) == mont['targetScene']:
                #mont._target = scene.objects[mont['target']]
                return scene.objects[mont['target']]
        except KeyError:    pass
    #return mont._target

class MultiSceneMoniter(bge.types.KX_GameObject):
    target = property(multiSceneTarg)
    def __init__(mont, DNU):
        mont._target = None
        mont.active = False
    
    def input(mont):
        if mont.active:
            util.input.catch()
            if util.input.window:
                #mont['pathThumbNail'] = util.input.window.pathThumbNail
                mont.sendMessage('pathThumbNail', util.input.window.pathThumbNail, mont['pathThumbNail'])
                mont.sendMessage('discription', util.input.window.discription, mont['discription'])
                mont.sendMessage('discription', util.input.window.nameProper, mont['nameProper'])
#            try:
#                #mont.target.source = mont.sensors['mouseOver'].hitObject[mont['source']]
#                source = getattr(mont.sensors['mouseOver'].hitObject, mont['source'])
#                setattr(mont.target, mont['dest'], source)
#            except (TypeError, AttributeError):    pass





def gameProp_getter(gameObj, prop):
    return gameObj[prop]

def gameProp_setter(gameObj, valu, prop):
    gameObj[prop] = valu

def gameProp_updater(gameObj, valu, prop, cmd):
    gameObj[prop] = valu
    getattr(gameObj, cmd)()




def text_getter(textBloc):
    return textBloc._text

def text_setter(textBloc, text):
    textBloc._text = text
    textBloc.update()

def scroll_getter(textBloc):
    return textBloc._scroll

def scroll_setter(textBloc, text):
    textBloc._scroll = text
    textBloc.update()





def textBlock_update(textBloc):
    pass
#    from textwrap import wrap
#    text = wrap(textBloc.text, width = textBloc.wrap)
#    textLen = len(text)
#    center = round(textLen * textBloc.scroll)
#    rowNum = textBloc.rowNum /2
#    if center < rowNum:    center = rowNum
#    elif center > textLen - rowNum:    center = textLen - rowNum
#    
#    start = int(center - rowNum)
#    finish = int(start + rowNum * 2)
    #start, finish, text = textPart(textBloc.text, textBloc.rowNum, textBloc.scroll, wrapNum = textBloc.wrap)
    
#    count = 0
#    for i in range(start, finish):
#        try:    line = text[i]
#        except IndexError:    line = ''
#        textBloc.lines[count].text = line
#        count += 1
    
    
#    text = textPart(textBloc.text, textBloc.rowNum, 1-textBloc.scrollY, wrapNum = textBloc.wrap)
#    for i, line in enumerate(text):
#        textBloc.lines[i].text = line
        






def listScroller(list, rowNum, post):
    rowHalf = rowNum / 2
    center = (len(list) - rowNum) * post + rowHalf
    start = int(center-rowHalf)
    finish = int(start + rowNum)
    
    listPart = []
    if start < 0:    mod = -start
    else:    mod = 0
    for i in range(start, finish):
        try:    line = list[i+mod]
        except IndexError:    line = ''
        listPart.append(line)
    return listPart




class TextBloc(bge.types.KX_GameObject):
    source = property( util.partial(gameProp_getter, prop='source'), util.partial(gameProp_updater, prop='source', cmd='update') )
    #text = property(text_getter, text_setter)
    #scroll = property(scroll_getter, scroll_setter)
    scrollY = property( util.partial(gameProp_getter, prop='scrollY'), util.partial(gameProp_updater, prop='scrollY', cmd='update') )
    
    def __init__(text, DNU):
        text.wrap = text['wrap']
        text.rowNum = text['lines']
        text['scrollY'] = 0.0
        text['source'] = ''
#        text._scroll = 0.0
#        text._text = ''
        text.back = text.children[text.name+' Back']
        
        text.lines = []
        for i in range(text.rowNum):
            line = text.children[text.name+' Line '+str(i)]
            text.lines.append(line)
        
        text.scrollY = 1.0
        text.source = ''



    def update(text):
        from textwrap import wrap
        #print(text.text)
        textList = wrap(text.source, width = text.wrap)
        textList = listScroller(textList, text.rowNum, 1-text.scrollY)
        
        #print(textList)
        
        #start = False
        for i, line in enumerate(textList):
            text.lines[i].text = line
    
    def input(text):
        try:    text.source = text.sensors['mouseOver'].hitObject['discription']
        except TypeError:    pass
    
    
    
    def message(text, subject, body):
        if subject == 'scrollY':
            text.scrollY = float(body)
        
        elif subject == 'discription':
            text.source = body




def scrollButton_getter(scroll, axis):
    return scroll[axis]

def scrollProp_updater(scroll, localHit, axis):
    if axis == 'x':    axisNum = 0
    elif axis == 'y':    axisNum = 1
    elif axis == 'z':    axisNum = 2
    localHit = util.capValu(localHit, 0.0, 1.0)
    scroll.button.localPosition[axisNum] = (localHit -0.5) *scroll.bar.localScale[axisNum]
    scroll[axis] = localHit



class Scroller(bge.types.KX_GameObject):
    child = util.child_getter
    target = property(multiSceneTarg)
    
    x = property( util.partial(gameProp_getter, prop='x'), util.partial(scrollProp_updater, axis='x') )
    y = property( util.partial(gameProp_getter, prop='y'), util.partial(scrollProp_updater, axis='y') )
    def __init__(scroll, DNU):
        #scroll.back = scroll.children[scroll.name+' Back']
        #scroll.bar = scroll.children[scroll.name+' Bar']
        #scroll.button = scroll.children[scroll.name+' Button']
        scroll.back = scroll.child('Back')
        scroll.bar = scroll.child('Bar')
        scroll.button = scroll.child('Button')
        scroll.scrollX = scroll['scrollX']
        scroll.scrollY = scroll['scrollY']
        scroll.scrolling = False
#        acts = scroll.actuators
#        prop = acts['Property']
#        print(type(prop.value))
        def iniProp(axis):
            try:
                scene, obj, prop = scroll[axis].split(',')
                obj = util.scenes[scene].objects[obj]
                value = obj[prop]
            except AttributeError:
                value = scroll[axis]
            setattr(scroll, axis, value)
        iniProp('x')
        iniProp('y')
        
        
        #scroll.y = scroll['y']
        #scroll['x'] = 0.5
        scroll._target = None
        if scroll.target:
            scroll.x = getattr(scroll.target, scroll['targetPropX'])
            scroll.y = getattr(scroll.target, scroll['targetPropY'])

    def input(scroll):
        pass
        Click = util.input.Click
        #reClick = util.input.reClick
        deClick = util.input.deClick
        keys = util.settings
        if util.input.window == scroll:
            if {keys.activate, 'scroller'} <= Click:
                scroll.scrolling = True
        if keys.activate in deClick:
            scroll.scrolling = False

        
        
        if scroll.scrolling:
            if scroll.scrollX:
                scroll.x = ((util.input.hitWorld.x - scroll.worldPosition.x)/scroll.bar.worldScale.x)+0.5
                if scroll.target:    setattr(scroll.target, scroll['targetPropX'], scroll.x)
            if scroll.scrollY:
#                scaleY = scroll.bar.worldScale.y
#                postY = util.input.hitWorld.y
#                worldMin = scroll.worldPosition.y - (scaleY/2)
#                worldMax = scroll.worldPosition.y + (scaleY/2)
#                postY = util.capValu(postY, worldMin, worldMax)
#                scroll.button.worldPosition.y = postY
#                scroll.y = scroll.button.localPosition.y /scroll.bar.localScale.y +0.5
#                scroll.y2 = scroll.y
#                scroll['y'] = scroll.y
                scroll.y = ((util.input.hitWorld.y - scroll.worldPosition.y)/scroll.bar.worldScale.y)+0.5
                if scroll.target:    setattr(scroll.target, scroll['targetPropY'], scroll.y)
                #localHit = util.capValu(localHit, 0.0, 1.0)
                #scroll.y = localHit


def maniUpdate(mani):
    from textwrap import shorten
    sheets = listScroller(mani.text, mani.rowNum, 1-mani.scrollY)
    mani.sheets = sheets
    titls = listScroller(mani.stats, mani.columnNum, mani.scrollX)
    mani.titls = titls
    for x, titl in enumerate(titls):
        mani.lines[x+1, 0].text = shorten(titl['name'], mani.wrap, placeholder="")
    
    
    mani.lines[0, 0].text = 'Name'
    for y, line in enumerate(sheets):
        if line != '':
            mani.lines[0, y+1].text = shorten(line['Discription']['nameProper'], mani.wrapName, placeholder="")
            mani.buttonRows[y]['pathThumbNail'] = line['Path']['pathThumbNail']
            mani.buttonRows[y]['discription'] = line['Discription']['discription']
            mani.buttonRows[y]['target'] = line
            for x in range(mani.columnNum):
                mani.lines[x+1, y+1].text = shorten(line[titls[x]['loc0']][titls[x]['loc1']], mani.wrap, placeholder="")
        else:
            mani.lines[0, y+1].text = ''
            mani.buttonRows[y]['pathThumbNail'] = '//stuff/system/NoImage.png'
            mani.buttonRows[y]['discription'] = ''
            mani.buttonRows[y]['target'] = line
            for x in range(mani.columnNum):
                mani.lines[x+1, y+1].text = ''
            
            
class Manifest(bge.types.KX_GameObject):
    text = property( util.partial(gameProp_getter, prop='text'), util.partial(gameProp_updater, prop='text', cmd='update') )
    scrollX = property( util.partial(gameProp_getter, prop='scrollX'), util.partial(gameProp_updater, prop='scrollX', cmd='update') )
    scrollY = property( util.partial(gameProp_getter, prop='scrollY'), util.partial(gameProp_updater, prop='scrollY', cmd='update') )
    #text = property(text_getter, text_setter)
    #scroll = property(scroll_getter, scroll_setter)
    update = maniUpdate
    def __init__(mani, DNU):
        
        mani['scrollX'] = 0.0
        mani['scrollY'] = 1.0
#        mani._scroll = 0.0
#        mani._text = ''
        mani.wrap = mani['wrap']
        mani.wrapName = mani['wrapName']
        mani.rowNum = mani['lines']
        mani.columnNum = mani['columns']
        #mani.stats = util.input.maniStats
        
        #print(util.tags['hair'])
        #mani.text = util.tags['hair']
        
        
        
#        ##this is each collom, the displayed name, then the spot in the sheet
#        ##the first colum is always the proper name, so this is just the colums that get shifted
#        mani.stats = [{'name':'uId', 'loc0':'Discription', 'loc1':'uId'},
#            {'name':'type', 'loc0':'Discription', 'loc1':'type'},
#            {'name':'tags', 'loc0':'Discription', 'loc1':'tags'},
#            {'name':'slot', 'loc0':'Stats', 'loc1':'slot'}]
        
        #mani.stats = util.input.maniStats
        
        
        import numpy as np
        mani.lines = np.empty( (5,11), dtype=object)
        mani.names = []
        mani.infos = []
        for x in range(1, 5):
            for y in range(0, 11):
                mani.lines[x, y] = mani.children['c'+str(x)+'r'+str(y+1)+'t']
        for y in range(0, 11):
            mani.lines[0, y] = mani.children['n'+str(y+1)+'t']
        
        mani.buttonRows = []
        for y in range(mani.rowNum):
            mani.buttonRows.append(mani.children['r'+str(y+2)])
        
        
        #print(equips[0]['Discription']['uId'])
        
        #text = textPart(equips, 10, 0.5)
        #mani.update()
        ##this is a list of sheets that will be read from, it run update
        jinni = util.input.currentGM
        mani.stats = jinni.maniStats
        mani.text = util.tags[jinni.maniText]
    
    def input(mani):
        input = util.input
        Click = input.Click
        
        
        if 'sortName' in Click:
            #prt = getAttrSheet(mani.text[0], 'Discription', 'nameProper')
            #print(prt)
            mani.text.sort(key=util.partial(util.getAttrSheet, section='Discription', item='nameProper'))
            mani.update()
        
        if 'sort' in Click:
            i = input.button['column']-1
            mani.text.sort(key=util.partial(util.getAttrSheet, section=mani.titls[i]['loc0'], item=mani.titls[i]['loc1']))
            mani.update()
        
        if 'equip' in Click:
#            sheet = input.button['target']
#            if sheet != '':
#                newSet = set()
#                for char in util.input.select:
#                    new = util.subStuff(char, sheet)
#                    newSet.add(new)
#                util.input.select = newSet
#            print(sheet['Discription']['uId'])



#            sheet = input.button['target']
#            uId = sheet['Discription']['uId']
#            slot = sheet['Stats']['slot']
#            for char in util.input.select:
#                setattr(char, slot, uId)




            
#            bge.logic.getCurrentScene().replace(util.input.maniReturn)
#            for scene in bge.logic.getSceneList():
#                if scene.name == 'Kiln':
#                    scene.restart()
#            util.input.select = set()
#            util.load.flush()
#            scene = util.getScene('Main')
#            jinni = scene.objects['Main JinniGM']
#            sheet = input.button['target']
#            jinni.sheet['Equip'][sheet['Stats']['slot']] = sheet['Discription']['uId']

            sheet = input.button['target']
            uId = sheet['Discription']['uId']
            mani.sendMessage('equip', uId)



            
    def message(mani, subject, body):
        if subject == 'scrollY':
            mani.scrollY = float(body)
        elif subject == 'scrollX':
            mani.scrollX = float(body)
        
        if subject == 'stats':
            print(body)
            #mani.stats = body
            








class Button(bge.types.KX_GameObject):
    child = util.child_getter
    def __init__(button, DNU):
        button.button = button.child('Button')
    
    def input(button):
        keys = util.settings
        Click = util.input.Click
        if {keys.activate, 'startTargets'} <= Click:
            bge.logic.getCurrentScene().replace('Targets')
            for char in util.input.select:    char.camera = 4



    


class Console(bge.types.KX_GameObject):
    child = util.child_getter
    def __init__(console, DNU):
        console.text = console.child('Text')
        console.text.text = util.input.currentGM.quin.nameProper
        console.button = console.child('Button')
        console.typing = False
        console.colText = console.text.color.copy()
        console.colButton = console.button.color.copy()
    
    def input(console):
        keys = util.settings
        Click = util.input.Click
        reClick = util.input.reClick
        if {keys.activate, 'consoleEdit'} <= Click:
            console.typing = True
            console.button.color = console.colText
            console.text.color = console.colButton
            console.wrap = console['wrap']
        
        if console.typing:
            if bge.events.LEFTSHIFTKEY in reClick or bge.events.RIGHTSHIFTKEY in reClick:    shift = True
            else:    shift = False
            
            if bge.events.ENTERKEY in Click:
                console.typing = False
                console.text.color = console.colText
                console.button.color = console.colButton
                console['text'] = console.text.text
            elif bge.events.BACKSPACEKEY in Click:    console.text.text = console.text.text[:-1]
            elif len(console.text.text) <= console.wrap:
                for key in Click:
                    try:
                        letter = bge.events.EventToCharacter(key, shift)
                        console.text.text += letter
                    except TypeError:    pass



def char_getter(menu):
    from random import sample
    return sample(util.input.select, 1)[0]

class KilnMenu(bge.types.KX_GameObject):
    target = property(char_getter)
    child = util.child_getter
    def __init__(menu, DNU):
        scene = util.getScene('Main')
        jinni = scene.objects['Main JinniGM']
        menu.jinni = jinni
        menu.nameP = menu.child('Name')
#        from random import sample
#        menu.target = sample(util.input.select, 1)[0]
        menu.nameP.text.text = menu.jinni.sheet['Discription']['nameProper']
        #menu.target.camera = 3
        menu.thumb = menu.child('ThumbNail')
        #print(menu.target.pathThumbNail)
        #menu.thumb.source = menu.target.pathThumbNail
        menu.thumb.source = jinni.sheet['Path']['pathThumbNail']
        
    def input(menu):
        keys = util.settings
        Click = util.input.Click
        #deClick = util.input.deClick
        if bge.events.ENTERKEY in Click:
            #menu.target.nameProper = menu.nameP.text.text
            #scene = util.getScene('Main')
            #jinni = scene.objects['Main JinniGM']
            #menu.target.uId = 'custom'+menu.nameP.text.text.replace(' ', '')
            menu.jinni.sheet['Discription']['nameProper'] = menu.nameP.text.text
            menu.jinni.sheet['Discription']['uId'] = 'custom'+menu.nameP.text.text.replace(' ', '')
            util.load.flush()
            util.getScene('Kiln').restart()
            
        if {keys.activate, 'saveChar'} <= Click:
            menu.target.save(thumb=True)
            menu.thumb.source = menu.target.pathThumbNail
        
        if {keys.activate, 'infoChars'} <= Click:
            util.input.maniTags = 'char'
            util.input.maniStats = [
                {'name':'uId', 'loc0':'Discription', 'loc1':'uId'},
                {'name':'type', 'loc0':'Discription', 'loc1':'type'},
                {'name':'tags', 'loc0':'Discription', 'loc1':'tags'},
                {'name':'brow', 'loc0':'Targets', 'loc1':'brow'},
                {'name':'cheek', 'loc0':'Targets', 'loc1':'cheek'},
                {'name':'pThumbn', 'loc0':'Path', 'loc1':'pathThumbNail'}]
            for char in util.input.select:    char.camera = 3
            bge.logic.getCurrentScene().replace('Manifest')
        
        if {keys.activate, 'infoHairs'} <= Click:
            util.input.maniTags = 'hair'
            util.input.maniStats = [
                {'name':'uId', 'loc0':'Discription', 'loc1':'uId'},
                {'name':'type', 'loc0':'Discription', 'loc1':'type'},
                {'name':'tags', 'loc0':'Discription', 'loc1':'tags'},
                {'name':'path', 'loc0':'Path', 'loc1':'pathMeshFemale'},
                {'name':'path', 'loc0':'Path', 'loc1':'pathMeshMale'},
                {'name':'pThumbn', 'loc0':'Path', 'loc1':'pathThumbNail'}]
            for char in util.input.select:    char.camera = 4
            bge.logic.getCurrentScene().replace('Manifest')
            util.input.maniReturn = 'Menu'

        if {keys.activate, 'infoHands'} <= Click:
            util.input.maniTags = 'hands'
            util.input.maniStats = [
                {'name':'uId', 'loc0':'Discription', 'loc1':'uId'},
                {'name':'type', 'loc0':'Discription', 'loc1':'type'},
                {'name':'tags', 'loc0':'Discription', 'loc1':'tags'},
                {'name':'path', 'loc0':'Path', 'loc1':'pathMeshFemale'},
                {'name':'path', 'loc0':'Path', 'loc1':'pathMeshMale'},
                {'name':'pThumbn', 'loc0':'Path', 'loc1':'pathThumbNail'}]
            for char in util.input.select:    char.camera = 3
            bge.logic.getCurrentScene().replace('Manifest')
            util.input.maniReturn = 'Menu'

        if {keys.activate, 'infoTorso'} <= Click:
            util.input.maniTags = 'torso'
            util.input.maniStats = [
                {'name':'uId', 'loc0':'Discription', 'loc1':'uId'},
                {'name':'type', 'loc0':'Discription', 'loc1':'type'},
                {'name':'tags', 'loc0':'Discription', 'loc1':'tags'},
                {'name':'path', 'loc0':'Path', 'loc1':'pathMeshFemale'},
                {'name':'path', 'loc0':'Path', 'loc1':'pathMeshMale'},
                {'name':'pThumbn', 'loc0':'Path', 'loc1':'pathThumbNail'}]
            for char in util.input.select:    char.camera = 3
            bge.logic.getCurrentScene().replace('Manifest')
            util.input.maniReturn = 'Menu'
        
        if {keys.activate, 'infoLegs'} <= Click:
            util.input.maniTags = 'legs'
            util.input.maniStats = [
                {'name':'uId', 'loc0':'Discription', 'loc1':'uId'},
                {'name':'type', 'loc0':'Discription', 'loc1':'type'},
                {'name':'tags', 'loc0':'Discription', 'loc1':'tags'},
                {'name':'path', 'loc0':'Path', 'loc1':'pathMeshFemale'},
                {'name':'path', 'loc0':'Path', 'loc1':'pathMeshMale'},
                {'name':'pThumbn', 'loc0':'Path', 'loc1':'pathThumbNail'}]
            for char in util.input.select:    char.camera = 3
            bge.logic.getCurrentScene().replace('Manifest')
            util.input.maniReturn = 'Menu'
            
        if {keys.activate, 'infoFeet'} <= Click:
            util.input.maniTags = 'feet'
            util.input.maniStats = [
                {'name':'uId', 'loc0':'Discription', 'loc1':'uId'},
                {'name':'type', 'loc0':'Discription', 'loc1':'type'},
                {'name':'tags', 'loc0':'Discription', 'loc1':'tags'},
                {'name':'path', 'loc0':'Path', 'loc1':'pathMeshFemale'},
                {'name':'path', 'loc0':'Path', 'loc1':'pathMeshMale'},
                {'name':'pThumbn', 'loc0':'Path', 'loc1':'pathThumbNail'}]
            for char in util.input.select:    char.camera = 3
            bge.logic.getCurrentScene().replace('Manifest')
            util.input.maniReturn = 'Menu'
        
        if {keys.activate, 'infoAccessory'} <= Click:
            util.input.maniTags = 'accessory'
            util.input.maniStats = [
                {'name':'uId', 'loc0':'Discription', 'loc1':'uId'},
                {'name':'type', 'loc0':'Discription', 'loc1':'type'},
                {'name':'tags', 'loc0':'Discription', 'loc1':'tags'},
                {'name':'path', 'loc0':'Path', 'loc1':'pathMeshFemale'},
                {'name':'path', 'loc0':'Path', 'loc1':'pathMeshMale'},
                {'name':'pThumbn', 'loc0':'Path', 'loc1':'pathThumbNail'}]
            for char in util.input.select:    char.camera = 3
            bge.logic.getCurrentScene().replace('Manifest')
            util.input.maniReturn = 'Menu'



def kilnTarg_setter(jinni, value, attr):
    for char in util.input.select:
        setattr(char, attr, value)
    jinni.sheet['Targets'][attr] = str(value)
def kilnTarg_getter(jinni, attr):
    return float(jinni.sheet['Targets'][attr])


class KilnJinniGM(bge.types.KX_GameObject):
    cheek = property(
        util.partial(kilnTarg_getter, attr='cheek'),
        util.partial(kilnTarg_setter, attr='cheek'))
    brow = property(
        util.partial(kilnTarg_getter, attr='brow'),
        util.partial(kilnTarg_setter, attr='brow'))
    ear = property(
        util.partial(kilnTarg_getter, attr='ear'),
        util.partial(kilnTarg_setter, attr='ear'))
    mouth = property(
        util.partial(kilnTarg_getter, attr='mouth'),
        util.partial(kilnTarg_setter, attr='mouth'))
    rotate = property(
        util.partial(kilnTarg_getter, attr='rotate'),
        util.partial(kilnTarg_setter, attr='rotate'))
    lid = property(
        util.partial(kilnTarg_getter, attr='lid'),
        util.partial(kilnTarg_setter, attr='lid'))
    greek = property(
        util.partial(kilnTarg_getter, attr='greek'),
        util.partial(kilnTarg_setter, attr='greek'))
    curve = property(
        util.partial(kilnTarg_getter, attr='curve'),
        util.partial(kilnTarg_setter, attr='curve'))
    size = property(
        util.partial(kilnTarg_getter, attr='size'),
        util.partial(kilnTarg_setter, attr='size'))
    width = property(
        util.partial(kilnTarg_getter, attr='width'),
        util.partial(kilnTarg_setter, attr='width'))
    volume = property(
        util.partial(kilnTarg_getter, attr='volume'),
        util.partial(kilnTarg_setter, attr='volume'))
    height = property(
        util.partial(kilnTarg_getter, attr='height'),
        util.partial(kilnTarg_setter, attr='height'))
    chin = property(
        util.partial(kilnTarg_getter, attr='chin'),
        util.partial(kilnTarg_setter, attr='chin'))
    jaw = property(
        util.partial(kilnTarg_getter, attr='jaw'),
        util.partial(kilnTarg_setter, attr='jaw'))
    afro = property(
        util.partial(kilnTarg_getter, attr='afro'),
        util.partial(kilnTarg_setter, attr='afro'))
    euro = property(
        util.partial(kilnTarg_getter, attr='euro'),
        util.partial(kilnTarg_setter, attr='euro'))
    asio = property(
        util.partial(kilnTarg_getter, attr='asio'),
        util.partial(kilnTarg_setter, attr='asio'))
    
    def __init__(jinni, DNU):
        bge.logic.addScene('Kiln', 0)
        bge.logic.addScene('Menu', 1)
        
        import copy
        jinni.sheet = copy.copy(util.sheets['baseJeanSung'])


















