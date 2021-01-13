#Scrapes the Vennt wiki "all paths" page for path and ability data
#
#Author: Ryan Muther, December 2020

import sys
import time
import json

from bs4 import BeautifulSoup
import requests

#gets the list of paths and their URLs from the vennt wiki
# returns a list of (path name, URL) tuples
def getPaths():
	pathsURL = "https://vennt.fandom.com/wiki/List_of_Paths"

	#get the page
	pathsPage = requests.get(pathsURL).content
	pathsPage = BeautifulSoup(pathsPage,features="lxml")

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
	page = BeautifulSoup(page,features="lxml")

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

if __name__ == "__main__":
	try:
		outfile = sys.argv[1]
	except:
		print("Usage: scrapePaths.py outfile")
		print("Requires json, requests, bs4, lmxl")
		exit(1)

	#get the list of paths
	paths = getPaths()
	print("Found %d paths"%len(paths))

	#open the output file
	out = open(outfile,"w",encoding="utf8")

	all_entries = []
	#for each path...
	for i,(name,url) in enumerate(paths):
		print("(%d/%d) Scraping %s"%(i+1,len(paths),url))

		#get the path's abilities
		abilities = getAbilities(url)

		#write each ability name as well as its path and URL to the file
		for ability in abilities:
			entry = {"path":name,"ability":ability,"url":url}
			all_entries.append(entry)
			
		#sleep to be polite to the server
		time.sleep(1)
	out.write(json.dumps(all_entries,ensure_ascii=False, indent=4)+"\n")