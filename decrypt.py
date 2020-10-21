import collections
from itertools import product

from colorama import Fore

from alphabet import dict_words, dict_length
from vignere_tools import is_english_word, within_allowed_English_IC_margin, find_IC

PROXIMITY = 0.85

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
				# get close max
				lambda thing: thing[1] >= current_max_frequency * PROXIMITY,
				result))
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


def get_key_from_nested_list_core(most_frequent_characters: list, index: int, initial: str):
	if index == len(most_frequent_characters):
		_holder_.append(initial)
	else:
		for thing in most_frequent_characters[index]:
			get_key_from_nested_list_core(
				most_frequent_characters,
				index + 1,
				initial + chr((dict_words.index(thing[0]) - _INDEX_OF_E_) % dict_length + ord('a'))
			)


def get_key_from_nested_list(most_frequent_characters: list) -> list:
	global _holder_
	_holder_ = []
	get_key_from_nested_list_core(most_frequent_characters, 0, '')
	return _holder_


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
	
	possible_keys_1 = []
	for key in possible_keys:
		if within_allowed_English_IC_margin(decrypt_with_key(cypher_text, key)):
			possible_keys_1.append(key)
	
	print(f"is this the key:{Fore.YELLOW} %s" % sorted(possible_keys))
	print(f'after trial 1: {Fore.YELLOW}%s' % possible_keys_1)
	
	if len(possible_keys_1) == 0:
		return ''
	
	possible_keys_2 = get_key_vote(possible_keys_1)
	print(f'after trial 2:{Fore.YELLOW} %s' % sorted(possible_keys_2))
	
	if len(possible_keys_2) == 0:
		return ''
	
	possible_keys_3 = possible_keys_2[0]
	if len(possible_keys_2) == 2:
		possible_keys_3 = (possible_keys_2[0]
		                   if find_IC(possible_keys_2[0]) >= find_IC(possible_keys_2[1]) else
		                   possible_keys_2[1]
		                   )
	
	print(f'after trial 3:{Fore.YELLOW} %s' % possible_keys_3)
	
	return decrypt_with_key(cypher_text, possible_keys_3)


def decrypt_with_key_length_and_frequency_collision(cypher_text: str, key_length: int) -> str:
	text_groups = [[] for _ in range(key_length)]
	for i in range(len(cypher_text)):
		text_groups[i % key_length].append(cypher_text[i])
	text_groups = [''.join(characters) for characters in text_groups]
	character_occurrences = [get_occurrence_map(text) for text in text_groups]
	
	most_frequent_characters_groups = [get_group_of_key_of_highest_value_from_dict(character_dict) for character_dict in
	                                   character_occurrences]
	index_of_e = dict_words.index('e')
	
	possible_keys_unhandled = [element for element in product(*most_frequent_characters_groups, repeat=1)]
	
	possible_keys = [''.join(
		(dict_words[(dict_words.index(character) - index_of_e) % dict_length]
		 for character in most_frequent_characters)) for most_frequent_characters in possible_keys_unhandled]
	for possible_key in possible_keys:
		print("testing key:" + possible_key)
		text = decrypt_with_key(cypher_text, possible_key)
		if text_is_english(text):
			return text
	
	# print("is this the key: %s" % possible_key)
	# print("foo")
	
	return None


def text_is_english(text: str) -> bool:
	try:
		test_words = ''.join([text.split(' ')[x] for x in range(5)])
	except:
		return False
	for word in test_words:
		if not is_english_word(word):
			return False
	return True
