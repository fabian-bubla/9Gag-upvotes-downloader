# -*- coding: utf-8 -*-
"""
Created on Sat Apr 24 19:39:48 2021

@author: fabia
"""
#IMPORT PACKAGES
import time
import bs4
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from os import getcwd
import os
import codecs
import string
import re
from urllib.request import Request, urlopen

#INITIALIZE LISTS
liked_posts_list = []
successfully_downloaded = []
allowed_characters = list(string.ascii_lowercase)

def initialize_browser():
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=960x480")
    
    browser = webdriver.Chrome(chrome_options=chrome_options, executable_path= getcwd() + '\\chromedriver.exe')
    print('browser started successfully')
    return browser
# "C:\Users\fabia\Nextcloud\Sync\Coding\Small or unfinished scripts\some more\9gag scrape\Your 9GAG data.html"
def get_data_from_9gag_html():
    file = codecs.open("Your 9GAG data.html", "r", "utf-8")
    soup = bs4.BeautifulSoup(file, 'lxml')
    first_link = soup.a

    for i in first_link.find_all_next('a'):
        name = i.parent.next_sibling.next_sibling.get_text()
        url = i.get_text()
        liked_posts_list.append([url, name])
    file.close
    
    
get_data_from_9gag_html()
#VARIABLES
browser = initialize_browser()
browser.get('https://9gag.com')
print('Browser ready.')
print('You now have 8 seconds to press the 9GAG "I accept" button, then the script will continue')


#CLICK AWAY THE POP UP WHERE YOU SIGN AWAY YOUR RIGHTS
time.sleep(8)

#%% HERE STARTS THE MAIN LOOP

for idx, entry in enumerate(liked_posts_list):
    if entry not in successfully_downloaded:
        try:
            #GO TO WEBPAGE
            url = entry[0]
            browser.get(url)
            
            
            #Click more button
            menu = browser.find_element_by_class_name('more')
            actions = webdriver.ActionChains(browser)
            actions.click(menu)
            actions.perform()
            
            #find DL link
            html_file= browser.page_source
            soup = bs4.BeautifulSoup(html_file, 'lxml')
            down_link= soup.findAll('a', href=True, text='Download')[0].get('href')
            filename_throw_away, file_extension = os.path.splitext(down_link)
            down_link = r'https://9gag.com' + str(down_link)
            
            
            #Download Image
            req = Request(down_link, headers={'User-Agent': 'Mozilla/5.0'})
            content = urlopen(req).read()
            
            #CreateFileName
            truncated_title = entry[1][:230]
            imgfilestring = re.sub('\W+',' ', truncated_title) + str(file_extension)
            
            #Save Image
            imageFile = open( r'downloads/' + imgfilestring, 'wb+')
            imageFile.write(content)
            imageFile.close()
            
            print('post ' + str(idx) + ' of ' + str(len(liked_posts_list)))
            successfully_downloaded.append(entry)
        except Exception as e:
            print(e)
            print("Download failed: " +str(entry) )
            continue
    else:
        continue
    
print('finished!')






