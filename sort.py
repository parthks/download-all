import json

print("Sorting movies.txt by rating")


f = open('movies.txt', 'r')
moviesDict = json.load(f)
f.close()

print("parsing "+str(len(moviesDict))+" movies!")

sortedDict = {}
ratings = []

for name in moviesDict:
    if moviesDict[name]['status'] == 'toVisit':
        continue
    imbd = moviesDict[name]['IMBD']
    imbd = ''+str(imbd)+''
    if imbd in sortedDict:
        sortedDict[imbd].append({name : moviesDict[name]['link']})
    else:
        ratings.append(float(imbd))
        sortedDict[imbd] = [{name : moviesDict[name]['link']}]
    # if imbd in sortedDict:
    #     sortedDict[imbd].append(moviesDict[name]['link'])
    # else:
    #     ratings.append(float(imbd))
    #     sortedDict[imbd] = [moviesDict[name]['link']]

print sorted(ratings)
f = open('sortedByRating.txt', 'w')
f.write(json.dumps(sortedDict, indent=4))
# for key in sorted(sortedDict.iterkeys()):
#     f.write("%s: %s" % (key, sortedDict[key]))
#     f.write('\n\n\n')
f.close()
