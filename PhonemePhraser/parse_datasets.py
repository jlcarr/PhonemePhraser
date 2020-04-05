"""
A script to parse dataset that are used for the project
"""

import re
import json
import pickle

from _classes import *


def CMU_phonetic(file_path):
	with open(file_path, 'r') as file:
		phonetic_dict = file.read()
	# split to records
	phonetic_dict = phonetic_dict.splitlines()
	# Filter for only words and primary
	phonetic_dict = list(filter(lambda x: not x.startswith(';'), phonetic_dict))
	# split to word and phoneme
	phonetic_dict = list(map(lambda x: x.split('  '), phonetic_dict))
	# remove weirdos
	phonetic_dict = list(filter(lambda x: re.match(r"\A[A-Z']*\Z", x[0]), phonetic_dict))
	# Remove stresses
	phonetic_dict = dict(map(lambda x: (x[0], str(filter(lambda c: not c.isdigit(), x[1])).split(' ')), phonetic_dict))
	return phonetic_dict


def Google_freq(file_path):
	with open(file_path, 'r') as file:
		count_dict = file.read()
	# split to records and remove headers
	count_dict = count_dict.upper()
	count_dict = count_dict.splitlines()[1:]
	# Filter for only words and primary
	count_dict = list(map(lambda x: x.split(','), count_dict))
	count_dict = dict(map(lambda x: (x[0], int(x[1])), count_dict))
	return count_dict


def fill_trie(phonetic_dict, count_dict, min_count=100*1000):
	result = phoneme_trie()
	for word,phonemes_list in phonetic_dict.items():
		# The counts doesn't include plurals
		count = count_dict.get(word.split("'")[0], 0)
		if count > min_count:
			result.add_word(phonemes_list, word, count=count)
	return result


if __name__ == "__main__":
	with open('./datasets/config.json','r') as file:
		config = json.load(file)

	phonetic_dict = CMU_phonetic(config['phonetic_dataset'])
	count_dict = Google_freq(config['freq_dict'])
	pt = fill_trie(phonetic_dict, count_dict)

	with open(config['phonetic_dict'],'w') as file:
		json.dump(phonetic_dict, file, indent=4)

	with open(config['trie_dict'],'w') as file:
		json.dump(pt.to_dict(), file, indent=4)

	with open(config['trie_pickle'],'w') as file:
		pickle.dump(pt, file)
