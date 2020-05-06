# PhonemePhraser
A Python module for phonetic matching

## Features
* Uses ASCII encoded ARPABET for phonemes
* Comes with parsing tools for the CMU Pronouncing Dictionary
* Comes with parsing tools for the counts of the Google Web Trillion Word Corpus
* Comes with a probibalistic phontetic phrase re-writer
* Comes with a trie datastructure for matching phoneme lists to words

## Usage Examples
### Convert a string to list of phonemes
```python
>>> import PhonemePhraser
>>> example_phrase = "Wave the sails"
>>> PhonemePhraser.to_phonetic(example_phrase)
[u'W', u'EY', u'V', u'DH', u'AH', u'S', u'EY', u'L', u'Z']
```

### Rewrite a string phonetically
```python
>>> import PhonemePhraser
>>> example_phrase = "Wave the sails"
>>> phoneme_list = PhonemePhraser.to_phonetic(example_phrase)
>>> PhonemePhraser.rephrase(phoneme_list)
[u'WAIVE', u'THUS', u'AILS']
```

### Generate all homophones of a string
```python
>>> import PhonemePhraser
>>> example_phrase = "perceive"
>>> phoneme_list = PhonemePhraser.to_phonetic(example_phrase)
>>> PhonemePhraser.all_phrases(phoneme_list)
[[u'PERCEIVE'], [u'PERS', u'YVES'], [u'PERS', u'EAVE'], [u'PERS', u'EVE'], [u'PERCE', u'YVES'], [u'PERCE', u'EAVE'], [u'PERCE', u'EVE'], [u'PEARSE', u'YVES'], [u'PEARSE', u'EAVE'], [u'PEARSE', u'EVE'], [u'PERSE', u'YVES'], [u'PERSE', u'EAVE'], [u'PERSE', u'EVE'], [u'PURSE', u'YVES'], [u'PURSE', u'EAVE'], [u'PURSE', u'EVE']]
```

## References
<https://en.wikipedia.org/wiki/Phoneme>  
<https://en.wikipedia.org/wiki/ARPABET>  
<http://www.speech.cs.cmu.edu/cgi-bin/cmudict?in=>  
<https://www.kaggle.com/rtatman/english-word-frequency>  
<https://en.wikipedia.org/wiki/Trie>  
