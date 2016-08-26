import cloudinary.api as cda
import cloudinary
from cloudinary import uploader
import threading
import json
import re

cloudinary.config( 
  cloud_name = "dominicbett", 
  api_key = "897862564791181", 
  api_secret = "AJcDSocxqA4wrXSxqxD06iHtnDY" 
)

class Images:
	def __init__(self, name, url):
		self.name = name
		self.url = url

cloudinaryURLs = []
with open("../ExtractPhotos/imageURLData.txt", 'r') as lines:
	for line in lines:
		url = line.strip()
		print "Uploading: %s" % url
		image_name = url.split("/")[-1]
		response = cloudinary.uploader.upload(url, public_id=image_name, folder="Aphorites/")
		cloudinaryURL = response["url"]
		name = re.findall(r"(.*?)-[0-9_]+?\.[a-z]+", image_name)[0]
		name = name.replace("-", " ")
		image = Images(name, cloudinaryURL)
		cloudinaryURLs.append(image)

def obj_dict(obj):
		return obj.__dict__
serializedData = json.dumps(cloudinaryURLs, default=obj_dict)


#print serializedData
with open('data.json','w') as f:
	f.write(str(serializedData))
f.close()
print "DONE!"
