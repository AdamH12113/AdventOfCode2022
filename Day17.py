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

# Process the input. It's a sequence of left and right movements for a Tetris-like game. Since
# it's just a one-line string, no processing is necessary.
moves = input_text

# Part 1: After 2022 rocks have stopped falling, how tall will the tower be? I am
# 99% sure the rocks will have to rotate, but until we know exactly how there's
# no point in worrying about it.
class Rock:
	def __init__(self, rock_type, highest_y):
		self.x = 2 if rock_type != 'plus' else 3
		self.y = highest_y + 4
		self.rock_type = rock_type
		self.stopped = False
		self.update_ranges()

	# Get the coordinates with an optional offset for collision detection
	def get_coords(self, dx, dy):
		x,y = self.x + dx, self.y + dy
		if self.rock_type == 'hline':
			# Anchored on the leftmost square
			return [(x,y), (x+1,y), (x+2,y), (x+3,y)]
		elif self.rock_type == 'plus':
			# Anchored on the bottom square
			return [(x,y), (x,y+1), (x-1,y+1), (x+1,y+1), (x,y+2)]
		elif self.rock_type == 'L':
			# Anchored on the bottom-left square
			return [(x,y), (x+1,y), (x+2,y), (x+2,y+1), (x+2,y+2)]
		elif self.rock_type == 'vline':
			# Anchored on the bottom square
			return [(x,y), (x,y+1), (x,y+2), (x,y+3)]
		elif self.rock_type == 'square':
			# Anchored on the bottom-left square
			return [(x,y), (x+1,y), (x,y+1), (x+1,y+1)]
		else:
			print(f"Bad rock type {self.rock_type}")
	
	def move(self, direction):
		if direction == '<':
			self.x -= 1
		elif direction == '>':
			self.x += 1
		elif direction == 'v':
			self.y -= 1
		self.update_ranges()

	def update_ranges(self):
		x, y = self.x, self.y
		if self.rock_type == 'hline':
			self.minx = x
			self.maxx = x + 3
			self.miny = y
			self.maxy = y
		elif self.rock_type == 'plus':
			self.minx = x - 1
			self.maxx = x + 1
			self.miny = y
			self.maxy = y + 2
		elif self.rock_type == 'L':
			self.minx = x
			self.maxx = x + 2
			self.miny = y
			self.maxy = y + 2
		elif self.rock_type == 'vline':
			self.minx = x
			self.maxx = x
			self.miny = y
			self.maxy = y + 3
		elif self.rock_type == 'square':
			self.minx = x
			self.maxx = x + 1
			self.miny = y
			self.maxy = y + 1
	
	def __str__(self):
		return f"Rock ({self.x},{self.y})"
	def __repr__(self):
		return str(self)


def move_would_collide(rock, direction, rocks):
	possible_colliders = [r for r in rocks if r.y >= rock.y - 6 and r.y <= rock.y + 6]
	if direction == '<':
		if rock.minx <= 0:
			return True
		dx = -1
		dy = 0
	elif direction == '>':
		if rock.maxx >= 6:
			return True
		dx = 1
		dy = 0
	elif direction == 'v':
		if rock.miny <= 0:
			return True
		dx = 0
		dy = -1
	rock_coords = rock.get_coords(dx, dy)
	for pc in possible_colliders:
		pc_coords = pc.get_coords(0, 0)
		for coord in rock_coords:
			if coord in pc_coords:
				return True
	return False
		
def print_rocks(rocks):
	squares = set()
	for rock in rocks:
		for coord in rock.get_coords(0,0):
			squares.add(coord)

	for y in range(15, -1, -1):
		for x in range(7):
			print('#' if (x,y) in squares else '.', end='')
		print()
	print()


rock_order = ['hline', 'plus', 'L', 'vline', 'square']
rocks = []
highest_y = -1
move = 0
for rock_num in range(10):
	rock = Rock(rock_order[rock_num % len(rock_order)], highest_y)
	while not rock.stopped:
		next_move = moves[move % len(moves)]
		move += 1
		if not move_would_collide(rock, next_move, rocks):
			rock.move(next_move)
			print_rocks(rocks + [rock])
		
		if move_would_collide(rock, 'v', rocks):
			rock.stopped = True
			highest_y = rock.maxy
			rocks.append(rock)
		else:
			rock.move('v')
			print_rocks(rocks + [rock])

print("Part 1: After 2022 rocks, the tower will be", highest_y, "units tall.")
