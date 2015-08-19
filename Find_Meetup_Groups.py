import urllib
import json
import pandas as pd
import matplotlib.pyplot as plt
from geopy.geocoders import Nominatim
geolocator = Nominatim() #create object
places = [ "san fransisco", "california", "boston ", "new york" , "pennsylvania", "colorado", "seattle", "washington","los angeles", "san diego", "houston", "austin", "kansas", "delhi", "chennai", "bangalore", "mumbai" , "Sydney","Melbourne", "Perth", "Adelaide", "Brisbane", "Launceston", "Newcastle" , "beijing", "shanghai", "Suzhou", "Shenzhen","Guangzhou","Dongguan", "Taipei", "Chengdu", "Hong Kong"]
# login on meetup.com. if you dont have an account, then please signup
# Go to https://secure.meetup.com/meetup_api/console/?path=/2/groups
# In the topics like "Python", enter topic of your choice. and click on show response
# copy the signed key. in the singed key, copy the sig_id and sig and initialise variables sig_id and sig
# sample signed key : "https://api.meetup.com/2/groups?offset=0&format=json&topic=python&photo-host=public&page=20&radius=25.0&fields=&order=id&desc=false&sig_id=******&sig=*****************"
urls = [] #url lists
radius = 50.0 #add the radius in miles
data_format = "json" #you can add another format like XML
topic = "Python" #add your choice of topic here
sig_id = "186640998" # initialise with your sign id, check sample signed key
sig = "6dba1b76011927d40a45fcbd5147b3363ff2af92" # initialise with your sign, check sample signed key
for place in places: 
 location = geolocator.geocode(place)
 urls.append("https://api.meetup.com/2/groups?offset=0&format=" + data_format + "&lon=" + str(location.longitude) + "&topic=" + topic + "&photo-host=public&page=500&radius=" + str(radius)+"&fields=&lat=" + str(location.latitude) + "&order=id&desc=false&sig_id=" +sig_id + "&sig=" + sig)
city,country,rating,name,members = [],[],[],[],[]
for url in urls:
 response = urllib.urlopen(url)
 data = json.loads(response.read())
 data=data["results"]
 
 for i in data :
 city.append(i['city'])
 country.append(i['country'])
 rating.append(i['rating'])
 name.append(i['name'])
 members.append(i['members']) 
 
df = pd.DataFrame([city,country,rating,name,members]).T
df.columns=['city','country','rating','name','members']
df.sort(['members','rating'], ascending=[False, False])
freq = df.groupby('country').city.count()
fig = plt.figure(figsize=(8,4))
ax1 = fig.add_subplot(121)
ax1.set_xlabel('Country')
ax1.set_ylabel('Count of Groups')
ax1.set_title("Number of Python Meetup Groups")
freq.plot(kind='bar')
freq = df.groupby('country').members.sum()/df.groupby('country').members.count()
ax1.set_xlabel('Country')
ax1.set_ylabel('Average Members in each group')
ax1.set_title("Python Meetup Groups")
freq.plot(kind='bar')
freq = df.groupby('country').rating.sum()/df.groupby('country').rating.count()
ax1.set_xlabel('Country')
ax1.set_ylabel('Average rating')
ax1.set_title("Python Meetup Groups")
freq.plot(kind='bar')
df=df.sort(['country','members'], ascending=[False,False])
df.groupby('country').head(2)
