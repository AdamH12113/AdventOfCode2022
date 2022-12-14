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

# Process the input. Each line is one pair of group assignments, with each assignment
# being a range of numbers.
pairs = []
for line in input_text.split('\n')[:-1]:
	nums = [int(s) for s in re.findall(r'\d+', line)]
	pairs.append([[nums[0], nums[1]], [nums[2], nums[3]]])


# Part 1: In how many assignment pairs does one range fully contain the other?
def pair_contained(pair1, pair2):
	if (pair1[0] >= pair2[0] and pair1[1] <= pair2[1]) or (pair2[0] >= pair1[0] and pair2[1] <= pair1[1]):
		return 1
	else:
		return 0
count = sum(pair_contained(pair[0], pair[1]) for pair in pairs)
print("Part 1:", count, "pairs have one range that fully contains the other")

# Part 2: In how many assignment pairs does one range overlap the other?
def pairs_overlap(pair1, pair2):
	if (pair1[0] <= pair2[0] and pair1[1] >= pair2[0]) or (pair2[0] <= pair1[0] and pair2[1] >= pair1[0]):
		return 1
	else:
		return 0
count = sum(pair_contained(pair[0], pair[1]) or pairs_overlap(pair[0], pair[1]) for pair in pairs)
print("Part 2:", count, "pairs overlap")
