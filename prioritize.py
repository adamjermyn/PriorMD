import numpy as np
from glob import glob
from rich.console import Console
from rich.markdown import Markdown
from rich.table import Table
from comparator import compute_rankings, pick_next_comparison
from parser import uuids, flat_split_contents, comparisons, uuids_active
console = Console()

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
		delta_log_value = float(console.input('Enter log3[Value if Left if Successful / Value if Right is Successful]: '))
		delta_log_p = float(console.input('Enter log3[Prob[Left is Successful] / Prob[Right is Successful]]: '))
		delta_log_time = float(console.input('Enter log3[Time Estimate for Left / Time Estimate for Right]: '))
		#delta_log_value = np.random.rand()
		#delta_log_p = np.random.rand()
		#delta_log_time = np.random.rand()

		# Store the comparison
		comparisons.append([i, j, delta_log_value, delta_log_p, delta_log_time])
		fi.write(' '.join(map(str, comparisons[-1])) + '\n')
		fi.flush()

		# Pick the next comparison
		next_comparison = pick_next_comparison(uuids, comparisons)

# Print sorted list by score and make prioritized list
with open('/Users/ajermyn/Dropbox/Notes/Priorities/prioritized.md', 'w+') as fi:
	uuids, uuid_to_index, scores = compute_rankings(comparisons)
	inds = np.argsort(scores)[::-1]
	for i in inds:
		if 'ALREADY DONE' in flat_split_contents[uuids[i]] or 'COMPLETE' in flat_split_contents[uuids[i]]:
			continue

		score = round(3**(scores[i]),2)

		description = flat_split_contents[uuids[i]]
		description = description.split('\n')

		if uuids[i] in uuids_active:
			description[0] = '# *' + description[0][2:]

		description[1] = description[1] + ' **Score = ' + str(score) + '**'
		description = '\n'.join(description)

		console.print(Markdown(flat_split_contents[uuids[i]]))
		console.print('Expected Value / Time = ', score)

		fi.write(description)
		fi.write('\n')
		fi.write('\n')
		fi.flush()

# Print only active, sorted list by score and make prioritized list
with open('/Users/ajermyn/Dropbox/Notes/Priorities/active_prioritized.md', 'w+') as fi:
	uuids, uuid_to_index, scores = compute_rankings(comparisons)
	inds = np.argsort(scores)[::-1]
	for i in inds:
		if uuids[i] not in uuids_active:
			continue

		if 'ALREADY DONE' in flat_split_contents[uuids[i]] or 'COMPLETE' in flat_split_contents[uuids[i]]:
			continue

		score = round(10**(scores[i]/2),2)
		description = flat_split_contents[uuids[i]]
		description = description.split('\n')
		description[1] = description[1] + ' **Score = ' + str(score) + '**'
		description = '\n'.join(description)

		console.print(Markdown(flat_split_contents[uuids[i]]))
		console.print('Expected Value / Time = ', score)

		fi.write(description)
		fi.write('\n')
		fi.write('\n')
		fi.flush()
