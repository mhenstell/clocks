import urllib2
import urllib
from bs4 import BeautifulSoup
import pickle
import json
import time

downloadFolder = "/Users/max/Desktop/clocks"
base = "http://commons.wikimedia.org"

# url = "https://commons.wikimedia.org/wiki/Time_on_clocks_and_watches"
# response = urllib2.urlopen(url)
# html = response.read()


from Queue import Queue
from threading import Thread

class Worker(Thread):
    """Thread executing tasks from a given tasks queue"""
    def __init__(self, tasks):
        Thread.__init__(self)
        self.tasks = tasks
        self.daemon = True
        self.start()
    
    def run(self):
        while True:
            func, args, kargs = self.tasks.get()
            try: func(*args, **kargs)
            except Exception, e: print e
            self.tasks.task_done()

class ThreadPool:
    """Pool of threads consuming tasks from a queue"""
    def __init__(self, num_threads):
        self.tasks = Queue(num_threads)
        for _ in range(num_threads): Worker(self.tasks)

    def add_task(self, func, *args, **kargs):
        """Add a task to the queue"""
        self.tasks.put((func, args, kargs))

    def wait_completion(self):
        """Wait for completion of all the tasks in the queue"""
        self.tasks.join()

imagePages = []
images = []

with open("images.txt", "r") as f:
	lines = f.readlines()
	for line in lines:
		images.append(json.loads(line))

	# print images

# with open("clocks.html", 'r') as f:
# 	print "Loading clocks directory"
# 	soup = BeautifulSoup(f.read())
# 	hits = soup.findAll("li", { "class" : "gallerybox" })

# 	for hit in hits:
# 		link = hit.a["href"]
# 		time = hit.div.p.contents[0]
# 		imagePages.append({'time': time, 'link': link})


# def getImageUrl(imagePage, imagePages):
# 	print "Processing image (time %s) (len images %s)" % (imagePage['time'], len(images))
# 	url = base + imagePage['link']
# 	response = urllib2.urlopen(url)
# 	html = response.read()
# 	soup = BeautifulSoup(html)
# 	imageLink = soup.findAll('div', {'class': "fullImageLink"})[0].a["href"]
# 	imagePage['imageLink'] = imageLink
# 	images.append(imagePage)

def getImage(image, count, num, length):
	print "Downloading image %s/%s (time %s)" % (count, length, image['time'])
	name = image['link'].replace("/wiki/", "")
	urllib.urlretrieve("http:" + image['imageLink'], "%s/(%s)-%s" % (downloadFolder, image['time'], name))
	# print "http:" + image['imageLink']
	time.sleep(0.5)



pool = ThreadPool(10)
timeCounters = {}
count = 0
for image in images:

	if image['time'] in timeCounters:
		timeCounters[image['time']] += 1
	else:
		timeCounters[image['time']] = 0

	pool.add_task(getImage, image, count, timeCounters[image['time']], len(images))
	count += 1

pool.wait_completion()




# with open("images.txt", 'w') as f:
# 	for image in images:
# 		f.write(json.dumps(image))
# 		f.write("\n")




# count = 0
# timeCounters = {}

# for image in images:

# 	print "Downloading image %s (%s) for time %s" % (count, image['link'], image['time'])


# 	urllib.urlretrieve(base + image['link'], downloadFolder + "/" + image['time'] + "-" + str(timeCounters[image['time']]) + ".jpg")
# 	count += 1


