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

# Process the input. It's a map of a field showing blizzards and their directions. The
# field is rectangular, so we don't need to store any particular information about it.
# Keeping track of the blizzards is a bit of a pain since they overlap, and this is one
# of those shortest-path problems so we're going to need to be efficient. The blizzard
# state repeats after a while, so let's just store a set of blocked spaces for every
# time step.
rows_text = input_text.split('\n')
ysize = len(rows_text) - 2
xsize = len(rows_text[0]) - 2
period = math.lcm(xsize, ysize)

starting_blizzards = {}
for y in range(len(rows_text)):
	for x in range(len(rows_text[y])):
		# Ignoring the outer walls makes it easier to handle the periods
		c = rows_text[y][x]
		if c == '>':
			starting_blizzards[(x-1,y-1)] = (1,0)
		elif c == '<':
			starting_blizzards[(x-1,y-1)] = (-1,0)
		elif c == 'v':
			starting_blizzards[(x-1,y-1)] = (0,1)
		elif c == '^':
			starting_blizzards[(x-1,y-1)] = (0,-1)

blizzards = []
for step in range(period):
	s = set()
	for b in starting_blizzards:
		x,y = b
		dx,dy = starting_blizzards[b]
		nx = (x + step*dx) % xsize
		ny = (y + step*dy) % ysize
		s.add((nx,ny))
	blizzards.append(s)

# Part 1: What is the fewest number of minutes required to reach the end while avoiding
# the blizzards?
