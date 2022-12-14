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

# Process the input. This one comes in two parts -- first, a 2D side-view map of
# the initial crate stack-up, then a list of moves. The crate stack-up is padded,
# so we can use the character offset for the stack number.
stackup_rows, moves = [s.split('\n') for s in input_text.split('\n\n')]
num_stacks = int(re.findall(r'\d+', stackup_rows[-1])[-1])
stacks = [[] for n in range(num_stacks)]

for row in stackup_rows[:-1]:
	for stack in range(num_stacks):
		char = row[1 + 4*stack]
		if char.isalpha():
			stacks[stack].insert(0, char)

# Part 1: Which crate ends up on the top of each stack?
def do_move(stacks, move):
	qty, src, dst = (int(n) for n in re.findall(r'\d+', move))
	for n in range(qty):
		stacks[dst-1].append(stacks[src-1].pop())

stacks_part1 = copy.deepcopy(stacks)
for move in moves:
	do_move(stacks_part1, move)

tops = ''.join(stack[-1] for stack in stacks_part1)
print("Part 1: The top crates are", tops)

# Part 2: The crane can actually move multiple crates at once. Which crates end up on top?
def do_group_move(stacks, move):
	qty, src, dst = (int(n) for n in re.findall(r'\d+', move))
	grabbed = stacks[src-1][-qty:]
	stacks[src-1] = stacks[src-1][:-qty]
	stacks[dst-1].extend(grabbed)

for move in moves:
	do_group_move(stacks, move)

tops = ''.join(stack[-1] for stack in stacks)
print("Part 2: The top crates are", tops)
