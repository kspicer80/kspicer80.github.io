--- 
title: .JSON Dump Testing
date: 2022-05-27
draft: false
---

Here's some dumped .json data:

{{ range $.Site.Data.hj_target_counts }}
	{{ partial "hj_counts.html" . }}
{{ end }}


