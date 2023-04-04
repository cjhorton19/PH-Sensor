import sys
sys.path.append('../')
import time
from CQRobot import ADS1115

ADS1115_REG_CONFIG_PGA_6_144V = 0x00  # 6.144V range = Gain 2/3
ads1115 = ADS1115()
ads1115.setAddr_ADS1115(0x48)
ads1115.setGain(ADS1115_REG_CONFIG_PGA_6_144V)

VREF = 5.0
analogBuffer = [0] * 30
analogBufferTemp = [0] * 30
analogBufferIndex = 0
copyIndex = 0
averageVoltage = 0
tdsValue = 0
temperature = 25

def getMedianNum(arr):
    sortedArr = sorted(arr)
    if len(arr) % 2 == 0:
        medianNum = (sortedArr[int(len(arr) / 2) - 1] + sortedArr[int(len(arr) / 2)]) / 2
    else:
        medianNum = sortedArr[int(len(arr) / 2)]
    return medianNum

while True:
    if time.time() - analogSampleTimepoint > 0.04:
        analogSampleTimepoint = time.time()
        analogBuffer[analogBufferIndex] = ads1115.readVoltage(0)['r']
        analogBufferIndex += 1
        if analogBufferIndex == 30:
            analogBufferIndex = 0

    if time.time() - printTimepoint > 0.8:
        printTimepoint = time.time()
        for copyIndex in range(30):
            analogBufferTemp[copyIndex] = ads1115.readVoltage(0)['r']
        medianVoltage = getMedianNum(analogBufferTemp)
        pHValue = 7 - (medianVoltage - 2.5) / 0.18
        print("pH: %.2f" % pHValue)
