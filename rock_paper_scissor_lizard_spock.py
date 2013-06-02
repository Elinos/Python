# Rock-paper-scissors-lizard-Spock template


# The key idea of this program is to equate the strings
# "rock", "paper", "scissors", "lizard", "Spock" to numbers
# as follows:
#
# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors

#module that we need to generate random computer number
import random

def number_to_name(number):
    """Function to convert number to the corresponding name"""
    if number == 0:
        return "rock"
    elif number == 1:
        return "Spock"
    elif number == 2:
        return "paper"
    elif number == 3:
        return "lizard"
    elif number == 4:
        return "scissors"
    else:
        print "Invalid Number!"


def name_to_number(name):
    """ Function to convert the name to a number from 0 to 4"""
    if name == "rock":
        return 0
    elif name == "Spock":
        return 1
    elif name == "paper":
        return 2
    elif name == "lizard":
        return 3
    elif name == "scissors":
        return 4
    else:
        return "Invalid Name!"


def rpsls(name):
    """Function that represents the game of Rock-paper-scissor-lizard-Spock"""

    # convert name to player_number using name_to_number
    player_number = name_to_number(name)
    # compute random guess for comp_number using random.randrange()
    comp_number = random.randrange(0, 5)
    # compute difference of player_number and comp_number modulo five
    difference = (player_number - comp_number) % 5
    # use if/elif/else to determine winner and then print the results
    if (difference == 1) or (difference == 2):
        print "Player chooses", number_to_name(player_number)
        print "Computer chooses", number_to_name(comp_number)
        print "Player Wins!"
        print
    elif (difference == 3) or (difference == 4):
        print "Player chooses", number_to_name(player_number)
        print "Computer chooses", number_to_name(comp_number)
        print "Computer Wins!"
        print
    else:
        print "Player chooses", number_to_name(player_number)
        print "Computer chooses", number_to_name(comp_number)
        print "Player and computer tie!"
        print
# test your code
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")
