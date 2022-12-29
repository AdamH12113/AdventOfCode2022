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

# Process the input. We get a 2D map followed by a list of movement instructions.
raw_map, raw_instructions = input_text.split('\n\n')
raw_map_lines = raw_map.split('\n')
map_tiles = {}
rmax = len(raw_map_lines)
cmax = max(len(raw_map_lines[r]) for r in range(rmax))
for row in range(rmax):
	for col in range(len(raw_map_lines[row])):
		char = raw_map_lines[row][col]
		if char == '.':
			map_tiles[(col, row)] = True
		elif char == '#':
			map_tiles[(col, row)] = False
start_pos = (raw_map_lines[0].index('.'), 0)

inst_numbers = [int(n) for n in re.findall(r'\d+', raw_instructions)]
inst_letters = [c for c in re.findall(r'[LR]', raw_instructions)]

# Trick for interleaving from Stack Overflow: https://stackoverflow.com/a/7947461/5220760
instructions = inst_numbers + inst_letters
instructions[::2] = inst_numbers
instructions[1::2] = inst_letters

# It's time for vectors again!
class Vector:
	def __init__(self, dx, dy):
		self.dx = dx
		self.dy = dy
	
	# Our coordinate system is mirrored (positive y = down), so the rotation matrix is
	# backwards from normal.
	def rotate(self, direction):
		if direction == 'L':
			return Vector(self.dy, -self.dx)
		else:
			return Vector(-self.dy, self.dx)

	def __mul__(self, c):
		return Vector(self.dx * c, self.dy * c)
	
	def __add__(self, dir2):
		return Vector(self.dx + dir2.dx, self.dy + dir2.dy)
	
	def __sub__(self, dir2):
		return Vector(self.dx - dir2.dx, self.dy - dir2.dy)
	
	def __neg__(self):
		return Vector(-self.dx, -self.dy)
	
	def __iter__(self):
		yield self.dx
		yield self.dy
	def __str__(self):
		return f"({self.dx},{self.dy})"
	def __repr__(self):
		return f"Vector({self.dx},{self.dy})"

# Our coordinate system is mirrored (positive y = down), so the rotation matrix is
# backwards from normal.
right = (1,0)
left = (-1, 0)
up = (0, -1)
down = (0, 1)

# Part 1: Follow the directions. What are the final row, column, and facing?
def move(vpos, vface):
	next_pos = tuple(vpos + vface)
	if next_pos not in map_tiles:
		# Wrap around
		vnext = vpos
		while True:
			vnext -= vface
			if tuple(vnext - vface) not in map_tiles:
				break
		next_pos = tuple(vnext)
		
	if map_tiles[next_pos]:
		return Vector(*next_pos)
	else:
		return vpos

def print_map(pos, face):
	for r in range(rmax):
		for c in range(cmax):
			if (c,r) == tuple(pos):
				if tuple(face) == right:
					print('>', end='')
				elif tuple(face) == up:
					print('^', end='')
				elif tuple(face) == left:
					print('<', end='')
				else:
					print('v', end='')
			else:
				if (c,r) in map_tiles:
					print('.' if map_tiles[(c,r)] else '#', end='')
				else:
					print(' ', end='')
		print()

pos = Vector(*start_pos)
face = Vector(1, 0)
for inst in instructions:
	if type(inst) is int:
		for step in range(inst):
			next_pos = move(pos, face)
			if next_pos == pos:
				break
			pos = next_pos
#			print('\n' * 9)
#			print(pos,face)
#			print_map(pos, face)
	else:
		face = face.rotate(inst)
#		print('\n' * 9)
#		print(pos,face)
#		print_map(pos, face)

col = pos.dx + 1
row = pos.dy + 1
facing = 0 if tuple(face) == right else 1 if tuple(face) == down else 2 if tuple(face) == left else 3
print(row, col, facing)
print("Part 1: The final password is", 1000*row + 4*col + facing)

# Part 2: Oh no, now the map represents the surface of a cube and walking off an edge
# can change both position and direction in odd ways.



