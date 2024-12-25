from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import time
import random


subject = ["hey good morning","have a great day","i think you are fine",] #add more if you want more text and replace the text in which you required

option = webdriver.ChromeOptions()
option.add_experimental_option("debuggerAddress","localhost:9222")

driver = webdriver.Chrome(options=option)

time.sleep(2)

driver.get("https://www.gmail.com")

time.sleep(3)

driver.find_element_by_css_selector("body > div:nth-child(23) > div.nH > div > div.nH.aqk.aql.bkL > div.aeN.WR.baA.nH.oy8Mbf > div.aic > div > div").click() #click on compose button
time.sleep(6)
to = driver.find_element_by_name('to')
ActionChains(driver)\
.send_keys("toyou123@gmail.com")\
.perform()
#replace with your sender mail id

time.sleep(3)

driver.find_element_by_xpath('//input[@type="file"]').send_keys(r"C:\Users\Hp\Desktop\Bots\gmail\data.txt") #here the file or document will send (replace path with your where your file located if you don't want to use means add # in these line in starting of these code)

time.sleep(3)

driver.find_element_by_name("subjectbox").send_keys(random.choice(subject)) #subject

time.sleep(5)

driver.find_element_by_css_selector('.T-I.J-J5-Ji.aoO.v7.T-I-atl.L3').click()

time.sleep(30)   

driver.close()
