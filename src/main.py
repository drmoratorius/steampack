from morutils import *
from steampack import *
import uasyncio as asyncio
import time

##############
### CONFIG ###
##############
# Config is read from config.json file so that no code needs to be changed for changing the configuration!
config = UTIL_getJSON('config.json')

# Initial values/always holding the current values at any time
currentState = config['defaultValues']
lastState = currentState

## Variables for runtime
steamOn = False
steamCurrentlyOn = False
lastSteamOn = time.time() - (60 * 60 * 24)
startTs = time.time()
mcp2Found = False
soundActive = False

##########################
### CALLBACK FUNCTIONS ###
##########################

def playSound(no):
    if mcp2Found and soundActive:
        SP_playSound(no)
        time.sleep(0.05)
        SP_stopPlayingSound()
    
# MAIN PROGRAM
# Handles the current state, i.e. updates everything
def handle_current_state(currentStateNew):
    global currentState, steamOn, steamCurrentlyOn, lastSteamOn, soundActive
    currentState = currentStateNew
    if currentState['REED'] == False or currentState['S1'] == False:
        print('[X] Case open or main switch turned off')
        # Case open, turn all off OR main switch turned off
        sp_switchRelais(1, False)
        sp_switchRelais(2, False)
        currentState = SP_switchLedS1(currentState, False)
        currentState = SP_switchLedS2(currentState, False)
        currentState = SP_switchLedS3(currentState, False)
        currentState = SP_switchLedB1(currentState, False)
        currentState = SP_switchLedB2(currentState, False)
    else:
        if currentState['S1'] == True and currentState['REED'] == True:
            print('[X] Case closed and main switch turned on')
            
            if currentState['S2'] == True:
                # TODO: Zahnradenkoppelung
                print('[X] S2 Zahnradenkoppelung ON')
                currentState = SP_switchLedS1(currentState, False)
                soundActive = False
            else:
                # TODO: Zahnradenkoppelung
                print('[X] S2 Zahnradenkoppelung OFF')
                currentState = SP_switchLedS1(currentState, True)
                soundActive = True
                
            if currentState['S3'] == True:
                # Feuerdämpfer (ON = fire off)
                print('[x] Turning off fire')
                sp_switchRelais(1, False)
                currentState = SP_switchLedS2(currentState, False)
            else:
                # Feuerdämpfer (OFF = fire on)
                print('[x] Turning on fire')
                sp_switchRelais(1, True)
                currentState = SP_switchLedS2(currentState, True)
                
            # TODO FOGGER: only exactly when fogging turn on B1 and B2? FLicker?
            # TODO Read dampfdruck poti and the more far right the more often it should happen
            if currentState['S4'] == True:
                # Dampfventilöffnung (ON = Fogger ON)
                # TODO
                print('[x] Turning on fogger program')
                currentState = SP_switchLedS3(currentState, True)
                currentState = SP_switchLedB1(currentState, True)
                currentState = SP_switchLedB2(currentState, True)
                time.sleep(1)
                steamOn = True
                steamCurrentlyOn = False
                lastSteamOn = startTs
            else:
                # Dampfventilöffnung (OFF = Fogger OFF)
                # TODO
                print('[x] Turning off fogger program')
                currentState = SP_switchLedS3(currentState, False)
                currentState = SP_switchLedB1(currentState, False)
                currentState = SP_switchLedB2(currentState, False)
                steamOn = False
                
    lastState = currentState
    

# Always receives an array of values: [['SP1', True], ['SP2', False]]...
def input_callback(changes):
    global currentState, lastSteamOn, steamOn, soundActive
    print('---> INPUT CALLBACK')
    print(changes)
    for change in changes:
        currentState[change[0]] = change[1]
        
        if change[0] == 'poti2':
            lastSteamOn = startTs - (60 * 60 * 24) # reset so that it takes immediate effect
            steamInterval, steamDuration = getSteamDurations()
            print('POTI2 changed steamInterval', steamInterval, 'duration', steamDuration)

        if change[0] == 'S1':
            if change[1] == False:
                steamOn = False
                playSound(12)
            else:
                steamOn = currentState['S4']
                playSound(11)
                
        if change[0] == 'S2':
            soundActive = not change[1]
            
        if change[0] == 'S3':
            if change[1] == True:
                playSound(13)
            else:
                playSound(14)
            
        if change[0] == 'S4':
            lastSteamOn = startTs - (60 * 60 * 24)
            if change[1] == True:
                playSound(15)
            else:
                playSound(16)

    print(currentState)
    
    handle_current_state(currentState)
 
# TODO: this should be in config.json instead!
def getSteamDurations():
    curPercentage = currentState['poti2'];
    steamInterval = 300
    steamDuration = 5
    
    if curPercentage < 10:
        steamInterval = 240
        steamDuration = 5
    elif curPercentage < 25:
        steamInterval = 120
        steamDuration = 7
    elif curPercentage < 50:
        steamInterval = 60
        steamDuration = 3
    elif curPercentage < 75:
        steamInterval = 30
        steamDuration = 2
    elif curPercentage <= 100:
        steamInterval = 10
        steamDuration = 3
        
    #print('steamInterval', steamInterval, 'duration', steamDuration)
    return steamInterval, steamDuration

###################
### ASYNC SETUP ###
###################
async def function1():
    while True:
        SP_getCurrentPotiValue(1)
        SP_getCurrentPotiValue(2)
        await asyncio.sleep(0.25)
        
async def function2():
    global steamCurrentlyOn, lastSteamOn
    while True:
        steamInterval, steamDuration = getSteamDurations()
        #print("Function 2 is running")
        curTs = time.time()
        #print('#STEAM async function')
        if steamOn:
            #print('#STEAM switch is currently on')
            if not steamCurrentlyOn:
                #print('#STEAM switch is currently on, but fogger not')
                if curTs - lastSteamOn > steamInterval:
                    #print('#STEAM switch is currently on, but fogger not, longer than 10 seconds ago, turning on')
                    lastSteamOn = curTs
                    sp_switchRelais(2, True)
                    print('!STEAM! ON')
                    steamCurrentlyOn = True
                    playSound(4)
            else:
                if curTs - lastSteamOn > steamDuration:
                    #print('#STEAM switch is currently on, and fogger also, but longer than 2 seconds, turning off')
                    lastSteamOn = curTs
                    sp_switchRelais(2, False)
                    print('!STEAM! OFF')
                    steamCurrentlyOn = False
        else:
            # Not on, so ensure it's off - this is required for when the user switches during run
            #print('#STEAM switch is currently OFF, turning off fogger')
            steamCurrentlyOn = False
            lastSteamOn = startTs
            sp_switchRelais(2, False)
            
        await asyncio.sleep(1)

# Run both functions concurrently
async def main():
    task1 = asyncio.create_task(function1())
    task2 = asyncio.create_task(function2())
    
    # Wait for both tasks to run forever
    await asyncio.gather(task1, task2)

#############
### SETUP ###
#############
i2c, mcpFound, prevBankAPins, currentState, mcp2Found = SP_setup(currentState, config['hardware']['pins']['relais1'], config['hardware']['pins']['relais2'], config['hardware']['pins']['poti1'], config['hardware']['pins']['poti2'], config['hardware']['mcp23017addr'], config['hardware']['pins']['i2c_scl'], config['hardware']['pins']['i2c_sda'], config['hardware']['pins']['mcpIrq'], input_callback, config['inputNames'])
currentState['REED'] = prevBankAPins[3]
currentState['S4'] = prevBankAPins[6]
currentState['S3'] = prevBankAPins[5]
currentState['S2'] = prevBankAPins[4]
currentState['S1'] = prevBankAPins[7]
currentState = SP_writeOutputs(currentState, i2c, currentState['ledB1'], currentState['ledB2'], currentState['ledS1'], currentState['ledS2'], currentState['ledS3'], currentState['outNC1'], currentState['outNC2'], currentState['outNC3'])
print (prevBankAPins)
print('INITIAL VALUES AFTER SETUP')
print(currentState)
print('REED switch is ', currentState['REED'])
print('Main switch S1 is ', currentState['S1'])
print('Switch S2 Zahnrad... is ', currentState['S2'])
print('Switch S3 Feuerd... is ', currentState['S3'])
print('Switch S4 is ', currentState['S4'])

# Initial setup
handle_current_state(currentState)
SP_stopPlayingSound()
time.sleep(0.1)

playSound(11)


####################
### MAIN PROGRAM ###
####################
if mcpFound == False:
    print('EXITING - MCP23017 was not found!')
else:
    # Start the event loop
    asyncio.run(main())


