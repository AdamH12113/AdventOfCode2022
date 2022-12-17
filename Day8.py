import re, sys, copy

# Read the input
try:
	day_num = int(re.findall(r'\d+', __file__)[-1])
	filename_base = 'Example' if '--example' in sys.argv else 'Input'
	filename = filename_base + str(day_num) + '.txt'
	with open(filename, 'rt') as f:
		input_text = f.read()[:-1]
except Exception as e:
	print(f"Error reading input: [{exception.__class__.__name__}] {exception}")

# Process the input. It's a grid of numbers, each of which represents the height
# of a tree.
heights = [[int(col) for col in row] for row in input_text.split('\n')]
xsize = len(heights[0])
ysize = len(heights)

# Part 1: How many trees are visible from outside the grid? A visible tree is
# taller than any tree between it and the edge in at least one direction.
def is_tree_visible(heights, x, y):
	height = heights[y][x]

	# Edge trees are always visible
	if x == 0 or x == xsize - 1 or y == 0 or y == ysize - 1:
		return True
	
	heights_north = [heights[yn][x] for yn in range(0, y)]
	heights_south = [heights[ys][x] for ys in range(y+1,ysize)]
	heights_west = [heights[y][xw] for xw in range(0, x)]
	heights_east = [heights[y][xe] for xe in range(x+1, xsize)]
	
	north_clear = all(h < height for h in heights_north)
	south_clear = all(h < height for h in heights_south)
	west_clear = all(h < height for h in heights_west)
	east_clear = all(h < height for h in heights_east)

	return north_clear or south_clear or west_clear or east_clear

num_visible = sum(is_tree_visible(heights, x, y) for y in range(ysize) for x in range(xsize))
print("Part 1: There are", num_visible, "trees visible")

# Part 2: Find the maximum number of trees visible from any one location.
def get_scenic_score(heights, xh, yh):
	height = heights[yh][xh]

	# Count west
	west_visible = 0
	for x in range(xh-1, 0-1, -1):
		west_visible += 1
		if heights[yh][x] >= height:
			break

	# Count east
	east_visible = 0
	for x in range(xh+1, xsize, 1):
		east_visible += 1
		if heights[yh][x] >= height:
			break

	# Count north
	north_visible = 0
	for y in range(yh-1, 0-1, -1):
		north_visible += 1
		if heights[y][xh] >= height:
			break

	# Count south
	south_visible = 0
	for y in range(yh+1, ysize, 1):
		south_visible += 1
		if heights[y][xh] >= height:
			break

	return north_visible * south_visible * east_visible * west_visible

scenic_scores = [get_scenic_score(heights, x, y) for y in range(ysize) for x in range(xsize)]
print("Part 2: The maximum scenic score is", max(scenic_scores))
