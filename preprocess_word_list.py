import re

patterns_that_is_unlikely_to_match = [
	r".*[0123456789\-.,'&\/\\].*",
	'^z[uw].*',
	'.*aa.*',
	'.*ux$',
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
	'.*sis$',
	'.*lin$',
	'.*rie$',
	'.*rix$',
	'.*j$',
	'.*ci$',
	'.*[lk]os$',
	'.*len$',
	'.*azo.*',
	'.*ass.*',
	'.*wort.*',
	'.*z{2,}.*',
	'.*pek$',
]

_PRINT_RATE_ = 10000

if __name__ == '__main__':
	add_count = 0
	remove_count = 0
	draw = 0
	
	source = ''
	target = ''
	
	new_file = open(target, 'w')
	
	for line in open(source, 'r'):
		should_write = True
		
		if line.rstrip().isupper():
			# might consider this for speed?
			should_write = False
		
		line = line.lower()
		if should_write:
			for pattern in patterns_that_is_unlikely_to_match:
				if re.fullmatch(pattern, line.rstrip()):
					should_write = False
					break
		
		if (
				should_write
				and len(line) > 13
				# as 'unfortunately' has length 13
				or (len(line.rstrip()) == 1
				    and line.rstrip() != 'a'
				    and line.rstrip() != 'i')
		):
			should_write = False
		elif not re.fullmatch(r'.*[aeiouy].*', line.rstrip()):
			should_write = False
		
		if should_write:
			new_file.write(line.lower())
			add_count += 1
			if add_count // _PRINT_RATE_ != draw:
				draw = add_count // _PRINT_RATE_
				print('.', end='')
		else:
			remove_count += 1
	
	print()
	print("add_count %s" % add_count)
	print("remove_count %s" % remove_count)
	
	new_file.close()
