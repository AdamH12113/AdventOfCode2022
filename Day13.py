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

# Process the input. It's pairs of lines, each of which contains a list that we can
# interpret as a Python statement. Convenient!
pairs_text = input_text.split('\n\n')
pairs = [(eval(pt.split('\n')[0]), eval(pt.split('\n')[1])) for pt in pairs_text]

# Part 1: How many pairs of packets are already in the right order? The comparison
# algorithm can return either "true", "false", or "keep going".
def compare(left, right):
	if type(left) is int and type(right) is int:
		result = True if left < right else False if left > right else None
		return result
	
	if type(left) is int and type(right) is list:
		left = [left]
	if type(left) is list and type(right) is int:
		right = [right]
	
	ll = len(left)
	lr = len(right)
	
	for n in range(max(ll, lr)):
		if n >= ll and n < lr:
			return True
		if n >= lr and n < ll:
			return False
		if n == ll and n == lr:
			return None
		
		result = compare(left[n], right[n])
		if result is not None:
			return result
	return None
	
# Part 1: What is the sum of the indices of the pairs that are in the right order?
# Note that indices are 1-based, not 0-based.
correct_indices = [n+1 for n in range(len(pairs)) if compare(pairs[n][0], pairs[n][1])]
print("Part 1: The sum of the correct indices is", sum(correct_indices))

# Part 2: Sort all of the packets using the comparison function, including two newly-
# added divider packets. The answer is the product of the resulting indices of those
# two packets.
packets = [eval(pkt_text) for pkt_text in input_text.replace('\n\n', '\n').split('\n')]
packets.append([[2]])
packets.append([[6]])

# Python's built-in sorts don't support comparison functions directly,
# but the functools module has a helper function to do the conversion.
def sort_comparison_function(left, right):
	c = compare(left, right)
	return 1 if c else -1 if c == False else 0

packets.sort(key=cmp_to_key(sort_comparison_function), reverse=True)
div1 = packets.index([[2]]) + 1
div2 = packets.index([[6]]) + 1
print("Part 2: The product of the indices is", div1 * div2)
