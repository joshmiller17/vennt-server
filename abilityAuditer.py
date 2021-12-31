import sys, time, json, argparse
from collections import defaultdict
from bs4 import BeautifulSoup
import requests

#gets the list of paths and their URLs from the vennt wiki
# returns a list of (path name, URL) tuples
def getPaths(whichPaths):
	if whichPaths is None:
		print("Searching all paths")
	else:
		print("Searching these paths:", ", ".join(whichPaths))

	pathsURL = "https://vennt.fandom.com/wiki/List_of_Paths"

	#get the page
	pathsPage = requests.get(pathsURL).content
	pathsPage = BeautifulSoup(pathsPage,features="lxml")

	#get all the path links from the page,
	# filter only to those that lead to paths that have existing pages
	links = pathsPage.find_all("a")
	pathLinks = [link for link in links if link.has_attr("title") and "Path of the" in link["title"] and (whichPaths is None or link["title"][12:] in whichPaths)]
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
	#pTags = [p for p in pTags if "This ability is not required for the Path Completion Bonus." not in p]
	#pTags = [p for p in pTags if not "Prerequisite" in p]
	pTags = [p for p in pTags if not "Activation:" in p]

	abilities = []
	expediteCount = defaultdict(int)
	secondLineStarts = ["This ability", "Cost", "Prereq", "Unlock"]
	found = False
	exclusives = {}
	for idx,text in enumerate(pTags):
		for s in secondLineStarts:
			if s in text and not found:
				abilityName = pTags[idx-1]
				abilities.append(abilityName)
				found = True
		if text == "" or text == "\n":
			found = False
		if found and text.startswith("Expedited"):
			exps = text[15:].split(",")
			for e in exps:
				expediteCount[e.replace(" ", "")] += 1
		if found and "Prereq" in text and "Gift" in text:
			exclusives[abilities[-1]] = text[22:]

	return abilities, expediteCount, exclusives
	
def dict_print(d):
	for key, val in d.items():
		print(key + ":", val, end="   ")
	print()
	
def add_dicts(d1, d2):
	d3 = defaultdict(int)
	keys = list(d1.keys()) + list(d2.keys())
	for key in keys:
		d3[key] = d1[key] + d2[key]
	return d3

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Vennt server.')
	parser.add_argument('-out', default='vaudit.json', help="Output file")
	parser.add_argument('-paths', default=None, help="List specific paths to scrape instead of all (ignore 'Path of the')")

	args = parser.parse_args()
	#get the list of paths
	if args.paths is not None:
		paths = getPaths(args.paths.split(","))
	else:
		paths = getPaths(args.paths)
	print("Found %d paths"%len(paths))

	all_entries = []
	totalExpediteCount = defaultdict(int)
	totalExclusives = {}
	#for each path...
	for i,(name,url) in enumerate(paths):
		print("(%d/%d) Scraping %s"%(i+1,len(paths),url))

		#get the path's abilities
		abilities, expediteCount, exclusives = getAbilities(url)

		print(name)
		dict_print(expediteCount)
		totalExpediteCount = add_dicts(expediteCount, totalExpediteCount)
		totalExclusives.update(exclusives)

		#write each ability name as well as its path and URL to the file
		for ability in abilities:
			cleaned_ability = ability.replace("’", "'")
			entry = {"path":name,"ability":cleaned_ability,"url":url}
			all_entries.append(entry)
			
		#sleep to be polite to the server
		time.sleep(1)
	
	print("Total expedited:")
	dict_print(totalExpediteCount)
	
	print("Total exclusive:")
	vals = set(totalExclusives.values())
	for val in vals:
		print(val + ":", sum(v == val for v in totalExclusives.values()))

	duplicate_search = {}
	for ability in all_entries:
		if ability["ability"] in duplicate_search:
			duplicate_search[ability["ability"]].append(ability)
		else:
			duplicate_search[ability["ability"]] = [ability]

	print("------------------------------------------------------------------\nDuplicates:")
	
	for name, abilities in duplicate_search.items():
		if len(abilities) >= 2:
			print("Duplicate Ability: " + name + "\nLocations:")
			for ability in abilities:
				dict_print(ability)
	
	#open the output file
	out = open(args.out,"w",encoding="utf8")
	out.write(json.dumps(all_entries,ensure_ascii=False, indent=4)+"\n")
