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

# Process the input. Each line contains sensor coordinates associated with the coordinates
# of the nearest beacon. Let's reuse the vector class from yesterday.
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
	
	# Changed to give the Manhattan distance
	def __abs__(self):
		return abs(self.dx) + abs(self.dy)
	
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

relations = {}
for line in input_text.split('\n'):
	ns = [int(n) for n in re.findall(r'-?\d+', line)]
	relations[(ns[0], ns[1])] = (ns[2], ns[3])
sensors = set(relations.keys())
beacons = set(relations.values())
all_coords = list(sensors) + list(beacons)
ranges = {s: abs(b[0] - s[0]) + abs(b[1] - s[1]) for s,b in relations.items()}

max_range = max(ranges.values())
minx = min(c[0] for c in all_coords) - max_range
maxx = max(c[0] for c in all_coords) + max_range
miny = min(c[1] for c in all_coords) - max_range
maxy = min(c[1] for c in all_coords) + max_range

# Part 1: How many positions in row y=2,000,000 cannot contain a beacon? This is slow,
# but it works.
y_coord = 10 if '--example' in sys.argv else 2000000
exclusion_count = 0
for x in range(minx, maxx+1):
	if (x, y_coord) in beacons:
		continue
	for s in sensors:
		dist = abs(s[0] - x) + abs(s[1] - y_coord)
		if ranges[s] >= dist:
			exclusion_count += 1
			break

print("Part 1: There are", exclusion_count, "locations that cannot contain a beacon.")

# Part 2: Where is the one position between (0,0) and (4000000,4000000) that can
# contain a beacon? [(0,0) to (20,20) for the example.] Clearly we're not going
# to brute-force this one, so something clever is required. In order for there to
# be a gap, there has to be a group of sensors whose distance is two greater than
# the sum of their ranges. If we limit the search space to those, it should make
# the problem more tractable.
closest_sensors = set()
for s1 in ranges:
	for s2 in ranges:
		dist = abs(s2[0] - s1[0]) + abs(s2[1] - s1[1])
		range_sum = ranges[s1] + ranges[s2]
		if dist == range_sum + 2:
			closest_sensors.add(s1)
			closest_sensors.add(s2)

# That does indeed make the problem more tractable -- now there are (with my
# input) only four sensors to worry about! Unfortunately, there's still a vast
# space between them. Let's search along the perimeters of the sensor ranges.
points = set()
for s in closest_sensors:
	x,y = s
	r = ranges[s] + 1
	
	for shift in range(0, r+1):
		points.add((x + (r - shift), y + shift))
		points.add((x + (r - shift), y - shift))
		points.add((x - (r - shift), y + shift))
		points.add((x - (r - shift), y - shift))


# Still slow, but it still works.
minx = min(s[0] for s in closest_sensors)
maxx = max(s[0] for s in closest_sensors)
miny = min(s[1] for s in closest_sensors)
maxy = max(s[1] for s in closest_sensors)

for p in points:
	if p[0] < minx or p[0] > maxx or p[1] < miny or p[1] > maxy:
		continue
	found = True
	for s in sensors:
		dist = abs(p[0] - s[0]) + abs(p[1] - s[1])
		if dist <= ranges[s]:
			found = False
	if found:
		print("Part 2: Found the missing beacon at", (p[0],p[1]), "with tuning frequency", 4000000*p[0] + p[1])
		break
