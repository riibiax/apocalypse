#!/usr/bin/python
# -*- coding: utf-8 -*-
try:
  import time, random, re, os, sys, flickrapi
  from selenium import webdriver
  from selenium.webdriver.common.by import By
  from selenium.webdriver.support.ui import Select
  from selenium.webdriver.common.keys import Keys
  from selenium.common.exceptions import NoSuchElementException
  from bs4 import BeautifulSoup
 #sys.path.append(os.path.join("Sources"))
  from yocto_api import *
  from yocto_lightsensor import *
except ImportError:
  print "You should install some modules like:\n"
  print "time, random, re, os, sys, Selenium, BeautifulSoup, flickrapi\n"


###Global Variables#################################################
api_key ="7cf1a32b029967579424cdf6afc6b104"
my_image = 0
comments = []
usernames = []
my_username = ""
brightness = "11"

###has_attribute#####################################################
def has_attribute(tag):
  return tag.has_key('data-track') and tag.get('data-track')=="thumb"

###take_dom##########################################################
def take_dom(page):
  soup = BeautifulSoup(page)
  return soup

###find_sentence#####################################################
def find_sentence(c):
  sentenceEnders = re.compile('[.!?]')
  infile = open("comments_book.txt", "r")
  text = infile.read()
  infile.close()
  sentenceList = sentenceEnders.split(text)
  sentences = []
  for sentence in sentenceList:
    if c in sentence:
     sentences.append(sentence)
  return sentences

###light_conversion##################################################
def light_conversion():
  global brightness
  if brightness == "10":
    result = "Satan"
  elif brightness == "9":
    result = "Devil"
  elif brightness == "8":
    result = "Hell"  
  elif brightness == "7":
    result = " death"
  elif brightness == "6":
    result = " beast"
  elif brightness == "5":
    result = " horse"
  elif brightness == "4":
    result = " angel" 
  elif brightness == "3":
    result = " king"
  elif brightness == "2":
    result = "Lord"
  elif brightness == "1":
    result = "Christ"
  elif brightness == "0":
    result = "God"
  else:
    result = "Jesus"
  return result

###random_comment####################################################  
def random_comment():
  light = light_conversion()
  sentences =find_sentence(light)
  sentence = sentences[random.randint(0,len(sentences)-1)]
  comment_result = sentence.replace('\n', ' ').replace('\r',' ').replace('             ', ' ').replace('0','').replace(':','').replace('1','').replace('2','').replace('3','').replace('4','').replace('5','').replace('6','').replace('7','').replace('8','').replace('9','').lstrip(' ')
  return comment_result

###wget_image########################################################
def wget_image(image, directory):
  src = image.get('src')
  string = "wget -P " + directory + " " + src
  os.system(string)

###fetch_info########################################################
def fetch_info():
  global my_image, usernames
  elements = take_dom(driver.page_source)
  image = elements.find_all(id="liquid-photo")
  icons = elements.find_all("img", class_="buddyicon personmenu-trigger")
  users = elements.find_all("strong", class_="username")
  username = users[0].contents[1].string
  usernames.append(username)
  wget_image(image[0], "flickr_comments/images/")
  wget_image(icons[0], "flickr_comments/usr/")
  if my_image==0:
    buddy = elements.find_all("img", class_="comment-buddy-icon") 
    wget_image(buddy[0], "flickr_comments/buddy/")
    my_image=1

###add_comment#######################################################
def add_comment():
  global comments
  time.sleep(2)
  try:
    driver.find_element_by_id("message").clear()
    comment = random_comment()
    comments.append(comment)
    driver.find_element_by_id("message").send_keys(comment)
    time.sleep(2)
    driver.find_element_by_name("Submit").click()
    #ser.write("a")
    time.sleep(5)
  except:
    time.sleep(1)

###explore_7_days####################################################
def explore_7_days(r_url):
  driver.get(r_url)
  soup = take_dom(driver.page_source)
  links = soup.find_all(has_attribute)
  n = random.randint(0,len(links)-1) 
  link = links[n]
  url = link.get('href')
  if not url.startswith("http"):
    url = "http://www.flickr.com" + url
  return url

###gen_arguments#####################################################
def gen_arguments():
  global brightness
  date_day = str(random.randrange(1,29))
  date_month = str(random.randrange(1,13))
  date_year = str(random.randrange(2008,2013))
  string = date_year+"-"+date_month+"-"+date_day
  if brightness == "0":
    min_date = string + " 05:30:00"
    max_date = string + " 06:30:00"
  elif brightness == "1":
    min_date = string + " 06:30:00"
    max_date = string + " 07:30:00"
  elif brightness == "2":
    min_date = string + " 08:30:00"
    max_date = string + " 09:30:00"
  elif brightness == "3":
    min_date = string + " 11:30:00"
    max_date = string + " 12:30:00"
  elif brightness == "4":
    min_date = string + " 13:30:00"
    max_date = string + " 14:30:00"
  elif brightness == "5":
    min_date = string + " 16:00:00"
    max_date = string + " 16:59:59"
  elif brightness == "6":
    min_date = string + " 17:00:00"
    max_date = string + " 18:59:59"
  elif brightness == "7":
    min_date = string + " 19:00:00"
    max_date = string + " 20:59:59"
  elif brightness == "8":
    min_date = string + " 21:00:00"
    max_date = string + " 21:59:59"
  elif brightness == "9":
    min_date = string + " 22:00:00"
    max_date = string + " 23:59:59"    
  elif brightness == "10":
    min_date = string + " 23:00:00"
    max_date = string + " 23:59:59"
  arguments = {"tag_mode": "all", "min_taken_date": min_date, "max_taken_date": max_date}
  return arguments

###call_loop#########################################################
def call_loop():
  args = gen_arguments()
  for photo in flickr.walk(**args):
    owner = photo.get('owner')
    photo_id = photo.get('id')
    if owner !="" and photo_id !="":
      picture_url = "http://www.flickr.com/photos/" + owner + "/" + photo_id
      break
  return picture_url

###get_automatic#####################################################
def get_automatic():
  while True:
    userAutomatic = raw_input("Do you want to use the apocalyptic web bot? [ y / n ]\n")
    if userAutomatic not in ["y","n"]:
      print "You should choose y or n!!\n"
      continue
    else:     
      break
  if userAutomatic == "y":
    result= True
  else:
    result = False
  return result

###log_in############################################################
def log_in(user, passwd):
  driver.get("http://www.flickr.com/signin/")
  time.sleep(2)
  driver.find_element_by_id("username").clear()
  driver.find_element_by_id("username").send_keys(user,Keys.ARROW_DOWN)
  time.sleep(2)
  driver.find_element_by_id("passwd").clear()
  driver.find_element_by_id("passwd").send_keys(passwd, Keys.ARROW_DOWN)
  time.sleep(2)
  driver.find_element_by_id(".save").click()
  time.sleep(2)

###download_apocalypse###############################################
def download_apocalypse():
  url = "http://www.gutenberg.org/cache/epub/8066/pg8066.txt"
  command = "curl -o comments_book.txt -A Mozilla/4.0 " + url
  try:
    with open('comments_book.txt') as f: pass
  except IOError as e:
    os.system(command)
    
###make_conversion###################################################
def make_conversion(n):
  if n in ["0","1","2","3","4","5","6","7","8","9"]:
	lux = "0"
  elif n in ["10","11","12","13","14","15","16","17","18","19"]:
	lux = "1"
  elif n in ["20","21","22","23","24","25","26","27","28","29"]:
	lux = "2"
  elif n in ["30","31","32","33","34","35","36","37","38","39"]:
	lux = "3"
  elif n in ["40","41","42","43","44","45","46","47","48","49"]:
	lux = "4"
  elif n in ["50","51","52","53","54","55","56","57","58","59"]:
	lux = "5"
  elif n in ["60","61","62","63","64","65","66","67","68","69"]:
	lux = "6"
  elif n in ["70","71","72","73","74","75","76","77","78","79"]:
	lux = "7"
  elif n in ["80","81","82","83","84","85","86","87","88","89"]:
	lux = "8"
  elif n in ["90","91","92","93","94","95","96","97","98","99"]:
	lux = "9"
  elif n  == 100:
	lux = "10"	   
  return lux

###die###############################################################
def die(msg):
  sys.exit(msg+' (check USB cable)')

###read_serial#######################################################
def read_serial():
  if target=='any':
    # retreive any Light sensor
    sensor = YLightSensor.FirstLightSensor()
    if sensor is None :
      die('No module connected')
  else:
    sensor= YLightSensor.FindLightSensor(target + '.lightSensor')
  if not(sensor.isOnline()):die('device not connected')
  incoming_brightness = str(int(sensor.get_currentValue()))
  light = make_conversion(incoming_brightness)
  YAPI.Sleep(1000)
  return light

###Main##############################################################
os.system('clear')
print "\n\n*** Welcome to the apoclyptic posting script on Flickr ***\n"
##print "\n** Logging.. **\n"
##automatic = get_automatic()
username = "apocalypsehead@yahoo.com"
password = "head2012"
#if not automatic:
##  username = raw_input("Please enter a flickr username: \n")
##  password = getpass.getpass("..and the password: \n")
print "\n** Loading.. **"  
driver = webdriver.Firefox()

#flickr log-in
log_in(username, password)

os.system('if [ -d ./flickr_comments ]; then rm -r flickr_comments/; fi')
#Download apocalype book
download_apocalypse()

flickr = flickrapi.FlickrAPI(api_key)
errmsg=YRefParam()
target = sys.argv[1]
if YAPI.RegisterHub("usb", errmsg)!= YAPI.SUCCESS:
    sys.exit("init error"+errmsg.value)
brightness = read_serial()

#loop to add comments
while True:
  if brightness != "11" and old_bright != brightness:
    if brightness in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]:
      random_url = call_loop()
    else:
      random_url = explore_7_days("http://www.flickr.com/explore/interesting/7days/")
    driver.get(random_url)
    #fetch_info()
    add_comment()
    old_bright = brightness
  brightness = read_serial()
os.system('if [ -d ./flickr_comments ]; then rm -r flickr_comments/; fi')
os.system('if [ -e comments_book.txt ]; then rm comments_book.txt; fi')
driver.close()
driver.quit


### fare l'algoritmo sui pixeles


