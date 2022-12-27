#!/usr/bin/env python
#
# Command Line usage:
#   xmas.py <input sequence> <audio file>
x = 0
import RPi.GPIO as GPIO, time
import sys
import time
import pygame
import random

import subprocess
import random
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.ili9341 as ili9341
import adafruit_rgb_display.st7789 as st7789  # pylint: disable=unused-import
import adafruit_rgb_display.hx8357 as hx8357  # pylint: disable=unused-import
import adafruit_rgb_display.st7735 as st7735  # pylint: disable=unused-import
import adafruit_rgb_display.ssd1351 as ssd1351  # pylint: disable=unused-import
import adafruit_rgb_display.ssd1331 as ssd1331  # pylint: disable=unused-import

GPIO.setmode(GPIO.BCM)
# First define some constants to allow easy resizing of shapes.

# Configuration for CS and DC pins (these are PiTFT defaults):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = digitalio.DigitalInOut(board.D24)

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 24000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Create the display:
disp = st7735.ST7735R(spi, rotation=90,                           # 1.8" ST7735R
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
)

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.

if disp.rotation % 180 == 90:
	height = disp.width  # we swap height/width to rotate it to landscape!
	width = disp.height
else:
	width = disp.width  # we swap height/width to rotate it to landscape!
	height = disp.height
	
image = Image.new("RGB", (width, height))
draw = ImageDraw.Draw(image)

ipfontsize = 15#ipfont size
ipfont = ImageFont.truetype("/home/pi/christmas_tree_lights/fonts/chr5.ttf", ipfontsize)

FONTSIZE = 23
font = ImageFont.truetype("/home/pi/christmas_tree_lights/fonts/chr13.ttf", FONTSIZE)
# Get drawing object to draw on image.

treefont = ImageFont.truetype("/home/pi/christmas_tree_lights/fonts/trees.ttf", 130)
# Draw a green filled box as the background
flkf = ImageFont.truetype("/home/pi/christmas_tree_lights/fonts/flakes.ttf", 10)

(trfw,trfh) = treefont.getsize('C')
draw.text((width//2-trfw//2,height-ipfontsize-trfh),'C',font=treefont, fill=(255,255,255))
draw = ImageDraw.Draw(image)
for i in range(15):
    letter = chr(random.randint(48,123))
    draw.text((random.randrange(5,width//2,15),random.randrange(5,height-ipfontsize-7,15)),letter,font=flkf, fill=(150,150,150))
    draw.text((random.randrange(width//2,width-10,15),random.randrange(5,height-ipfontsize-7,15)),letter,font=flkf, fill=(150,150,150))


cmd = "hostname -I "
IP = subprocess.check_output(cmd, shell = True ).decode("utf-8")
draw.text((38,height-ipfontsize), 'IP: '+str(IP) ,font=ipfont, fill=(255,255,255))
disp.image(image)

time.sleep(2.5)

# This is the array that stores the SPI sequence
# blinks is used to handle the Star Blinking Effect

# Defines the mapping of logical mapping to physical mapping
# 1 - 5 are lights from top to bottom on tree
# 6 = RED
# 7 = GREEN
# 8 = BLUE
#time.sleep(10.0)
logical_map = [0 for i in range(9)]

# Defines the mapping of the GPIO1-8 to the pin on the Pi
pin_map = [0, 4,17,27,22,5,6,13,12]

# Setup the board
for i in pin_map[1:]:
	GPIO.setup(i, GPIO.OUT)
time.sleep(2.0);

# Calculate gamma correction
gamma = bytearray(256)
for i in range(256):
	gamma[i] = int(pow(float(i) / 255.0, 2.5) * 255.0 + 0.5)


# Open the setup config file and parse it to determine
# how GPIO1-8 are mapped to logical 1-8
with open("/home/pi/christmas_tree_lights/setup1.txt", 'r') as f:
	data = f.readlines()
	for i in range(8):
		logical_map[i + 1] = int(data[i])


# Current light states
lights = [True for i in range(8)]
buttonplus = 21
GPIO.setup(buttonplus,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
buttonminus = 20
GPIO.setup(buttonminus,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

#list of sons
songs = [ ['/home/pi/christmas_tree_lights/seq_txt/1.txt','/home/pi/christmas_tree_lights/songs_mp3/1.mp3',['Setting',' up...']],
#         ['/home/pi/christmas_tree_lights/Desktop/pbdb.txt','/home/pi/christmas_tree_lights/Desktop/pbdb.mp3',['Podme','bratia','do','Betlema']],
#         ['/home/pi/christmas_tree_lights/Desktop/KazdyDen.txt','/home/pi/christmas_tree_lights/Desktop/KazdyDen.mp3',['Kazdy','den budu', 'vraj','Vianoce']],
#         ['/home/pi/christmas_tree_lights/Desktop/ChristmasLights.txt','/home/pi/christmas_tree_lights/Desktop/ChristmasLights.mp3',['Christmas','Lights']],#
#         ['/home/pi/christmas_tree_lights/Desktop/ocayf.txt','/home/pi/christmas_tree_lights/Desktop/ocayf.mp3',['Oh come','all ye','faithful']],
#         ['/home/pi/christmas_tree_lights/Desktop/jttw.txt','/home/pi/christmas_tree_lights/Desktop/jttw.mp3',['Joy to', 'the','world']],
#         ['/home/pi/christmas_tree_lights/Desktop/ZimaNaSaniach.txt','/home/pi/christmas_tree_lights/Desktop/ZimaNaSaniach.mp3',['Zima na','saniach']],
#         ['/home/pi/christmas_tree_lights/Desktop/nz.txt','/home/pi/christmas_tree_lights/Desktop/nz.mp3',['Noc','zazrakov']],#
#         ['/home/pi/christmas_tree_lights/Desktop/scictt.txt','/home/pi/christmas_tree_lights/Desktop/scictt.mp3',['Santa','Claus is','coming','to town']],
#         ['/home/pi/christmas_tree_lights/Desktop/carol.txt','/home/pi/christmas_tree_lights/Desktop/carol.mp3',['Carol','orchestra']],#
#         ['/home/pi/christmas_tree_lights/Desktop/hjch.txt','/home/pi/christmas_tree_lights/Desktop/hjch.mp3',['Holy','jolly','Christmas']],
#         ['/home/pi/christmas_tree_lights/Desktop/lal.txt','/home/pi/christmas_tree_lights/Desktop/lal.mp3',['idk']],
#         ['/home/pi/christmas_tree_lights/Desktop/madr.txt','/home/pi/christmas_tree_lights/Desktop/madr.mp3',['Mad','russian','Christmas']],#
#         ['/home/pi/christmas_tree_lights/Desktop/jbr.txt','/home/pi/christmas_tree_lights/Desktop/jbr.mp3',['Jingle','Bell','rock']],
#         ['/home/pi/christmas_tree_lights/Desktop/lig.txt','/home/pi/christmas_tree_lights/Desktop/lig.mp3',['Let it','go']],
#         ['/home/pi/christmas_tree_lights/Desktop/def.txt', '/home/pi/christmas_tree_lights/Desktop/def.mp3',['Light','pattern','','no music']]
]

currsong = 0


while True:
    # Display image.
	currsong += 1
	draw.rectangle((0,0,width,height), fill=(0,0,0))
	(trfw,trfh) = treefont.getsize('C')
	draw.text((width//2-trfw//2,height-ipfontsize-trfh),'C',font=treefont, fill=(100,100,100))
	cmd = "hostname -I "
	IP = subprocess.check_output(cmd, shell = True ).decode("utf-8")
	draw.text((38,height-ipfontsize), 'IP: '+str(IP) ,font=ipfont, fill=(255,255,255))
	for i in range(30):
		letter = chr(random.randint(48,123))
		col = random.randint(100,210)
		draw.text((random.randrange(5,width-10,10),random.randrange(5,height-ipfontsize-10,10)),letter,font=flkf, fill=(col,col,col))

	if currsong > len(songs):
		currsong = 2
	if currsong < 0:
		currsong = len(songs)
	print(currsong)
	with open(songs[currsong-1][0], 'r') as f:
		seq_data = f.readlines()
		for i in range(len(seq_data)):
			seq_data[i] = seq_data[i].rstrip()
    # Load and play the music
	pygame.mixer.init()
	pygame.mixer.music.load(songs[currsong-1][1])
	pygame.mixer.music.play()
	x = -9
	draw = ImageDraw.Draw(image)
	    # Start sequencing
	start_time = int(round(time.time() * 1000))
	step = 1  # ignore the header line
	font = ImageFont.truetype("/home/pi/christmas_tree_lights/fonts/chr13.ttf", FONTSIZE)
	if len(songs[currsong-1][2]) > 4:
			FONTSIZE = 20
			x = -6
			font = ImageFont.truetype("/home/pi/christmas_tree_lights/fonts/chr13.ttf", FONTSIZE)
	if currsong-1 in [0,3,7,9,10,12]:
		x = -6
		font = ImageFont.truetype("/home/pi/christmas_tree_lights/fonts/chr13.ttf", 18)        
	for i in songs[currsong-1][2]:#
		(font_width, font_height) = font.getsize(i)
		draw.text((width //2 - font_width // 2, x), str(i.strip()), font=font, fill=(255,255,255))
		x += FONTSIZE+2
    # Display image.
	
	disp.image(image)
	while True:
		next_step = seq_data[step].split(",")
		next_step[1] = next_step[1].rstrip()
		cur_time = int(round(time.time() * 1000)) - start_time - 150

		if GPIO.input(buttonplus) == GPIO.HIGH and cur_time > 900:
			break
		if GPIO.input(buttonminus) == GPIO.HIGH and cur_time > 900:
			currsong -= 2
			break

        # time to run the command
		if int(next_step[0]) <= cur_time:
	
			next_step
            # if the command is Relay 1-8
			if next_step[1] >= "1" and next_step[1] <= "8":

                # change the pin state
				if next_step[2] == "1":
                    #print(pin_map[logical_map[int(next_step[1])]])
					GPIO.output(pin_map[logical_map[int(next_step[1])]], True)
				else:
                    #print(pin_map[logical_map[int(next_step[1])]])
					GPIO.output(pin_map[logical_map[int(next_step[1])]], False)

            # if the END command
			if next_step[1].rstrip() == "END":
				for i in range(1, 9):
					GPIO.output(pin_map[logical_map[i]], True)
				break
			step += 1
	
