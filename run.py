import math

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from pyvirtualdisplay import Display

import urllib

import time
import json
import thread

import traceback
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


url = 'https://solarmoviez.to/movie/harry-potter-and-the-sorcerers-stone-1552.html'

moviesDict = {}
moviesToVisit = []
errorNum = 0
done = 0

#COMMENT THESE 2 LINES IF RUNNING LOCALLY!
# display = Display(visible=0, size=(800, 600))
# display.start()

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
#driver = webdriver.Chrome('/usr/local/bin/chromedriver')
driver = webdriver.Chrome('/usr/local/bin/chromedriver', chrome_options=chrome_options)
print("Started Chrome!! YAYY")



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



# class Movie(object):
#     name = ""
#     link = ""

#     def __init__(self, name, link):
#         self.name = name.encode()
#         self.link = link.encode()
        
#     def __str__(self):
#         return "name: "+self.name+"\nlink: "+self.link+"\n\n"




'''
 SETUP
 - first get a list of 10 related movies and put it in 
 moviesDict with all values toDo
 - Also put all in moviesToVisit

LOOP until moviesToVisit is empty
 - get first movie from moviesToVisit and check with moviesDict
 - if it says toDo then go there else delete it and continue
 - go to the page and make it "visited" in moviesDict
 - add new related movies to moviesDict and movesToDo
 - repeat! 

'''







def start():
    global driver, url

    driver.get(url)
    #time.sleep(1)

    getRelatedMovies()

    makeListOfAllMovies()



def getRelatedMovies():
    global driver, moviesDict, moviesToVisit

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
            #moviesToVisit.append(Movie(movieName, relatedMovie.get_attribute("href")))
            moviesToVisit.append(movieName)
            getLittleMovieInfo(movieName, relatedMovie.get_attribute("href"))
            #moviesDict[movieInfo[1]] = "toVisit"

    print("got "+str(len(moviesDict))+" movies in all")
    print(str(len(moviesToVisit))+" movies left to visit!")


def getLittleMovieInfo(movieName, movieLink):
    global moviesDict
    tempDict = { 'link': movieLink,
     'status': "toVisit"

    }
    moviesDict[movieName] = tempDict




def getMoreMovieInfo(movieName, movieLink):
    global driver, moviesDict

    xpathDescription = "/html/body/div[@id='xmain']/div[@id='main']/div[@class='container']/div[@class='main-content main-detail ']/div[@class='md-top']/div[@id='mv-info']/div[@class='mvi-content']/div[@class='mvic-desc']/div[@class='desc']"
    xpathImbd = "/html/body/div[@id='xmain']/div[@id='main']/div[@class='container']/div[@class='main-content main-detail ']/div[@class='md-top']/div[@id='mv-info']/div[@class='mvi-content']/div[@class='mvic-desc']/div[@class='mvic-info']/div[@class='mvici-right']/p[4]"
    xpathDate = "/html/body/div[@id='xmain']/div[@id='main']/div[@class='container']/div[@class='main-content main-detail ']/div[@class='md-top']/div[@id='mv-info']/div[@class='mvi-content']/div[@class='mvic-desc']/div[@class='mvic-info']/div[@class='mvici-right']/p[3]"
    xpathActors = "/html/body/div[@id='xmain']/div[@id='main']/div[@class='container']/div[@class='main-content main-detail ']/div[@class='md-top']/div[@id='mv-info']/div[@class='mvi-content']/div[@class='mvic-desc']/div[@class='mvic-info']/div[@class='mvici-left']/p[2]"
    xpathGenres = "/html/body/div[@id='xmain']/div[@id='main']/div[@class='container']/div[@class='main-content main-detail ']/div[@class='md-top']/div[@id='mv-info']/div[@class='mvi-content']/div[@class='mvic-desc']/div[@class='mvic-info']/div[@class='mvici-left']/p[1]"


    status = "done"
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
    #print moviesDict

def visitMovie(movie):
    global driver, moviesDict, url, done
    url = moviesDict[movie]["link"]
    driver.get(url)
    #time.sleep(1)
    getRelatedMovies()
    getMoreMovieInfo(movie, url)
    done += 1
    if (done % 50 == 0):
        outputInFile()
    print("visited "+str(done)+" movies, can save n stop now")



def makeListOfAllMovies():
    global moviesDict, moviesToVisit

    while len(moviesToVisit) > 0:
        movieName = moviesToVisit[0].encode()
        if movieName in moviesDict.keys() and moviesDict[moviesToVisit[0]]["status"] == "toVisit":
            visitMovie(moviesToVisit[0])

        print('poping unique!')
        moviesToVisit.pop(0)


    outputInFile()
    print_success("!DONE EVERYTHING :D!")
    sys.exit()
    


def outputInFile():
    global driver

    f = open('movies.txt', 'w')
    f.write(json.dumps(moviesDict, indent=4))
    f.close()

    g = open('moviesToVisit.txt', 'w')
    json.dump(moviesToVisit, g)
    g.close()

    d = open('done.txt', 'w')
    d.write(str(done))
    d.close()

    print_success("DONE SAVING!!!")

    


def command():
    takeInput = raw_input('Press "s" at any time to SAVE\n')
    if takeInput == "s":
        outputInFile()
        thread.start_new_thread(command, ())



i = raw_input("continue? press c: ")
if i == 'c':
        #done = int(raw_input("how many done? "))
        f = open('movies.txt', 'r')
        g = open('moviesToVisit.txt', 'r')
        d = open('done.txt','r')
        moviesDict = json.load(f)
        moviesToVisit = json.load(g)
        done = int(d.read())
        f.close()
        g.close()

thread.start_new_thread(command, ())

while True:
    
    try:
        if i == "c":
            makeListOfAllMovies()
        else:
            # i = raw_input("are you sure you want to start over?")
            start()        

    except Exception as e:
        print_error("ERROR")
        #print_error(e)
        ex_type, ex, tb = sys.exc_info()
        traceback.print_tb(tb)
        outputInFile()
        #driver.get_screenshot_as_file('error'+str(errorNum)+'.png')

        errFile = open('errorMovies.txt', 'r+')
        errFile.seek(0,2)
        traceback.print_tb(tb, file=errFile)
        errFile.write(str(errorNum) +' -- '+ str(e)+'\n\n')
        errFile.write(str(moviesToVisit[0])+'\n')
        errFile.close()
        moviesDict[moviesToVisit[0]]["status"] = "ERROR"
        moviesToVisit.pop()
        print_warning("Popped element!")
        print(moviesToVisit[0])
        outputInFile()
        print("continue...")
        thread.start_new_thread(command, ())






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



