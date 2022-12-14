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

# Process the input. It's Linux-style console output listing files and directories.
# Parsing this is most of the work.
output = input_text.split('\n')

class File:
	def __init__(self, size):
		self.size = size

class Directory:
	def __init__(self, parent):
		self.contents = {}
		self.parent = parent
	
	def get_total_size(self):
		total_size = 0
		for name in self.contents:
			item = self.contents[name]
			total_size += item.size if type(item) is File else item.get_total_size()
		return total_size
	
	def add_file(self, name, size):
		self.contents[name] = File(size)

	def add_directory(self, name):
		self.contents[name] = Directory(self)
	
	def get_all_subdirectories(self):
		local_subdirs = [self.contents[name] for name in self.contents if type(self.contents[name]) is Directory]
		nested_subdirs = [d for sd in local_subdirs for d in sd.get_all_subdirectories()]
		return local_subdirs + nested_subdirs

	def list(self, indent):
		for name in self.contents:
			item = self.contents[name]
			if type(item) is File:
				print('  ' * indent, name, '  ', item.size)
			else:
				print('  ' * indent, '/' + name, item.get_total_size())
				item.list(indent + 1)

# Parse the directory tree from the console output
root = Directory(None)
line = 0
pwd = root
while line < len(output):
	tokens = output[line].split(' ')
	if tokens[0] == '$':
		if tokens[1] == 'cd':
			if tokens[2] == '/':
				pwd = root
			elif tokens[2] == '..':
				pwd = pwd.parent
			else:
				pwd = pwd.contents[tokens[2]]
		elif tokens[1] == 'ls':
			pass
	else:
		if tokens[0] == 'dir':
			pwd.add_directory(tokens[1])
		elif tokens[0].isdecimal():
			pwd.add_file(tokens[1], int(tokens[0]))
	line += 1

# Part 1: What is the sum of the total sizes of each directory whose size is at most 100000?
sizes = [d.get_total_size() for d in (root.get_all_subdirectories() + [root])]
print("Part 1: The sum is", sum(s for s in sizes if s <= 100000))

# Part 1: Find the smallest directory that could be deleted leave at least 30000000/70000000
# of the disk free. What is the size of that directory?
disk_size = 70000000
min_free_size = 30000000
unused = disk_size - root.get_total_size()
needed = min_free_size - unused

candidate_dir_sizes = [s for s in sizes if s >= needed]
print("Part 2: The smallest deleteable directory's size is", min(candidate_dir_sizes))