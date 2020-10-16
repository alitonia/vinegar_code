from alphabet import dict_length, word_dict


def shifting(character: str, shift: str) -> str:
	# Error if character not in character_list
	new_index = (word_dict.index(character) + word_dict.index(shift)) % dict_length
	return word_dict[new_index]


def vinegar_it(text: str, key: str) -> str:
	key_length = len(key)
	return ''.join(
		[shifting(value, key[index % key_length]) for (index, value) in enumerate(text)]
	)
