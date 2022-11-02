"""The main script"""
""" This script takes the first page of as input,
scrapes it, then scrapes all the remaining pages,
then creates .md files with YAML that is readable for Obsidian.
It is then stored in the Obsidian vault XXX.
"""

#import python packages
import re #regular expression
import io #for UTF8 processing
from bs4 import BeautifulSoup #HTML parser library
import glob #to create file name from variable

#import functions from the "code" script
from code import *

#download all members!
all_url = "https://dummy.url.com" #first page of member directory, contains a list of members with links to their profiles
next_url = all_url
tag = "tag_name"

#this script will collect all links on a page 
#then find the "next page" button, get the url of the next page
#and start over to collect all links on the next page 
#it will end when there is no "next page" button
while next_url: #check whether there's a next page button
    #create soup from page
    soup_all = make_request(next_url)
    #get all links on page
    if soup_all: #check if soup has been successfully created
        print("retrieved links on page") #console confirmation text
        member_urls = get_members(soup_all) #a list of links to member profiles

    # process each member
    for person_url in member_urls:
        soup_person = make_request(person_url) #get soup of that person's profile
        if soup_person: #check if soup has been successfully created
            print("\n------------\nfound a person") #console confirmation text
            name = get_name(soup_person) # get name
            print(name) #console confirmation text
            project_urls = get_project_url(soup_person) # get list of project urls of this person
            create_md_file_person(name, person_url, tag) # create person .md file

        # get project info from project url, there may be more than one project per person
        for url in project_urls:
              soup_project = make_request(url)
              if soup_project:
                  print("\nfound their project!") #console confirmation text
                  
                  # get project metadata string
                  string = get_fellow_string(soup_project)

                  #create profile for each project
                  proj_profile = []
                  proj_profile.append(get_fellowship_type(string)) #0
                  proj_profile.append(get_fellowship_startdate(string)) #1
                  proj_profile.append(get_fellowship_enddate(string)) #2
                  proj_profile.append(get_research_area(string)) #3
                  proj_profile.append(get_project_title(soup_project)) #4
                  proj_profile.append(get_project_abstract(soup_project)) #5
                  print("\nproject profile created for " + name) #console confirmation text

                  create_md_file_project(name, person_url, proj_profile) #create project files

    #get next page
    next_url = get_next_page(soup_all)

print ("\n\nDownload complete") #console confirmation text
