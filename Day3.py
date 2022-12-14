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

# Process the input. Each line is one knapsack, with the first half of the characters
# being the items in the first compartment and the second half being the items in the
# second compartment.
whole_knapsacks = input_text.split('\n')[:-1]
knapsacks = [[line[:len(line)//2], line[len(line)//2:]] for line in whole_knapsacks]

def priority(item):
	if item.islower():
		return 1 + ord(item) - ord('a')
	else:
		return 27 + ord(item) - ord('A')

def find_common_item(group1, group2):
	return (set(group1) & set(group2)).pop()

# Part 1: What is the sum of the priorities of each item stored in both compartments?
priorities = [priority(find_common_item(k[0], k[1])) for k in knapsacks]
print("Part 1: The sum of the priorities is", sum(priorities))

# Part 2: What is the sum of the priorities of the common item in each group of 3 knapsacks?
def find_common_group_item(knapsack1, knapsack2, knapsack3):
	return (set(knapsack1) & set(knapsack2) & set(knapsack3)).pop()

group_items = [find_common_group_item(whole_knapsacks[k], whole_knapsacks[k+1], whole_knapsacks[k+2]) for k in range(0, len(whole_knapsacks), 3)]
group_priorities = [priority(item) for item in group_items]
print("Part 2: The sum of the priorities is", sum(group_priorities))
