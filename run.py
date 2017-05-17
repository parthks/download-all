import wget

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
#from pyvirtualdisplay import Display


import time


'''
- parse html of the page to get video link, name of file
- download! and save name of file to txt file
- navigate to another movie
- repeat
'''

f = open('sites.txt', 'r+')
f.seek(0,2)
f.write('hi hi\n')
f.seek(0,2)
f.write('lol\n')
f.seek(0,2)
f.write('habadaaaduba3tu37786876423\n')
f.close()


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





#display = Display(visible=0, size=(800, 600))
#display.start()
#driver = webdriver.Chrome('/Users/Parth/Desktop/download-all/chromedriver')
#driver = webdriver.PhantomJS(service_args=['--ssl-protocol=any'])  
#driver.implicitly_wait(1) 

#driver.get(startingUrl)

#get movie page

url = "https://solarmoviez.to/movie/the-accidental-spy-2014.html"

movies = []


while True:
    driver = webdriver.Chrome('/Users/Parth/Desktop/download-all/chromedriver')
    driver.get(url)

    time.sleep(1)

    nextMovieLink = driver.find_element_by_class_name('ml-mask').get_attribute("href")
    print(nextMovieLink)


    movieName = driver.find_element_by_tag_name("h3").get_attribute("innerText")
    print("downloading " + str(movieName))
    movies.append(movieName)

    
    movieLink = driver.find_element_by_class_name('bwac-btn').get_attribute("href")


    driver.get(movieLink)

    time.sleep(1)

    downloadLink = driver.find_element_by_tag_name('video').get_attribute("src")
    driver.close()


    movieSave = str(movieName) + ".mp4"
    wget.download(downloadLink, movieSave)

    
    print('DONE\n')

    url = nextMovieLink



