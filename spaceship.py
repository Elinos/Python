# program template for Spaceship
import simpleguitk as simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0.5
c = 0.01
a_vel = 0

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated


# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim

# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.ogg")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.ogg")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.ogg")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.ogg")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

def keydown(key):
    global a_vel, vel
    if key==simplegui.KEY_MAP["left"]:
        a_vel -= 0.05
        my_ship.a_vel(a_vel)
    elif key==simplegui.KEY_MAP["right"]:
        a_vel += 0.05
        my_ship.a_vel(a_vel)
    elif key==simplegui.KEY_MAP["up"]:
        my_ship.on_thrust()
    elif key==simplegui.KEY_MAP["space"]:
        my_ship.shoot()

def keyup(key):
    global a_vel, vel
    if key==simplegui.KEY_MAP["left"]:
        a_vel = 0
        my_ship.a_vel(a_vel)
    elif key==simplegui.KEY_MAP["right"]:
        a_vel = 0
        my_ship.a_vel(a_vel)
    elif key==simplegui.KEY_MAP["up"]:
        my_ship.off_thrust()


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()

    def draw(self,canvas):
        #canvas.draw_circle(self.pos, self.radius, 1, "White", "White")
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)

    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]

        self.vel[0] *= (1 - c)
        self.vel[1] *= (1 - c)

        forward = angle_to_vector(self.angle)
        if self.thrust:
            self.vel[0] += forward[0]*0.3
            self.vel[1] += forward[1]*0.3

        self.angle += self.angle_vel
        if (self.pos[0] < 0) or (self.pos[0] > WIDTH):
            self.pos[0] %= WIDTH
        if (self.pos[1] < 0) or (self.pos[1] > HEIGHT):
            self.pos[1] %= HEIGHT

    def a_vel(self, a_vel):
        self.angle_vel = a_vel

    def on_thrust(self):
        self.thrust = True
        self.image_center[0] = 135
        ship_thrust_sound.play()

    def off_thrust(self):
        self.thrust = False
        self.image_center[0] = 45
        ship_thrust_sound.rewind()

    def shoot(self):
        global a_missile
        missile = angle_to_vector(self.angle)
        missile_loc = (missile[0] * self.radius, missile[1] * self.radius)

        a_missile = Sprite([(missile_loc[0] + self.pos[0]), (missile_loc[1] + self.pos[1])] , [(self.vel[0] + missile[0]*3), (self.vel[1] + missile[1]*3)], 0, 0, missile_image, missile_info, missile_sound)




# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()

    def draw(self, canvas):
        #canvas.draw_circle(self.pos, self.radius, 1, "Red", "Red")
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)

    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]

        if (self.pos[0] < 0) or (self.pos[0] > WIDTH):
            self.pos[0] %= WIDTH
        if (self.pos[1] < 0) or (self.pos[1] > HEIGHT):
            self.pos[1] %= HEIGHT

        self.angle += self.angle_vel


def draw(canvas):
    global time

    # animiate background
    time += 1
    center = debris_info.get_center()
    size = debris_info.get_size()
    wtime = (time / 8) % center[0]
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, [center[0] - wtime, center[1]], [size[0] - 2 * wtime, size[1]],
                                [WIDTH / 2 + 1.25 * wtime, HEIGHT / 2], [WIDTH - 2.5 * wtime, HEIGHT])
    canvas.draw_image(debris_image, [size[0] - wtime, center[1]], [2 * wtime, size[1]],
                                [1.25 * wtime, HEIGHT / 2], [2.5 * wtime, HEIGHT])

    # draw ship and sprites
    my_ship.draw(canvas)
    a_rock.draw(canvas)
    a_missile.draw(canvas)

    # update ship and sprites
    my_ship.update()
    a_rock.update()
    a_missile.update()

    canvas.draw_text("Lives", (50, 30), 30, "White")
    canvas.draw_text("%s" %lives, (50, 60), 30, "White")
    canvas.draw_text("Score", (650, 30), 30, "White")
    canvas.draw_text("%s" %score, (650, 60), 30, "White")

# timer handler that spawns a rock
def rock_spawner():
    global a_rock
    r_pos1 = random.randrange(100, 700)
    r_pos2 = random.randrange(70, 530)
    r_vel1 = random.randrange(-300, 301) / 100
    r_vel2 = random.randrange(-300, 301) / 100
    r_ang_vel = random.randrange(-11, 11) / 100
    a_rock = Sprite([r_pos1, r_pos2], [r_vel1, r_vel2], 0, r_ang_vel, asteroid_image, asteroid_info)

# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [0, 3], 0, 0.05, asteroid_image, asteroid_info)
a_missile = Sprite([-1, -1], [0,0], 0, 0, missile_image, missile_info)

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
