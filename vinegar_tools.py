import functools
from collections import defaultdict

_LOOSE_ENGLISH_IC_ = 0.062
_ERROR_MARGIN_ = 0.05
_STRICT_ENGLISH_IC_ = 0.0615

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


def is_text_within_allowed_English_IC_margin(text: str) -> bool:
	if _LOOSE_ENGLISH_IC_ * (1 - _ERROR_MARGIN_) <= calculate_IC(text) <= _LOOSE_ENGLISH_IC_ * (1 + _ERROR_MARGIN_):
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
	key_length = 0
	MAXIMUM_KEY_LENGTH = 100
	# keep history of last 3
	IC_triad = []
	
	for i in range(min(len(text), MAXIMUM_KEY_LENGTH + 1)):
		key_length += 1
		text_groups = [[] for _ in range(key_length)]
		
		for i in range(len(text)):
			text_groups[i % key_length].append(text[i])
		
		current_IC = 0
		for text_group in text_groups:
			current_IC += calculate_IC(''.join(text_group))
		current_IC /= key_length
		
		# print(f'Current length: %s, IC: %s' % (key_length, current_IC))
		if len(IC_triad) > 3:
			IC_triad.pop(0)
		IC_triad.append(current_IC)
		
		# 	IC of a key component satisfy:
		#   * if key_length = 1 --> IC > IC_2
		#   * else IC_(X-1) < IC_(X) > IC_(X+1)
		if key_length == 1:
			continue
		elif key_length == 2:
			if IC_triad[0] > _STRICT_ENGLISH_IC_ and IC_triad[0] > IC_triad[1]:
				key_length = 1
				break
		else:
			if IC_triad[1] > _STRICT_ENGLISH_IC_ and IC_triad[0] < IC_triad[1] > IC_triad[2]:
				key_length -= 2
				break
	
	return key_length


if __name__ == '__main__':
	print(is_english_word('hello'))
	
	target = 'wellhellothererrrr'
	print(target, len(target))
	print(is_text_english(target))
	print(is_text_partially_english(target, len(target) - 3))
