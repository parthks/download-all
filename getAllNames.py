#Browsing the top IMBD pages on solar movies

import json

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from pyvirtualdisplay import Display

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




def getAllEmMovies():
    global allMovies, driver
    xpath = "/html/body/div[@id='xmain']/div[@id='main']/div[@class='container']/div[@class='main-content main-category']/div[@class='movies-list-wrap mlw-category']/div[@class='movies-list movies-list-full']/div[@class='ml-item']"
    addXpath = "/a[@class='ml-mask']" #prepend -> [1]
    numOfMoviesOnPage = len(driver.find_elements_by_xpath(xpath))

    for i in range(1,numOfMoviesOnPage+1):
        movieXpath = xpath + '[' + str(i)+ ']' + addXpath
        movieElement = driver.find_element_by_xpath(movieXpath)
        movieInfo = movieElement.get_attribute("innerText").split('\n')
        #print(movieInfo)
        if movieInfo[0] == 'HD':
            #moviesToVisit.append(Movie(movieName, relatedMovie.get_attribute("href")))
            movieLink = movieElement.get_attribute("href")
            allMovies.append(movieLink)
            #moviesDict[movieInfo[1]] = "toVisit"

    print("got "+str(len(allMovies))+" in all")
    print("saving...")
    g = open('allMovieLinks.txt', 'w')
    json.dump(allMovies, g)
    g.close()
    print("done saving")


# f = open('movies.txt', 'r')
# moviesDict = json.load(f)
# f.close()

link = 'https://solarmoviez.to/top-imdb/movie/page-332.html'
allMovies = []
currentPage = 332

g = open('allMovieLinks.txt', 'r')
allMovies = json.load(g)
g.close()

display = Display(visible=0, size=(800, 600))
display.start()

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
driver = webdriver.Chrome('/usr/local/bin/chromedriver', chrome_options=chrome_options)
driver.get(link)

print_success("Started Chrome!! YAYY")

while currentPage < 346:
    getAllEmMovies()
    while True:
        try:
            nextButtonXpath = "/html/body/div[@id='xmain']/div[@id='main']/div[@class='container']/div[@class='main-content main-category']/div[@class='movies-list-wrap mlw-category']/div[@id='pagination']/nav/ul[@class='pagination']/li[@class='next']/a"
            driver.find_element_by_xpath(nextButtonXpath).click()
            print_success("Finished getting page "+str(currentPage))
            currentPage += 1
            break
        except Exception as e:
            print_error("ERROR! :(")
            print_warning("NOTE-> CURRENT PAGE: "+str(currentPage))
            print_error(e) 
            print_warning("TRYING AGAIN")

print_success("ALL DONE!")



