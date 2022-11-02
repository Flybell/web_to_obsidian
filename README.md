# Web to Obsidian
A script that scrapes an html/xml page to extract markdown text for Obsidian


## Introduction 

This Python 3 web scraping script consists of two components: 
(1) using Beautifulsoup to comb the web and extract relevant information, 
(2) writing the info into .MD files that can be read by Obsidian, specifically by the dataview plugin.

The goal of this specific script is to comb through a public html-based database and link them together in Obsidian. For privacy purposes, the specific website will not be revealed and the code will contain dummy links. The scripts here are thus instructive demonstrations, not meant to be fully operational out of the box. The goal is to help you get started with your own project. 

I will first introduce the logic of the procedure, then explain the specifics of the script itself.

## The Logic of the Script

### PART 1: USING BEAUTIFULSOUP TO SCRAPE THE WEB

"Beautiful Soup is a Python package for parsing HTML and XML documents." 
Think of it as a bot that pretends to be a human clicking through a website on a specific browser that you specify. 

It generates a "soup" from a html/xml page, an object that can be operated over by functions such as "find". For instance, if I'm interested in extracting a list of animal names from the html webpage of my local zoo, my script would create a "soup" object that page, return a list of the html elements (e.g., div, a, h1,) that contain the names with the "find_all" function, then extract the text therein.

To know where the data's at, you need to actually look at the source html code. Right click on the website and examine the source code. Find thei nfo you need, identify the html container around it, then put that in your code. The bot will just go through the site and extract all the info from those containers.  

### PART 2: WRITING .MD FILES FOR OBSIDIAN

Once you've extracted all the info you need and put them in variables, you can now bave python write them line by line into a .md file that lives in the folder of your Obsidian file. The first few lines define the YAML heading. YAML & in-line formatting were designed so that dataview can read the code.

## The target website of my script & samples

To simplify things, the dummy target website dummy.site.com has a list of members. Imagine that when you click on each member's link, you will see a list of projects the person is leading. I want to create, in my local Obsidian database, a note for each person and a note for each project, with each project containing a wikilink to the person. 

Since I want to use dataview to analyze the notes I've created, I format the files to contain YAML metadata and also inline variables for dataview underneath the YAML heading. Why both? It is important to keep in mind that YAML is invalidated when there are ":" symbols in your text. Therefore, I put longer texts (titles, abstracts, etc., between YAML). 

*Sample person YAML:

Note Title: First Last

---
type: person
aliases: []
create_date: 2022-11-01
url:
---

*Sample project YAML: 

Note Title: 

---
type: project
tags: tag
aliases: []
create_date: 2022-11-01
url:
---

name:: [[First Last]]

project_role:: Visitor
project_start_date:: 2019-09-02
project_end_date:: 2019-09-07
research_area:: [[Other]]
title:: XYZ
abstract:: ABC
