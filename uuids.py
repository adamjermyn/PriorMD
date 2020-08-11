from uuid import uuid1, UUID

def add_uuids(fname):
	# Adds UUID's to each entry in a file if the entry doesn't already have one as the first line below the header.

	with open(fname, 'r') as fi:
		contents = []
		counter = 0
		for line in fi:
			contents.append(line)
			counter += 1
			if counter >= 2 and '# ' in contents[-2] and 'UUID' not in contents[-1]:
				contents.insert(-1, '- UUID: ' + str(uuid1()) + '\n')

	with open(fname, 'w') as fi:	
		for line in contents:
			fi.write(line)

def get_uuid(contents):
	# Parses the UUID from an entry.

	c = contents.split('\n') # Split by lines
	for line in c:
		if '- UUID: ' in line:
			uid = UUID(line.split('- UUID: ')[1])
			return uid