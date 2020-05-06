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
>>> PhonemePhraser
>>> example_phrase = "Wave the sails"
>>> PhonemePhraser.to_phonetic(example_phrase)
[u'W', u'EY', u'V', u'DH', u'AH', u'S', u'EY', u'L', u'Z']
```

### Rewrite a string phonetically
```python
>>> PhonemePhraser
>>> example_phrase = "Wave the sails"
>>> phoneme_list = PhonemePhraser.to_phonetic(example_phrase)
>>> PhonemePhraser.rephrase(phoneme_list)
[u'WAIVE', u'THUS', u'AILS']
```

## References
<https://en.wikipedia.org/wiki/Phoneme>  
<https://en.wikipedia.org/wiki/ARPABET>  
<http://www.speech.cs.cmu.edu/cgi-bin/cmudict?in=>  
<https://www.kaggle.com/rtatman/english-word-frequency>  
<https://en.wikipedia.org/wiki/Trie>  
