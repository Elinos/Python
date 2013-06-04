# template for "Stopwatch: The Game"
import simpleguitk as simplegui


# define global variables
time = 0
started = False
total = 0
success = 0

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D


def format(time):
    A = time // 600
    B = (time // 100) % 6
    C = (time // 10) % 10
    D = time % 10
    return "%s:%s%s.%s" % (A, B, C, D)

# define event handlers for buttons; "Start", "Stop", "Reset"


def start():
    global started
    timer.start()
    started = True


def stop():
    global started, total, success
    timer.stop()
    if started:
        total += 1
        if (time % 10) == 0:
            success += 1
    started = False


def reset():
    timer.stop()
    global time, total, success, started
    time, total, success, started = 0, 0, 0, False

# define event handler for timer with 0.1 sec interval


def timer_handler():
    global time
    time += 1

# define draw handler


def draw(canvas):
    canvas.draw_text(format(time), [90, 120], 50, "White")
    canvas.draw_text("%s / %s" % (success, total), [250, 30], 20, "Yellow")

# create frame
frame = simplegui.create_frame("Stopwatch: The Game", 300, 200)

# register event handlers
frame.add_button("Start", start, 70)
frame.add_button("Stop", stop, 70)
frame.add_button("Reset", reset, 70)
timer = simplegui.create_timer(100, timer_handler)
frame.set_draw_handler(draw)

# start frame
frame.start()
