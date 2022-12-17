import re, sys, copy, math

# Read the input
try:
	day_num = int(re.findall(r'\d+', __file__)[-1])
	filename_base = 'Example' if '--example' in sys.argv else 'Input'
	filename = filename_base + str(day_num) + '.txt'
	with open(filename, 'rt') as f:
		input_text = f.read()[:-1]
except Exception as e:
	print(f"Error reading input: [{exception.__class__.__name__}] {exception}")

# Process the input. Monkeys are surprisingly complicated.
class Monkey:
	def __init__(self, start_items, operation, mod_test, true_target, false_target):
		self.items = start_items
		self.items.reverse()             # Python wants to pop from the end of the list
		self.operation = operation
		self.test = mod_test
		self.true_target = true_target
		self.false_target = false_target
		self.inspection_count = 0

	def inspect_item(self):
		self.inspection_count += 1
		old = self.items.pop()
		new = eval(self.operation)   # Security vulnerability
		return new // 3

	def get_target(self, worry_level):
		if worry_level % self.test == 0:
			return self.true_target
		else:
			return self.false_target
	
	def catch(self, worry_level):
		self.items.insert(0, worry_level)
	
	def has_items(self):
		return len(self.items) > 0

	def __str__(self):
		return f"Monkey ({self.operation}) {self.test} {self.true_target} {self.false_target} {self.items}"

def get_numbers(text):
	return [int(n) for n in re.findall(r'\d+', text)]
monkeys_text = input_text.split('\n\n')
monkeys = []
for monkey_text in monkeys_text:
	mt = monkey_text.split('\n')
	items = get_numbers(mt[1])
	op = mt[2].split('= ')[1]
	test = get_numbers(mt[3])[0]
	true_target = get_numbers(mt[4])[0]
	false_target = get_numbers(mt[5])[0]
	monkeys.append(Monkey(items, op, test, true_target, false_target))

# Part 1: What is the product of the number of inspections of the two busiest monkeys?
monkeys_p1 = copy.deepcopy(monkeys)
for round in range(20):
	for m in range(len(monkeys_p1)):
		while monkeys_p1[m].has_items():
			next_item = monkeys_p1[m].inspect_item()
			target = monkeys_p1[m].get_target(next_item)
			monkeys_p1[target].catch(next_item)
monkey_business = math.prod(sorted([m.inspection_count for m in monkeys_p1])[-2:])
print("Part 1: The total amount of monkey business is", monkey_business)

# Part 2: Worry levels are no longer divided by 3 after inspection. What is the level
# of monkey business after 10,000 rounds? The numbers get too large to run a simulation.
# Fortunately, the monkeys are all testing for prime factors, so any operation involving
# multiplication can be simplified. But what to do about addition...?
def new_inspection(self):
	self.inspection_count += 1
	old = self.items.pop()
	new = eval(self.operation)   # Security vulnerability
	return new

#Monkey.inspect_item = new_inspection
monkeys_p2 = copy.deepcopy(monkeys)

for round in range(2):
	print(f"Round {round}")
	for m in range(len(monkeys_p2)):
		while monkeys_p2[m].has_items():
			next_item = monkeys_p2[m].inspect_item()
			target = monkeys_p2[m].get_target(next_item)
			monkeys_p2[target].catch(next_item)
	for monkey in monkeys_p2:
		print(monkey)
monkey_business = math.prod(sorted([m.inspection_count for m in monkeys_p2])[-2:])
print("Part 2: The total amount of monkey business is", monkey_business)
