import pygame
import operator
from functions import *

#Functions Porting TODO
#-------------------------------

def runRender(renderScreenStack,overlayScreenStack):
    
    #renderScrenStack
    #reordering stack example
    if renderScreenStack:
        renderScreenStack = sorted(renderScreenStack, key = operator.itemgetter('y', 'x'),reverse=True)
        renderScreenStack = sorted(renderScreenStack, key = operator.itemgetter('priority',))

        for renderElement in renderScreenStack:
            renderScreen.blit(renderElement['element'],(renderElement['x'],renderElement['y']))
    
    #reordering stack example
    if overlayScreenStack:
        overlayScreenStack = sorted(overlayScreenStack, key = operator.itemgetter('y', 'x'),reverse=True)
        overlayScreenStack = sorted(overlayScreenStack, key = operator.itemgetter('priority',))


        for renderElement in overlayScreenStack:
            overlayScreen.blit(renderElement['element'],(renderElement['x'],renderElement['y']))
        
    upscaledRenderScreen = pygame.transform.scale(renderScreen, (mainScreenWidth,mainScreenHeight))
    mainScreen.blit(upscaledRenderScreen, (0,0))
    mainScreen.blit(overlayScreen, (0,0))        
    pygame.display.update()
#-------------------------------
pygame.init() 

#customEvents
startSceneTicks = pygame.time.get_ticks()
AddBootEvent = pygame.USEREVENT + 0 #32850
bootEvent = pygame.event.Event(AddBootEvent)
pygame.event.post(bootEvent)

#getSettingsFromJSON
mainScreenWidth     = getSettingsJSON()['mainScreenWidth']
mainScreenHeight    = getSettingsJSON()['mainScreenHeight']
windowCaption       = getSettingsJSON()['windowCaption']
downscaleMultiplier = getSettingsJSON()['downscaleMultiplier']
windowMode          = getSettingsJSON()['windowMode']

#mainScreen
icon = pygame.image.load('images/logo.png')
pygame.display.set_icon(icon)
pygame.display.set_caption(windowCaption)

if windowMode == "resizable":
    mainScreen = pygame.display.set_mode((mainScreenWidth,mainScreenHeight),pygame.RESIZABLE)
elif windowMode == "fullscreen":
    mainScreen = pygame.display.set_mode((mainScreenWidth,mainScreenHeight),pygame.FULLSCREEN)
else:
    mainScreen = pygame.display.set_mode((mainScreenWidth,mainScreenHeight))

#renderScreen
renderScreenWidth  = mainScreenWidth  / downscaleMultiplier
renderScreenHeight = mainScreenHeight / downscaleMultiplier
renderScreen = pygame.Surface((renderScreenWidth,renderScreenHeight),pygame.SRCALPHA)

#overlayScreen
overlayScreen = pygame.Surface((mainScreenWidth,mainScreenHeight),pygame.SRCALPHA)

#framerate
framerateLimit = getSettingsJSON()['framerateLimit']
clockFramerate = pygame.time.Clock()
framerateMultiplier = 1
    
#colors
whiteColor = 255, 255, 255 
blackColor = 0, 0, 0
transparentColor = 0, 0, 0, 0

#fonts
pygame.font.init()
m5x7_16 = pygame.font.Font('fonts/m5x7.ttf',16)
m5x7_32 = pygame.font.Font('fonts/m5x7.ttf',32)
m5x7_64 = pygame.font.Font('fonts/m5x7.ttf',64)

#static game elements
logoImg = pygame.image.load('images/logo.png').convert()
logoText = m5x7_32.render('Pygame Boilerplate', True, whiteColor)
helloworldText = m5x7_32.render('Hello World!', True, whiteColor)
logoTextWebsite = m5x7_16.render('studioultima.com', True, whiteColor)
fadeInScreen = pygame.Surface((renderScreenWidth,renderScreenHeight),pygame.SRCALPHA)
menuItems = [{'value':'newgame','label':'NEW GAME','selected':bool(1)},{'value':'continue','label':'CONTINUE','selected':bool(0)},{'value':'settings','label':'SETTINGS','selected':bool(0)},{'value':'exit','label':'EXIT','selected':bool(0)}]
settingsMenuItems = [{'value':'windowMode','label':'Window Mode: default (' + str(windowMode) +')','selected':bool(1)},{'value':'fpsChange','label':'Limit FPS: default (' + str(framerateLimit) +')','selected':bool(0)},{'value':'save','label':'Apply','selected':bool(0)},{'value':'mainMenu','label':'Go back to the main menu','selected':bool(0)}]
windowModeSubMenuItems = [{'value':getSettingsJSON()['windowMode'],'label':'Window Mode: ' + str(getSettingsJSON()['windowMode']) + ' (default)','selected':bool(1)},{'value':'fullscreen','label':'Window Mode: fullscreen','selected':bool(0)}, {'value':'resizable','label':'Window Mode: resizable','selected':bool(0)},{'value':'normal','label':'Window Mode: normal','selected':bool(0)}]
fpsChangeSubMenuItems = [{'value':getSettingsJSON()['framerateLimit'],'label':'Limit FPS: '+ str(getSettingsJSON()['framerateLimit']) + ' (default)','selected':bool(1)},{'value':30,'label':'Limit FPS: 30 Fps','selected':bool(0)}, {'value':60,'label':'Limit FPS: 60 Fps','selected':bool(0)}]
menuPointer = ''
placeHolder = m5x7_32.render(str(menuPointer) + ' ' + 'placeholder', True, whiteColor)

#game Flags & Variables
settingDummyFpsLimit = framerateLimit
settingDummyWindowMode = windowMode
currentScene = 'splashscreen'
finishedFadeInFlag = bool(0)
transparencyFadeInScreen = 255
transparencyTransitionSpeed = 0.1



#gameLoop
while True:
    #update Framerate Multiplier
    framerateMultiplier = updateFramerateMultiplier(clockFramerate,framerateLimit)

    #resetting screens --> TODO make it a function
    mainScreen.fill(blackColor) 
    renderScreen.fill(blackColor) 
    overlayScreen.fill(transparentColor) 
    #-------------------

    if currentScene == 'splashscreen':

        #-------------------------------
        sceneName = 'Splash Screen'
        nextScene = 'splashscreen'

        for event in pygame.event.get():
            #debug events
            #print (event)
            #Quitting the game
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pass
                if event.key == pygame.K_RETURN:
                    nextScene = 'mainMenu'  
                    startSceneTicks = pygame.time.get_ticks()
            if event.type == pygame.USEREVENT + 0:
                print ('BootEvent') 

        
        renderScreenStack =  []
        overlayScreenStack = []

        sceneTimeWidget = m5x7_32.render('Scene Time: ' + str(getCurrentSeconds(startSceneTicks,pygame.time.get_ticks())), True, whiteColor)
        fpsCounter = m5x7_32.render('FPS: ' + str(round(clockFramerate.get_fps())), True, whiteColor)
        sceneNameWidget = m5x7_32.render('Scene: ' + str(sceneName), True, whiteColor)

        overlayScreenStack.append(addToRenderStack(sceneNameWidget,0,0,0))
        overlayScreenStack.append(addToRenderStack(sceneTimeWidget,0,0 + getHeight(sceneNameWidget),0))
        overlayScreenStack.append(addToRenderStack(fpsCounter,mainScreenWidth - getWidth(fpsCounter),0,0))

        if getCurrentSeconds(startSceneTicks,pygame.time.get_ticks()) > 0 :
            if finishedFadeInFlag == bool(0):
                if transparencyFadeInScreen > 0:
                    failsafePrediction = transparencyFadeInScreen - (transparencyTransitionSpeed * framerateMultiplier)
                    if failsafePrediction <= 0:
                        transparencyFadeInScreen = 0
                    else:
                        transparencyFadeInScreen -= transparencyTransitionSpeed * framerateMultiplier
                #activate finishedFadeInFlag
                if transparencyFadeInScreen == 0:
                    finishedFadeInFlag = bool(1)

        
        if getCurrentSeconds(startSceneTicks,pygame.time.get_ticks()) > 8 :
            if transparencyFadeInScreen < 255:
                failsafePrediction = transparencyFadeInScreen + (transparencyTransitionSpeed * framerateMultiplier)
                if failsafePrediction >= 255:
                    transparencyFadeInScreen = 255
                else:
                    transparencyFadeInScreen += transparencyTransitionSpeed * framerateMultiplier
            
            
        fadeInScreen.fill((0,0,0,transparencyFadeInScreen))

        
        if getCurrentSeconds(startSceneTicks,pygame.time.get_ticks()) > 11 :
            nextScene = 'mainMenu'  
            startSceneTicks = pygame.time.get_ticks()

        
        renderScreenStack.append(addToRenderStack(fadeInScreen,0,0,1))
        renderScreenStack.append(addToRenderStack(logoImg,renderScreenWidth/2 - getWidth(logoImg)/2 ,renderScreenHeight/2 - getHeight(logoImg)/2,0))
        renderScreenStack.append(addToRenderStack(logoText,renderScreenWidth/2 - getWidth(logoText)/2 ,renderScreenHeight/2 + getHeight(logoImg)/2 ,0))
        renderScreenStack.append(addToRenderStack(logoTextWebsite,renderScreenWidth/2 - getWidth(logoTextWebsite)/2 ,renderScreenHeight/2 + getHeight(logoImg)/2 + getHeight(logoText) ,0))

        #-------------------------------

    elif currentScene == 'mainMenu':

        #-------------------------------
        sceneName = 'Main Menu'
        nextScene = 'mainMenu'

        for event in pygame.event.get():
            #debug events
            #print (event)
            #Quitting the game
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pass
                if event.key == pygame.K_DOWN:
                    indexFinder = 0
                    for count, menuElement in enumerate(menuItems):
                        if menuElement['selected'] == bool(1):
                            menuElement ['selected'] = bool(0)
                            indexFinderFailsafe = count + 1
                            if indexFinderFailsafe > len(menuItems) -1:
                                indexFinder = 0
                            else:
                                indexFinder = count + 1
                    menuItems[indexFinder]['selected'] = bool(1)
                if event.key == pygame.K_UP:
                    indexFinder = 0
                    for count, menuElement in enumerate(menuItems):
                        if menuElement['selected'] == bool(1):
                            menuElement ['selected'] = bool(0)
                            indexFinderFailsafe = count - 1
                            if indexFinderFailsafe < 0:
                                indexFinder = len(menuItems) -1
                            else:
                                indexFinder = count - 1
                    menuItems[indexFinder]['selected'] = bool(1)
                if event.key == pygame.K_RETURN:
                    elementSelected = ''
                    indexFinder = 0
                    for count, menuElement in enumerate(menuItems):
                        if menuElement['selected'] == bool(1):
                            indexFinder = count
                    elementSelected = menuItems[indexFinder]['value']
                    # if elementSelected == something:
                    if elementSelected == 'exit':
                        pygame.quit()
                        quit()
                    elif elementSelected == 'newgame':
                        nextScene = 'newgame'  
                        startSceneTicks = pygame.time.get_ticks()
                    elif elementSelected == 'continue':
                        nextScene = 'continue'  
                        startSceneTicks = pygame.time.get_ticks()
                    elif elementSelected == 'settings':
                        nextScene = 'settings'  
                        startSceneTicks = pygame.time.get_ticks()
            if event.type == pygame.USEREVENT + 0:
                print ('BootEvent') 

        
        renderScreenStack =  []
        overlayScreenStack = []

        fpsCounter = m5x7_32.render('FPS: ' + str(round(clockFramerate.get_fps())), True, whiteColor)
        sceneNameWidget = m5x7_32.render('Scene: ' + str(sceneName), True, whiteColor)

        overlayScreenStack.append(addToRenderStack(sceneNameWidget,0,0,0))
        overlayScreenStack.append(addToRenderStack(fpsCounter,mainScreenWidth - getWidth(fpsCounter),0,0))



        
        spacing = 0
        for count, itemForRender in enumerate(menuItems):
            if count > 0:
                spacing = getHeight(placeHolder) * count
            if itemForRender['selected']:  
                menuPointer = '>'
            else:
                menuPointer = ' '  
            item = m5x7_32.render(str(menuPointer) + ' ' + str(itemForRender['label']), True, whiteColor)
            renderScreenStack.append(addToRenderStack(item,renderScreenWidth/2 - getWidth(item)/2 ,renderScreenHeight/2 - getHeight(item)/2 + spacing,0))
            

        #-------------------------------

    elif currentScene == 'settings':

        #-------------------------------
        sceneName = 'Setting Screen'
        nextScene = 'settings'

        for event in pygame.event.get():
            #debug events
            #print (event)
            #Quitting the game
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    nextScene = 'mainMenu'  
                    startSceneTicks = pygame.time.get_ticks()
                if event.key == pygame.K_DOWN:
                    indexFinder = 0
                    for count, menuElement in enumerate(settingsMenuItems):
                        if menuElement['selected'] == bool(1):
                            menuElement ['selected'] = bool(0)
                            indexFinderFailsafe = count + 1
                            if indexFinderFailsafe > len(settingsMenuItems) -1:
                                indexFinder = 0
                            else:
                                indexFinder = count + 1
                    settingsMenuItems[indexFinder]['selected'] = bool(1)
                if event.key == pygame.K_UP:
                    indexFinder = 0
                    for count, menuElement in enumerate(settingsMenuItems):
                        if menuElement['selected'] == bool(1):
                            menuElement ['selected'] = bool(0)
                            indexFinderFailsafe = count - 1
                            if indexFinderFailsafe < 0:
                                indexFinder = len(settingsMenuItems) -1
                            else:
                                indexFinder = count - 1
                    settingsMenuItems[indexFinder]['selected'] = bool(1)
                if event.key == pygame.K_RETURN:
                    elementSelected = ''
                    indexFinder = 0
                    for count, menuElement in enumerate(settingsMenuItems):
                        if menuElement['selected'] == bool(1):
                            indexFinder = count
                    elementSelected = settingsMenuItems[indexFinder]['value']
                    # if elementSelected == something:
                    if elementSelected == 'exit':
                        pygame.quit()
                        quit()
                    elif elementSelected == 'save':
                        framerateLimit = settingDummyFpsLimit
                        windowMode = settingDummyWindowMode
                        if windowMode == "resizable":
                            mainScreen = pygame.display.set_mode((mainScreenWidth,mainScreenHeight),pygame.RESIZABLE)
                        elif windowMode == "fullscreen":
                            mainScreen = pygame.display.set_mode((mainScreenWidth,mainScreenHeight),pygame.FULLSCREEN)
                        else:
                            mainScreen = pygame.display.set_mode((mainScreenWidth,mainScreenHeight))


                    elif elementSelected == 'fpsChange':
                        indexFinder = 0
                        for count, menuElement in enumerate(fpsChangeSubMenuItems):
                            if menuElement['selected'] == bool(1):
                                menuElement ['selected'] = bool(0)
                                indexFinderFailsafe = count + 1
                                if indexFinderFailsafe > len(fpsChangeSubMenuItems) -1:
                                    indexFinder = 0
                                else:
                                    indexFinder = count + 1
                        fpsChangeSubMenuItems[indexFinder]['selected'] = bool(1)
                        elementSelected = ''
                        indexFinder = 0
                        for count, menuElement in enumerate(fpsChangeSubMenuItems):
                            if menuElement['selected'] == bool(1):
                                indexFinder = count
                        elementSelected = fpsChangeSubMenuItems[indexFinder]
                        #---
                        indexFinder = 0
                        for count, menuElement in enumerate(settingsMenuItems):
                            if menuElement['value'] == 'fpsChange':
                                indexFinder = count
                        settingsMenuItems[indexFinder]['label'] = elementSelected['label']
                        settingDummyFpsLimit = elementSelected['value']
                    #------
                    elif elementSelected == 'windowMode':
                        indexFinder = 0
                        for count, menuElement in enumerate(windowModeSubMenuItems):
                            if menuElement['selected'] == bool(1):
                                menuElement ['selected'] = bool(0)
                                indexFinderFailsafe = count + 1
                                if indexFinderFailsafe > len(windowModeSubMenuItems) -1:
                                    indexFinder = 0
                                else:
                                    indexFinder = count + 1
                        windowModeSubMenuItems[indexFinder]['selected'] = bool(1)
                        elementSelected = ''
                        indexFinder = 0
                        for count, menuElement in enumerate(windowModeSubMenuItems):
                            if menuElement['selected'] == bool(1):
                                indexFinder = count
                        elementSelected = windowModeSubMenuItems[indexFinder]
                        #---
                        indexFinder = 0
                        for count, menuElement in enumerate(settingsMenuItems):
                            if menuElement['value'] == 'windowMode':
                                indexFinder = count
                        settingsMenuItems[indexFinder]['label'] = elementSelected['label']
                        settingDummyWindowMode = elementSelected['value']
                    


                    elif elementSelected == 'mainMenu':
                        nextScene = 'mainMenu'  
                        startSceneTicks = pygame.time.get_ticks()
                    
            if event.type == pygame.USEREVENT + 0:
                print ('BootEvent') 

        
        renderScreenStack =  []
        overlayScreenStack = []

        fpsCounter = m5x7_32.render('FPS: ' + str(round(clockFramerate.get_fps())), True, whiteColor)
        sceneNameWidget = m5x7_32.render('Scene: ' + str(sceneName), True, whiteColor)

        overlayScreenStack.append(addToRenderStack(sceneNameWidget,0,0,0))
        overlayScreenStack.append(addToRenderStack(fpsCounter,mainScreenWidth - getWidth(fpsCounter),0,0))


        
        spacing = 0
        for count, itemForRender in enumerate(settingsMenuItems):
            if count > 0:
                spacing = getHeight(placeHolder) * count
            if itemForRender['selected']:  
                menuPointer = '>'
            else:
                menuPointer = ' '  
            item = m5x7_32.render(str(menuPointer) + ' ' + str(itemForRender['label']), True, whiteColor)
            renderScreenStack.append(addToRenderStack(item,renderScreenWidth/2 - getWidth(item)/2 ,renderScreenHeight/2 - getHeight(item)/2 + spacing,0))
            


    
        #-------------------------------

    elif currentScene == 'newgame':

        #-------------------------------
        sceneName = 'New game scene'
        nextScene = 'newgame'

        for event in pygame.event.get():
            #debug events
            #print (event)
            #Quitting the game
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pass
            if event.type == pygame.USEREVENT + 0:
                print ('BootEvent') 

        
        renderScreenStack =  []
        overlayScreenStack = []

        fpsCounter = m5x7_32.render('FPS: ' + str(round(clockFramerate.get_fps())), True, whiteColor)
        sceneNameWidget = m5x7_32.render('Scene: ' + str(sceneName), True, whiteColor)

        overlayScreenStack.append(addToRenderStack(sceneNameWidget,0,0,0))
        overlayScreenStack.append(addToRenderStack(fpsCounter,mainScreenWidth - getWidth(fpsCounter),0,0))


        renderScreenStack.append(addToRenderStack(helloworldText,renderScreenWidth/2 - getWidth(helloworldText)/2 ,renderScreenHeight/2 - getHeight(helloworldText)/2 ,0))

        
        #-------------------------------

    elif currentScene == 'continue':

        #-------------------------------
        sceneName = 'Continue game scene'
        nextScene = 'continue'

        for event in pygame.event.get():
            #debug events
            #print (event)
            #Quitting the game
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pass
            if event.type == pygame.USEREVENT + 0:
                print ('BootEvent') 

        
        renderScreenStack =  []
        overlayScreenStack = []

        fpsCounter = m5x7_32.render('FPS: ' + str(round(clockFramerate.get_fps())), True, whiteColor)
        sceneNameWidget = m5x7_32.render('Scene: ' + str(sceneName), True, whiteColor)

        overlayScreenStack.append(addToRenderStack(sceneNameWidget,0,0,0))
        overlayScreenStack.append(addToRenderStack(fpsCounter,mainScreenWidth - getWidth(fpsCounter),0,0))


        renderScreenStack.append(addToRenderStack(helloworldText,renderScreenWidth/2 - getWidth(helloworldText)/2 ,renderScreenHeight/2 - getHeight(helloworldText)/2 ,0))

        
        #-------------------------------

    currentScene = nextScene

    runRender(renderScreenStack,overlayScreenStack)



