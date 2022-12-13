import re, sys

# Read the input
try:
	day_num = int(re.findall(r'\d+', __file__)[-1])
	filename_base = 'Example' if '--example' in sys.argv else 'Input'
	filename = filename_base + str(day_num) + '.txt'
	with open(filename, 'rt') as f:
		input_text = f.read()
except Exception as e:
	print(f"Error reading input: [{exception.__class__.__name__}] {exception}")

# Process the input. Groups are delimited by double newlines. There's a double-newline
# at the end as well.
input_text_groups = input_text[:-1].split('\n\n')
input_groups = [[int(n) for n in s.split('\n')] for s in input_text_groups]

# Part 1: Find the Elf carrying the most Calories. How many Calories is that elf carrying?
totals = [sum(group) for group in input_groups]
print("Part 1: The largest total Calorie count is", max(totals))

# Part 2: Sum the three largest Calorie totals
top_total_sum = sum(sorted(totals)[-3:])
print("Part 2: The sum of the three largest total Calorie counts is", top_total_sum)
