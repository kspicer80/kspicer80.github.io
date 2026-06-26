---
title: "The Bard Aboard the Enterprise: Tracking Shakespeare References in Star Trek: The Next Generation"
date: 2026-06-24
tags:
  - digital humanities
  - Python
  - Shakespeare
  - Star Trek
  - TNG
  - natural language processing
  - fuzzy matching
  - sentence transformers
  - TF-IDF
  - text analysis
  - web scraping
  - beautiful soup
  - rapidfuzz
  - data visualization
  - matplotlib
  - pandas
  - scikit-learn
  - PyTorch
---

So, recently, I've been watching episodes of *Star Trek: The Next Generation*, which is available on Paramound. I'm not sure why, frankly. Honestly, I was watching them for the first time---yes, I know, embarrassingly late to the party (I am old enough to have caught snatches and snippets from it when it originally aired)---and within the first two episodes I had already noticed a couple of Shakespeare references. In the pilot, a character quips something very close to a line from *Henry VI* about killing all the lawyers; in the second episode, Data---the android crew member whose entire arc is about what it means to be human---says something to the effect of "If you prick me, do I not leak?", a reworking of Shylock's famous speech from *The Merchant of Venice* that is, of course, all the more poignant coming from a being who literally leaks hydraulic fluid rather than blood.[^1] Two episodes in and two Shakespeare hits already. Which naturally piqued my interest: just how many times does Shakespeare appear across all 176 episodes of TNG? And could we build a pipeline to find them?

As it turned out, the answer to the second question was yes---and the answer to the first was, as of this writing, somewhere around 1,109 confirmed references. But the interesting intellectual and methodological questions, as I'll try to lay out here, are not really about that number at all. They're about what we mean when we say something "is" a Shakespeare reference in the first place.

## Building the Corpus

The first order of business was getting the data. For Shakespeare, I used the plain-text editions available from the [Folger Shakespeare Library](https://shakespeare.folger.edu), which offers authoritative texts of all forty-two works free for non-commercial use. For TNG, I needed the episode transcripts. The go-to resource for these is [chakoteya.net](http://www.chakoteya.net/NextGen/), which has clean, speaker-tagged transcripts for every episode in a pleasingly consistent format. A fairly straightforward scraper using `requests` and `BeautifulSoup` pulled all 176 episodes down into individual files:

```python
BASE_URL  = "http://www.chakoteya.net/NextGen/"
INDEX_URL = BASE_URL + "episodes.htm"

def scrape_episode(ep: dict) -> str:
    soup = get_soup(ep["url"])
    # Speaker names appear in <b> tags; dialogue follows as plain text nodes
    for element in body_td.descendants:
        if element.name == "b":
            flush_buffer()
            current_speaker = element.get_text(strip=True).upper()
        elif element.name is None:
            buffer.append(str(element).strip())
```

Each file ends up named something like `S01E01_Encounter_at_Farpoint.txt`, with the content structured as clean `SPEAKER: dialogue` pairs, which makes everything downstream considerably easier.[^2]

Once both corpora were in hand, a parsing script processed them into two CSVs: `shakespeare/passages.csv` and `tng/lines.csv`. For Shakespeare, each speech is broken into overlapping sliding-window chunks of roughly twelve words (with a six-word step), so that the matcher can find partial quotations rather than requiring a full speech to match. The TNG side required a bit of normalization---chakoteya uses several variant forms of character names (`CAPTAIN PICARD`, `JEAN-LUC PICARD`, `COMMANDER PICARD`, and so on), all of which need to resolve to a single `PICARD` for any character-level analysis to make sense. After filtering for length, the final corpus broke down as follows:

- **Shakespeare**: 108,138 passage windows across 37 plays
- **TNG**: 76,499 lines across 176 episodes (40,107 after filtering out very short lines and unattributed scene directions)

## The Matching Problem

Here is where things get interesting---and where the computational choices start to have real interpretive consequences.

Exact string matching is obviously a non-starter. The whole point is to catch paraphrases and allusions, not just verbatim quotations. But the naïve alternative---computing some similarity score between every TNG line and every Shakespeare passage---would require evaluating something on the order of 8 billion pairs. Even a very fast similarity function would take days on a laptop. The solution is a three-stage pipeline:

**Stage 0: TF-IDF pre-filter.** A TF-IDF vectorizer is fit on the combined corpus, and for each TNG line we retrieve the top 20 most lexically similar Shakespeare passages using sparse matrix cosine similarity. This collapses the 8-billion-pair space down to about 800,000 candidate pairs---and it does it in a little over a minute:

```python
vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=2,
                              max_df=0.95, sublinear_tf=True)
vectorizer.fit(corpus)
shak_vecs = vectorizer.transform(shak["passage"])
tng_vecs  = vectorizer.transform(tng["line_text"])
# For each TNG line, retrieve top-20 Shakespeare candidates
sims = sk_cosine(batch, shak_vecs)
```

**Stage 1: Fuzzy matching.** The `rapidfuzz` library's `token_set_ratio` function runs over the 800,000 candidate pairs. Token-set ratio is particularly well-suited here because it is order-insensitive---so "If you prick me do I not leak" still scores well against "If you prick us do we not bleed" despite the word substitutions and the shift from first-person plural to singular. Any pair scoring 60 or above (on a 0–100 scale) survives to stage 2.

**Stage 2: Semantic similarity.** The `sentence-transformers` library's `all-MiniLM-L6-v2` model encodes all unique texts that survived stage 1---roughly 25,000 passages---and computes cosine similarity on the resulting embeddings.[^3] This catches looser thematic allusions that might survive semantic similarity even when the surface wording has diverged significantly. The full stage 2 encoding took about four and a half minutes.

The relationship between the two scoring methods is itself worth examining. The scatter plot below shows fuzzy score against semantic score for a sample of 2,000 matches, coloured by play. Points in the upper-right quadrant---high on both axes---represent the most confident matches; points that score high on fuzzy but lower on semantic tend to be lexical overlaps that don't hold up under deeper comparison, while the reverse (high semantic, moderate fuzzy) often flags looser thematic allusions where the wording has been substantially reworked.

![Fuzzy vs. semantic score by play](images/imgforblogposts/post_50/tng_shakespeare/05_scatter.png)

The final output is two files: `matching/candidates.csv` (everything above the loose threshold) and `matching/confirmed.csv` (the high-confidence subset). The confirmed set came in at 1,109 matches.

## What the Numbers Show---and What They Don't

The top-line results are, frankly, quite fun to look at. Hamlet leads with 91 confirmed references, followed by *Twelfth Night* (76), *Henry VIII* (70), *Othello* (65), and *Measure for Measure* (57).

![Top 15 Shakespeare plays referenced in TNG](/images/imgforblogposts/post_50/tng_shakespeare/01_plays_bar.png)

Hamlet leading the field is hardly surprising---it is the most canonical of canonical texts, and Picard's obsession with it is explicitly scripted in several episodes. What is perhaps more interesting is the presence of *Twelfth Night* so near the top, and the strong showing from the histories (*Henry VIII*, *Henry V*) and the problem plays (*Measure for Measure*, *Troilus and Cressida*). These are not the plays one would necessarily expect a television writing room to reach for, which suggests either that the matching is picking up on something real about the show's literary texture or that the algorithm is finding coincidental overlaps in registers---political, martial, formal---that these plays happen to share with TNG's dialogue. That question is, as I'll talk about below, one the algorithm cannot resolve on its own.

On the speaker side, Picard leads with 223 references, followed by Data (137), Worf (86), Riker (80), and Crusher (50).

![Top 10 TNG speakers quoting Shakespeare](/images/imgforblogposts/post_50/tng_shakespeare/02_speakers_bar.png)

The Picard and Data numbers make intuitive sense and are probably among the most reliable hits in the dataset. Picard is famously literary---there are whole episodes built around his love of Shakespeare, and the writers clearly use Shakespearean allusion as a characterization device. When Picard quotes, it tends to be deliberate, close to the source text, and easy to score with high confidence. Data's references are similarly intentional but differently motivated: his quotations tend to be slightly off in ways that are themselves meaningful, as with the "prick me / leak" substitution, where the computational detection of a paraphrase happens to mirror the character's own computational relationship to human language and embodied experience.

The Worf number is where things get genuinely interesting from a methodological standpoint---and where I think the most important work remains to be done. 86 Worf references sounds plausible on one reading: Klingon honor culture maps naturally onto the martial-aristocratic world of the *Henry* plays, onto Coriolanus, onto the Roman tragedies generally. And there are certainly moments in the show where one could argue the writers are consciously reaching for that resonance. But there are also a lot of Worf lines that match Shakespeare passages simply because both are dealing in the kind of heightened, formal language of honor, combat, and duty that is not owned by Shakespeare---it is a register that has a long history before him and a long history after. Whether a given Worf match is an intentional allusion, an unconscious stylistic parallel, or pure coincidence is a question the algorithm cannot answer. That requires close reading, contextual knowledge about the episode, and---ideally---some sense of what the writers' room was actually doing.

The heatmap below breaks the confirmed matches down by season and play, which adds a useful temporal dimension to the picture:

![References by season and play](/images/imgforblogposts/post_50/tng_shakespeare/03_heatmap.png)

A few things stand out here. Hamlet references are distributed fairly evenly across all seven seasons rather than clustering in particular years, which makes sense given that Picard's literary interests are a consistent characterization device throughout the series rather than a phase the writers went through. The *Henry VIII* concentration in certain seasons is worth investigating further---it is possible that a handful of episodes involving formal political ceremony or ritual are driving those numbers. The relative absence of references in Season 2 is also interesting; Season 2 is generally considered the shakiest of the run, and it would be worth checking whether the reduced Shakespeare count is a real signal about the writing or an artifact of shorter episodes or transcript quality.

The timeline view makes the episode-by-episode distribution somewhat clearer:

![Shakespeare references across all 176 episodes](/images/imgforblogposts/post_50/tng_shakespeare/04_timeline.png)

What I find most striking here is not the spikes---though some of those are worth looking at individually---but the cumulative line, which is reassuringly close to linear. A genuinely random distribution of references across the run would produce a roughly linear cumulative curve, and that is broadly what we see, which is at least consistent with the hypothesis that Shakespearean language is a fairly steady background feature of the show's dialogue rather than something the writers turned on and off in particular seasons or arcs. There are some visible upticks in Seasons 3–4, which coincide with what most fans and critics consider the creative peak of the series, but I would want to do more work before drawing any firm conclusions from that.

This is, of course, not a weakness unique to this particular project. It is, I think, the central methodological tension in computational literary studies more broadly: the pipeline surfaces candidates at a scale no individual reader could manage, but the pipeline cannot adjudicate between the categories of reference, allusion, parallel, and coincidence that the humanistic interpreter is actually interested in. The numbers are the beginning of the conversation, not the end of it.[^4]

## What Comes Next

There is quite a lot still to do. The most pressing task is exactly the kind of close-reading work I described above for the Worf examples: going through the confirmed matches and trying to sort them into the intentional/allusive/parallel/coincidental taxonomy, which will require watching (or rewatching) specific episodes with the match data in hand. That process will also, no doubt, reveal some false positives in the confirmed set that will help with threshold calibration. It would also be worth adding the plays-as-genre metadata back into the analysis---whether references to tragedies, comedies, and histories distribute differently across characters and seasons seems like a genuinely interesting question. And at some point the project probably wants to think about what it would mean to write this up as scholarship (I've been wondering about this a lot recently, if I'm being honest)rather than just as a blog post---which means engaging with the existing literature on Shakespeare and *TNG* (there is some, though not a great deal) and with the methodological literature in computational humanities on the question of what "allusion detection" can and cannot do.

As usual, more to come, for sure.

---

[^1]: The original Shylock speech, of course, runs: "If you prick us, do we not bleed? If you tickle us, do we not laugh? If you poison us, do we not die? And if you wrong us, shall we not revenge?" (*The Merchant of Venice*, III.i). Data's version substitutes "leak" for "bleed," which is both a joke about his android physiology and, depending on how one reads it, something considerably more than a joke, to be sure.

[^2]: There was one small hiccup with the scraper: chakoteya numbers its episode pages sequentially (1.htm, 2.htm, ... 176.htm), and the original scraping script misread 3-digit sequential numbers like `101` as "Season 1, Episode 1" rather than "episode 101 overall." A quick fix script using the canonical episode list sorted everything out without requiring a re-download---skipping over two episodes with accented characters in their titles ("Déjà Q" and "Ménage à Troi") that needed a manual rename.

[^3]: `sentence-transformers` requires PyTorch >= 2.4, which necessitated creating a dedicated conda environment (`conda create -n tng_shakespeare python=3.11`) rather than fighting with the base environment's existing PyTorch 2.2 install.

[^4]: There is a useful framing for this in Alan Liu's work on the "meaning" of distant reading---the idea that computational methods and the digital humanities more generally are best understood not as replacements for close reading (who would ever think of getting rid of "close reading"!) but as instruments for generating hypotheses that close reading can then evaluate. All the code for this project is available [here](https://github.com/kspicer80/tng-shakespeare).
