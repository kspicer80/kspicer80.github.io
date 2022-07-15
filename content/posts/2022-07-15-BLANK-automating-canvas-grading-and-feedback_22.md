---
title: "Automating Canvas Discussion Board Grading and Feedback"
date: 2022-07-15 00:01:00
draft: false
toc: false
images:
tags:
  - digital humanities
  - canvas instructure
  - discussion boards
  - online learning
  - lms
  - automating grading
  - automating student feedback
  - online discussion boards
  - json
  - xml
  - work stuff
  - python
  - python for digital humanities
  - pandas
---

If you're like me and you do a lot of teaching online (I know, I know, who among us _don't_ fit into that category today?) with courses that are really "Discussion Board"-heavy, you know that responding to students through [Canvas's LMS](https://www.instructure.com/) is, on its face, a bit of a bear. I have a tendency to produce some rather extensive comments to student posts each and every week. As Canvas veterans know all too well, there are all kinds of things about Canvas that are frighteningly "user-hostile," as [Robby Burns puts it](http://www.robbyburns.com/blog/eliminating-canvas-stress-by-writing-content-in-markdown). Just for myself, I would like to add just another thing that, as of late, has bugged me greatly. If one writes responses to student posts in Markdown (Burns doesn't explicitly suggest this, but I think of it as a nice extension of this line of thinking ), it's easy to get the Rich Context Editor in the discussion board area to take the Markdown without much of a  problem. If I want to, instead, respond directly not on the discussion board itself but in the "Comments" area of the SpeedGrader, it won't let me input any Markdown there, only plain text—heaven forbid someone wanted to put a link in the comments, one has to copy out the whole URL and cannot utilize the very simple syntax Markdown has for wrapping the link text in brackets, ```[]```, followed by the full link in parentheses after it, ```()```. Sigh. But I digress! Anyways, I wanted to find some way to be able to compose all of my responses to individual students in a separate file on my computer and not have to either copy and paste every single comment into the SpeedGrader for each and every student or, even worse, just use the native "Comments" box in SpeedGrader. Well, let's find a better way. I've gone through a couple of iterations here with streamlining this whole grading workflow—and I thought I could post a little work-up here of my explorations.

The main library we're going to use here is [a fantastic little wrapper](https://github.com/ucfopen/canvasapi) (available through [PIP](https://pypi.org/project/canvasapi/)) that allows one to interact with [Canvas's own API](https://canvasapi.readthedocs.io/en/stable/index.html) through Python. Before we get to the script that I use to quickly upload every single response for each individual student, we need to figure out how we want to store and structure the data we're going to be uploading. In the first iteration, I just put everything into a simple XML file that looked like this:

``` xml
<?xml version="1.0" encoding="UTF-8"?>
<data>
  <student name="Hary Potter">
    <assignment_id>1111111</assignment_id>
    <student_id>0000000</student_id>
    <text_comments_to_upload>Hey, Harry, thanks so much for the post this week. Blargh blargh blargh! Have a great week this next week!
    <text_comments_to_upload/>
    <score>10<score/>
  </student>
  <student name="Hermione Granger">
    <assignment_id>1111111</assignment_id>
    <student_id>2222222</student_id>
    <text_comments_to_upload>Hello, Hermione, thanks so much for the incredibly exemplary post this week. Keep up the good work!</text_comments_to_upload>
    <score>10</score>
  </student>
</data>
```

Simple enough, no? For some reason here this summer I thought that it was a tad-bit overkill to put it in an .xml format, which, [as many have noted](https://www.toptal.com/web/json-vs-xml-part-1#:~:text=JSON%20is%20faster%20because%20it,more%20than%20just%20data%20interchange), is better-suited for far more complex applications and situations than what I'm up to here. The data I'm storing is terribly simple here—just text—so it seemed to me like the .json format might be even better, easier, smoother ... it also strikes me as much cleaner, no ```<>``` and no tags, just simple quotation marks, semicolons, commas, etc. Both file formats work perfectly well, but I found myself preferring the .json here recently, though I'm not exactly sure why. 

``` json
{"data": 
    [
        {
            "student_name": "Harry Potter",
            "course_number": "9999999",
            "student_id": "0000000",
            "assignment_id": "1111111",
            "text_comments_to_upload": "Hey, Harry, thanks so much for the post this week. Blargh blargh blargh! Have a great week this next week!",
            "score": "10"
        },
        {  
            "student_name": "Hermione Granger",
            "course_number": "9999999",
            "student_id": "2222222",
            "assignment_id": "1111111",
            "text_comments_to_upload": "Hello, Hermione, thanks so much for the incredibly exemplary post this week. Keep up the good work!",
            "score": "10"
        },
    ]
}
```

So the remaining steps in the procedure so far are really easy. We put all of the data we want to upload to our Canvas shell for students in the very same file. The other information you need in order to get this to work (e.g. the "course_number" and the "assignment_id" are available in the URL when you navigate to the actual assignment in question's SpeedGrader) is also easy enough to grab. So, for example, the URL for Harry's submission above will look something like this (one would just change-up the main address for one's own particular school/institution):

``` html
https://learn.stfrancis.edu/courses/9999999/gradebook/speed_grader?assignment_id=1111111&student_id=00000000
``` 

After we have all our responses to all of our students' submissions ready to go and in the same file, we can write the script that will upload everything for us to the LMS shell with just a single click of a button. (Honestly, I'm still amazed that one can get all of this so simplified and streamlined with just a few lines of code—it's fantastic.) Before we feed data through the API, we need to obtain an API key (the main documentation for this via Instructure is [here](https://canvas.instructure.com/doc/api/file.oauth.html) and there is man even more simplified version available [here](https://kb.iu.edu/d/aaja)). Once we have our API Key we can get to importing our libraries and code some stuff!

``` python
from canvasapi import Canvas
import pandas as pd
from pathlib import Path
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 00)
```

With our necessary libraries all imported and tailored how we want them, we can set up some variables to store the URL of the Canvas shell, the API Key, etc.:

``` python
API_URL = 'https://learn.stfrancis.edu'
API_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX' # Here's where your own API Key goes ...
course_number = 9999999 # Change this up for your own particular course_id number

filename_path = Path() # Pass the path to the .json file with all our stored data/responses/grades/etc.
```

Now we can instantiate a Canvas object with the canvasapi library—and call the ```get_course()``` function which will allow us to interact with the individual course. 

``` python
canvas = Canvas(API_URL, API_KEY)
course = canvas.get_course(course_number)
```

The canvasapi library has all kinds of fantastic functions—most of which I haven't even really played around with yet. Let's say you wanted to get all of the ids of all the students in a section (those numbers would go in the ```student_id``` of our .json file, by the way)—simple enough:

``` python
students_in_course = course.get_users(enrollment_type=['student'])
for user in students_in_course:
    print(user)
```

Want all the individual assignment_id numbers? Again, too easy:

``` python
all_assignments = course.get_assignments()
for assignment in all_assignments:
    print(assignment)
```

Okay, so now we want the real meat here, the process where we write some code to iterate through all of the data in the .json file and then post the data in the appropriate places in the Canvas shell. Again, just a few lines of pandas syntax in a very simple ```for loop``` gets us exactly what we want. First we read the .json file into a dataframe (you need not do it this way—of course, you could just read the .json data into a [python dictionary](https://docs.python.org/3/tutorial/datastructures.html#dictionaries)—```dict()```—and then iterate through all the keys and values in that)—:

``` python
df = pd.read_json(filename_path, orient='split')

for index, row in df.iterrows():
    assignment = course.get_assignment(row['assignment_id'])
    user_submission = assignment.get_submission(row['student_id'])
    user_submission.edit(submission=({'posted_grade': row['score']}))
    user_submission.edit(comment={'text_comment': row['text_comments_to_upload']})
```

Done and done—all of the individualized responses and grades for each and every student will be uploaded to Canvas, all in just a few lines of code. 

There are, to be sure, some improvements that I can imagine someone wanting. For instance, the code above assumes that you do not have any rubrics attached to any of the assignments. It would be nice, if one did like to use the Canvas rubrics feature, to be able to structure the .json file so that you could score each of the criteria that are present in a rubric (this endpoint of the Instructure API has not been implemented yet, [but I did suggest it](https://github.com/ucfopen/canvasapi/issues/538)). As [Brian noted over on the canvasapi repo]((https://github.com/ucfopen/canvasapi/discussions/537)), there is a way to do this going straight through Instructure's API, but I haven't had a chance to fiddle and tinker with that just yet. 

I find that this whole process has really streamlined things for me—I hated having to copy and paste; I also love being able to keep all of my responses to all of the students' posts in the very same file; it definitely makes it easier for me to remember exactly what I wrote to other students: I can thus weave together different responses, reuse some boilerplate when necessary (I usually include a similar "greeting" or salutation to each student before actually responding to their post, so it's easy to copy and paste from one entry to another, etc.) I find the whole things allows me to individualize everything still for students while also reducing my workflow with things that used to take a pretty good deal of time ... 

All in all, a nice little project that will continue to save me a great deal of time in the future, that's for sure—and I look forward to seeing what I can do with feeding data directly into the rubric for an assignment (especially when one checks that little box that says something like "Use Rubric for Assignment Grading," which would mean we could remove the ```score``` part of the .json file above and then create separate lines for each of the individual criteria of the rubric).