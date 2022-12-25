import re, sys, copy, math
from functools import cmp_to_key

# Read the input
try:
	day_num = int(re.findall(r'\d+', __file__)[-1])
	filename_base = 'Example' if '--example' in sys.argv else 'Input'
	filename = filename_base + str(day_num) + '.txt'
	with open(filename, 'rt') as f:
		input_text = f.read()[:-1]
except Exception as e:
	print(f"Error reading input: [{exception.__class__.__name__}] {exception}")

# Process the input. It's a list of valves with associated flow rates and connecting tunnels.
valves = []
flow_rates = {}
raw_tunnels = {}
for line in input_text.split('\n'):
	names = re.findall(r'[A-Z][A-Z]', line)
	name = names[0]
	valves.append(name)
	flow_rate = int(re.findall(r'\d+', line)[0])
	raw_tunnels[name] = names[1:]
	flow_rates[name] = flow_rate

# Part 1: What is the maximum amount of pressure that can be released in 30 minutes? Many
# of the valves have no flow associated with them. Since there's no reason to ever stop at
# those, we can prune the connection graph by assigning different transit times to the tunnels.
flow_valves = sorted(valve for valve in flow_rates if flow_rates[valve] > 0)

def find_shortest_distance(valve1, valve2):
	if valve1 == valve2:
		return 0
	queue = [(valve1, 0)]
	distances = {valve1: 0}

	while len(queue) > 0:
		next_valve, cur_dist = queue.pop()
		if next_valve == valve2:
			continue
		for tunnel in raw_tunnels[next_valve]:
			if tunnel not in distances or distances[tunnel] > cur_dist + 1:
				distances[tunnel] = cur_dist + 1
				if tunnel != valve2:
					queue.insert(0, (tunnel, cur_dist + 1))
	return distances[valve2]

flow_distances = {}
for valve1 in ['AA'] + flow_valves:
	for valve2 in flow_valves:
		if valve1 == valve2:
			continue
		flow_distances[(valve1, valve2)] = find_shortest_distance(valve1, valve2)

# Let's try brute force. The 30-minute time limit puts a limit on how many valves we
# can open, so we shouldn't have to try anywhere near 15! combinations.
def flow_potential(minute, location, target):
	movement_cost = flow_distances[(location, target)]
	remaining_time = 30 - (minute + movement_cost + 1)
	return minute + movement_cost + 1, flow_rates[target] * remaining_time

def find_best_score(minute, location, remaining_valves, indent=0):
	if remaining_valves == []:
		return 0

	scores = []
	for valve in remaining_valves:
		new_minute, score = flow_potential(minute, location, valve)
		if new_minute > 30:
			scores.append(0)
		else:
			index = remaining_valves.index(valve)
			new_remaining = remaining_valves[:index] + remaining_valves[index+1:]
			scores.append(score + find_best_score(new_minute, valve, new_remaining, indent+1))
	return max(scores)

score = find_best_score(0, 'AA', flow_valves)
print("Part 1: The best possible score is", score)

# Part 2: We spent 4 of the 30 minutes training an elephant to help. Now there are two
# actors moving simultaneously. Unfortunately, they don't sync up, so our search code
# needs some work.
def find_best_team_score(minute, location, remaining_valves, indent=0):
	if indent == 0:
		print(' '*indent, minute, location, remaining_valves)
	if remaining_valves == []:
		return 0

	scores = []
	for valve in remaining_valves:
		new_minute, score = flow_potential(minute, location, valve)
		if new_minute > 30:
			scores.append(0)
		else:
			index = remaining_valves.index(valve)
			new_remaining = remaining_valves[:index] + remaining_valves[index+1:]
			scores.append(score + find_best_team_score(new_minute, valve, new_remaining, indent+1))
	if indent == 0:
		print(' '*(indent+1), scores)
	return max(scores)





