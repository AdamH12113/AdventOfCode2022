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

# Okay, weird thought -- if we divide a valve's flow rate by the time it takes to get there,
# we get a proxy for how much pressure release we gain by opening a valve earlier. Let's
# see if this works.
proxy_vals = {v: flow_rates[v] / flow_distances[('AA', v)] for v in flow_valves}
valve_order = sorted(proxy_vals, key=proxy_vals.__getitem__, reverse = True)

active_capacity = 0
total_release = 0
minute = 1
location = 'AA'
for valve in valve_order:
	dt = flow_distances[(location, valve)]
	if minute + dt >= 30:
		print(f"Overtime: {valve} {minute} {dt}")
		dt = 31 - minute
		print(f"Reducing dt to {dt}")
		total_release += active_capacity * dt
		minute += dt
		print(f"  Release {active_capacity} * {dt} = {active_capacity * dt} -> {total_release}")
		break
	location = valve
	print(f"Minute {minute:02d}: Go to {valve} (dt = {dt})")
	minute += dt
	new_release = active_capacity * dt
	total_release += new_release
	print(f"  Release {active_capacity} * {dt} = {new_release} -> {total_release}")
	if minute > 30:
		print(f"Overtime: {minute}")
		break

	dt = 1
	print(f"Minute {minute:02d}: Open {valve} (dt = {dt})")
	minute += dt
	if minute > 30:
		print(f"Overtime: {minute}")
		break
	new_release = active_capacity * dt
	total_release += new_release
	print(f"  Release {active_capacity} * {dt} = {new_release} -> {total_release}")
	
	active_capacity += flow_rates[valve]
	print(f"  Active capacity +{flow_rates[valve]} -> {active_capacity}")
print(f"Minute {minute:02d}: Done opening valves")
if minute <= 30:
	total_release += (31 - minute) * active_capacity
	print(f"Final: Release {active_capacity} * {31 - minute} = {(31 - minute) * active_capacity} -> {total_release}")
print("Part 1: The maximum possible pressure that can be released is", total_release)
