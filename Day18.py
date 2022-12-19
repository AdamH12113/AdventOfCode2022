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

# Process the input. Each line contains the X, Y, and Z coordinates of a cube.
cubes = [tuple(int(c) for c in re.findall(r'\d+', line)) for line in input_text.split('\n')]

# Part 1: Count the number of sides on each cube that are not immediately connected
# to another cube. We can abuse Python's implicit boolean -> int conversion for more
# concise code.
open_side_count = 0
for cube in cubes:
	x,y,z = cube
	open_side_count += (x+1,  y,  z) not in cubes
	open_side_count += (x-1,  y,  z) not in cubes
	open_side_count += (  x,y+1,  z) not in cubes
	open_side_count += (  x,y-1,  z) not in cubes
	open_side_count += (  x,  y,z+1) not in cubes
	open_side_count += (  x,  y,z-1) not in cubes

print("Part 1: The number of open sides is", open_side_count)

# Part 2: What is the exterior surface area of the cube structure? We need to ignore
# any air pockets trapped within the cubes. First, we can construct a list of empty
# spaces that border the cube structure, then count the cube faces adjacent to those.
maxx = max(c[0] for c in cubes)
maxy = max(c[1] for c in cubes)
maxz = max(c[2] for c in cubes)
minx = min(c[0] for c in cubes)
miny = min(c[1] for c in cubes)
minz = min(c[2] for c in cubes)

# We can do a breadth-first search starting from the boundary of the cube region to
# fill in the exterior empty spaces.
queue = [(minx-1,miny-1,minz-1)]
exterior_spaces = [(minx-1,miny-1,minz-1)]
while len(queue) > 0:
	xc,yc,zc = queue.pop()
	
	# Add the neighboring spaces to the queue if possible
	for option in [(xc-1,yc,zc), (xc+1,yc,zc), (xc,yc-1,zc), (xc,yc+1,zc), (xc,yc,zc-1), (xc,yc,zc+1)]:
		x,y,z = option
		if (x,y,z) in exterior_spaces:
			continue
		if (x,y,z) in cubes:
			continue
		if x < minx-1 or x > maxx+1 or y < miny-1 or y > maxy+1 or z < minz-1 or z > maxz+1:
			continue
		exterior_spaces.append((x,y,z))
		queue.insert(0, (x,y,z))

# Now we can count the exterior faces
open_side_count = 0
for cube in cubes:
	x,y,z = cube
	open_side_count += (x+1,  y,  z) in exterior_spaces
	open_side_count += (x-1,  y,  z) in exterior_spaces
	open_side_count += (  x,y+1,  z) in exterior_spaces
	open_side_count += (  x,y-1,  z) in exterior_spaces
	open_side_count += (  x,  y,z+1) in exterior_spaces
	open_side_count += (  x,  y,z-1) in exterior_spaces
print("Part 2: The exterior surface area is", open_side_count)
