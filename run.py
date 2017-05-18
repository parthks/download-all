import math

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
#from pyvirtualdisplay import Display

import urllib

import time
import json
import thread

import traceback
import sys
reload(sys)
sys.setdefaultencoding('utf-8')




'''
- parse html of the page to get video link, name of file
- download! and save name of file to txt file
- navigate to another movie
- repeat
'''

'''
 - write down the links and names of the movies that solar movies has 
'''

#Store all the movies here!
# f = open('sites.txt', 'r+')
# f.seek(0,2)
# f.write('hi hi\n')
# f.seek(0,2)
# f.write('lol\n')
# f.seek(0,2)
# f.write('habadaaaduba3tu37786876423\n')
# f.close()


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
        numBlocks = arg3 / arg2
        percent = math.floor((float(arg1) / numBlocks) * 100)
        #print(percent)
        if percent > currentPercent:
            currentPercent = percent
            print_success(str(currentPercent)+"%")



class Movie(object):
    name = ""
    link = ""

    def __init__(self, name, link):
        self.name = name.encode()
        self.link = link.encode()
        
    def __str__(self):
        return "name: "+self.name+"\nlink: "+self.link+"\n"


#display = Display(visible=0, size=(800, 600))
#display.start()
#driver = webdriver.Chrome('/Users/Parth/Desktop/download-all/chromedriver')
#driver = webdriver.PhantomJS(service_args=['--ssl-protocol=any'])  
#driver.implicitly_wait(1) 

#driver.get(startingUrl)

#get movie page

#url = "https://solarmoviez.to/movie/the-accidental-spy-2014.html"




'''
 SETUP
 - first get a list of 10 related movies and put it in 
 moviesDict with all values toDo
 - Also put all in moviesToVist

LOOP until moviesToVist is empty
 - get first movie from moviesToVist and check with moviesDict
 - if it says toDo then go there else delete it and continue
 - go to the page and make it "visited" in moviesDict
 - add new related movies to moviesDict and movesToDo
 - repeat! 

'''





url = 'https://solarmoviez.to/movie/voyage-of-the-damned-13167.html'

moviesDict = {}
moviesToVist = []
errorNum = 0

driver = webdriver.Chrome('/Users/Parth/Desktop/download-all/chromedriver')

def start():
    global driver, url

    driver.get(url)
    #time.sleep(1)

    getRelatedMovies()

    makeListOfAllMovies()



def getRelatedMovies():
    global driver, moviesDict, moviesToVist

    relatedMoviesXpath = "/html/body/div[@id='xmain']/div[@id='main']/div[@class='container']/div[@class='main-content main-detail ']/div[@class='movies-list-wrap mlw-related']/div[@id='movies-related']/div[@class='ml-item']"
    #driver.find_elements_by_xpath(du)[1].text
    addXpath = "/a[@class='ml-mask']" #prepend -> [1]
    numOfRelatedMovies = len(driver.find_elements_by_xpath(relatedMoviesXpath))

    #print(numOfRelatedMovies)

    for i in range(1,numOfRelatedMovies+1):
        xpath = relatedMoviesXpath + '[' + str(i)+ ']' + addXpath
        relatedMovie = driver.find_element_by_xpath(xpath)
        movieInfo = relatedMovie.get_attribute("innerText").split('\n')
        movieName = movieInfo[1].encode()
        #print(movieInfo)
        if movieInfo[0] == 'HD' and not movieName in moviesDict.keys():
            moviesToVist.append(Movie(movieName, relatedMovie.get_attribute("href")))
            getMoreMovieInfo(movieName, relatedMovie.get_attribute("href"))
            #moviesDict[movieInfo[1]] = "toVisit"

    print("got "+str(len(moviesDict))+" movies in all")
    print(str(len(moviesToVist))+" movies left to visit!")


def getMoreMovieInfo(movieName, movieLink):
    global driver, moviesDict

    xpathDescription = "/html/body/div[@id='xmain']/div[@id='main']/div[@class='container']/div[@class='main-content main-detail ']/div[@class='md-top']/div[@id='mv-info']/div[@class='mvi-content']/div[@class='mvic-desc']/div[@class='desc']"
    xpathImbd = "/html/body/div[@id='xmain']/div[@id='main']/div[@class='container']/div[@class='main-content main-detail ']/div[@class='md-top']/div[@id='mv-info']/div[@class='mvi-content']/div[@class='mvic-desc']/div[@class='mvic-info']/div[@class='mvici-right']/p[4]"
    xpathDate = "/html/body/div[@id='xmain']/div[@id='main']/div[@class='container']/div[@class='main-content main-detail ']/div[@class='md-top']/div[@id='mv-info']/div[@class='mvi-content']/div[@class='mvic-desc']/div[@class='mvic-info']/div[@class='mvici-right']/p[3]"
    xpathActors = "/html/body/div[@id='xmain']/div[@id='main']/div[@class='container']/div[@class='main-content main-detail ']/div[@class='md-top']/div[@id='mv-info']/div[@class='mvi-content']/div[@class='mvic-desc']/div[@class='mvic-info']/div[@class='mvici-left']/p[2]"
    xpathGenres = "/html/body/div[@id='xmain']/div[@id='main']/div[@class='container']/div[@class='main-content main-detail ']/div[@class='md-top']/div[@id='mv-info']/div[@class='mvi-content']/div[@class='mvic-desc']/div[@class='mvic-info']/div[@class='mvici-left']/p[1]"


    status = "toVisit"
    descrip = driver.find_element_by_xpath(xpathDescription).text
    imbd = driver.find_element_by_xpath(xpathImbd).text.split(': ')[1]
    date = driver.find_element_by_xpath(xpathDate).text.split(': ')[1]
    actors = driver.find_element_by_xpath(xpathActors).text.split(': ')[1].split(', ')
    genres = driver.find_element_by_xpath(xpathGenres).text.split(': ')[1].split(', ')


    tempDict = {   'status': status, 'link': movieLink,
        'description': descrip,
        'IMBD': imbd,
        'Release': date,
        'BigShots': actors,
        'Genres': genres 
    }

    moviesDict[movieName] = tempDict


def visitMovie(movie):
    global driver, moviesDict, url
    #print('LOLOLOLOLOLOLOL')
    url = movie.link
    name = movie.name.encode()
    driver.get(movie.link)
    #time.sleep(1)
    getRelatedMovies()
    moviesDict[name]["status"] = "done"



def makeListOfAllMovies():
    global moviesDict, moviesToVist

    while len(moviesToVist) > 0:
        movie = moviesToVist[0]
        movieName = movie.name.encode()
        if movieName in moviesDict.keys() and moviesDict[movieName]["status"] == "toVisit":
            visitMovie(movie)

        print('poping unique!')
        moviesToVist.pop(0)


    outputInFile()
    print_success("!DONE EVERYTHING :D!")
    sys.exit()
    


def outputInFile():
    global driver

    f = open('movies.txt', 'w')
    f.write(json.dumps(moviesDict, indent=4))
    f.close()
    


def command():
    takeInput = raw_input('Press "s" at any time to SAVE\n')
    if takeInput == "s":
        outputInFile()
        print_success("DONE SAVING!!!")
        thread.start_new_thread(command, ())



thread.start_new_thread(command, ())

while True:
    
    try:
        #command()
        start()        
        print("contine...")
        

    except Exception as e:
        print_error(e)
        ex_type, ex, tb = sys.exc_info()
        traceback.print_tb(tb)

        outputInFile()
        driver.get_screenshot_as_file('error'+str(errorNum)+'.png')

        errFile = open('error.txt', 'r+')
        errFile.seek(0,2)
        traceback.print_tb(tb, file=errFile)
        errFile.write(str(errorNum) +' -- '+ str(e)+'\n\n')
        errFile.close()

        errorNum += 1
        if errorNum > 10:
            sys.exit()
        #driver.close()
    




# while True:
#     driver = webdriver.Chrome('/Users/Parth/Desktop/download-all/chromedriver')
#     driver.get(url)

#     time.sleep(2)

#     # nextMovieLink = driver.find_element_by_class_name('ml-mask').get_attribute("href")
#     # print(nextMovieLink)

    



#     # print("downloading " + str(movieName))
#     # movies.append(movieName)

#     # if driver.find_element_by_class_name("mli-quality").get_attribute("innerText") == 'HD':
#     #     pass



#     movieLink = driver.find_element_by_class_name('bwac-btn').get_attribute("href")


#     driver.get(movieLink)

#     time.sleep(1)

#     downloadLink = driver.find_element_by_tag_name('video').get_attribute("src")
#     driver.close()


#     movieSave = str(movieName) + ".mp4"
#     #exampleurl = 'https://r4---sn-ab5szn7l.googlevideo.com/videoplayback?id=928514188706eacf&itag=22&source=webdrive&requiressl=yes&ttl=transient&pl=17&sc=yes&ei=fFEdWfRKgsipBcP_vKAF&driveid=0B8HbXCjz8jjwNENjaFVBaE5XWTA&mime=video/mp4&lmt=1489784776389217&ip=162.243.61.106&ipbits=0&expire=1495108028&sparams=driveid,ei,expire,id,ip,ipbits,itag,lmt,mime,mm,mn,ms,mv,pl,requiressl,sc,source,ttl&signature=70653B46FC920C73E0487A0D753855098172033D.3599D2E8EEE308C880FB2D66F9944A45F2B41F1A&key=cms1&app=explorer&cms_redirect=yes&mm=31&mn=sn-ab5szn7l&ms=au&mt=1495102525&mv=m'
#     urllib.urlretrieve(downloadLink, movieSave, hook)

#     moviesDict
    
#     print_success('DONE\n')

#     url = nextMovieLink



