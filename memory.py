# implementation of card game - Memory

import simpleguitk as simplegui
import random

# helper function to initialize globals


def init():
    global cardList, exposed, state, card1, card2, moves
    state = 0
    moves = 0
    card1, card2 = -1, -1
    exposed = []
    cardList = range(8) + range(8)
    random.shuffle(cardList)
    for x in range(16):
        exposed.append(False)
    label.set_text("Moves = 0")

# define event handlers


def mouseclick(pos):
    # add game state logic here
    global state, card1, card2, moves
    card = pos[0] // 50
    if exposed[card]:
        return
    if state == 0:
        state = 1
        exposed[card] = True
        card1 = card
    elif state == 1:
        moves += 1
        label.set_text("Moves = " + str(moves))
        state = 2
        card2 = card
        exposed[card] = True
    else:
        state = 1
        if not cardList[card1] == cardList[card2]:
            exposed[card1] = False
            exposed[card2] = False
        card1 = card
        exposed[card] = True

# cards are logically 50x100 pixels in size


def draw(canvas):
    i = -35
    j = -50
    for card in cardList:
        i += 50
        canvas.draw_text(str(card), (i, 65), 48, "Red")
    for x in exposed:
        j += 50
        if not x:
            canvas.draw_polygon([(j, 0), (j + 50, 0), (
                j + 50, 100), (j, 100)], 1, "Black", "Green")

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Restart", init)
label = frame.add_label("Moves = 0")

# initialize global variables
init()

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
frame.start()
