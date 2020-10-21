from colorama import init, Fore, deinit, Style

from decrypt import decrypt_with_key_length, decrypt_with_key
from encrypt import vinegar_it
from vignere_tools import find_key_length

if __name__ == '__main__':
	init(autoreset=True)
	path = './corpus_new.txt'
	source_file = open(path, 'r')
	text = source_file.read().rstrip()
	key = 'fdoo'
	cypher_text = vinegar_it(text, key)
	
	print(f'{Fore.BLUE}Key: {Fore.YELLOW}%s' % key)
	print(f'{Fore.BLUE}Plain text:{Style.RESET_ALL}  ' + text[:100] + '...')
	print(f'{Fore.BLUE}Cypher text:{Style.RESET_ALL} ' + cypher_text[:100] + '...')
	
	print(f"Decrypt with key:{Fore.YELLOW} %s" %
	      (decrypt_with_key(cypher_text, key) == text)
	      )
	estimated_key_length = find_key_length(cypher_text)
	print(f"Estimated key_length of cypher_text: {Fore.YELLOW} %s" % estimated_key_length)
	
	print(f"Decrypt with key length: {Fore.YELLOW} %s" %
	      (decrypt_with_key_length(cypher_text, estimated_key_length) == text)
	      )
	source_file.close()
	deinit()
