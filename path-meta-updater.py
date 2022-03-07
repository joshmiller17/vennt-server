# Josh Aaron Miller 2021 + path scraping by Ryan Muther 2020
# Vennt Path metadata scraper

import time, requests, datetime, re, sys, json, os, pickle
from bs4 import BeautifulSoup
from collections import defaultdict
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

pathsURL = "https://vennt.fandom.com/wiki/List_of_Paths"
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
VALID_GIFTS = ['Alertness', 'Craft', 'Alacrity', 'Charm', 'Finesse', 'Magic', 'Mind', 'Rage', 'Science']

SPREADSHEET_ID = open('sheet.txt').read()

g_Service = None

def loginToGoogleSheets():
    global g_Service
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
    g_Service = build('sheets', 'v4', credentials=creds)
    sheet = g_Service.spreadsheets()
    
    
def updateSheet(spreadsheet_id, sheet_range, vs):
    global g_Service
    print("update_to_sheets: updating {0} in {1} with {2}".format(sheet_range, spreadsheet_id, vs))
    body = {'values' : vs}
    result = g_Service.spreadsheets().values().update(
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
    
#given a soup
# gets all the ability names from that path
# returns a list of strings
def getAbilities(page):
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


# Returns contents of ability as list of lines
def getAbilityContents(ability, soup, smartquotes = False):
    found = False
    contents = []
    last_had_newline = False
    best_match = 999
    for hit in soup.find_all('p'):
        text = hit.get_text()
        if (smartquotes):
            text = text.replace("'", "’")
        else:
            text = text.replace("’", "'")
        if ability in text and len(text) < best_match: # Goes through the whole page, takes the *shortest* valid line which matches the given description
            found = True
            best_match = len(text)
            contents = []
        if found and (text.isspace() or (text.startswith('\n') and last_had_newline)):
            found = False
        if found:
            contents.append(text)
            if text.endswith('\n'):
                last_had_newline = True
            else:
                last_had_newline = False
    if (not smartquotes and contents == []):
        return getAbilityContents(ability, soup, True) # if we failed, try with smartquotes
    return contents

def countExpedited(line):
    m = re.match("Expedited for: (.*)", line)
    if not m:
        return "ERROR"
    result = m.group(1)
    gifts = result.split(", ")
    return gifts
    

if __name__ == "__main__":

    print("Logging into Google Sheets...")
    loginToGoogleSheets()
    headers = ["Path", "Requirements", "Completion Bonus", "Num Abilities", "Total XP Cost"]
    for g in VALID_GIFTS:
        headers.append("Expedited for " + g)
    
    print("Fetching paths...")
    paths = getPaths()
    for i,(name,url) in enumerate(paths):
        print("(%d/%d) Scraping %s"%(i+1,len(paths),url))
        
        #get the pa]ge
        page = requests.get(url).content
        soup = BeautifulSoup(page, 'html.parser') #features="lxml")
        
        abilities = getAbilities(soup)
        expedited_count = defaultdict(int)
        XP_sum = 0  
        requirements = ""
        completion_bonus = ""
        
        for b in soup.body:
            if "Requirements:" in b:
                m = re.match("Requirements: (.*)", b)
                result = m.group(1)
                requirements = result
            if "Path Completion Bonus:" in b:
                m = re.match("Path Completion Bonus: (.*)", b)
                result = m.group(1)
                completion_bonus = result
        
        if requirements == "":
            print("WARNING: " + name + " has bad Requirements")
        if completion_bonus == "":
            print("WARNING: " + name + " has bad Path Completion Bonus")
        
        for ability in abilities:
            contents = getAbilityContents(ability, soup)
            if contents == []:
                print("WARNING: " + ability + " not found")
            else:
                for line in contents:
                    if line.startswith("Expedited"):
                        gifts = countExpedited(line)
                        for key in gifts:
                            if key not in VALID_GIFTS:
                                print("WARNING: " + key + " is not a valid Expedited for " + ability)
                            expedited_count[key] += 1
                    if line.startswith("Cost"):
                            m = re.match("Cost: (.*) XP", line)
                            if not m:
                                print("WARNING: No Cost found for " + line + " in " + ability)
                            else:
                                cost = m.group(1)
                                if not cost.isnumeric():
                                    print("WARNING: " + cost + " is not a valid XP Cost for " + ability)
                                else:
                                    XP_sum += int(cost)
        
        # rquirements, completion bonus, num abilities
        row = [name, requirements, completion_bonus, len(abilities), XP_sum]
        for g in VALID_GIFTS:
            row.append(expedited_count[g])
        updateSheet(SPREADSHEET_ID, "Paths!A%d:N%d"%(i+2,i+2), [row])
        #print(expedited_count)
        #print(XP_sum)
                
        #sleep to be polite to the server
        time.sleep(1)
        
    # add header last
    updateSheet(SPREADSHEET_ID, "Paths!A1:N1", [headers])
