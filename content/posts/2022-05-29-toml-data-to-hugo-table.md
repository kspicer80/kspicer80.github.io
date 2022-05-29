--- 
title: "Fetching Data from a TOML File into a HUGO Table"
date: 2022-05-29 17:51:00
draft: false
toc: false
tags:
  - digital humanities
  - TOML
  - HUGO shortcodes
  - turn of the screw
  - HUGO tables
  - word frequency counts
  - work stuff
  - python
  - python for digital humanities
---

Continuing to learn the whole HUGO ecosystem here, I figured I would try a little testing of some things. What if I had a bunch of data in a simple [.json](https://www.json.org/json-en.html) or [.toml](https://toml.io/en/) or [.yaml](https://yaml.org/) or whatever file and wanted to pull/fetch data from that file into one of my posts? I did have some data from [the last post](https://kspicer80.github.io/posts/2022-05-27-henry-james-turn-of-the-screw-data-analysis/) about Henry James's use of certain words that we used to generate some of the graphs. A little bit of fiddling around on the HUGO Discourse [site](https://discourse.gohugo.io/), which provides [a mountain of posts](https://discourse.gohugo.io/t/how-do-i-generate-a-table-from-data-bundle/20396) yielded some rather simple little [shortcodes](https://gohugo.io/content-management/shortcodes/) to fetch and pull data from another file stored in the ```data``` folder of this HUGO website. (Two other short writeups were quite helpful as well: [here](https://harrycresswell.com/writing/passing-data-to-templates-hugo/) and [here](https://zwbetz.com/create-an-html-table-from-a-toml-data-file-in-hugo/) and also [here](https://peterychuang.co.uk/tech/hugo-data-files/) and in this short YouTube [video](https://www.youtube.com/watch?v=zJjJuS7LgS8) from "Pragmatic Reviews").)

Assuming we had a .toml file that looked like the following, 

![.toml datafile screenshot](/images/imgforblogposts/post_14/toml_datafile_screenshot.png),

it's pretty simple to get that data fetched and into a table here in this post, like this:

{{< tomlTable "hj_prodigious_portentous_word_counts" >}}

What's nice about the solution provided by [Zachary Wade Betz](https://zwbetz.com) is that it's quite easy to add data to the file that then gets fed into the table in the post. So, I haven't looked at every single Henry James text—if there were more in the future, it would be easy enough to add those texts to a script and then let the computer take care of the rest, ultimately updating the table easily enough. 

More to come, no doubt ...