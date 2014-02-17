import sys
import os
import re
import pygame
import time
import random
import platform

# if platform.system() == "Darwin":
# 	images_folder = "/Users/max/Desktop/clocks"
# elif platform.system() == "Linux":
# 	images_folder = "../clock_images"

specificRE = """\((\d{2}:\d{2})\)-File:.*?(.jpg|.JPG|.png|.PNG|.svg|.jpeg|.GIF|.gif|.Jpg)"""
genericRE = """\(between (\d{2}:00) and (\d{2}:00)\)-File.*"""

specificTimes = {}
nonSpecificTimes = {}

specificPattern = re.compile(specificRE)
genericPattern = re.compile(genericRE)

try:
	width = int(sys.argv[1])
	height = int(sys.argv[2])
	images_folder = sys.argv[3]
	waitTime = int(sys.argv[4])
	angle = int(sys.argv[5])
except:
	print "Usage: python clocks.py screen-width screen-height"
	sys.exit(1)

pygame.init()
pygame.mouse.set_visible(False)
screen = pygame.display.set_mode((width, height))
c = pygame.time.Clock()

for dirname, dirnames, filenames in os.walk(images_folder):
      # print path to all filenames.
	for filename in filenames:
		specificResult = specificPattern.match(filename)
		genericResult = genericPattern.match(filename)

		if specificResult:
			itime = specificResult.groups()[0]
			if itime not in specificTimes:
				specificTimes[itime] = [filename]
			else:
				specificTimes[itime].append(filename)
		
		elif genericResult:
			startTime = genericResult.groups()[0]
			endTime = genericResult.groups()[1]

			key = "%s-%s" % (startTime, endTime)
			if key not in nonSpecificTimes:
				nonSpecificTimes[key] = [filename]
			else:
				nonSpecificTimes[key].append(filename)


# # Code to make sure we have full coverage
# noTimes = []

def inGeneric(testTime):
	testHour = int(testTime.split(":")[0])

	for timeRange in nonSpecificTimes:
		startHour = int(timeRange.split("-")[0].split(":")[0])
		# endHour = int(timeRange.split("-")[1].split(":")[0])

		if testHour == startHour: return nonSpecificTimes[timeRange]

	return False

# for hour in range(0, 12):
# 	for minute in range(0, 60):
# 		testTime12 = "%02d:%02d" % (hour, minute)
# 		testTime24 = "%02d:%02d" % (hour+12, minute)

# 		if testTime12 not in specificTimes and testTime24 not in specificTimes:
# 			if not inGeneric(testTime12) and not inGeneric(testTime24):
# 				noTimes.append(testTime12)
# print noTimes

# print inGeneric("06:53")

# Clock display code
while True:

	imageCandidates = []
	time12h = time.strftime("%I:%M")
	time24h = str(int(time12h.split(":")[0]) + 12) + ":" + time12h.split(":")[1]

	# print time12h, time24h

	if time12h in specificTimes:
		imageCandidates = specificTimes[time12h]
	if time24h in specificTimes:
		imageCandidates += specificTimes[time24h]

	if len(imageCandidates) == 0:
		imageHour12 = time12h.split(":")[0]
		imageHour24 = time24h.split(":")[0]

		generic12 = inGeneric(imageHour12)
		generic24 = inGeneric(imageHour24)
		if generic12:
			for filename in generic12: imageCandidates.append(filename)
		if generic24:
			for filename in generic24: imageCandidates.append(filename)

		if len(imageCandidates) == 0:
			print "No coverage found for time %s" % time12h
			time.sleep(1)
			continue

	# print "Image Candidates: %s" % imageCandidates
	imageFilename = imageCandidates[random.randrange(0, len(imageCandidates))]

	# print "Image: %s" % imageFilename

	imageFile =  images_folder + "/" + imageFilename
	img = pygame.image.load(imageFile)
	img = pygame.transform.rotate(img, angle)
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
	pygame.time.wait(waitTime * 1000)