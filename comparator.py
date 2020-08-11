import numpy as np
from scipy.sparse.linalg import lsqr
from random import choice

def expected_value_per_time_difference(comparison):
	log_value_diff = comparison[2]
	log_prob_success_diff = comparison[3]
	log_time_diff = comparison[4]

	log_EV_per_time_ratio = log_value_diff + log_prob_success_diff - log_time_diff
	return log_EV_per_time_ratio

def compute_rankings(comparisons):
	# Get unique list of UUID's
	uuids = set(c[0] for c in comparisons)
	uuids.update(set(c[1] for c in comparisons))
	uuids = list(uuids)
	uuid_to_index = {key:i for i,key in enumerate(uuids)} # key -> index

	# Produce a set of equations. Each of these is of the form (log[EV/time][1] - log[EV/time][2] = user input difference)
	equations = []
	results = []
	for c in comparisons:
		eq = np.zeros(len(uuids))
		eq[uuid_to_index[c[0]]] = 1
		eq[uuid_to_index[c[1]]] = -1
		equations.append(eq)

		results.append(expected_value_per_time_difference(c))

	equations = np.array(equations)
	results = np.array(results)

	# Solve with least squares
	res = lsqr(equations, results)

	return uuids, uuid_to_index, res[0]

def pick_next_comparison(full_uuids, comparisons):
	uuids, uuid_to_index, scores = compute_rankings(comparisons)

	# Expand the list of UUID's to include all entries, not just those with comparisons already.
	# We do this in a way that preserves the indexing of those with comparisons.
	counter = len(uuids)
	for u in full_uuids:
		if u not in uuid_to_index:
			uuid_to_index[u] = counter
			uuids.append(u)
			counter += 1

	# Count the number of comparisons each UUID is involved in
	comparison_counter = list(0 for _ in uuids)
	for c in comparisons:
		comparison_counter[uuid_to_index[c[0]]] += 1
		comparison_counter[uuid_to_index[c[1]]] += 1

	# We never repeat a comparison.
	already_done = set()
	for c in comparisons:
		already_done.add((uuid_to_index[c[0]],uuid_to_index[c[1]]))
		already_done.add((uuid_to_index[c[1]],uuid_to_index[c[0]]))

	# If any entries haven't had at least three comparisons,
	# pick one of those and a random other entry.
	for i,c in enumerate(comparison_counter):
		if c < 3:
			options = list(range(len(uuids)))
			options.remove(i)
			print(options)

			for done in already_done:
				if i == done[0] and done[1] in options:
					options.remove(done[1])
				if i == done[1] and done[0] in options:
					options.remove(done[0])

			print(options)

			if len(options) == 0:
				continue
			return (uuids[i], uuids[choice(options)])

	return None