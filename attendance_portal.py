#-- coding: utf-8 --
'''
NOTE: This code may not suit your purpose. Designed for a specific portal.
Python version 2.7

This script automatically logs in to the attendance portal 
and fetches the "In time" of the current day.
If 9 hours is consumed from the In time, it generates a 
notification on the system tray as a pop up for every 15 minutes.
Module "fnotify" which is used here is available as "windows_tray_notifer" 
in my Git repository.

Author - Srini
Blog: https://creativentechno.wordpress.com/
GitHub: https://github.com/gsrini2
'''
import os
import sys
import time
import datetime
import fnotify as fnotification

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import selenium.webdriver.support.ui as ui
from selenium.webdriver import ActionChains

#Launching browser and Logging to portal 
chromedriver = 'C:\chromedriver.exe'
browser = webdriver.Chrome(chromedriver)
#browser.set_window_size(0,0)
browser.get("url of the portal")

#browser.maximize_window()
wait = ui.WebDriverWait(browser, 1)  
username = browser.find_element_by_name("txtUsername")
password = browser.find_element_by_name("txtPassword")

username.send_keys("your user name")
password.send_keys("your pass word")

wait = ui.WebDriverWait(browser, 1)
browser.find_element_by_id("btnLogin").click()

wait = ui.WebDriverWait(browser, 1)

#Navigating to the required attendance sheet
actions = ActionChains(browser)
spans = browser.find_elements_by_tag_name('span')
actions.move_to_element(spans[2])
actions.perform()
spans_submenu = browser.find_elements_by_tag_name('span')
spans_submenu[1].click()

all_btns = browser.find_elements_by_xpath("//input[@type='submit']")
all_btns[0].click()

entries = browser.find_elements_by_tag_name("td")
lines = entries[4].text.split('\n')

current_date_time = time.asctime(time.localtime(time.time()))
current_date_time = current_date_time.split()
current_date = current_date_time[1]+' '+current_date_time[2] 
current_time = current_date_time[3]

#Getting the current InTime from the attendance sheet
for line in lines:
    if current_date in line:
        today = line.split()

for word in today:
    if 'AM' in word:
        #Intime = word.split()
        Intime = str(word).strip('AM').split(':')#+':00'

browser.close()
# Calculates and sends notification for every 15 minutes if 9 hours is expired from the In time
while True:
    Man_hours = datetime.datetime.now() - datetime.timedelta(hours = int(Intime[0]),minutes = int(Intime[1]))
    print "Man hours is",Man_hours
    if Man_hours.hour>=9:
        fnotification.balloon_tip("Time up","Today's Man hours ="+str(Man_hours.hour)+"hrs and "+str(Man_hours.minute)+"min")
        time.sleep(900)
  
