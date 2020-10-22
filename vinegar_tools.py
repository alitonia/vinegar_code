import functools
from collections import defaultdict

ENGLISH_IC = 0.067
ERROR_MARGIN = 0.12

_HASH_MAP_ = defaultdict(list)
_target_wordlist_file_ = 'resources/english_wordlist.txt'


def _make_HASH_MAP_():
	for line in open(_target_wordlist_file_, 'r'):
		_HASH_MAP_[hash(line[:-1])].append(line[:-1])


@functools.lru_cache(10000)
def is_english_word(word: str) -> bool:
	if not _HASH_MAP_:
		_make_HASH_MAP_()
	hash_chain = _HASH_MAP_.get(hash(word))
	result = (word in hash_chain) if hash_chain else False
	return result


@functools.lru_cache(100)
def is_text_english(text: str) -> bool:
	if len(text) == 0:
		return True
	for possible_length in range(1, len(text) + 1):
		word = text[:possible_length]
		rest = text[possible_length:]
		if is_english_word(word) and is_text_english(rest):
			return True
	return False


def is_text_partially_english(text: str, lower_bound: int) -> int:
	"""if a text of at least length lower_bound from beginning --> true
		ex: "youewrewr" with lower_bound 3 -> true
		ex: "youewrewr" with lower_bound 4 -> false
	"""
	if not (0 <= lower_bound <= len(text)):
		return False
	for possible_length in range(lower_bound, len(text) + 1):
		current_text = text[:possible_length]
		if is_text_english(current_text):
			return True
	return False


def is_within_allowed_English_IC_margin(text: str) -> bool:
	if ENGLISH_IC * (1 - ERROR_MARGIN) <= calculate_IC(text) <= ENGLISH_IC * (1 + ERROR_MARGIN):
		return True
	else:
		return False


def calculate_IC(text: str) -> float:
	occurrence_list = [text.count(i) for i in set(text)]
	text_length = len(text)
	index_of_coincidence = 0
	for x in occurrence_list:
		index_of_coincidence += x * (x - 1)
	index_of_coincidence /= text_length * (text_length - 1)
	return index_of_coincidence


def find_key_length(text: str) -> int:
	key_length = 1
	
	# IC is not mono
	previous_IC = calculate_IC(text)
	if previous_IC > 0.06:
		return key_length
	
	while True:
		key_length += 1
		text_groups = [[] for _ in range(key_length)]
		
		for i in range(len(text)):
			text_groups[i % key_length].append(text[i])
		
		current_IC = 0
		for text_group in text_groups:
			current_IC += calculate_IC(''.join(text_group))
		current_IC /= key_length
		
		if current_IC > 0.06:
			break
	
	return key_length


if __name__ == '__main__':
	print(is_english_word('hello'))
	
	target = 'wellhellothere'
	print(target, len(target))
	print(is_text_english(target))
	for i in range(len(target)):
		print(i, is_text_partially_english(target, len(target) - i))
