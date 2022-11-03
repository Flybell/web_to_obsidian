"""Functions for main_script.py"""


import re #regular expression
from bs4 import BeautifulSoup #web parsing library
import io #manipulate files
import os #manipulate paths
import string
from datetime import date, datetime #get dates

#----make requests as a browser-----#
import requests
headers = requests.utils.default_headers()
headers.update({ 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'})
#----------------------------------#

## BEAUTIFUL SOUP
## useful: https://stackoverflow.com/questions/60045381/how-to-get-the-text-and-url-from-a-link-using-beautifulsoup

def make_request(url): #create a soup
    """request HTML soup object from url via beautiful soup"""
    req = requests.get(url, headers)
    soup = BeautifulSoup (req.content, "html5lib")
    return soup

## Scraping data

def get_next_page(soup):
  """ locate the next page button and output url"""
    page = soup.find("li", {"class": "next"}) # customize this search term
    url = page.find("a", href=True) 
    if url != None:
        output_url = "https://dummy.site.com" + url["href"]
        print("starting next page")
    else:
        output_url = 0
        print("\n\nfinal page")
    return output_url

def get_members(soup):
  """ output list of profile urls extracted from page"""
    page = soup.find("div",  {"class": "row"}) # customize this search term
    member_urls = []
    for a in page.find_all("a", href=True): 
        member_urls.append("https://dummy.site.com" + a["href"])
    return member_urls

def get_name(soup):
    """ on profile page, find the "Person Details" section, 
    return full name"""
    name = soup.find("div", {"class": "list_title"}) # customize this search term
    given_name = name.find("span", {"itemprop": "givenName"})
    family_name = name.find("span", {"itemprop": "familyName"})
    return given_name.text.strip() + " " + family_name.text.strip()
  
def get_project_url(soup):
    """ find the "Related Projects" section
    return list of project urls from member profile page"""
    section = soup.find("div", {"class": "related_content"}) # customize this search term
    project_urls = []
    for a in section.find_all("a", href=True, text=True):
        project_urls.append("https://dummy.site.com" + a["href"])
    return project_urls

def get_project_details_soup(soup):
    """ find the Project Details section """
    return soup.find("div", {"class": "view_wrapper"}) # customize this search term

def get_member_string(soup):
    """ finds the string with project info from "Project Details"
    cleans up a string full of tabs and line breaks & rejoins with spaces
    returns a string that looks like this
    First Last | Role 2022-10-15 - 2023-04-14 | Research area: Animals"""
    section = get_project_details_soup(soup)
    string = section.find("div", {"class": "list_category"}).text # customize this search term
    string = " ".join(string.split())
    return string

def get_project_startdate(string):
    """ takes second item of string (member role and dates)
    Role 2022-10-15 - 2023-04-14
    and returns the first string of dates
    2022-10-15"""
    type_date = string.split(" | ")[1]
    return type_date[-23:-13]

def get_project_enddate(string):
    """ takes second item of string (member role and dates)    
    Role 2022-10-15 - 2023-04-14
    and retrieves the second string of dates
    2023-04-14"""
    type_date = string.split(" | ")[1]
    return type_date[-10:]

def get_project_type(string):
    """ takes second item of string (project role and dates)
    and retrieves the role text"""
    type_date = string.split(" | ")[1]
    return type_date.split(" ")[0] + " " + type_date.split(" ")[1]

def get_research_area(string):
    """ takes third item of string (research area)
    and retrieves the text"""
    area = string.split(" | ")[2]
    return area.split(" ")[2]

def get_project_title(soup):
  """get project title from soup"""
    section = get_project_details_soup(soup)
    title = section.find("div", {"class": "list_title"}).text # customize this search term
    return title

def get_project_abstract(soup):
  """get project abstract from soup"""
    section = get_project_details_soup(soup)
    abstract = section.find("div", {"class": "list_text"}).text # customize this search term
    abstract = " ".join(abstract.split())
    return abstract


#for the event webpage, I created a modified "main_script.py" to get events.
#leaving this here for your reference.
def get_event(soup):
  """on event page, find the event details, output a dictionary of name, title, date"""
    title = soup.find_all("h4", {"class": "list_title"}) # customize this search term
    name = soup.find_all("div", {"class": "list_subtitle"}) # customize this search term
    date = soup.find_all("div", {"class": "list_date"}) # customize this search term
    event_dict = []
    for n in range(len(name)): # create list of dictionaries
        dict = {
            "name": name[n].text.title().split(" (")[0].strip(),
            "title": title[n].text,
            "date": date[n].text
        }
        event_dict.append(dict)
    return event_dict

## Creating md files


def create_md_file_project(name, person_url, project):
    """output: project md file"""
    filename_project = "%s-%s.md" % (name, project[2]) # this will be the note file name
    project_path = "C:\\Users\\XXX\\XXX\\" + filename_project #designate where to put the folder, in this case it's the Obsidian vault
    with io.open(project_path, "w+", encoding="UTF8") as f:
        write_YAML_project(f, name, person_url, project)

def create_md_file_person(name, person_url, tag):
    """output: person md file """
    filename_person = "%s.md" % name # this will be the note file name
    person_path = "C:\\Users\\XXX\\XXX\\" + filename_person #designate where to put the folder, in this case it's the Obsidian vault
    
    # if file already exists, then only append
    # important when a person got a promotion and thus changed roles, the new role (designed by tag & a wikilink) will be appended to the pre-existing file
    if os.path.exists(person_path):
        with io.open(person_path, "a", encoding="UTF8") as f:
            f.write("\n\n" + "[[" + tag + "]]") # I created notes for high-level "roles" in the company and had them wiki-linked to the person note  
            f.write("\n\n#" + tag) #add tag
            
    # if file doesn't exist, create new file
    else:
        with io.open(person_path, "w+", encoding="UTF8") as f:
            write_YAML_person(f, name, person_url, tag)
    print("\n person created")

def write_YAML_person(f, name, person_url, tag):
    #YAML
    f.writelines(["---", "\ntype: person","\naliases: []"])
    f.write("\ncreate_date: " + datetime.today().strftime('%Y-%m-%d'))
    f.write("\nurl: " + person_url)
    f.write("\ntags: " + tag)
    f.writelines(["\n", "---", "\n"])

def write_YAML_project(f, name, person_url, project):
    """ write file into .md file for Obsidian to read"""
    #within YAML
    f.writelines(["---", "\ntype: project", "\naliases: []"])
    f.write("\ncreate_date: " + datetime.today().strftime('%Y-%m-%d'))
    f.write("\nurl: " + person_url)
    f.writelines(["\n", "---", "\n"])
    # under YAML
    f.write("\nname:: " + "[[" + name + "]]")
    f.write("\n\nmember_role:: " + project[0])
    f.write("\n\nproject_start_date:: " + project[1])
    f.write("\n\nproject_end_date:: " + project[2])
    f.write("\n\nresearch_area:: " + "[[" + project[3] + "]]")
    f.write("\n\ntitle:: " + project[4])
    f.write("\n\nabstract:: " + project[5])
    f.write("\n\n")
    
#for the event webpage, I created a modified "main_script.py" to get events.
#leaving this here for your reference.
    def create_md_file_event(title, name, date):
    filename_project = "event_%s.md" % (date[0:10])
    project_path = "C:\\Users\\XXX\\XXX\\XXX\\" + filename_project
    with io.open(project_path, "w+", encoding="UTF8") as f:
        #write YAML
        f.writelines(["---", "\n"])
        f.write("\ntags: tag1, tag2")
        f.write("\ntitle: " + "\"" + title + "\"")
        f.write("\ndate: " + date[0:10])
        f.write("\nmode: ") #hybrid, online, etc.
        f.write("\nattendance: ")
        f.writelines(["\n", "---", "\n"])
        #write below YAML
        f.write("\nname:: " + "[[" + name + "]]")
