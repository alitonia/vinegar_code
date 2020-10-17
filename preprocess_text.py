import re

from alphabet import dict_string

old_file_path = './corpus.txt'
new_file_path = './corpus_new.txt'

old_file = open(old_file_path, 'r')
new_file = open(new_file_path, 'w')

data = old_file.read()

# remove all characters not in alphabet_list
data = re.sub("[^%s]+" % dict_string, '', data)
new_file.write(data)

old_file.close()
new_file.close()
