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

# Process the input. Each line has an opcode and an optional operand.
program = [line.split(' ') for line in input_text.split('\n')]


# Hooray! It's time to implement an assembly interpeter!
class Interpreter:
	def __init__(self, instructions):
		self.program = instructions
		self.cycle = 1
		self.pc = 0
		self.x = 1
		self.state = 'fetch'
		self.exec_countdown = 0
		self.instruction = []
	
	def run_one_cycle(self):
		if self.state == 'fetch':
			self.instruction = self.program[self.pc]
			self.pc += 1
			if self.pc >= len(self.program):
				self.pc = 0
			if self.instruction[0] == 'noop':
				self.exec_countdown = 1
			elif self.instruction[0] == 'addx':
				self.state = 'execute'
				self.exec_countdown = 2
			self.state = 'execute'
		
		if self.state == 'execute':
			self.exec_countdown -= 1
			if self.exec_countdown == 0:
				if self.instruction[0] == 'noop':
					pass
				elif self.instruction[0] == 'addx':
					self.x += int(self.instruction[1])
				self.state = 'fetch'
		self.cycle += 1
	
	def get_signal_strength(self):
		return self.cycle * self.x
	
	def __str__(self):
		return f"{self.cycle:04d} {self.pc:03d} {self.state:7s} {self.exec_countdown} {self.x:3d} {self.instruction}"

# Part 1: The signal strength is defined to be the product of the cycle count and the X
# register. What is the sum of the signal strengths at cycles 20, 60, 100, 140, 180, and 220?
interpreter = Interpreter(program)
signal_strengths = []
for cycle in range(220):
	interpreter.run_one_cycle()
	if interpreter.cycle in [20, 60, 100, 140, 180, 220]:
		signal_strengths.append(interpreter.get_signal_strength())
print("Part 1: The sum of the signal strengths is", sum(signal_strengths))


# Part 2: Hooray, now we get to simulate a CRT!
interpreter = Interpreter(program)
print("Part 2: The CRT looks like this:")
for row in range(6):
	for col in range(40):
		if col >= interpreter.x - 1 and col <= interpreter.x + 1:
			print('#', end='')
		else:
			print('.', end='')
		interpreter.run_one_cycle()
	print()


