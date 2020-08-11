from uuid import UUID
from glob import glob
from uuids import add_uuids, get_uuid

g = glob('/Users/ajermyn/Dropbox/Notes/Brainstorming/*.md', recursive=True) # Find Files
g = g + ['/Users/ajermyn/Dropbox/Notes/Priorities/active_projects.md']

# Add UUID's if they aren't already in the files
for fi in g:
	add_uuids(fi)

files = (open(fname, 'r') for fname in g) # Open files
contents = (fi.read() for fi in files) # Read files
split_contents = (content.split('# ') for content in contents) # Split on '# ' to get headers
flat_split_contents = (content for split_content in split_contents for content in split_content) # Flatten
flat_split_contents = (content.strip() for content in flat_split_contents) # Strip whitespace
flat_split_contents = (content for content in flat_split_contents if len(content) > 0) # Filter out empty entries
flat_split_contents = (content for content in flat_split_contents if content != '\n') # Filter out empty newlines
flat_split_contents = ('# ' + content for content in flat_split_contents) # Re-add initial Markdown character
flat_split_contents = {get_uuid(content):content for content in flat_split_contents} # Parses to a dictionary keyed by UUID

uuids = list(flat_split_contents.keys())

# Parse the comparisons file
comparisons = []
with open('/Users/ajermyn/Dropbox/Notes/Priorities/comparisons.dat','r') as fi:
	for line in fi:
		# s[0] is the first UUID, s[1] is the second UUID.
		s = line.strip('\n').strip().split(' ')
		s[0] = UUID(s[0])
		s[1] = UUID(s[1])
		for i in range(2,len(s)):
			s[i] = float(s[i])
		comparisons.append(s)