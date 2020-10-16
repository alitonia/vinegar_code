from encrypt import vinegar_it
from decrypt import decrypt_with_known_key

if __name__ == '__main__':
	text = 'hellothere'
	key = 'ab'
	cypher_text = vinegar_it(text, key)
	print(cypher_text)
	print(decrypt_with_known_key(cypher_text, key))
