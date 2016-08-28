import cloudinary.api as cda
import cloudinary
from cloudinary import uploader
import threading
import json
import re

cloudinary.config( 
  cloud_name = "dominicbett", 
  api_key = "897862543535181", 
  api_secret = "AJcDSocxqA43s5sf3qxD06" 
)

class Images:
	def __init__(self, name, url):
		self.name = name
		self.url = url

cloudinaryURLs = []

with open("../ExtractPhotos/imageURLData.txt", 'r') as lines:
	for line in lines:
		try:
			url = line.strip()
			print "Uploading: %s" % url
			image_name = url.split("/")[-1].split(".")[0]
			response = cloudinary.uploader.upload(url, public_id=image_name, folder="Aphorites/")
			cloudinaryURL = response["url"]
			name = re.findall(r"(.*?)-[0-9_]+?", image_name)[0]
			name = name.replace("-", " ")
			image = Images(name, cloudinaryURL)
			cloudinaryURLs.append(image)
		except Exception, e:
			print e
			continue

def obj_dict(obj):
		return obj.__dict__
serializedData = json.dumps(cloudinaryURLs, default=obj_dict)


#print serializedData
with open('data.json','w') as f:
	f.write(str(serializedData))
f.close()
print "DONE!"
