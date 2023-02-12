import json

def getCurrentSeconds(startSceneTicks,currentTicks):
    seconds = (currentTicks-startSceneTicks)/1000
    roundedSeconds = int(round(seconds))
    return roundedSeconds

def getSettingsJSON():
    jsonSettings = open('settings.json','r')
    jsonString = jsonSettings.read()
    jsonConverted = json.loads(jsonString)
    return jsonConverted

#get the width trought the get_size function
def getWidth(object):
    width = object.get_size()[0]
    return width

#get the width trought the get_size function
def getHeight(object):
    height = object.get_size()[1]
    return height

def addToRenderStack(element,x,y,priority):
    renderElement = {'element':element,'x':x,'y':y,'priority':priority}
    return renderElement

def updateFramerateMultiplier(clockFramerate,framerateLimit):
    framerateMultiplier = clockFramerate.tick(framerateLimit)
    return framerateMultiplier

