# -*- coding: utf-8 -*-
"""Searching and Downloading Google Images/Image Links

This module do Searching and Downloading Google Images/Image Links

Example:
        $ python example_google.py

Attributes:
    None

Todo:
    * Add Attributes
    * Multi-Thread

"""

#Import Libraries

import time  #Importing the time library to check the time of code execution
import sys   #Importing the System Library
import hashlib
import urllib
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
from pathlib import Path

########### Edit From Here ###########

#This list is used to search keywords. You can edit this list to search for google images of your choice. 
#You can simply add and remove elements of the list.

firstRound = ['anime girl', 'pixiv']
secondRound = ['color drawing', 'orange', 'red', 'light', 'color', 'face', 'green', 'blue', 'coloring', 'dark', 'gray', 'pretty']
thirdRound = ['eye', 'face', 'body', 'weapon', 'hair', 'uniform', 'summer', 'winter', 'autumn', 'spring', 'kimono', 'swim', 'school']
USER_AGENT = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17'
########### End of Editing ###########




#Downloading entire Web Document (Raw Page Content)
def download_page(url):
    version = (3, 0)
    cur_version = sys.version_info
    if cur_version >= version:     #If the Current Version of Python is 3.0 or above
        import urllib.request    #urllib library for Extracting web pages
        try:
            headers = {}
            headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
            req = urllib.request.Request(url, headers=headers)
            resp = urllib.request.urlopen(req)
            respData = str(resp.read())
            return respData
        except Exception as e:
            print(str(e))


#Finding 'Next Image' from the given raw page
def _images_get_next_item(s):
    start_line = s.find('rg_di')
    if start_line == -1:    #If no links are found then give an error!
        end_quote = 0
        link = "no_links"
        return link, end_quote
    else:
        start_line = s.find('"class="rg_meta"')
        start_content = s.find('"ou"', start_line+1)
        end_content = s.find(',"ow"', start_content+1)
        content_raw = str(s[start_content+6:end_content-1])
        return content_raw, end_content


#Getting all links with the help of '_images_get_next_image'
def _images_get_all_items(page):
    _items = []
    while True:
        item, end_content = _images_get_next_item(page)
        if item == "no_links":
            break
        else:
            _items.append(item)      #Append all the links in the list named 'Links'
            time.sleep(0.1)        #Timer could be used to slow down the request for image downloads
            page = page[end_content:]
    return _items


############## Main Program ############
T0 = time.time()   #start the timer

intNoC = len(firstRound) * len(secondRound) * len(thirdRound)
print("Number of keyword combinations: " + str(intNoC))

#Download Image Links
items = []
for i in firstRound:
    for j in secondRound:
        for k in thirdRound:
            temp = ' '.join([i, j, k])
            print("Evaluating keyword name = " + temp)
            search = temp.replace(" ", "%20")

            print("Keyword:" + search)
            URL = 'https://www.google.com/search?q=' + search + '&espv=2&biw=1366&bih=667&site=webhp&source=lnms&tbm=isch&sa=X&ei=XosDVaCXD8TasATItgE&ved=0CAcQ_AUoAg'
            RAW_HTML = (download_page(URL))
            time.sleep(0.1)
            items.extend(_images_get_all_items(RAW_HTML))
            #print ("Image Links = "+str(items))
            print("Total Image Links = "+str(len(items)))
            print("\n")


            #This allows you to write all the links into a test file.
            #This text file will be created in the same directory as your code.
            #You can comment out the below 3 lines to stop writing the output to the text file.
            FH = open('output.txt', 'a')        #Open the text file called database.txt

            FH.write(search + ": " + str(items) + "\n\n\n")
            #Write the title of the page

            FH.close()                            #Close the file

#Calculating the total time required to crawl, find and download all the links of 60,000 images
print("Total time taken: " + str(time.time() - T0) + " Seconds")
print("Starting Download...")

## To save imges to the same directory
# IN this saving process we are just skipping the URL if there is any error

errorCount = 0
for item in items:
    try:
        outputPath = "output/" + hashlib.md5(item).hexdigest() + ".jpg"

        if Path(outputPath).is_file:
            print(outputPath + " is already downloaded. Skip.")
        else:
            REQ = urllib.request.Request(item, headers={"User-Agent": USER_AGENT})
            RESPONSE = urlopen(REQ)
            DATA = RESPONSE.read()
            open(outputPath, 'wb').write(DATA)
            RESPONSE.close()

        print("completed ====> "+str(item))

    except IOError:   #If there is any IOError
        errorCount += 1
        print("IOError on image "+str(item))
    except HTTPError as e:  #If there is any HTTPError
        errorCount += 1
        print("HTTPError"+str(item))
    except URLError as e:
        errorCount += 1
        print("URLError "+str(item))

print("\n")
print("All are downloaded")
print("\n"+str(errorCount)+" ----> total Errors")

#----End of the main program ----#
