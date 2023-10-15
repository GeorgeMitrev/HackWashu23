import time

import board

import busio

import adafruit_mcp3xxx.mcp3008 as MCP

import digitalio

import math

import pygame.mixer
import simpleaudio as sa

from adafruit_mcp3xxx.analog_in import AnalogIn

from pydub import AudioSegment

#define audio functions
def start_audio(file_path):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    
def stop_audio():
    pygame.mixer.music.stop()

#start_audio(low[0])

# Create an SPI connection on the specified pins.

spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
#spi = busio.SPI(clock = 18,MOSI = 24, MISO=23)

#cs = digitalio.DigitalInOut(22)
cs = digitalio.DigitalInOut(board.D5)  # Specify the chip select pin (can be any GPIO pin)


#mcp = Adafruit_MCP3008.MCP3008(spi = SPI.SpiDev(0,0))

# Create the MCP3008 instance.

mcp = MCP.MCP3008(spi, cs)

pygame.mixer.init() 

print('Reading MCP3008 values, press Ctrl-C to quit...')

# Print nice channel column headers.

#print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*range(8))

#print('--------------------------------------')

# Main program loop.
movAvgLong = 0
movAvgShort = 0
active = 0
first = True


lookState = 0
stateChangeVal = 20 #Num of things to change state
deltaForLook = 30 #Threshold

#Songs
low = ["Hallelujah 58.mp3","Hello 80.mp3","I'm Yours 77.mp3","Imagine 77.mp3","Mirrors 77.mp3","Miss Summer 69.mp3","Someone Like You 68.mp3","Somewhere Over the Rainbow 86.mp3"]

middle = ["Demons 90.mp3","Higher Love 104.mp3","I Like You 102.mp3","Love You Like a Love Song 117.mp3","New Rules 116.mp3","Shape of You 96.mp3","SOS 101.mp3","We Don't Talk Anymore 99.mp3"]

high = ["All Of The Lights 145.mp3","Don't Stop Me Now 154.mp3","Hot N Cold 133.mp3","Shake It Off 160.mp3","Still Into You 137.mp3","The One That Got Away 137.mp3","Wake Me Up 122.mp3","Womanizer 141.mp3"]


heartAvg = 0
oldHeartAvg = 0
heartState = 0
heartFirst = True
songMode = 0
lastSongMode = 0
index = 0

while True:
    # Read all the ADC channel values in a list.
    values = [0] * 8


    #Get values
    for i in range(3):
        # Create an analog input for the specified channel.
        channel = AnalogIn(mcp, getattr(MCP, 'P{}'.format(i)))
        # Read the ADC value for the channel.
        values[i] = math.floor(channel.value/64)
    
    #print('| {0:>4} | {1:>4} |'.format(*values),movAvgLong)
    
    if heartFirst:
        heartAvg = values[0]
        heartFirst = False
    else:
        heartAvg = (heartAvg*30 + values[0])/31

    if (songMode < 2) and (heartAvg - oldHeartAvg > 3):
        songMode+=1
        oldHeartAvg = heartAvg
    elif (songMode > 0) and (oldHeartAvg - heartAvg) > 3:
        songMode -=1
        oldHeartAvg = heartAvg
    elif heartAvg - oldHeartAvg > 30:
        oldHeartAvg = heartAvg
    elif (oldHeartAvg - heartAvg) > 30:
        oldHeartAvg= heartAvg

    if lastSongMode!=songMode:
        stop_audio()
        index = 0
        if songMode == 0:
            start_audio(low[index])
        elif songMode == 1:
            start_audio(middle[index])
        else:
            start_audio(high[index])
        lastSongMode=songMode
    

    # Code for determining look direction
    if(values[1] > (.5*movAvgLong+20)):
        print('| {0:>4} | {1:>4} |'.format(*values),movAvgLong," avg:state ",lookState)
        movAvgLong = (movAvgLong*30 + values[1])/31
        if first:
            movAvgLong = (values[i]+values[i]-1)/2
            first = False
        if values[1] - movAvgLong > 15:
            lookState+=1
            if lookState > 5:
                print("Looking left")
                if index == 0:
                    index = 7
                else:
                    index-=1
                stop_audio()
                if songMode == 0:
                    start_audio(low[index])
                elif songMode == 1:
                    start_audio(middle[index])
                else:
                    start_audio(high[index])
                lookState = 0
        elif movAvgLong - values[1] > 15:
            lookState-=1
            if lookState < -5:
                print("Looking right")
                lookState = 0
                if index == 7:
                    index = 0
                else:
                    index+=1
                stop_audio()
                if songMode == 0:
                    start_audio(low[index])
                elif songMode == 1:
                    start_audio(middle[index])
                else:
                    start_audio(high[index])
    # Pause
    time.sleep(0.15)
