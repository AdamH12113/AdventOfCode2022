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

# Process the input. This time it's just a single stream of characters. Nice!
stream = input_text
length = len(stream)

# Part 1: Find the first position where the four most recently received characters
# were all different.
for c in range(4, length+1):
	if len(set(stream[c-4:c])) == 4:
		print("Part 1: Found a start-of-packet marker at position", c)
		break

# Part 2: Same as part 1, but fourteen characters instead of four.
for c in range(14, length + 1):
	if len(set(stream[c-14:c])) == 14:
		print("Part 2: Found a start-of-message marker at position", c)
		break
