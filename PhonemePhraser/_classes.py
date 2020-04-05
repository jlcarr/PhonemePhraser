

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
	
	def load_dict(self, trie_dict, to_return=False):
		self.phoneme = trie_dict['phoneme']
		self.count = trie_dict['count']
		self.children = {child_phoneme:phoneme_trie(phoneme=child_phoneme).load_dict(child_dict, to_return=True) for child_phoneme,child_dict in trie_dict['children'].items()}
		self.leaves = trie_dict['leaves']
		return self if to_return else None
