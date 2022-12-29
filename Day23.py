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

# Process the input. For convenience, we'll let south and east be positive.
input_lines = input_text.split('\n')
elf_starts = set()
for y in range(len(input_lines)):
	for x in range(len(input_lines[y])):
		if input_lines[y][x] == '#':
			elf_starts.add((x,y))

# We need to do a lot of coordinate manipulation, so let's borrow the old Vector class.
class Vector:
	def __init__(self, dx, dy):
		self.dx = dx
		self.dy = dy

	def __mul__(self, c):
		return Vector(self.dx * c, self.dy * c)
	
	def __add__(self, dir2):
		return Vector(self.dx + dir2.dx, self.dy + dir2.dy)
	
	def __sub__(self, dir2):
		return Vector(self.dx - dir2.dx, self.dy - dir2.dy)
	
	def __iter__(self):
		yield self.dx
		yield self.dy
	def __str__(self):
		return f"({self.dx},{self.dy})"
	def __repr__(self):
		return f"Vector({self.dx},{self.dy})"

north_vectors = [Vector(-1,-1), Vector(0,-1), Vector(1,-1)]
south_vectors = [Vector(-1,1), Vector(0,1), Vector(1,1)]
west_vectors = [Vector(-1,-1), Vector(-1,0), Vector(-1,1)]
east_vectors = [Vector(1,-1), Vector(1,0), Vector(1,1)]
surrounding_vectors = [Vector(-1,-1), Vector(0,-1), Vector(1,-1), Vector(1,0), Vector(1,1), Vector(0,1), Vector(-1,1), Vector(-1,0)]

# Part 1: After 10 rounds of following the movement rules, how many empty ground tiles are
# contained in the smallest rectangle that also contains all of the elves?
def get_coordinate_boundaries(elves):
	xmin = min(e[0] for e in elves)
	xmax = max(e[0] for e in elves)
	ymin = min(e[1] for e in elves)
	ymax = max(e[1] for e in elves)
	return xmin, ymin, xmax, ymax

def print_elves(elves):
	xmin, ymin, xmax, ymax = get_coordinate_boundaries(elves)
	for y in range(ymin, ymax+1):
		for x in range(xmin, xmax+1):
			print('#' if (x,y) in elves else '.', end='')
		print()
	
def do_round(elves, dir_sets):
	# First half: Create the list of proposed movements
	skip_count = 0
	proposals = {}
	for elf in elves:
		ev = Vector(*elf)
		surroundings = [ev + dir for dir in surrounding_vectors]
		if any(tuple(neighbor) in elves for neighbor in surroundings):
			for directions in dir_sets:
				adj_v = [ev + dir for dir in directions]
				empty = all(tuple(av) not in elves for av in adj_v)
				if empty:
					proposal = tuple(adj_v[1])
					break
			else:
				proposal = elf
		else:
			proposal = elf
		if proposal in proposals:
			proposals[proposal].add(elf)
		else:
			proposals[proposal] = set([elf])
		if proposal == elf:
			skip_count += 1
	
	# Second half: Update elf positions, removing duplicates in the process
	new_elves = set()
	for p in proposals:
		candidates = proposals[p]
		if len(candidates) == 1:
			new_elves.add(p)
		else:
			new_elves.update(candidates)
	return new_elves, skip_count == len(new_elves)
		
elves_p1 = copy.deepcopy(elf_starts)
direction_sets = [north_vectors, south_vectors, west_vectors, east_vectors]
for round in range(10):
	elves_p1 = do_round(elves_p1, direction_sets)[0]
	direction_sets = direction_sets[1:] + direction_sets[:1]

xmin, ymin, xmax, ymax = get_coordinate_boundaries(elves_p1)
empty_tiles = sum((x,y) not in elves_p1 for y in range(ymin, ymax+1) for x in range(xmin, xmax+1))
print("Part 1: The number of empty ground tiles in the bounding rectangle is", empty_tiles)

# Part 2: What is the number of the first round where no elf moves? A simple modification
# of the do_round() function can handle this.
elves_p2 = copy.deepcopy(elf_starts)
direction_sets = [north_vectors, south_vectors, west_vectors, east_vectors]
round = 1
while True:
	elves_p2, no_movement = do_round(elves_p2, direction_sets)
	direction_sets = direction_sets[1:] + direction_sets[:1]
	if no_movement:
		break
	round += 1
print("Part 2: The first round where no elf moved was", round)
