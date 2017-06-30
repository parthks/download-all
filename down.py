import json

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from pyvirtualdisplay import Display

import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import urllib
import wget
import math
import subprocess


"""
Prints message in red.
"""
def print_error(message):
    print '\033[31m{}\033[0m'.format(str(message))

"""
Prints message in yellow.
"""
def print_warning(message):
    print '\033[33m{}\033[0m'.format(str(message))

"""
Prints message in green.
"""
def print_success(message):
    print '\033[32m{}\033[0m'.format(str(message))


currentPercent = -1
def hook(arg1, arg2, arg3):
    global currentPercent
    #print(arg1, arg2, arg3)
    if arg1 != 0:
        numBlocks = arg3 / float(arg2)
        percent = math.floor((float(arg1) / numBlocks) * 100)
        #print(percent)
        if percent > currentPercent:
            currentPercent = percent
            print_success(str(currentPercent)+"%")



# url = 'https://ph2dol.oloadcdn.net/dl/l/HixliSej0z1-8vrM/yDTIgWU2U3c/Forest.Warrior.1996.720p.BluRay.x264.YIFY.mp4?mime=true'
# urllib.urlretrieve(url, 'name.mp4', hook)

# raw_input("hi STOP!")

f = open('sortedByRating.txt', 'r')
movies = json.load(f)
f.close()

f = open('movies.txt', 'r')
moviesDict = json.load(f)
f.close()

currentRating = 8.9

# display = Display(visible=0, size=(800, 600))
# display.start()
#url = 'https://openload.co/embed/yDTIgWU2U3c/Forest.Warrior.1996.720p.BluRay.x264.YIFY.mp4'
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
#capabilities = DesiredCapabilities.FIREFOX()
#driver = webdriver.Firefox(executable_path='/usr/local/bin/geckodriver',capabilities=capabilities)

#driver.get(url)


def get_movie(name, link):
    driver = webdriver.Chrome('/usr/local/bin/chromedriver', chrome_options=chrome_options)
    print("Started Chrome!! YAYY")

    driver.get(link)
    movieLink = driver.find_element_by_class_name('bwac-btn').get_attribute("href")
    driver.get(movieLink)
    main_window = driver.current_window_handle

    driver.find_element_by_xpath("/html/body/div[@id='xmain']/div[@id='main']/div[@class='container']/div[@class='main-content main-detail']/div[@class='md-top']/div[@id='player-area']/div[@class='pa-server']/div[@class='pas-header']/div[@class='pash-choose']/div[@class='btn-group']/ul[@id='servers-list']/li[@id='sv-14']/a").click()
    driver.switch_to_window(main_window)
    
    driver.switch_to.frame("iframe-embed")
    driver.find_element_by_id("videooverlay").click()
    driver.find_element_by_class_name("vjs-big-play-button").click()
    dl = driver.find_element_by_id("olvideo_html5_api").get_attribute("src")

    #wget.download(dl)
    print("starting download!")
    subprocess.call("mkdir "+str(name), shell=True)
    subprocess.call("cd "+str(name), shell=True)
    time.sleep(5)

    #urllib.urlretrieve(dl, str(name)+'.mp4', hook)

    print("finished downloading!")
    driver.quit()



def upload_movie(name):
    print("uploading...")
    subprocess.call("cd ..", shell=True)
    subprocess.call("gdrive upload -p 0B5SLYItizrrvbk51R3JXb0Y5Zkk -r "+str(name)+"/", shell=True)
    print("done uploading...")
   



while currentRating > 8.7:
    imbd = ''+str(currentRating)+''
    if not imbd in movies:
        currentRating -= 0.1
        continue
    else:
        moviesForRating = movies[imbd]
        #print(len(moviesForRating))

        for movie in moviesForRating:
            movie = movie.items()
            print movie[0][0]
            #get_movie(movie[0][0],movie[0][1])
            upload_movie(movie[0][0])

    currentRating -= 0.1





