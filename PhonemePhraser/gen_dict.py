import re
import numpy as np

class phoneme_trie():
	def __init__(self, phoneme=''):
		self.phoneme = phoneme
		self.children = dict()
		self.leaves = dict()
		self.count = 0
	def add_word(self, phonemes_list, word, count=0):
		self.count += count
		if not phonemes_list:
			self.leaves[word] = count
			return
		next_phoneme = phonemes_list[0]
		if next_phoneme not in self.children:
			self.children[next_phoneme] = phoneme_trie(phoneme=next_phoneme)
		self.children[next_phoneme].add_word(phonemes_list[1:], word, count=count)
	def __repr__(self, tabs=0):
		return_val = '|\t'*tabs + self.phoneme + ':\n'
		return_val += '|\t'*(tabs+1) + 'count: ' + str(self.count) +' leaves: ' + str(self.leaves) + '\n'
		return_val += ''.join(map(lambda x: x.__repr__(tabs=tabs+1), self.children.values()))
		return return_val
	def __str__(self):
		return self.__repr__()
	def to_dict(self):
		return_val = dict()
		return_val['phoneme'] = self.phoneme
		return_val['count'] = self.count
		return_val['children'] = {child_phoneme:child_trie.to_dict() for child_phoneme,child_trie in self.children.items()}
		return_val['leaves'] = self.leaves
		return return_val


with open('cmudict-0.7b', 'r') as file:
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
print len(phonetic_dict)




with open('unigram_freq.csv', 'r') as file:
	count_dict = file.read()

# split to records
count_dict = count_dict.upper()
count_dict = count_dict.splitlines()[1:]
# Filter for only words and primary
count_dict = list(map(lambda x: x.split(','), count_dict))
count_dict = dict(map(lambda x: (x[0], int(x[1])), count_dict))
print len(count_dict)




# create trie (could add freq data)
# leaves are poosible dict words with freqs
# nodes contain sum child freqs
pt = phoneme_trie()

i = 0
for word,phonemes_list in phonetic_dict.items():
	#print word
	#print phonemes_list
	count = count_dict.get(word.split("'")[0], 1)
	if count == 0 or count < 1000*100:
		continue
	#print count
	#print ''
	pt.add_word(phonemes_list, word, count=count)
	i += 1
	#if i>100:
	#	break

#print pt
#print pt.to_dict()


#import json
#file = open('testout','w')
#json.dump(pt.to_dict(), file)
#file.close()


#phrase = 'site queue'
#phrase = 'wave the sales'
phrase = 'a tale of two cities'
#phrase = 'keg reef flux'
#phrase = 'gag reflex'

def to_phonetic(phrase):
	phrase = str(filter(lambda x: x.isspace() or x.isalpha(), phrase))
	phrase = ' '.join(map(lambda x: ' '.join(phonetic_dict[x]), phrase.upper().split(' ')))
	phrase = phrase.split(' ')
	return phrase
print(to_phonetic(phrase))




def rephrase(phrase, current_trie = pt):
	new_phrase = []
	phoneme = phrase[0]
	current_trie = current_trie.children[phoneme]
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
		print 'Selections: ' + str(selections)
		print 'Probabilities: ' + str(probabilities)
		print 'Normal Probabilities: ' + str(normal_probabilities)
		print 'Selection Index: ' + str(selection_index)
		print 'Selection: ' + str(selection)
		# Was a word chosen?
		if isinstance(selection, str):
			# At the end of the phrase?
			if not phrase[1:]:
				return [selection]
			# Is there a valid following phrase?
			print ''
			following_phrase = rephrase(phrase[1:])
			if following_phrase:
				return [selection] + following_phrase
		# Otherwise next syllable
		else:
			print ''
			following =  rephrase(phrase[1:], current_trie = current_trie)
			if following:
				return following
		print("Didn't work out\n")
		# This selection didn't work out, try again
		selections.pop(selection_index)
		probabilities.pop(selection_index)
	print "Bad turn"
	return []


print rephrase(to_phonetic(phrase))



