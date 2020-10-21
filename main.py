from decrypt import decrypt_with_key, decrypt_with_key_length,decrypt_with_key_length_and_frequency_collision
from encrypt import vinegar_it
from vignere_tools import find_key_length

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
	#print("Decrypt with key length and frequency collision %s" %
	#      (decrypt_with_key_length_and_frequency_collision(cypher_text, len(key)) == text)
	#      )
	print("Estimated keylength of cyphertext: " + str(find_key_length(cypher_text)))

	source_file.close()
