# Web to Obsidian
A Python 3 script that scrapes an html/xml page then creates markdown files for Obsidian & the dataview plugin


## Introduction 

This Python 3 web scraping script consists of two components: 
(1) using Beautifulsoup to comb the web and extract relevant information, 
(2) writing the info into .MD files that can be read by Obsidian, specifically by the dataview plugin.

It combs through a public html-based database (a webpage with a list of links), creat markdown notes for each item. As it writes Obsidian wikilinks into the files, the notes are now connected through wikilinks and backlinks. For privacy purposes, the specific website I've been working on will not be revealed and the code will contain dummy links. As parts of the code are highly specific to the target website, the scripts here are only meant to be instructive demonstrations. They are not operational out of the box. The goal is to help you get started with your own project. 

I will first introduce the logic of the procedure, then explain the specifics of the script itself.

## The Logic of the Script

### PART 1: USING BEAUTIFULSOUP TO SCRAPE THE WEB

"Beautiful Soup is a Python package for parsing HTML and XML documents." 
Think of it as a bot that pretends to be a human clicking through a website on a specific browser that you specify. 

*What, how?*

By feeding it a url, it generates a so-called "soup" object from the html/xml page, an object that can be operated over by Beautifulsoup functions such as "find". For instance, if I'm interested in extracting a list of animal names from the html webpage of my local zoo, my script would create a "soup" object of that page, return a list with the "find_all" function of the html elements (e.g., div, a, h1,) that contain the names, then extract the text therein. 

What's cool though, is that the script can also locate a url, *feed the url back into itself*, and then extract more data from that url. This is the beauty of automation. To use the zoo example, if the website is not a list of names but a list of links to different animal pages, I can write a script that identifies and retrieves all of these links, then automatically processes these links one by one to create more soup objects to work with. 

With this technique, I can ask the script to look for the url of the "next page" button and move on to scrape the next page. And the next. And the next. The main_script.py included here is a script that does exactly this, flipping through pages until there is no "next page" button. Of course, I've also created a similar script for single pages for my own purposes. For you to do the same, just remove the looping code in this script and thus modify it to scrape a single page.

*Wow, so Beautifulsoup just magically knows where the text is at?* 

Uh... I wish. YOU need to know this before writing the code! To know where the data's at, you need to actually look at the source html code. Right click on the website and examine the source code. Find the info you need, identify the html container around it, then put that html element in your code. The bot will just go through the site and extract all the info from those html containers.  

Note: read the BeautifulSoup documentation, especially the part that explains how to use "find" and "find_all." It's actually a bit difficult to get what you're looking for the first try. You need to know the syntax of these two functions well. Beautiful soup is much more powerful than this (e.g., it can move up and down html hierarchies like a spider), but I don't know much beyond these two functions!

### PART 2: WRITING .MD FILES FOR OBSIDIAN

Once you've extracted all the info you need and put them in variables, you can now write them line by line into a .md file that lives in the folder of your Obsidian vault. The first few lines define the YAML heading. YAML & in-line formatting were designed so that dataview can read the code. 

Since I want to use the powerful dataview community plugin to analyze the notes I've created, I formatted the files to contain YAML metadata 

```
---
name: First Last
role: manager
---
```

and also inline variables underneath the YAML heading.

```
title:: The God of Winds
```
 
Why both? It is important to keep in mind that YAML is invalidated when there are ":" symbols in your text. Therefore, I put longer texts (titles, abstracts, etc., under the YAML just in case there's a : in there.). Read the Dataview documentation to learn more.

## The target website of my script & samples

To simplify things, here's the use case. A dummy target website dummy.site.com has a list of members profile links. Imagine that when you click on each member's link, you will see a list of links to the projects the person is leading. I want to create, in my local Obsidian database, a note for each person and a note for each project, with each project containing a wikilink that goes back to the person. Then, when I am looking at the person file, there will be a backlink to all the projects it's associated with. 

See sample People (First Last.md) and Project (First Last-2022-10-10.md) files for examples of the final output. 

## Dataview examples

In this dataview, I look at the number of notes per research area. 

```dataview
TABLE without ID area, length(rows) as count
where research_area
group by research_area
sort length(rows) DESC
```

In this dataview, I look at the people who are still employed. 

```dataview
TABLE without id
	file.link as Project,
	name as NAME,
	project_start_date as START, 
	project_end_date as END, 
	member_role as role, 
	research_area as area 
WHERE type = "project" and project_end_date >= date(today)
sort project_end_date desc
```

In this dataview, I look at the number of projects versus number of people 

```dataview
TABLE without ID type, length(rows) as count
where type
group by type
sort length(rows) DESC
```


---

Many thanks to r/Obsidian for pushing me to publish this repo. 
https://www.reddit.com/r/ObsidianMD/comments/yjzake/used_obsidian_to_recreate_a_local_copy_of_a/
