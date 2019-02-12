"""CS 61A Presents The Game of Hog."""

from dice import four_sided, six_sided, make_test_dice
from ucb import main, trace, log_current_line, interact

GOAL_SCORE = 100  # The goal of Hog is to score 100 points.


######################
# Phase 1: Simulator #
######################

def roll_dice(num_rolls, dice=six_sided):
	"""Simulate rolling the DICE exactly NUM_ROLLS>0 times. Return the sum of
	the outcomes unless any of the outcomes is 1. In that case, return the
	number of 1's rolled.
	"""
	# These assert statements ensure that num_rolls is a positive integer.
	assert type(num_rolls) == int, 'num_rolls must be an integer.'
	assert num_rolls > 0, 'Must roll at least once.'
	# BEGIN PROBLEM 1
	i, n, sum, pigout = 0, 0, 0, False
	while n < num_rolls:
		k = dice()
		if k == 1:
			pigout = True
			i = i + 1
		else:
			sum += k
		n += 1
	return (pigout and i) or sum
	# END PROBLEM 1

def free_bacon(opponent_score):
	"""Return the points scored from rolling 0 dice (Free Bacon)."""
	# BEGIN PROBLEM 2
	points = max(opponent_score // 10, opponent_score % 10) + 1
	return points
	# END PROBLEM 2

# Write your prime functions here!
def is_prime(score):
	if score == 1:
		return False
	for i in range (2, score):
		if score % i == 0:
			return False
	return True

def next_prime(score):
	if (is_prime(score)):
		score += 1
		while not is_prime(score):
			score += 1
	return score
 
def take_turn(num_rolls, opponent_score, dice=six_sided):
	"""Simulate a turn rolling NUM_ROLLS dice, which may be 0 (Free Bacon).
	Return the points scored for the turn by the current player. Also
	implements the Hogtimus Prime and When Pigs Fly rules.

	num_rolls:       The number of dice rolls that will be made.
	opponent_score:  The total score of the opponent.
	dice:            A function of no args that returns an integer outcome.
	"""
	# Leave these assert statements here; they help check for errors.
	assert type(num_rolls) == int, 'num_rolls must be an integer.'
	assert num_rolls >= 0, 'Cannot roll a negative number of dice in take_turn.'
	assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
	assert opponent_score < 100, 'The game should be over.'
	# BEGIN PROBLEM 2
	if num_rolls == 0: # Free Bacon rule
		score = free_bacon(opponent_score)
		if is_prime(score): # Hogtimus Prime rule
			score = next_prime(score)
	else:
		score = roll_dice(num_rolls, dice)
		if is_prime(score):
			score = next_prime(score)
	return min(25 - num_rolls, score) # When Pigs Fly rule
	# END PROBLEM 2

def reroll(dice):
	"""Return dice that return even outcomes and re-roll odd outcomes of DICE."""
	def rerolled():
		# BEGIN PROBLEM 3
		cur_dice = dice()
		if cur_dice % 2 != 0:
			cur_dice = dice()
		return cur_dice
		# END PROBLEM 3
	return rerolled

def select_dice(score, opponent_score, dice_swapped):
	"""Return the dice used for a turn, which may be re-rolled (Hog Wild) and/or
	swapped for four-sided dice (Pork Chop).

	DICE_SWAPPED is True if and only if four-sided dice are being used.
	"""
	# BEGIN PROBLEM 4
	if dice_swapped:
		dice = four_sided
	else:
		dice = six_sided
	# END PROBLEM 4
	if (score + opponent_score) % 7 == 0:
		dice = reroll(dice)
	return dice


def other(player):
	"""Return the other player, for a player PLAYER numbered 0 or 1.

	>>> other(0)
	1
	>>> other(1)
	0
	"""
	return 1 - player


def play(strategy0, strategy1, score0=0, score1=0, goal=GOAL_SCORE):
	"""Simulate a game and return the final scores of both players, with
	Player 0's score first, and Player 1's score second.

	A strategy is a function that takes two total scores as arguments
	(the current player's score, and the opponent's score), and returns a
	number of dice that the current player will roll this turn.

	strategy0:  The strategy function for Player 0, who plays first
	strategy1:  The strategy function for Player 1, who plays second
	score0   :  The starting score for Player 0
	score1   :  The starting score for Player 1
	"""
	player = 0  # Which player is about to take a turn, 0 (first) or 1 (second)
	dice_swapped = False  # Whether 4-sided dice have been swapped for 6-sided
	# BEGIN PROBLEM 5
	while score0 < goal and score1 < goal:
		if player == 0:
			# Get number of dice rolls
			num_rolls = strategy0(score0, score1)
			# Dice type depending on player and opponent's score
			dice_type = select_dice(score0, score1, dice_swapped)
			# Get the player's score for the turn
			score0 += take_turn(num_rolls, score1, dice_type)
		else:
			num_rolls = strategy1(score1, score0)
			dice_type = select_dice(score1, score0, dice_swapped)
			score1 += take_turn(num_rolls, score0, dice_type)
			
		# Swine Swap
		if score0 == (2 * score1) or score1 == (2 * score0):
			temp = score0
			score0 = score1
			score1 = temp
		
		player = other(player)
			
	# END PROBLEM 5
	return score0, score1

