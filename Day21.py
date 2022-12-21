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

# Process the input. Each line is essentially a variable that corresponds to either a
# number or an operation involving two other variables. (There don't seem to be any
# variable+number operations.)
values = {}
operations = {}
for line in input_text.split('\n'):
	var, op = line.split(': ')
	if re.match(r'\d+', op):
		values[var] = int(op)
	else:
		operations[var] = tuple(op.split(' '))

# Part 1: What is the value of "root"?
while 'root' not in values:
	for var in list(operations.keys()):
		v1, op, v2 = operations[var]
		if v1 in values and v2 in values:
			values[var] = int(eval(f"{values[v1]} {op} {values[v2]}"))  # Security hazard
			del operations[var]
print(f"Part 1: The value of root is {values['root']}")
			


