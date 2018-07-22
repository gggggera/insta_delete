# -*- coding: UTF-8 -*-
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup, SoupStrainer
from datetime import datetime
import time
import os
import sys

# store urls to delete later
log_path = 'C:/Users/eddyizm/Source/Repos/seleniumTesting/env/media_urls.txt'
#ig_html = r'C:\Users\eddyizm\Downloads\eddyizm.html'
logintext = "C:\\Users\\eddyizm\\Desktop\\Work\\login.txt"
URLS = []

def stime(seconds):
    return time.sleep(seconds)

def OpenLog():
    with open(log_path, 'r', encoding= 'utf-8') as g:
        lines = g.read().splitlines()
        return (lines)

def WriteToArchive(log, data):
    with open(log, 'w', encoding= 'utf-8') as f:
        for d in data:
            if d.startswith('https://www.instagram.com/'):
                f.write(str(d)+'\n')
            else:
                f.write('https://www.instagram.com'+str(d)+'\n')
            
             
def parse_href(data):
    url_list = []
    for link in BeautifulSoup(data, "html.parser", parse_only=SoupStrainer('a') ):
        if link.has_attr('href'):
            t = link.get('href')
            print (t)
            if t is not None:
                url_list.append(t)
                
    return url_list            

def scroll_to_end():
    browser = webdriver.Chrome()
    get_html = None
    print (datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print ('scrolling profile to get more urls')
    try:
        browser.get("https://www.instagram.com/eddyizm")
        lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        match=False
        count = 0
        while(match==False):
            lastCount = lenOfPage
            time.sleep(10)
            lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
            count += 1
            if lastCount==lenOfPage:
                match=True
                
        get_html = browser.page_source                       
        browser.close()
        print ('scrolled down: '+str(count)+' times!')
        print (datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    except Exception as err:
        print (err)
        browser.close()
    
    return get_html

def login_to_site():
    print ('logging in as mobile device to delete')
    print (datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    mobile_emulation = { "deviceName": "Pixel 2" }
    options = webdriver.ChromeOptions()
    options.add_experimental_option("mobileEmulation", mobile_emulation)
    options.add_argument("window-size=500,800")
    browser = webdriver.Chrome(chrome_options=options)
    browser.get("https://www.instagram.com/accounts/login/")
    stime(3)
    f = open (logintext, 'r')
    login = f.read().splitlines()
    f.close()
    insta_username = login[0]
    insta_password = login[1]
    eUser = browser.find_elements_by_xpath(
        "//input[@name='username']")
    stime(1)
    ActionChains(browser).move_to_element(eUser[0]). \
        click().send_keys(insta_username).perform()
    stime(1)
    ePass = browser.find_elements_by_xpath(
        "//input[@name='password']")
    stime(2)
    ActionChains(browser).move_to_element(ePass[0]). \
        click().send_keys(insta_password).perform()

    
    stime(5)
    login_button = browser.find_element_by_xpath(
        "//form/span/button[text()='Log in']")
    
    ActionChains(browser).move_to_element(login_button).click().perform()
    stime(10)
        
    links = OpenLog()
    new_file = []
    deleted_urls = []
    counter = 10
    for l in links:
        if l.startswith('https://www.instagram.com/p/'):
            new_file.append(l)
    print ('counter should be set to 10: '+str(counter))
    print ('length of file: '+str(len(new_file)))
    if (counter >= len(new_file)):
        counter = (len(new_file) - 1)
    
    for n in new_file:
        print (n)
    print (counter)
    try:
        print ('in try block to go into delete while loop')
        print (datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        while (counter > -1):
            print (new_file[counter])
            browser.get(new_file[counter])
            stime(10)
            if ("Sorry, this page isn't available." in browser.page_source):
                deleted_urls.append(new_file[counter])
                counter -= 1
            else:                
                options_button = browser.find_element_by_xpath(
                    "//span[text()='More options']")
                ActionChains(browser).move_to_element(options_button).click().perform()                
                stime(5)
                delete_button = browser.find_element_by_xpath(
                    "//button[text()='Delete']")
                ActionChains(browser).move_to_element(delete_button).click().perform()
                stime(10)
                confirm_delete = browser.find_element_by_xpath(
                    "//button[text()='Delete']")
                ActionChains(browser).move_to_element(confirm_delete).click().perform()
                stime(10)
                deleted_urls.append(new_file[counter])
                counter -= 1

        l3 = [x for x in new_file if x not in deleted_urls]
        print ('while loop done and exited successfully')
        print (datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        WriteToArchive(log_path, l3)	    
        browser.close()

    except Exception as err:
        print (err)
        browser.close()
        sys.exit()

print ('--------------------------------------- new session ------------------------------------------------- ')
print (datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
file_size = os.stat(log_path).st_size
print ('file size: '+str(file_size))
if (os.stat(log_path).st_size == 0):
    print ('file empty, going to scroll')
    source_data = scroll_to_end()
    URLS = parse_href(source_data)
    print ('printing parsed URLS to write to log')
    print (URLS)
    WriteToArchive(log_path, URLS)    

# # manually load html file
# URLS = parse_href( open(ig_html, 'r',  encoding= 'utf-8') ) 
# WriteToArchive(log_path, URLS)

login_to_site()
print ('--------------------------------------- end session ------------------------------------------------- ')
print (datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
sys.exit()