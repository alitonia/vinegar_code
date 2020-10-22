import re

from alphabet import dict_string

TEXT_SIZE = -1
if __name__ == '__main__':
	old_file_path = ''
	new_file_path = ''
	
	old_file = open(old_file_path, 'r')
	new_file = open(new_file_path, 'w')
	
	data = old_file.read()
	
	# remove all characters not in alphabet_list
	data = re.sub("[^%s]+" % dict_string, '', data[:TEXT_SIZE].lower())
	new_file.write(data)
	
	old_file.close()
	new_file.close()
