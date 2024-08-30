---
title: "Recent Canvas Changes to Threaded Discussion Board Posts"
date: 2024-08-29 10:21:29 
draft: fakse
toc: false
tags:
  - python
  - API
---

### Introductory Remarks

Recently, the Canvas LMS put through a change that no doubt will affect many of us.  I received the following from my current institution's "Canvas Liason":

>Hello Faculty,
>
>On August 14th, Canvas did an update to the new design for Discussions.  In >the old design, you had the option for a threaded discussion.  In the new >design, it was not there.  When Canvas did the update, they set the ‘Disallow >threaded replies’ to on (checked).  Not all discussions changed as it depended >if you had the threaded discussion checked on the old design or not.  If you >were using the new design discussions, it is set to checked.

And then we were given the [Canvas Community Link](https://community.canvaslms.com/t5/The-Product-Blog/Disallow-Threaded-Replies-option-in-Discussions/ba-p/612073) for this change. 

The thought of manually unchecking the box to allow threaded discussions filled me with dread---so I wrote some code to check how many of my courses were affected by this.

```python
import requests

API_KEY = UR_API_KEY_FOR_CANVAS_GOES_HERE
header_argument = {"Authorization": "Bearer " + API_KEY}

# Define the dictionary with course IDs and names
COURSE_IDS_AND_NAMES = {
    "ENGL_200": CANVAS_COURSE_ID_FOR_Y0UR_COURSE_GOES_HERE,
    "ENGL_318": CANVAS_COURSE_ID_FOR_Y0UR_COURSE_GOES_HERE,
    "ENGL_510": CANVAS_COURSE_ID_FOR_Y0UR_COURSE_GOES_HERE
}

# Base URL with placeholder for course_id_number
base_url = "https://stfrancis.instructure.com:443/api/v1/courses/{course_id_number}/discussion_topics"

# List to store the data for each course
course_data_list = []

# Your API token
api_token = API_KEY

# Headers for the request
headers = {
    "Authorization": f"Bearer {api_token}"
}

# Iterate over the dictionary and format the URL
for course_name, course_id_number in COURSE_IDS_AND_NAMES.items():
    formatted_url = base_url.format(course_id_number=course_id_number)
    print(f"URL for {course_name}: {formatted_url}")
    
    # Make the API call with headers
    response = requests.get(formatted_url, headers=headers)
    
    # Check if the request was successful
    if response.status_code == 200:
        course_data = {
            "course_name": course_name,
            "course_id": course_id_number,
            "data": response.json()
        }
        course_data_list.append(course_data)
        print(f"Data for {course_name} stored successfully.")
    else:
        print(f"Failed to fetch data for {course_name}, status code: {response.status_code}")

# Print the collected data
print(course_data_list)

# List to store courses that do not meet the criterion
non_threaded_courses = []

# Check each course data for discussion_type
for course_data in course_data_list:
    course_name = course_data["course_name"]
    discussions = course_data["data"]
    
    for discussion in discussions:
        if discussion.get("discussion_type") != "threaded":
            non_threaded_courses.append(course_data)
            break  # No need to check further discussions for this course

# Print the courses that do not meet the criterion
print("Courses with non-threaded discussions:")
for course in non_threaded_courses:
    print(course["course_name"])
```

This should give you the course's that have the "threaded discussions disallowed" checked.  I'll upload some code soon to have it so you can instantly changed to the allowance of threaded discussions.

More to come, as always!