import simpleguitk as simplegui
import random
import math


# initialize global variables used in your code
rng = 100
secret_number = 0
guess = 0
n = 0

# define helper functions


def init():
    """ Function that resets the game """
    global secret_number
    secret_number = random.randrange(rng)
    f(0, rng)
    print "New game. Range is from 0 to", rng
    print "Number of remaining guesses is", n
    print


def f(low, high):
    """ Function to calculate the allowed number of guesses """
    global n
    n = math.ceil(math.log(high - low + 1, 2))

# define event handlers for control panel


def zth():
    """ Function to make the range from 0 to 100
        and then resets the game """
    global guess, rng
    rng = 100
    init()


def ztt():
    """ Function to make the range from 0 to 1000
        and then resets the game """
    global guess, rng
    rng = 1000
    init()


def input_handler(text):
    """ Function that takes the input from the text field
        and prints the output to the console """

    global guess, n, secret_number
    guess = int(text)
    print "Your guess is ", guess
    if guess == secret_number:
        print "Correct!"
        print
        init()
    elif guess < secret_number:
        n -= 1
        print "Number of remaining guesses is", n
        if n == 0:
            print "You ran out of guesses. The number was", secret_number
            print
            init()
        else:
            print "Higher!"
            print
    else:
        n -= 1
        print "Number of remaining guesses is", n
        if n == 0:
            print "You ran out of guesses. The number was", secret_number
            print
            init()
        else:
            print "Lower!"
            print

# create frame
frame = simplegui.create_frame("Guess the number", 200, 200)

# register event handlers for control elements
frame.add_button("Range is [0,100)", zth, 200)
frame.add_button("Range is [0,1000)", ztt, 200)
frame.add_input("Enter a guess:", input_handler, 200)

init()

# start frame
frame.start()
