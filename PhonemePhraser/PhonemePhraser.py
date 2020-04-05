"""
This is a module that contains tools for creating fun phoneme matching to phrases
"""
import os
cwd = os.path.dirname(os.path.realpath(__file__))

import pickle
import json
import numpy as np

from _classes import *


# initial loads
with open(os.path.join(cwd,'./datasets/config.json'), 'r') as file:
	config = json.load(file)

with open(os.path.join(cwd, config['trie_dict']), 'r') as file:
	root_trie = phoneme_trie().load_dict(json.load(file), to_return=True)

with open(os.path.join(cwd, config['phonetic_dict']), 'r') as file:
	phonetic_dict = json.load(file)

def to_phonetic(phrase):
	global phonetic_dict
	phrase = str(filter(lambda x: x.isspace() or x.isalpha(), phrase))
	phrase = ' '.join(map(lambda x: ' '.join(phonetic_dict[x]), phrase.upper().split(' ')))
	phrase = phrase.split(' ')
	return phrase


def rephrase(phrase, current_trie = root_trie, verbose=False):
	new_phrase = []
	phoneme = phrase[0]
	current_trie = current_trie.children[phoneme]
	if verbose:
		print 'Phoneme: ' + phoneme
		print 'Leaves: ' + str(current_trie.leaves)
		print 'Children: ' + str(current_trie.children.keys())

	next_trie = None if not phrase[1:] or phrase[1] not in current_trie.children else current_trie.children[phrase[1]]
	selections = [] if not next_trie else [None]
	probabilities = [] if not selections else [next_trie.count]
	selections += current_trie.leaves.keys()
	probabilities += current_trie.leaves.values()
	probabilities = list(map(np.log2, probabilities))
	while selections:
		normal_probabilities = np.array(probabilities)/float(sum(probabilities))
		selection_index = np.random.choice(range(len(selections)), p=normal_probabilities)
		selection = selections[selection_index]
		if verbose:
			print 'Selections: ' + str(selections)
			print 'Probabilities: ' + str(probabilities)
			print 'Normal Probabilities: ' + str(normal_probabilities)
			print 'Selection Index: ' + str(selection_index)
			print 'Selection: ' + str(selection)
			print ''
		# Was a word chosen?
		if isinstance(selection, str) or isinstance(selection, unicode):
			# At the end of the phrase?
			if not phrase[1:]:
				return [selection]
			# Is there a valid following phrase?
			following_phrase = rephrase(phrase[1:], verbose=verbose)
			if following_phrase:
				return [selection] + following_phrase
		# Otherwise next syllable
		else:
			following =  rephrase(phrase[1:], current_trie = current_trie, verbose=verbose)
			if following:
				return following
		if verbose:
			print("Bad selection\n")
		# This selection didn't work out, try again
		selections.pop(selection_index)
		probabilities.pop(selection_index)
	return []



