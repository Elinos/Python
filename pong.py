# Implementation of classic arcade game Pong

import simpleguitk as simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
ball_pos = [int(WIDTH / 2), int(HEIGHT / 2)]
ball_vel = [0, 0]
paddle1_pos = HALF_PAD_HEIGHT
paddle2_pos = HALF_PAD_HEIGHT
paddle1_vel = 0
paddle2_vel = 0
score1 = 0
score2 = 0

# helper function that spawns a ball by updating the
# ball's position vector and velocity vector
# if right is True, the ball's velocity is upper right, else upper left


def ball_init(right):
    global ball_pos, ball_vel  # these are vectors stored as lists
    ball_pos = [int(WIDTH / 2), int(HEIGHT / 2)]
    if right:
        ball_vel = [(random.randrange(120, 240) / 100), (
            random.randrange(60, 180) / -100)]
    else:
        ball_vel = [(random.randrange(120, 240) / -100), (
            random.randrange(60, 180) / -100)]

r = random.choice([True, False])
ball_init(r)
# define event handlers


def new_game():
    global score1, score2  # these are ints
    score1, score2 = 0, 0
    r = random.choice([True, False])
    ball_init(r)


def draw(c):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel

    # update paddle's vertical position, keep paddle on the screen
    if (paddle1_pos + paddle1_vel >= HALF_PAD_HEIGHT) and (paddle1_pos + paddle1_vel <= HEIGHT - HALF_PAD_HEIGHT):
        paddle1_pos += paddle1_vel

    if (paddle2_pos + paddle2_vel >= HALF_PAD_HEIGHT) and (paddle2_pos + paddle2_vel <= HEIGHT - HALF_PAD_HEIGHT):
        paddle2_pos += paddle2_vel

    # draw mid line and gutters
    c.draw_line([WIDTH / 2, 0], [WIDTH / 2, HEIGHT], 1, "White")
    c.draw_line([PAD_WIDTH, 0], [PAD_WIDTH, HEIGHT], 1, "White")
    c.draw_line([WIDTH - PAD_WIDTH, 0], [
                WIDTH - PAD_WIDTH, HEIGHT], 1, "White")

    # draw paddles
    c.draw_line([HALF_PAD_WIDTH, paddle1_pos - HALF_PAD_HEIGHT], [
                HALF_PAD_WIDTH, paddle1_pos + HALF_PAD_HEIGHT], PAD_WIDTH, "Blue")
    c.draw_line([WIDTH - HALF_PAD_WIDTH, paddle2_pos - HALF_PAD_HEIGHT], [
                WIDTH - HALF_PAD_WIDTH, paddle2_pos + HALF_PAD_HEIGHT], PAD_WIDTH, "Red")

    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    if ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    if ball_pos[1] >= (HEIGHT - BALL_RADIUS):
        ball_vel[1] = - ball_vel[1]
    if ball_pos[0] <= PAD_WIDTH + BALL_RADIUS:
        if paddle1_pos - HALF_PAD_HEIGHT <= ball_pos[1] <= paddle1_pos + HALF_PAD_HEIGHT:
            ball_vel[0] = - ball_vel[0]
            ball_vel[0] = ball_vel[0] * 1.1
            ball_vel[1] = ball_vel[1] * 1.1
        else:
            score2 += 1
            ball_init(True)
    if ball_pos[0] >= (WIDTH - PAD_WIDTH - BALL_RADIUS):
        if paddle2_pos - HALF_PAD_HEIGHT <= ball_pos[1] <= paddle2_pos + HALF_PAD_HEIGHT:
            ball_vel[0] = - ball_vel[0]
            ball_vel[0] = ball_vel[0] * 1.1
            ball_vel[1] = ball_vel[1] * 1.1
        else:
            score1 += 1
            ball_init(False)

    # draw ball and scores
    c.draw_text("%s   %s" % (score1, score2), [245, 50], 60, "Yellow")
    c.draw_circle(ball_pos, BALL_RADIUS, 2, "Green", "Green")


def keydown(key):
    global paddle1_vel, paddle2_vel

    acc = 2.5
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel -= acc
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel += acc
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel += acc
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel -= acc


def keyup(key):
    global paddle1_vel, paddle2_vel

    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel = 0

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", new_game, 90)


# start frame
frame.start()
