import sys
import os
import re
import pygame
import time
import random

images_folder = "/Users/max/Desktop/clocks"

specificRE = """\((\d{2}:\d{2})\)-File:.*?(.jpg|.JPG|.png|.PNG|.svg|.jpeg|.GIF|.gif|.Jpg)"""

specificTimes = {}
nonSpecificTimes = {}

pattern = re.compile(specificRE)

pygame.init()
width = 1024
height = 768
screen = pygame.display.set_mode((width, height))
c = pygame.time.Clock()

for dirname, dirnames, filenames in os.walk(images_folder):
      # print path to all filenames.
    for filename in filenames:
        result = pattern.match(filename)
        
        if result:
	        itime = result.groups()[0]
	        if itime not in specificTimes:
	        	specificTimes[itime] = [filename]
	        else:
	        	specificTimes[itime].append(filename)


while True:

	imageCandidates = None
	time12h = time.strftime("%I:%M")
	time24h = str(int(time12h.split(":")[0]) + 12) + ":" + time12h.split(":")[1]

	# print time12h, time24h

	if time12h in specificTimes:
		imageCandidates = specificTimes[time12h]
	if time24h in specificTimes:
		imageCandidates += specificTimes[time24h]

	if imageCandidates is None:
		print "No images found :("
		sys.exit()

	# print "Image Candidates: %s" % imageCandidates
	imageFilename = imageCandidates[random.randrange(0, len(imageCandidates))]

	# print "Image: %s" % imageFilename

	imageFile =  images_folder + "/" + imageFilename
	img = pygame.image.load(imageFile)
	size = img.get_size()
	proportion = float(height) / size[1]
	xResize = int(size[0] * proportion)
	img = pygame.transform.scale(img, (xResize, height))
	screen.fill((0,0,0))

	if xResize < width:
		xPos = (width / 2) - (xResize / 2)
	else: xPos = 0

	screen.blit(img, (xPos, 0))
	pygame.display.flip()
	pygame.time.wait(15000)