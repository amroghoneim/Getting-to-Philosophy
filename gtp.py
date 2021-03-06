import requests
from bs4 import BeautifulSoup 
import re
import time

history = []
while(True):
    link = input("url: ")
    if(link != ""):
        break
history.append(link)
r = requests.get(link)
time.sleep(0.5)
soup = BeautifulSoup(r.content, features = 'html.parser')

while soup.find(id = 'firstHeading').get_text() != 'Philosophy':
    for x in soup.find_all(['table']): # remove tables
            x.replace_with("")
    y = soup.find_all('p', {"class" : ""})
    for i in range(len(y) ):
        for s in y[i].find_all(href = re.compile('redlink=1$')): # remove redlinks
            s.replace_with("")
        for s in y[i].find_all(['i']): # remove italics
            s.replace_with("")
        s = str(y[i])
        s = re.sub(r'\s+\((?:[^)(]+|\((?:[^)(]+|\([^)(]*\))*\))*\)', '', s) # remove parenthesized text
        y[i] = BeautifulSoup(s, features = 'html.parser') # re-convert to soup object


    flag = True
    for i in range (len(y)): # go to paragraph that has a wiki link
        if y[i].find(href = re.compile('/wiki/')) != None:
            content = y[i]
            flag = False # found a paragraph that has a wiki link
            break

    if(flag == True):
        print("no link exists!")
        break

    firstLink = content.find(href = re.compile('^/wiki/')) # links that start with /wiki/ only
    
    link = 'http://en.wikipedia.org' + firstLink.get('href')
    if link in history:
        print("loop exists!")
        break
    print(link)
    history.append(link)
    r = requests.get(link)
    time.sleep(0.5)
    soup = BeautifulSoup(r.content, features = 'html.parser')
