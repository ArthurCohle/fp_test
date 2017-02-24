#USAGE
#python group.py --dataset 54274 --shelve db.shelve_54274 --query 0_0.978662_s0-131d0920-e1e1-11e6-885d-ff6e67f653c9.jpg --distance 0


# import the necessary packages
from PIL import Image
import imagehash
import argparse
import shelve
import glob
import shutil
import os

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required = True,
	help = "path to dataset of images")
ap.add_argument("-s", "--shelve", required = True,
	help = "path of shelve database")
ap.add_argument("-q", "--query", required = True,
	help = "path to the query image")
ap.add_argument("-dis", "--distance", required = True,
	help = "similarity,non-negative")

args = vars(ap.parse_args())

# open the shelve database
db = shelve.open(args["shelve"], writeback = True)

# load the query image, compute the image hash
query = Image.open(args["query"])
h = str(imagehash.dhash(query))

# make directory
if os.path.exists("similar"):
	shutil.rmtree("similar")
if os.path.exists("unsimilar"):
	shutil.rmtree("unsimilar")
os.mkdir("similar")
os.mkdir("unsimilar")

# grouping
for item in db.items():
	# similar
	if abs(int(item[0],16)-int(h,16)) <= int(args["distance"]):
		for filename in item[1]:
			shutil.copy(args["dataset"] + "/" + filename,"similar/" + filename)
	# unsimilar
	else:
		for filename in item[1]:
			shutil.copy(args["dataset"] + "/" + filename,"unsimilar/" + filename)
		
# close the shelf database
db.close()