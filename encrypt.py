from alphabet import dict_length, dict_words


def shifting(character: str, shift: str) -> str:
	# Error if character not in character_list
	new_index = (dict_words.index(character) + dict_words.index(shift)) % dict_length
	return dict_words[new_index]


def vinegar_it(plain_text: str, key: str) -> str:
	key_length = len(key)
	return ''.join(
		[shifting(value, key[index % key_length]) for (index, value) in enumerate(plain_text)]
	)
