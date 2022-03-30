---
title: "K-Nearest Neighbors Classification Fun! ... with some Literary Texts by Willa Cather and Sarah Orne Jewett"
date:
draft: true
toc: false
images:
tags:
  - machine learning
  - willa cather
  - sarah orne jewett
  - digital humanities
  - python for the digital humanities
  - Python
  - k-nearest neighbors
  - keras
  - tensorflow
  - literary style
  - word frequency
  - word frequencies
  - sklearn
---

In my DH journey, the work of [Dr. William Mattingly](https://pythonhumanities.com/python-for-dh-course/) has been something of a constant companion and guide.

His video laying out the steps for a ["Binary Data Classification"](https://www.youtube.com/watch?v=tPgQH5UTC9k) were clear quite clarifying for me in all kinds of ways. The classifier's job in this video was to see if it could tell the difference between the work of Oscar Wilde and Dan Brown. What if we tried a different pair of authors/texts? As I offhandedly mentioned in my previous [post](https://kspicer80.github.io/posts/2022-03-29-vector-space-models-and-shakespeare/), finding texts in the public domain (like Shakespeare's for example), saves one quite a bit of time wrangling things together. I also, for some, reason, have found myself going back to some of the works of Willa Cather (admittedly, she's definitely not in my wheelhouse/field of study by any stretch of the imagination) and was wondering how a machine learning classifier might perform when looking at Cather's texts alongside those of one of her key influences, Sarah Orne Jewett:

{{< figure src="/static/images/imgforblogposts/post_10/o_pioneers_1913_dedication_to_jewett.png" caption="Original Image of Cather's Dedication of _O Pioneers_ to Jewett, courtesy of UNL's fantastic _Willa Cather Archive_ [here](https://cather.unl.edu/writings/books/0017)> " >}}

Why not?—I figured I could tinker around a bit to see what's possible. Project Gutenberg has a number of texts by both [Cather](https://www.gutenberg.org/ebooks/author/22) and [Jewett](https://www.gutenberg.org/ebooks/author/202)—and the UNL _Willa Cather Archive_ has a good number of her texts [formatted in .xml](https://cather.unl.edu/writings/books). I grabbed as many of the texts from these two sources. Since the Gutenberg texts come with the typical boilerplate material at the start and end of the plain text file I pulled out a nice little script from ["C-W" on GitHub](https://github.com/c-w/gutenberg) that had a nice list of phrases used in the boilerplate material; [the simple script](https://github.com/kspicer80/authorship_attribution_studies/blob/main/cather_jewett/strip_headers_and_footers.py) would strip all the boilerplate when the text files get read in. 

The major steps here for this tinkering is to read in all the plain text files, split everything up by sentences, write a function that will "pad" the data so that any sentences that are less than a specific length ultimately get a ```?``` added to the sentence to bring it's length of the already specified ```max_length``` of each sentence. This is due to the way that the keras library likes to have data fed to it. That function looks as follows:

``` python
def padding_data(sentences, index, maxlen=25):
    new_sentences = []
    for sentence in sentences:
        sentence = text_to_word_sequence(sentence)
        new_sentence = []
        words = []
        for word in sentence:
            try:
                word = index[word]
            except:
                KeyError
                word = 0
            words.append(word)
        new_sentence.append(words)
        new_sentence = preprocessing.sequence.pad_sequences(new_sentence, maxlen=maxlen, padding='post')
        new_sentences.append(new_sentence[0])
    return(new_sentences)
  ```
  
Next is a function that will index each and every token within the text file and append it to a .json file that will store every token and its associated index number:

``` python
def create_index(texts, filename):
    words = texts.split()
    tokenizer = Tokenizer(num_words = 100000)
    tokenizer.fit_on_texts(words)
    sequences = tokenizer.texts_to_sequences(words)
    word_index = tokenizer.word_index
    print(f"Found {len(word_index)} unique words.")
    with open(filename, "w") as f:
        json.dump(word_index, f, indent=4)
``` 

In the tutorial, Mattingly uses a max_length of 25 words; a quick graph of the average sentence lengths for each of our author's texts would suggest that number is probably not a bad choice for our dataset:

![Jewett's Average Sentence Lengths](/static/images/imgforblogposts/post_10/jewett_mean_sentence_lengths.png)

![Cather's Average Sentence Lengths](/static/images/imgforblogposts/post_10/cather_mean_sentence_lengths.png)


  
