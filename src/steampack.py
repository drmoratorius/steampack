from machine import Pin, ADC
import machine
import morutils
from morutils import *

MCP_IODIRA = 0x00  # Controls the direction of the data I/O for port A.
MCP_IODIRB = 0x01  # Controls the direction of the data I/O for port B.
MCP_IPOLA = 0x02  # Configures the polarity on the corresponding GPIO-port bits for port A.
MCP_IPOLB = 0x03  # Configures the polarity on the corresponding GPIO-port bits for port B.
MCP_GPINTENA = 0x04  # Controls the interrupt-on-change for each pin of port A.
MCP_GPINTENB = 0x05  # Controls the interrupt-on-change for each pin of port B.
MCP_DEFVALA = 0x06  # Controls the default comparison value for interrupt-on-change for port A.
MCP_DEFVALB = 0x07  # Controls the default comparison value for interrupt-on-change for port B.
MCP_INTCONA = 0x08  # Controls how the associated pin value is compared for the interrupt-on-change for port A.
MCP_INTCONB = 0x09  # Controls how the associated pin value is compared for the interrupt-on-change for port B.
MCP_IOCON = 0x0A  # Controls the device.
MCP_GPPUA = 0x0C  # Controls the pull-up resistors for the port A pins.
MCP_GPPUB = 0x0D  # Controls the pull-up resistors for the port B pins.
MCP_INTFA = 0x0E  # Reflects the interrupt condition on the port A pins.
MCP_INTFB = 0x0F  # Reflects the interrupt condition on the port B pins.
MCP_INTCAPA = 0x10  # Captures the port A value at the time the interrupt occurred.
MCP_INTCAPB = 0x11  # Captures the port B value at the time the interrupt occurred.
MCP_GPIOA = 0x12  # Reflects the value on the port A.
MCP_GPIOB = 0x13  # Reflects the value on the port B.
MCP_OLATA = 0x14  # Provides access to the port A output latches.
MCP_OLATB = 0x15  # Provides access to the port B output latches.

relais1 = None
relais2 = None
poti1 = None
poti2 = None
globalCallback = None
prevBankAPins = []
mcpIc2Addr = None
mcp2Addr = 0x21
inputNames = []
curValues = []
potiThreshold = 1
poti1PrevValue = 0
poti1Value = 0
poti2PrevValue = 0
poti2Value = 0
poti1Callback = None
poti2Callback = None
i2c = None

def sp_switchRelais(no, status):
    # Low Trigger relais, i.e. False = on
    if no == 1:
        if status == False:
            relais1.value(1)
        else:
            relais1.value(0)
    elif no == 2:
        if status == False:
            relais2.value(1)
        else:
            relais2.value(0)

def SP_setupPins(relais1Pin, relais2Pin, poti1Pin, poti2Pin):
    global relais1, relais2, poti1, poti2
    relais1 = machine.Pin(relais1Pin, machine.Pin.OUT)
    relais2 = machine.Pin(relais2Pin, machine.Pin.OUT)
    poti1 = ADC(Pin(poti1Pin))
    poti2 = ADC(Pin(poti2Pin))
    return relais1, relais2, poti1, poti2

def SP_mcpCallback(pin):
    global prevBankAPins
    changes = []
    curValues = UTIL_convertBinaryValue(i2c.readfrom_mem(mcpIc2Addr, MCP_GPIOA, 1))
    changedOffsets = UTIL_compare_bool_arrays(prevBankAPins, curValues)
    if len(changedOffsets):
        for offset in changedOffsets:
            #print('INPUT ' + inputNames[offset] + ' changed to ' + str(curValues[offset]))
            changes.append([inputNames[offset], curValues[offset]])
        prevBankAPins = curValues
    if len(changes):
        globalCallback(changes)

def SP_mcpSetup(mcpAddr, sclPin, sdaPin, mcpIrqPinNo, irqCallback):
    global i2c, mcpIc2Addr, prevBankAPins
    mcpIc2Addr = mcpAddr

    # Find MCP23017 on i2c
    i2c = machine.I2C(0, scl=machine.Pin(sclPin), sda=machine.Pin(sdaPin), )
    i2cdevices = i2c.scan()
    mcpFound = False
    mcp2Found = False
    for device in i2cdevices:
        if device == mcpIc2Addr:
            print('[x] MCP23017 found on ' + str(hex(mcpIc2Addr)) + ' (' + str(mcpIc2Addr) + ')')
            mcpFound = True
        if device == mcp2Addr:
            print('[x] MCP23017 #2 found on ' + str(hex(mcp2Addr)) + ' (' + str(mcp2Addr) + ')')
            mcp2Found = True
    curValues = []

    if mcpFound == True:
        print('[.] Configuring MCP23017 for program...')
        i2c.writeto_mem(mcpAddr, MCP_IODIRA, b'\xFF')  # Bank A -> all input
        print('[.] Set Bank A to input')
        i2c.writeto_mem(mcpAddr, MCP_GPPUA, b'\xFF')
        print('[.] Set Bank A all pull-up resistors on')
        i2c.writeto_mem(mcpAddr, MCP_GPINTENA, b'\xFF')
        print('[.] Set Bank A IRQ mode')
        i2c.writeto_mem(mcpAddr, MCP_IODIRB, b'\x00')  # Bank B -> all output
        print('[.] Set Bank B to output')
        i2c.writeto_mem(mcpAddr, MCP_GPIOB, b'\x00')
        print('[.] Set Bank B all outputs to 0')
        print('[*] Reading current value of bank A')
        curValues = UTIL_convertBinaryValue(i2c.readfrom_mem(mcpAddr, MCP_GPIOA, 1))
        prevBankAPins = curValues
        mcpIrqPin = machine.Pin(mcpIrqPinNo, machine.Pin.IN)
        mcpIrqPin.irq(trigger=machine.Pin.IRQ_FALLING | machine.Pin.IRQ_RISING, handler=SP_mcpCallback)
        
        print('[.] Configuring MCP23017 #2 for program... (must be set to IO mode 0: 0,0,0')
        i2c.writeto_mem(mcp2Addr, MCP_IODIRA, b'\x00')  # Bank A -> all output
        i2c.writeto_mem(mcp2Addr, MCP_GPIOA, UTIL_bools_to_byte(1, 1, 1, 1, 1, 1, 1, 1)) # all off

    return i2c, mcpFound, curValues, mcp2Found

def SP_setup(currentState, relais1Pin, relais2Pin, poti1Pin, poti2Pin, mcpAddr, sclPin, sdaPin, mcpIrqPinNo, inputCallback, inputNameList):
    global globalCallback, inputNames
    globalCallback = inputCallback
    inputNames = inputNameList
    SP_setupPins(relais1Pin, relais2Pin, poti1Pin, poti2Pin)
    i2c, mcpFound, curValues, mcp2Found = SP_mcpSetup(mcpAddr, sclPin, sdaPin, mcpIrqPinNo, globalCallback)
    currentState['poti1'] = SP_getCurrentPotiValue(1)
    currentState['poti2'] = SP_getCurrentPotiValue(2)
    return i2c, mcpFound, curValues, currentState, mcp2Found

def SP_writeOutputs(currentState, i2c, b1, b2, b3, b4, b5, b6, b7, b8):
    #global currentState
    #print(b1, b2, b3, b4, b5, b6, b7, b8)
    global mcpIc2Addr
    result = UTIL_bools_to_byte(b1, b2, b3, b4, b5, b6, b7, b8)
    #print('[.] Writing outputs to...', result)
    #print(result)
    i2c.writeto_mem(mcpIc2Addr, MCP_GPIOB, result)
    currentState['outNC3'] = b8
    currentState['outNC2'] = b7
    currentState['outNC1'] = b6
    currentState['ledS3'] = b5
    currentState['ledS2'] = b4
    currentState['ledS1'] = b3
    currentState['ledB2'] = b2
    currentState['ledB1'] = b1
    return currentState

def SP_updateOutputs(currentState):
    return SP_writeOutputs(currentState, i2c, currentState['ledB1'], currentState['ledB2'], currentState['ledS1'], currentState['ledS2'], currentState['ledS3'], currentState['outNC1'], currentState['outNC2'], currentState['outNC3'])    

def SP_switchLedS1(currentState, newValue):
    #global currentState
    currentState['ledS1'] = newValue
    return SP_updateOutputs(currentState)

def SP_switchLedS2(currentState, newValue):
    #global currentState
    currentState['ledS2'] = newValue
    return SP_updateOutputs(currentState)
    
def SP_switchLedS3(currentState, newValue):
    #global currentState
    currentState['ledS3'] = newValue
    return SP_updateOutputs(currentState)

def SP_switchLedB1(currentState, newValue):
    #global currentState
    currentState['ledB1'] = newValue
    return SP_updateOutputs(currentState)

def SP_switchLedB2(currentState, newValue):
    #global currentState
    currentState['ledB2'] = newValue
    return SP_updateOutputs(currentState)

def SP_getCurrentPotiValue(no):
    global poti1PrevValue, poti2PrevValue, poti1CurValue, poti2CurValue
    retVal = None
    if no == 1:
        poti1CurValue = 100 - round((poti1.read_u16() / 65535) * 100)
        if abs(poti1CurValue - poti1PrevValue) > potiThreshold:
            retVal = poti1CurValue
            poti1PrevValue = poti1CurValue
            globalCallback([['poti1', poti1CurValue]])
        else:
            retVal = poti1PrevValue
    else:
        poti2CurValue = 100 - round((poti2.read_u16() / 65535) * 100)
        if abs(poti2CurValue - poti2PrevValue) > potiThreshold:
            retVal = poti2CurValue
            poti2PrevValue = poti2CurValue
            globalCallback([['poti2', poti2CurValue]])
        else:
            retVal = poti1PrevValue
    return retVal


# Will play sound 1 = 00001.mp3 to 255 = 00255.mp3 from SD card
def SP_playSound(no):
    if no < 0 or no > 255:
        print('[E] ERROR - only sounds from 0 (stop), 1-255 are supported!')
    else:
        if no != 0:
            print('[~] Playing sound #', no)
        binary_value = bin(no)[2:]
        binary_value = '0' * (8 - len(binary_value)) + binary_value
        b = [1 if bit == '0' else 0 for bit in binary_value]
        i2c.writeto_mem(mcp2Addr, MCP_GPIOA, UTIL_bools_to_byte(b[0], b[1], b[2], b[3], b[4], b[5], b[6], b[7]))
    
def SP_stopPlayingSound():
    print('[~] STOP playing sound')
    SP_playSound(0)
    