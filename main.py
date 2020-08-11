import numpy as np
from glob import glob
from uuid import UUID
from rich.console import Console
from rich.markdown import Markdown
from rich.table import Table
from uuids import add_uuids, get_uuid
from comparator import compute_rankings, pick_next_comparison
console = Console()



g = glob('/Users/ajermyn/Dropbox/Notes/Brainstorming/*.md', recursive=True) # Find Files

g = g[:2]

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

# Enter comparison loop
with open('/Users/ajermyn/Dropbox/Notes/Priorities/comparisons.dat','a') as fi:
	next_comparison = pick_next_comparison(uuids, comparisons)
	while next_comparison is not None:
		# Unpack the next comparison
		i,j = next_comparison

		# Print the comparison
		grid = Table.grid(expand=True)
		grid.add_column()
		grid.add_column()
		grid.add_row(Markdown(flat_split_contents[i]), Markdown(flat_split_contents[j]))
		console.print(grid)

		# Get the comparison data from the user
		delta_log_value = float(console.input('Enter ln[Value if Left if Successful / Value if Right is Successful]: '))
		delta_log_p = float(console.input('Enter ln[Prob[Left is Successful] / Proba[Right is Successful]]: '))
		delta_log_time = float(console.input('Enter ln[Time Estimate for Left / Time Estimate for Right]: '))

		# Store the comparison
		comparisons.append([i, j, delta_log_value, delta_log_p, delta_log_time])
		fi.write(' '.join(map(str, comparisons[-1])) + '\n')

		# Pick the next comparison
		next_comparison = pick_next_comparison(uuids, comparisons)


uuids, uuid_to_index, scores = compute_rankings(comparisons)
inds = np.argsort(scores)[::-1]
for i in inds:
	console.print(Markdown(flat_split_contents[uuids[i]]))
	console.print('Expected Value / Time = ', round(np.exp(scores[i]),2))