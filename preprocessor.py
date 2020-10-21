import random
import re

new_file = open('english_wordlist.txt', 'w')
no_pattern = [
	'.*aa.*',
	'.*ux',
	'aa.*',
	'.*ii.*',
	'.*isci.*',
	'.*ix.*',
	'.*ci$',
	'.*xi$',
	'.*lius$',
	'.*kar$',
	'.*tus$'
	'.ide$',
	'.*[nx]yl$',
	'.*ret$',
	'.*zoic$',
	'.*rile$',
	'.*xim.*',
	'.*rya.*',
	'.*rus$',
	'acyl.*',
	'acol.*',
	'acon.*',
	'.*sis',
	'.*lin',
	'.*rie',
	'.*rix',
	'.*z',
	'.*j',
	'.*ci',
	'.*[lk]os',
	'.*len',
	'.*azo.*',
	'.*ass.*',
	'.*wort.*'
	
]

for line in open('english_wordlist_new.txt', 'r'):
	should_write = True
	
	for pattern in no_pattern:
		if re.fullmatch(pattern, line.rstrip()):
			should_write = False
			break
	if len(line) > 9 and random.random() < 0.2:
		should_write = False
		
	if should_write:
		new_file.write(line)

new_file.close()
