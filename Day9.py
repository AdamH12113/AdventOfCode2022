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

# Process the input, which is a list of horizontal and vertical movements.
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
	
	# Total abuse of operator overloading
	def __truediv__(self, dir2):
		delta = self - dir2
		adx = abs(delta.dx)
		ady = abs(delta.dy)
		if abs(delta) <= 1:
			return Vector(0,0)
		elif adx >= 2 and ady == 0:
			return Vector(delta.dx // adx, 0)
		elif ady >= 2 and adx == 0:
			return Vector(0, delta.dy // ady)
		else:
			return Vector(delta.dx // adx, delta.dy // ady)
	
	def __str__(self):
		return f"({self.dx},{self.dy})"
	def __repr__(self):
		return f"Vector({self.dx},{self.dy})"

moves_text = input_text.split('\n')
move_dirs = {'L': Vector(-1,0), 'R': Vector(1,0), 'U': Vector(0,1), 'D': Vector(0,-1)}
moves = [(move_dirs[m.split(' ')[0]], int(m.split(' ')[1])) for m in moves_text]

# Part 1: Following the moves, how many locations does the tail visit at least once?
head = Vector(0,0)
tail = Vector(0,0)
visited = set()

for dir, dist in moves:
	for n in range(dist):
		head += dir
		td = head / tail
		tail += td
		visited.add((tail.dx, tail.dy))
print("Part 1: The number of locations visited is", len(visited))

# Part 2: Now there are ten knots in the rope. How many locations does the tail visit?
knots = [Vector(0,0) for n in range(10)]
visited = set()
for dir, dist in moves:
	for d in range(dist):
		knots[0] += dir
		for k in range(1, len(knots)):
			td = knots[k-1] / knots[k]
			knots[k] += td
		visited.add((knots[9].dx, knots[9].dy))
print("Part 2: The number of locations visited is", len(visited))
