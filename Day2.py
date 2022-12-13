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

# Process the input. Each row consists of two one-letter move codes.
turns = [turn.split(' ') for turn in input_text.split('\n')[:-1]]

# Decode the move instructions
def decode(code):
	if code == 'A' or code == 'X':
		return 'rock'
	elif code == 'B' or code == 'Y':
		return 'paper'
	else:
		return 'scissors'

# Play one round of rock-paper-scissors and return the score
def play_rps(opponent_move, player_move):
	choice_score = 1 if player_move == 'rock' else 2 if player_move == 'paper' else 3
	if player_move == opponent_move:
		return 3 + choice_score
	elif ((player_move == 'rock' and opponent_move == 'paper') or
	      (player_move == 'paper' and opponent_move == 'scissors') or
	      (player_move == 'scissors' and opponent_move == 'rock')):
		return 0 + choice_score
	else:
		return 6 + choice_score

# Part 1: What is the total score for this decoding scheme?
scores = [play_rps(decode(turn[0]), decode(turn[1])) for turn in turns]
print("Part 1: The total score is", sum(scores))


# Part 2: The second column is what the result should be, not the player move.
def get_player_move(opponent_move, result):
	if result == 'Y':
		return opponent_move
	elif result == 'Z':
		return 'rock' if opponent_move == 'scissors' else 'scissors' if opponent_move == 'paper' else 'paper'
	else:
		return 'rock' if opponent_move == 'paper' else 'paper' if opponent_move == 'scissors' else 'scissors'

scores = [play_rps(decode(turn[0]), get_player_move(decode(turn[0]), turn[1])) for turn in turns]
print("Part 2: The total score is", sum(scores))
