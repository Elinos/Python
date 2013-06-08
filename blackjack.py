# Mini-project #6 - Blackjack

import simpleguitk as simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")

# initialize some useful global variables
in_play = False
outcome = ""
outcome1 = ""
outcome2 = ""
score = 0


# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 10, 'Q': 10, 'K': 10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank),
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]],
                          CARD_SIZE)

# define hand class
class Hand:
    def __init__(self):
        self.cards = []

    def __str__(self):
        r = ""
        for card in self.cards:
            r += "%s " % card
        return "Hand contains %s" % (r)

    def add_card(self, card):
        self.cards.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        value = 0
        for card in self.cards:
            value += VALUES[card.get_rank()]
        aces = [card.get_rank() for card in self.cards]
        if ('A' in aces) and (value + 10 <= 21):
            value += 10
        return value

    def draw(self, canvas, pos):
        i = 0
        for card in self.cards:
            card.draw(canvas, [pos[0] + i, pos[1]])
            i += 75


# define deck class 
class Deck:
    def __init__(self):
        self.cards = []
        self.missing_cards = []
        for suit in SUITS:
            for rank in RANKS:
                self.cards.append(Card(suit, rank))

    def shuffle(self):
        self.cards.extend(self.missing_cards)
        self.missing_cards = []
        random.shuffle(self.cards)

    def deal_card(self):
        self.missing_cards.append(self.cards[0])
        return self.cards.pop(0)

    def __str__(self):
        r = ""
        for card in self.cards:
            r += "%s " % card
        return "Deck contains %s" % (r)


deck = Deck()
player_hand = Hand()
dealer_hand = Hand()


#define event handlers for buttons
def deal():
    global outcome, outcome1, outcome2, in_play, deck, player_hand, dealer_hand, score

    if in_play:
        outcome = "Player lose!"
        outcome1 = ""
        outcome2 = ""
        score -= 1
        in_play = False

    in_play = True

    deck.shuffle()
    player_hand = Hand()
    dealer_hand = Hand()
    player_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    if outcome == "Player lose!":
        outcome = "Player lose!"
        outcome1 = "Hit or Stand?"
        outcome2 = ""
    else:
        outcome = "Hit or Stand?"
        outcome1 = ""
        outcome2 = ""


def hit():
    global outcome, outcome1, outcome2, in_play, deck, player_hand, dealer_hand, score
    if in_play:
        if player_hand.get_value() <= 21:
            player_hand.add_card(deck.deal_card())
            outcome = "Hit or Stand?"
            outcome1 = ""
            outcome2 = ""

        if player_hand.get_value() > 21:
            outcome = "You have busted!"
            outcome1 = "New Deal?"
            outcome2 = ""
            score -= 1
            in_play = False


            # if the hand is in play, hit the player

            # if busted, assign a message to outcome, update in_play and score


def stand():
    global outcome, outcome1, outcome2, in_play, deck, player_hand, dealer_hand, score
    if in_play:

        if player_hand.get_value() > 21:
            outcome = "You have busted!"
            outcome1 = "New Deal?"
            outcome2 = ""
            in_play = False
        else:
            while (dealer_hand.get_value() <= 17):
                dealer_hand.add_card(deck.deal_card())

            if dealer_hand.get_value() > 21:
                outcome = "Dealer has busted!"
                outcome1 = "Player wins!"
                outcome2 = "New Deal?"
                score += 1
                in_play = False
            elif player_hand.get_value() <= dealer_hand.get_value():
                outcome = "Dealer wins!"
                outcome1 = "New Deal?"
                outcome2 = ""
                score -= 1
                in_play = False
            else:
                outcome = "Player wins!"
                outcome1 = "New Deal?"
                outcome2 = ""
                score += 1
                in_play = False


                # if hand is in play, repeatedly hit dealer until his hand has value 17 or more

                # assign a message to outcome, update in_play and score

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    global outcome, outcome1, outcome2, score, in_play
    player_hand.draw(canvas, [150, 500])
    dealer_hand.draw(canvas, [150, 200])
    canvas.draw_text("Blackjack", (185, 50), 60, "Black")
    canvas.draw_text("Score: %s" % score, (450, 400), 30, "Yellow")
    canvas.draw_text(outcome, (150, 395), 20, "White")
    canvas.draw_text(outcome1, (150, 415), 20, "White")
    canvas.draw_text(outcome2, (150, 435), 20, "White")
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE,
                          (150 + CARD_BACK_CENTER[0], 200 + CARD_BACK_CENTER[1]), CARD_BACK_SIZE)

#canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, (120,140), (50,50))

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit", hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)



# get things rolling
frame.start()
