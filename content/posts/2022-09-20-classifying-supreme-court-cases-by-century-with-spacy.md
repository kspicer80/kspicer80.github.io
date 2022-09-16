---
title: "Training a SpaCy Text Classifier on Supreme Court Opinions"
date: 2022-09-20 00:01:00
draft: true
toc: false
images:
tags:
  - python
  - spaCy
  - text classification
  - digital humanities
  - dh
  - pandas
  - machine learning
  - data wrangling
  - data cleaning
  - json data
---

Continuing some work with the Supreme Court databases I've been fiddling around with lately, I was wondering if I could get a machine learning model to be able to correctly identify and classify a Supreme Court opinion by the decade in which it was written. So let's grab some data and see what we can do!

There is a really wonderful [github repo](https://github.com/brianwc/bulk_scotus) that contains the .json files of all the Supreme Court cases made available through the [CourtListener API](https://www.courtlistener.com/api/). I forked this repo and then proceeded to do some basic data gathering/wrangling (all the code for this project is in my repo [here](https://github.com/kspicer80/ussc_text_classification)) First, our libraries:

``` python
import json
import os
from pathlib import Path
import pandas as pd
import spacy
from spacy.util import minibatch
from spacy.training.example import Example
nlp = spacy.blank('en')
```

All of the files are split up into folders by the century and then with subfolders by year. We can thus write a simple function to grab all these files and get them—as usual—into a nice dataframe:

``` python
def read_jsons_into_dataframe(directory):
    temp_list_of_dfs = []
    directory = directory
    pathlist = Path(directory).rglob('*.json')
    for path in pathlist:
        with open(path) as f:
            json_data = pd.json_normalize(json.loads(f.read()))
        temp_list_of_dfs.append(json_data)
    combined_df = pd.concat(temp_list_of_dfs, ignore_index=True)
    return(combined_df)
```
Simple enough, we can then just call this function on all of the different century-named folders:

``` python
df_1700s = read_jsons_into_dataframe('1700s)
```

After we do that for all four our centuries, we can just merge them all into one dataframe (oh—and after each of the four were read in we added a ```label``` column that had the century in it):

``` python
merged_df = pd.concat([df_1700s, df_1800s, df_1900s, df_2000s])
```

This gives us a nice dataframe with a shape of ```(63347, 42)```. Each of the CourtListener files has columns for the ```plain_text``` of the case along with other columns that give us the same information in HTML: ```html``` and ```html_with_citations```. We also need to create a ```label``` column that will store the century the case was written.

After some text cleaning using some of standard data cleaning functions, we could do a little teeny-tiny bit of exploratory EDA on our cleaned-up data:

![Figure 1](/images/imgforblogposts/post_25/figure_1.png)

![Figure 2](/images/imgforblogposts/post_25/figure_2_value_counts_of_our_labels.png)

Now, we do have a really sizeable data imbalance—we have a ton more examples from the 1800s-2000s than we do from the 1700s. That's something we'll want to keep in mind and I might return to ways one might want to explicitly handle such a situation in another post sometime. For now, we'll just continue on and see if we don't want to circle-back to that issue.

So now we need to let spaCy know that we want to add another pipe (specifically the [TextCategorizer pipeline](https://spacy.io/api/textcategorizer)) to our blank model with ```textcat = nlp.add_pipe('textcat')``` along with the labels that the model will also need:

``` python
textcat = nlp.add_pipe('textcat')
textcat.add_label("1700")
textcat.add_label("1800")
textcat.add_label("1900")
textcat.add_label("2000")
```

Then we can read in our cleaned-up file and separate out the texts and the labels, making sure that we pass the proper "cats" to the the model:

``` python
train_texts = df['cleaned_html'].values
train_labels = [{"cats": {"1700": label == 1700,
                        "1800": label==1800,
                        "1900": label==1900,
                        "2000": label==2000}} for label in df['label']]
```

We next zip together all our texts and labels into tuples: ```train_data = list(zip(train_texts, train_labels))```. We can next write another really simple function to train our model:

``` python
def train(model, train_data, optimizer, batch_size=8):
    losses = {}
    random.seed(1)
    random.shuffle(train_data)

    for batch in minibatch(train_data, size=batch_size):
        for text, labels in batch:
            doc = nlp.make_doc(text)
            example = Example.from_dict(doc, labels)
            nlp.update([example], sgd=optimizer, losses = losses)

    return losses
  ```

With the training function written, we can start the model learning!

``` python
spacy.util.fix_random_seed(1)
random.seed(1)

optimizer = nlp.begin_training()
losses = train(nlp, train_data, optimizer)
print(losses['textcat'])
```

  Of course, if one wants to save the trained model, that's simply enough too with spaCy: ```nlp.to_disk('saved_spacy_model')```.

Let's see what happens when we feed it a text the model hasn't seen before. Given that the [bulk_scotus repo](https://github.com/brianwc/bulk_scotus) only goes up to 2015, why don't we give it a much more recent opinion? (The two recent texts are in the ```texts_for_testing``` for the main repo.) We'll read 'em and see what the model thinks:

``` python
with open('./texts_for_testing/test_text.json', encoding="utf-8") as f:
    test_text = json.load(f)

opinion_of_text = test_text['plain_text']
spacy_doc = nlp(opinion_of_text)
spacy_doc.cats
```

``` python
{'1700': 2.4846047381288372e-05,
 '1800': 6.585433993677725e-07,
 '1900': 4.132466528972145e-06,
 '2000': 0.9999703168869019}
```

The model seems pretty sure it's from the 2000s. What about another one?

``` python
with open('./texts_for_testing/test_text_1.json', encoding='utf-8') as f:
    test_text_1 = json.load(f)

opinion_of_text_01 = test_text_1['plain_text']
spacy_doc_01 = nlp(opinion_of_text_01)
spacy_doc_01.cats
```

Again, pretty sure:

``` python
{'1700': 3.817029937636107e-05,
 '1800': 5.630177923876545e-08,
 '1900': 2.2707074549543904e-06,
 '2000': 0.9999594688415527}
```

These numbers seem really high, so it gets one wondering quite a bit here.















===================================================================



Main notebook for spaCy training is [here](https://github.com/kspicer80/bulk_scotus/blob/master/spacy_training_script_notebook.ipynb).