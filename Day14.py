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

# Process the input. It's a series of X/Y coordinates of rock beams. I can already tell
# that this one is going to be trouble. Let's borrow the Vector class from day 9 to
# use for coordinates.
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
	
	def __abs__(self):
		return max(abs(self.dx), abs(self.dy))
	
	# Total abuse of operator overloading. Gives a unit vector.
	def __truediv__(self, dir2):
		delta = self - dir2
		adx = abs(delta.dx)
		ady = abs(delta.dy)
		if adx == 0 and ady == 0:
			return Vector(0, 0)
		elif adx == 0:
			return Vector(0, delta.dy // ady)
		elif ady == 0:
			return Vector(delta.dx // adx, 0)
		else:
			return Vector(delta.dx // adx, delta.dy // ady)
	
	def __iter__(self):
		yield self.dx
		yield self.dy
	
	def __str__(self):
		return f"({self.dx},{self.dy})"
	def __repr__(self):
		return f"Vector({self.dx},{self.dy})"

# Extract the beam endpoint coordinates
beam_sets_text = input_text.split('\n')
beam_sets = [[Vector(int(c.split(',')[0]), int(c.split(',')[1])) for c in b.split(' -> ')] for b in beam_sets_text]
minx = min(v.dx for bs in beam_sets for v in bs)
maxx = max(v.dx for bs in beam_sets for v in bs)
miny = min(v.dy for bs in beam_sets for v in bs)
maxy = max(v.dy for bs in beam_sets for v in bs)

# Fill in the beams
beam_blocks = set()
for bs in beam_sets:
	for cn in range(len(bs) - 1):
		# This double-add the joining coordinates, but that's fine
		unit_vector = bs[cn+1] / bs[cn]
		for step in range(abs(bs[cn+1] - bs[cn]) + 1):
			step_vector = bs[cn] + unit_vector*step
			beam_blocks.add(tuple(step_vector))

# Part 1: How many units of sand come to rest before sand starts flowing into the abyss below?
obstacles = copy.deepcopy(beam_blocks)
settled_sand = set()
sand_units = 0
sand_spilled = False
while not sand_spilled:
	cx = 500
	cy = 0
	
	while True:
		if cy > maxy:
			sand_spilled = True
			break
		elif (cx,cy+1) not in obstacles and (cx,cy+1) not in settled_sand:
			cy += 1
		elif (cx-1,cy+1) not in obstacles and (cx-1,cy+1) not in settled_sand:
			cx -= 1
			cy += 1
		elif (cx+1,cy+1) not in obstacles and (cx+1,cy+1) not in settled_sand:
			cx += 1
			cy += 1
		else:
			settled_sand.add((cx,cy))
			sand_units += 1
			break

print("Part 1:", sand_units, "sand units came to rest before spilling into the abyss.")

# Part 2: Assuming an infinitely wide floor at maxy + 2, how many units of sand fall
# before the source at (500, 0) is blocked?
obstacles = copy.deepcopy(beam_blocks)
settled_sand = set()
sand_units = 0
source_blocked = False
while not source_blocked:
	cx = 500
	cy = 0
	
	while True:
		if cy == maxy + 1:
			settled_sand.add((cx,cy))
			sand_units += 1
			break
		elif (cx,cy+1) not in obstacles and (cx,cy+1) not in settled_sand:
			cy += 1
		elif (cx-1,cy+1) not in obstacles and (cx-1,cy+1) not in settled_sand:
			cx -= 1
			cy += 1
		elif (cx+1,cy+1) not in obstacles and (cx+1,cy+1) not in settled_sand:
			cx += 1
			cy += 1
		else:
			settled_sand.add((cx,cy))
			sand_units += 1
			if cx == 500 and cy == 0:
				source_blocked = True
			break

print("Part 2:", sand_units, "sand units came to rest before blocking the source.")
