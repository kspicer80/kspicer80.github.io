---
title: "Interacting with the Canvas Live API"
date: 2023-1-13 00:06:12
draft: false
toc: false
tags:
  - json
  - python json library
  - python
  - jupyter
  - jupyter notebooks
  - Canvas LMS
  - Canvas Instructure
  - grading
---

In a previous post (["Automating Canvas Discussion Board Grading and Feedback"](https://kspicer80.github.io/posts/2022-07-15-automating-canvas-grading-and-feedback_22/)), I recounted some of the ways I've been using the [CanvasAPI python library](https://canvasapi.readthedocs.io/en/stable/) from [ucfopen](https://github.com/ucfopen/canvasapi) to help with responding to discussion board posts from students each week. I have had a couple of times when running the script shown in that post where something goes slightly awry: perhaps I have mistyped one of the student or assignment ids and the script runs into an error while iterating through the dataframe that contains all of the data I want to upload. There's no error handling in that script, so if I go and correct the mistake in the data file and then rerun the script, it now ends up reposting all of the data in the rows that it runs through before running into the line of code containing the snag. I opened up an ["issue"](https://github.com/ucfopen/canvasapi/issues/581) on ucfopen's [github](https://github.com/ucfopen/canvasapi), asking where I would go via the canvasapi library to determine if a particular submission has any comments already uploaded to it—this would be one way to handle the potential duplication of comments. I got a really nice response from IonMich (Ioannis Michaloliakos) for how to handle this. For some reason that I'm not quite sure I can account for, this response pushed me to wonder if I couldn't myself figure out how to just interact with the Canvas Live API itself, rather than going through the python wrapper provided via canvasapi. (I have used the [```requests``` library](https://requests.readthedocs.io/en/latest/) in python for other projects before, but I got to thinking if things might be easier to just utilize that library alone.) This launched me off to the [official documentation](https://canvas.instructure.com/doc/api/index.html) for Instructure's API.

Following the path laid out by IonMich's response, I wandered over to the [```Submissions``` endpoint](https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.bulk_update), zeroing in on the [method](https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.bulk_update) that will allow one to "Grade or comment on multiple submissions." Having found the method that would seem to do what I want to do, the next step was getting the data I wanted to upload in the correct form and structure. As detailed in the earlier, previously mentioned, post, I am still keeping the data to be uploaded to Canvas in a ```.json``` file that has been slightly altered:

![testing_json_file](/images/imgforblogposts/post_28/test_json_datafile.png)

Typical workflow will follow: library import, getting all the information we need to successfully query the API, etc.:

``` python
import json
import requests

URL = # Here we'll store the URL to the appropriate API endpoint: one can play around with the Canvas Live API [here](https://canvas.instructure.com/doc/api/live)—although one will need to alter this to utilize the base URL to one's own Canvas system—through the web ahead of time to test out whether you've got the correct endpoint, that it's returning the data one expects, etc.)
API_KEY = XXXXX # Here's where you insert your own unique API key 
course_number = XXXXXXX # This variable will the course_id number that has the assignments one wants to upload grades to/for 
```

So what we need to do first is to get our data from the ```.json``` file into a format that we can then appropriately pass to the "Request Parameters" of the API ([here](https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.bulk_update) again is the documentation about what these parameters should look like).

Given that I have data that looks like the screenshot above, we need to do a little tiny bit of reworking here—although certainly not much, all things considered. 

``` python
with open('responses_json_for_blog_post.json') as f:
  data = json.load(f)
```

As seasoned veterans know, the ```json.load``` returns us a Python [dictionary](https://www.geeksforgeeks.org/json-load-in-python/)—in our case it gives us a dictionary with a single key, ```"grade_data"```. The value for that key is itself a list of dictionaries:

![json_object_type_and_full_dict](/images/imgforblogposts/post_28/type_from_json_load_and_full_dict_image.png)

Now we just need to write a (very!) simple ```for loop``` that will let us extract out the necessary data to feed as parameters to the ```POST``` call:

``` python
dict_for_upload = {}

for i in range(len(data['grade_data'])):
    id = data['grade_data'][i]['student_id']
    score = data['grade_data'][i]['posted_grade']
    comment = data['grade_data'][i]['text_comment']
    dict_for_upload[f'grade_data[{id}][posted_grade]'] = f"{score}"
    dict_for_upload[f'grade_data[{id}][text_comment]'] = f"{comment}"

dict_for_upload
```

This results in something that looks like the following:

![dict_for_upload_image](/images/imgforblogposts/post_28/dict_for_upload.png)

Of course, we're shooting for something that looks like this: 

![instructure_official_docs_screenshot](/images/imgforblogposts/post_28/canvas_api_docs_screenshot.png)

Looks good! Now all we need to do is get everything set up properly for the [requests library](https://requests.readthedocs.io/en/latest/user/quickstart/#passing-parameters-in-urls).

As with so much here in this whole "computer science" realm, one can often get exactly what they want in a single line of code:

``` python
header_argument = {"Authorization": "Bearer " + API_KEY}
response = requests.post(URL, headers=header_argument, data=dict_for_upload)
```

Simple as that.

Of course, the big question here is which avenue to prefer taking here: going through the ucf canvasapi wrapper or just dealing directly with the Instructure API. Furthermore, there is still the issue of how might want to do deal with the concern that started this investigation off in the first place—namely, making sure no duplicate comments get uploaded if the script fails somewhere along the line in the whole upload process. Of course, writing a function with the plan to use it directly with the API (not through the wrapper) seems easy enough. When you query the Instructure API to look at the data that contains whether or not a comment on a submission has been entered, one gets a response that has a key, ```submission_comments```, containing a list with a dictionary that has a sub-key, ```comment```. It's easy to check the response, if it gives us an empty list, then there's no existing comment, otherwise it returns the actual comment already posted, along with other data, of course. Again, once we know where that information is, one can simply write some code to check it before uploading the comments—thus avoiding the possibility of duplicating comments. Something not all that sophisticated would seem to do the trick (one would just need to make sure they were hitting the right data—```submission_comment[0]['comment']``` is the right spot to look and is what should be passed to the function below):

``` python
def check_if_comments_already_exist(submission_comments_field):
    if submission_comments_field == []:
        updated = False
    else:
        updated = True
    print(updated)
```

Then we just incorporate that into the for loop so we get no duplicate comments added to each submission. We also need to make sure that we query the correct API endpoint/address to get the information about the assignment—once again, the official Instructure API docs help out here:

![querying_correct_address](/images/imgforblogposts/post_28/get_request_that_returns_submission_comment_data.png)

It strikes me as perhaps much easier to deal directly with the Instructure API rather than going through the wrapper. I suppose it's difficult to give some principled reason for preferring one over the other. I suppose one could invoke something like "proximity" and "closeness" in terms of an idea like "mediation." Best to reduce the number of mediations in between where one is and where one wants to get to ... something more to ponder and ruminate upon, to be sure. 

(All code and sample testing data for this post is available in the following [repository](https://github.com/kspicer80/canvas_api_for_grading_and_commenting).)