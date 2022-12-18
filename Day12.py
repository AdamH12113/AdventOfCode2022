import re, sys, copy, math

# Read the input
try:
	day_num = int(re.findall(r'\d+', __file__)[-1])
	filename_base = 'Example' if '--example' in sys.argv else 'Input'
	filename = filename_base + str(day_num) + '.txt'
	with open(filename, 'rt') as f:
		input_text = f.read()[:-1]
except Exception as e:
	print(f"Error reading input: [{exception.__class__.__name__}] {exception}")

# Process the input. It's a 2D heightmap where heights are represented as letter from
# a (lowest) to z (highest), with special start and end characters S and E being of
# heights a and z, respectively.
heights = input_text.split('\n')
maxx = len(heights[0]) - 1
maxy = len(heights) - 1
start = [(x, y) for y in range(maxy+1) for x in range(maxx+1) if heights[y][x] == 'S'][0]
end = [(x, y) for y in range(maxy+1) for x in range(maxx+1) if heights[y][x] == 'E'][0]

# Part 1: What is the fewest number of steps required to move from start to end? We can
# only move up a single height level, although we can move down any number of height levels.
# It's time for our old friend, the breadth-first search.
def run_bfs(queue, distances, direction = 'up'):
	while (len(queue) > 0):
		x, y, cur_dist = queue.pop()
		height = heights[y][x]
		if height == 'S':
			height = 'a'
		if height == 'E':
			height = 'z'
		
		# Add the neighboring spaces to the queue if possible
		new_dist = cur_dist + 1
		for option in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]:
			nx, ny = option
			if nx < 0 or nx > maxx or ny < 0 or ny > maxy:
				continue

			nh = heights[ny][nx]
			if nh == 'E':
				nh = 'z'
			if nh == 'S':
				nh = 'a'

			if (nx, ny) in distances and distances[(nx,ny)] <= new_dist:
				continue
			dh = ord(nh) - ord(height)
			if direction == 'up' and dh > 1:
				continue
			if direction == 'down' and dh < -1:
				continue
			
			# Update the distances here to prevent duplicate queue entries
			distances[(nx,ny)] = new_dist
			queue.insert(0, (nx, ny, new_dist))
	return distances

best_distances = run_bfs([(start[0], start[1], 0)], {start: 0})
print("Part 1: It takes", best_distances[(end[0], end[1])], "steps to reach the end.")

# Part 2: Now we need to find the shortest path from the ending point to any location
# with height a. It's still basically the same BFS, though.
best_distances = run_bfs([(end[0], end[1], 0)], {end: 0}, direction = 'down')
a_distances = [best_distances[c] for c in best_distances if heights[c[1]][c[0]] == 'a']
print("Part 2: The shorest path from the end to an a-height location is", min(a_distances))


