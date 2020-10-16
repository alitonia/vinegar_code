from alphabet import dict_words, dict_length


def un_shifting(character: str, shift: str) -> str:
	new_index = (dict_words.index(character) - dict_words.index(shift)) % dict_length
	return dict_words[new_index]


def decrypt_with_known_key(cypher_text: str, key: str) -> str:
	key_length = len(key)
	return ''.join(
		[un_shifting(value, key[index % key_length]) for (index, value) in enumerate(cypher_text)]
	)
