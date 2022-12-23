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

# Process the input. It's just a list of integers, but we need to keep track of both
# their original positions and their positions after the "mixing" operation. This is
# an obvious use case for references, which means we need to wrap the numbers in objects.
raw_numbers = [int(n) for n in input_text.split('\n')]

class Number:
	def __init__(self, value, position):
		self.value = value
		self.position = position

	def __int__(self):
		return self.value

	def __str__(self):
		return f"{self.value}"
	def __repr__(self):
		return self.__str__()

numbers = tuple([Number(raw_numbers[n], n) for n in range(len(raw_numbers))])
mix = [numbers[n] for n in range(len(numbers))]
zero = [num for num in numbers if num.value == 0][0]

# Part 1: After mixing, what are the 1000th, 2000th, and 3000th numbers after 0? The
# tricky part here is that the end of the list doesn't count as a location, which breaks
# our modulus division.
for num in numbers:
	pos = num.position
	new_pos = (pos + num.value) % (len(mix) - 1)
	dir = 1 if new_pos >= pos else -1
	shift = abs(new_pos - pos)
	
	for _ in range(shift):
		mix[pos].position = pos + dir
		mix[pos+dir].position = pos
		mix[pos], mix[pos+dir] = mix[pos+dir], mix[pos]
		pos += dir

base = zero.position
coords = tuple(mix[(base + n) % len(mix)].value for n in (1000, 2000, 3000))
print(f"Part 1: The coordinates are {coords} and their sum is {sum(coords)}.")

# Part 2: Now we multiply each number by 811589153, then mix ten times. Our existing
# code handles this, although it's not the most efficient thing in the world. It would
# have been better to track the positions differently.
numbers = tuple([Number(raw_numbers[n] * 811589153, n) for n in range(len(raw_numbers))])
mix = [numbers[n] for n in range(len(numbers))]
zero = [num for num in numbers if num.value == 0][0]

for mix_num in range(10):
	for num in numbers:
		pos = num.position
		new_pos = (pos + num.value) % (len(mix) - 1)
		dir = 1 if new_pos >= pos else -1
		shift = abs(new_pos - pos)
		
		for _ in range(shift):
			mix[pos].position = pos + dir
			mix[pos+dir].position = pos
			mix[pos], mix[pos+dir] = mix[pos+dir], mix[pos]
			pos += dir

base = zero.position
coords = tuple(mix[(base + n) % len(mix)].value for n in (1000, 2000, 3000))
print(f"Part 2: The coordinates are {coords} and their sum is {sum(coords)}.")



