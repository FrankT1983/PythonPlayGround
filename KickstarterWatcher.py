import urllib.request
from bs4 import BeautifulSoup



def GetAllPledgeLevels(url) :
    f = urllib.request.urlopen(url)
    if f is None :
        return  None
    html= f.read()
    f.close()

    if html is None :
        return  None

    soup = BeautifulSoup(html , "lxml")
    pledges = soup.find_all("div", class_="pledge__info")
    if pledges is None :
        return  []

    all_Pledgeds = []
    for p in pledges:
        title = p.find("h3", class_="pledge__title")
        limit = p.find("span", class_="pledge__limit")

        if not title is None :
            pledgeName = title.text.strip()
            pledgeLimit = ""
            if not title is None:
                pledgeLimit = limit.text.strip()

            all_Pledgeds.append([pledgeName,pledgeLimit])

    return all_Pledgeds


def PrintToConsole(projects):
    for p in projects :
        print(str(p[0]))
        for pledge in p[1] :
            print("\t" + str(pledge[0]) + "\t" + str(pledge[1]))



toWatch = [[ "CubiOne" ,"https://www.kickstarter.com/projects/99671519/cubibot-the-new-standard-of-modern-consumer-3d-pri"]]

projects = []
for proj in toWatch :
    projects.append([proj[0], GetAllPledgeLevels(proj[1])])


PrintToConsole(projects)