import collections

from colorama import Fore

from alphabet import dict_words, dict_length
from vinegar_tools import is_text_within_allowed_English_IC_margin, calculate_IC, is_text_partially_english

_DETAIL_MODE_ = True
_PROXIMITY_ = 0.85

_holder_ = []
_INDEX_OF_E_ = dict_words.index('e')


def un_shifting(character: str, shift: str) -> str:
	new_index = (dict_words.index(character) -
	             dict_words.index(shift)) % dict_length
	return dict_words[new_index]


def decrypt_with_key(cypher_text: str, key: str) -> str:
	key_length = len(key)
	return ''.join(
		[un_shifting(value, key[index % key_length])
		 for (index, value) in enumerate(cypher_text)]
	)


def get_occurrence_map(text: str) -> dict:
	"""Return percentage of each character in text. Expect text to have length > 0"""
	total_length = len(text)
	return {i: (text.count(i) / total_length) for i in set(text)}


def get_key_of_highest_value_from_dict(occurrence_dict: dict) -> list:
	result = []
	current_max_frequency = 0
	
	for (item, frequency) in occurrence_dict.items():
		if current_max_frequency < frequency:
			current_max_frequency = frequency
			result = list(filter(
				# get close max-es
				lambda thing: thing[1] >= current_max_frequency * _PROXIMITY_,
				result))
			result.append([item, frequency])
		elif (current_max_frequency * _PROXIMITY_) <= frequency:
			result.append([item, frequency])
	
	return result


# Get group of highest values from dict
def get_group_of_key_of_highest_value_from_dict(occurrence_dict: dict) -> []:
	sorted_occurrence_dict = sorted(occurrence_dict.items(), key=lambda x: x[1], reverse=True)
	sorted_symbol_list = [sorted_occurrence_dict[x][0] for x in range(len(occurrence_dict))]
	if not bool(sorted_occurrence_dict):
		return None
	else:
		return [sorted_symbol_list[x] for x in range(5)]


# ex: [[a,b], [c,d]] -> [ab, ac, bc, bd]
def get_key_from_nested_list_core(most_frequent_characters: list, index: int, initial: str):
	if index == len(most_frequent_characters):
		_holder_.append(initial)
	else:
		for thing in most_frequent_characters[index]:
			get_key_from_nested_list_core(
				most_frequent_characters,
				index + 1,
				initial + dict_words[(dict_words.index(thing[0]) - _INDEX_OF_E_) % dict_length]
			)


def get_key_from_nested_list(most_frequent_characters: list) -> list:
	global _holder_
	_holder_ = []
	get_key_from_nested_list_core(most_frequent_characters, 0, '')
	return _holder_


# Take value with most occurrence at each index-es.
def get_key_vote(possible_keys: list) -> list:
	if len(possible_keys) == 2:
		return possible_keys
	possible_keys = sorted(possible_keys)
	result = []
	
	key_length = len(possible_keys[0])
	for index in range(key_length):
		matrix = [i[index] for i in possible_keys]
		result.append(collections.Counter(matrix).most_common(1)[0][0])
	
	return [''.join(result)]


def reduce_key(possible_keys_4: str) -> str:
	"""
	Reduce to minimum key. Ex: 'ababab' -> 'ab'
	:param possible_keys_4: current key
	:return: reduced key
	"""
	for i in range(1, len(possible_keys_4)):
		if len(possible_keys_4) % i == 0:
			j = 0
			k = i * 2
			divider = i
			while k <= len(possible_keys_4):
				if possible_keys_4[j:i] != possible_keys_4[i:k]:
					divider = -1
					break
				j, i, k = i, k, k + divider
			if k >= len(possible_keys_4) and divider != -1:
				return possible_keys_4[0: divider]
	return possible_keys_4


def decrypt_with_key_length(cypher_text: str, key_length: int) -> str:
	# Divide into groups.
	# --> each group will have character frequency similar to English?
	# So 'e' usually has the highest frequency for each group
	text_groups = [[] for _ in range(key_length)]
	for i in range(len(cypher_text)):
		text_groups[i % key_length].append(cypher_text[i])
	
	# convert back to list of strings
	text_groups = [''.join(characters) for characters in text_groups]
	# get occurrence map for each group
	character_occurrences = [get_occurrence_map(text) for text in text_groups]
	
	# for each group, take out the characters with highest occurrence
	most_frequent_characters = [get_key_of_highest_value_from_dict(character_dict) for character_dict in
	                            character_occurrences]
	
	# each highest occurrence correspond to 'e'. Calculate distance from 'e' ---> key
	possible_keys = get_key_from_nested_list(most_frequent_characters)
	
	if len(possible_keys) == 0:
		return ''
	
	# Cartesian product of characters with highest frequency in each position
	possible_keys_1 = []
	for key in possible_keys:
		if is_text_within_allowed_English_IC_margin(decrypt_with_key(cypher_text, key)):
			possible_keys_1.append(key)
	
	if _DETAIL_MODE_:
		print(f'1. Using IC : {Fore.YELLOW}%s' % sorted(possible_keys_1))
	
	if len(possible_keys_1) == 0:
		return possible_keys[0]
	
	# test if all keys can decrypt to english-ish paragraph
	possible_keys_2 = []
	for key in possible_keys_1:
		# Take the first 30 characters to check.
		# Increase this give higher precision result, but make the decrypting slower
		# Max length of words in dictionary is 14,
		# so we minus 14 for cases where we cut in the middle of words
		
		if is_text_partially_english(decrypt_with_key(cypher_text[:30], key), 14):
			possible_keys_2.append(key)
	
	if _DETAIL_MODE_:
		print(f'2. Using word detection: {Fore.YELLOW}%s' % sorted(possible_keys_2))
	
	if len(possible_keys_2) == 0:
		return possible_keys_1[0]
	
	# Vote for most popular character in each position
	possible_keys_3 = get_key_vote(possible_keys_2)
	
	if _DETAIL_MODE_:
		print(f'3. Using democratic voting: {Fore.YELLOW} %s' % sorted(possible_keys_3))
	
	if len(possible_keys_3) == 0:
		return possible_keys_2[0]
	
	# resolve conflict if len(possible_keys_2) > 1
	possible_keys_4 = possible_keys_3[0]
	if len(possible_keys_3) == 2:
		possible_keys_4 = (possible_keys_3[0]
		                   if calculate_IC(possible_keys_3[0]) >= calculate_IC(possible_keys_3[1]) else
		                   possible_keys_3[1]
		                   )
	
	if _DETAIL_MODE_:
		print(f'4. Using luck:{Fore.YELLOW} %s' % possible_keys_4)
	
	possible_keys_5 = reduce_key(possible_keys_4)
	
	if _DETAIL_MODE_:
		print(f'5. Use reduce key:{Fore.YELLOW} %s' % possible_keys_5)
	
	return decrypt_with_key(cypher_text, possible_keys_5)


if __name__ == '__main__':
	print(reduce_key('abab'))
	print(reduce_key('xabab'))
