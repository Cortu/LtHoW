import util
import bge

class CharKiln(bge.types.KX_GameObject):
    def __init__(kiln, DNU):
        util.input.currentGM = kiln
        scene = bge.logic.getCurrentScene()
        util.scenes[scene.name] = scene
        kiln.quin = scene.objects['Char']
        bge.logic.addScene('Hud')
        kiln.sendMessage('pathThumbNail', kiln.quin.pathThumbNail, 'ThumbNail.Hud')
        
    
    
    def input(kiln):
        pass
        
    
    
    
    def message(kiln, subject, body):
        if subject.split(',')[0] == 'target':
            setattr(kiln.quin, subject.split(',')[1], float(body))
        
        
        if subject == 'startLeft':
            kiln.slot = 'left'
            subject = 'startMani'
        if subject == 'startRight':
            kiln.slot = 'right'
            subject = 'startMani'
        if subject == 'startBoth':
            kiln.slot = 'right'
            subject = 'startMani'
        
        if subject == 'startMani':
            bge.logic.addScene('Manifest')
            util.scenes['Hud'].end()
            kiln.maniText = body
            
            
            if body == 'char':
                stats = [{'name':'uId', 'loc0':'Discription', 'loc1':'uId'},
                    {'name':'type', 'loc0':'Discription', 'loc1':'type'},
                    {'name':'tags', 'loc0':'Discription', 'loc1':'tags'},
                    {'name':'gender', 'loc0':'Stats', 'loc1':'gender'}]
            else:
                stats = [{'name':'uId', 'loc0':'Discription', 'loc1':'uId'},
                    {'name':'type', 'loc0':'Discription', 'loc1':'type'},
                    {'name':'tags', 'loc0':'Discription', 'loc1':'tags'},
                    {'name':'slot', 'loc0':'Stats', 'loc1':'slot'}]
            
            kiln.maniStats = stats
            
        
        
        if subject == 'startScene':
            bge.logic.addScene(body)
            util.scenes['Hud'].end()
        
        if subject == 'stopScene':
            bge.logic.addScene('Hud')
            kiln.sendMessage('pathThumbNail', kiln.quin.pathThumbNail, 'ThumbNail.Hud')
            util.scenes[body].end()
            #scene = util.scenes[body]
            #util.scenes[body].active_camera = scene.objects['Camera Hud Off']
            #util.scenes[body].suspend()
        
        
        
        
        if subject == 'equip':
            sheet = util.sheets[body]
            type = sheet['Discription']['type']
            
            if type in {'Equipment', 'Race'}:
                slot = sheet['Stats']['slot']
                if slot == 'wepon':
                    slot = kiln.slot
                setattr(kiln.quin, slot, body)
            
            if type == 'Character':
                kiln.quin = util.stuff.Character(kiln.quin, sheet)
                
        
        if subject == 'name':
            kiln.quin.nameProper = body
            kiln.quin.uId = 'custom'+body.replace(' ', '')
        
        
        if subject == 'save':
            kiln.quin.save()
            kiln.sendMessage('pathThumbNail', kiln.quin.pathThumbNail, 'ThumbNail.Hud')

















