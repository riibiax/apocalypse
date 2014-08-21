#!/usr/bin/python
try:
  from bs4 import BeautifulSoup
  from selenium import webdriver
  from selenium.webdriver.common.by import By
  from selenium.webdriver.support.ui import Select
  from selenium.webdriver.common.keys import Keys
  from selenium.common.exceptions import NoSuchElementException
  import time, re, random, os
except ImportError:
  print "You should install some modules like:\n"
  print "time, random, re, os, serial, Selenium, BeautifulSoup\n"


###Global Variables#################################################
brightness = "11"
light = ""
tweet = ""
#ser= serial.Serial("/dev/ttyACM0", 9600)

###take_dom##########################################################
def take_dom(page):
  soup = BeautifulSoup(page)
  return soup

###find_sentence#####################################################
def find_sentence(c, txt):
  lenT = len(txt)
  sentenceEnders = re.compile('[.!?;:]')
  infile = open("tweets_book.txt", "r")
  text = infile.read()
  infile.close()
  sentenceList = sentenceEnders.split(text)
  sentences = []
  for sentence in sentenceList:
    if c in sentence:
      sentence = sentence.replace('\n', ' ').replace('\r',' ').replace('             ', ' ').replace('0','').replace('1','').replace('2','').replace('3','').replace('4','').replace('5','').replace('6','').replace('7','').replace('8','').replace('9','').replace(':','').lstrip(' ')
      lenTweet = lenT + len(sentence)
      if lenTweet < 140:
        sentences.append(sentence)
  return sentences
             
###light_conversion##################################################
def light_conversion():
  global brightness
  if brightness == "10":
    result = "Satan"
  elif brightness == "9":
    result = " war"
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

###find_tweet########################################################
def find_tweet():
  global tweet
  soup = take_dom(driver.page_source)
  links = soup.find_all("a", class_="tweet-timestamp js-permalink js-nav")
  n = random.randint(0,len(links)-1) 
  link = links[n]
  url = link.get('href')
  splittedtweet = url.split('/')
  tweet = splittedtweet[len(splittedtweet)-1]
  if not url.startswith("https"):
    url = "https://twitter.com" + url
  driver.get(url)
  
###random_comment####################################################  
def random_comment(text):
  global light
  sentences = find_sentence(light, text)
  sentence = sentences[random.randint(0,len(sentences)-1)]
  return sentence

###findInText()######################################################
def findInText(text):
  previousReply = "ApocalypseHead"
  myname = "Apocalypse Head"
  previousPosts = driver.find_elements_by_css_selector('.fullname.js-action-profile-name.show-popup-with-id')
  if not previousReply in text:
    for sentence in previousPosts:
      if myname in sentence.text:
        return False
  else:
    return False
  return True
  
###add_comment#######################################################
def add_comment():
  global tweet
  tweet_reply = "tweet-box-reply-to-" + str(tweet)
  time.sleep(2)
  try:
    text = driver.find_element_by_id(tweet_reply).text
    previousPost = findInText(text)
    if previousPost:
      comment = random_comment(text)
      time.sleep(2)
      driver.find_element_by_id(tweet_reply).send_keys(comment, Keys.ARROW_DOWN)
      time.sleep(5)
      driver.find_element_by_css_selector('.btn.primary-btn.tweet-action').click()
  except:
    time.sleep(1)
  
###search_query######################################################
def search_query():
  global light
  time.sleep(2)
  light = light_conversion()
  driver.find_element_by_id("search-query").clear()
  driver.find_element_by_id("search-query").send_keys(light, Keys.ARROW_DOWN)
  driver.find_element_by_css_selector('.nav-search').click()
  time.sleep(5)

###read_serial#######################################################
def read_serial():
  incoming_brightness = ser.readline()
  light = incoming_brightness.strip("\r\n")
  return light
  
###download_apocalypse###############################################
def download_apocalypse():
  url = "http://www.gutenberg.org/cache/epub/8066/pg8066.txt"
  command = "curl -o tweets_book.txt -A Mozilla/4.0 " + url
  try:
    with open('tweets_book.txt') as f: pass
  except IOError as e:
    os.system(command)

###log_in############################################################
def log_in(user, passwd):
  driver.get("https://twitter.com")
  time.sleep(2)
  driver.find_element_by_id("signin-email").clear()
  driver.find_element_by_id("signin-email").send_keys(user, Keys.ARROW_DOWN)
  driver.find_element_by_id("signin-password").clear()
  driver.find_element_by_id("signin-password").send_keys(passwd, Keys.ARROW_DOWN)
  time.sleep(2)
  driver.find_element_by_id("signin-password").send_keys(Keys.RETURN)
  

###Main##############################################################
os.system('clear')
print "\n\n*** Welcome to the apoclyptic posting script on Tweet ***\n"
print "\n** Loading.. **"  
username = "ApocalypseHead"
password = "head2012"
driver = webdriver.Firefox()

#Twitter log-in
log_in(username, password)

#Download apocalype book
download_apocalypse()

#brightness = read_serial()

#loop to add comments
while True:
  if brightness != "11":
    search_query()
    find_tweet()
    add_comment()
  brightness = "10" #read_serial()
os.system('if [ -e tweets_book.txt ]; then rm tweets_book.txt; fi')
driver.close()
driver.quit



