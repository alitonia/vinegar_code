from decrypt import decrypt_with_key, decrypt_with_key_length
from encrypt import vinegar_it

if __name__ == '__main__':
	path = './corpus_new.txt'
	source_file = open(path, 'r')
	text = source_file.read().rstrip()
	key = 'asdjada'
	cypher_text = vinegar_it(text, key)
	# print(cypher_text)
	print("Decrypt with key %s" %
	      (decrypt_with_key(cypher_text, key) == text)
	      )
	print("Decrypt with key length %s" %
	      (decrypt_with_key_length(cypher_text, len(key)) == text)
	      )
	source_file.close()
