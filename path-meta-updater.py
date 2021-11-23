# Josh Aaron Miller 2021 + path scraping by Ryan Muther 2020
# Vennt Path metadata scraper

import time, requests, datetime, re, sys, json
from bs4 import BeautifulSoup

import os, pickle, time
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

pathsURL = "https://vennt.fandom.com/wiki/List_of_Paths"
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


def loginToGoogleSheets():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    
    
def update_to_sheets(spreadsheet_id, sheet_range, vs):
    print("update_to_sheets: updating {0} in {1} with {2}".format(sheet_range, spreadsheet_id, vs))
    body = {'values' : vs}
    result = service.spreadsheets().values().update(
    spreadsheetId=spreadsheet_id, range=sheet_range,
    valueInputOption='RAW', body=body).execute()



#gets the list of paths and their URLs from the vennt wiki
# returns a list of (path name, URL) tuples
def getPaths():
    pathsURL = "https://vennt.fandom.com/wiki/List_of_Paths"

    #get the page
    pathsPage = requests.get(pathsURL).content
    pathsPage = BeautifulSoup(pathsPage, 'html.parser') #features="lxml")

    #get all the path links from the page,
    # filter only to those that lead to paths that have existing pages
    links = pathsPage.find_all("a")
    pathLinks = [link for link in links if link.has_attr("title") and "Path of the" in link["title"]]
    pathLinks = [link for link in pathLinks if "does not exist" not in link["title"]]

    #Get the URLs and path names
    URLs = ["https://vennt.fandom.com"+link["href"] for link in pathLinks]
    names = [link["title"] for link in pathLinks]
    
    return list(zip(names,URLs))
    
#given a URL to a path's page,
# gets all the ability names from that path
# returns a list of strings
def getAbilities(url):
    #get the page
    page = requests.get(url).content
    page = BeautifulSoup(page, 'html.parser') #features="lxml")
    #soup = BeautifulSoup(page.content, 'html.parser')

    #get the abilities section and pull out the text of each
    # <p> tag in it, removing the non-completion requirement descriptors,
    # prereq descriptors, and activation costs
    abilitySection = page.find("div",{"class":"mw-parser-output"})
    pTags = [p.text.strip() for p in abilitySection.find_all("p")]
    pTags = [p for p in pTags if "This ability is not required for the Path Completion Bonus." not in p]
    pTags = [p for p in pTags if not "Prerequisite" in p]
    pTags = [p for p in pTags if not "Activation:" in p]

    #iterate through all the <p> tags finding those that
    # either immediately precede an "Unlocks: " line or a
    # "Cost: " line
    abilities = []
    for idx,text in enumerate(pTags):
        #handle the simpler case where we're on an unlock line
        if "Unlocks: " in text:
            abilityName = pTags[idx-1]
            abilities.append(abilityName)
        #and the more complex case where we're on a cost line
        # We need to not add an unlock line to the ability list
        # Yes, this could be one check, but that line would
        # be egregiously long
        elif text.startswith("Cost: ") and "Unlocks: " not in pTags[idx-1]:
            abilityName = pTags[idx-1]
            abilities.append(abilityName)

    return abilities





    # for hit in soup.find_all('p'):
        # text = hit.get_text()
        # text = text.replace("’", "'") # I hate smart quotes
        
            #   if found and (text.isspace() or (text.startswith('\n') and last_had_newline)):




if __name__ == "__main__":
    paths = getPaths()
    for i,(name,url) in enumerate(paths):
        print("(%d/%d) Scraping %s"%(i+1,len(paths),url))
        
        abilities = getAbilities(url)
        
        for ability in abilities:
            
        
        
        exit(0) # test
        
        #sleep to be polite to the server
        time.sleep(1)