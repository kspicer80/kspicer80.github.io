---
title: "Let's Do Some Real World HTML Table Parsing with Beautiful Soup!"
date: 2022-05-25 00:05:00
draft: true
toc: false
images:
tags:
  - digital humanities
  - digital rhetoric
  - beautiful soup
  - bs4
  - html tables
  - html table parsing
  - html parsing
  - work stuff
  - law school rankings
  - real world applications
  - real world implementations
---

Given that I'm continuing to chronicle my DH journeys here, I figured I'd showcase a little bit of my utilization of scraping data from a website with Beautiful Soup (docs are [here](https://beautiful-soup-4.readthedocs.io/en/latest/)). 

Doing some research for a favorite student of mine, I've been wandering around websites devoted to law school. One website [here](https://blog.powerscore.com/lsat/top-100-law-school-application-deadlines-2022-edition/) has a really fantastic little table on the page that has everything one could want—especially if one is a little behind on deadlines and trying to catch up a bit (i.e. figuring out which schools will allow students to start in the Spring or Summer semesters [for an answer to that query, head over [here](https://blog.powerscore.com/lsat/bid-153623-which-law-schools-offer-spring-and-summer-starts/)]). Now, of course, one could just do the simple ol' copy and paste of the table, but we all know how ornery that can be when one tries to paste it into Word or some other program and having to deal with all the formatting shenanigans. Instead, why don't we write a little code to get the thing into a nice format, maybe a simple Markdown table since the .md file extension seems to be my new best friend since getting into all this fantastically cool DH stuff.

First things we had a look at the html for the page, using the "View Page Source" function after right-clicking on the page. Looking for a ```div class=``` equal to ```<table>```, sure, enough, here it is:




