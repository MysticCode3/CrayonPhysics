import pygame
from win32api import GetSystemMetrics
import pymunk
import random

screen_width = int(GetSystemMetrics(0))
screen_height = int(GetSystemMetrics(1))

green_color = 150, 200, 20
blue_color = 67, 84, 255
orange_color = 255, 165, 0
red_color = 250, 0, 0
purple_color = 172, 79, 198
gray_color = 128, 128, 128
brown_color = 123, 63, 0

cx, cy = 0, 0
mx, my = 0, 0

stage = 0

stage_1 = False
stage_2 = False
stage_3 = False
stage_4 = False

gravity = (0, 0)

def create_house(x, y):
    static_segments.append(static_segment(space, x, y, 50, (-100, 0), (0, 0), (181, 155, 124)))
    static_segments.append(static_segment(space, x-50, y-40, 10, (-95, 25), (0, -25), (134, 59, 59)))
    static_segments.append(static_segment(space, x+45, y-40, 10, (-95, -25), (0, 25), (134, 59, 59)))
    #static_segments.append(static_segment(space, 350, screen_height / 2 + 140, 50, (-100, 0), (0, 0), (181, 155, 124)))
    #static_segments.append(static_segment(space, 300, screen_height / 2 + 100, 10, (-95, 25), (0, -25), (134, 59, 59)))
    #static_segments.append(static_segment(space, 395, screen_height / 2 + 100, 10, (-95, -25), (0, 25), (134, 59, 59)))

def get_collision(object_1, object_2):
    if object_1.colliderect(object_2):
        return True

class dynamic_circle():
    def __init__(self, space, x, y, radius, color):
        self.x, self.y = x, y
        self.radius = radius
        self.body = pymunk.Body(1, 100, body_type=pymunk.Body.DYNAMIC)
        self.body.position = x, y
        self.shape = pymunk.Circle(self.body, self.radius)
        self.shape.elasticity = 0.5
        self.color = color
        self.collision_rect = None
        self.image = pygame.image.load("Circle.png")
        self.image = pygame.transform.scale2x(self.image)
        space.add(self.body, self.shape)

    def draw(self):
        self.collision_rect = pygame.Rect((self.body.position.x - self.radius, self.body.position.y - self.radius), (self.radius*2, self.radius*2))
        #pygame.draw.rect(screen, (255, 0, 0), self.collision_rect)
        #pygame.draw.circle(screen, self.color, self.body.position, self.radius)
        screen.blit(self.image, (self.body.position.x-self.radius, self.body.position.y-self.radius))

    def change_pos(self, new_pos, new_vel):
        self.body.position = new_pos
        self.body.velocity = new_vel

class static_circle():
    def __init__(self, space, x, y, radius, color):
        self.space = space
        self.x, self.y = x, y
        self.radius = radius
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = x, y
        self.shape = pymunk.Circle(self.body, self.radius)
        self.shape.elasticity = 1
        self.color = color
        space.add(self.body, self.shape)

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

class static_segment():
    def __init__(self, space, x, y, radius, offset_1, offset_2, color):
        self.space = space
        self.x, self.y = x, y
        self.offset_1, self.offset_2 = offset_1, offset_2
        self.radius = radius
        self.body = pymunk.Body(body_type= pymunk.Body.STATIC)
        self.body.position = x, y
        self.shape = pymunk.Segment(self.body, (offset_1), (offset_2), self.radius)
        self.shape.elasticity = 1
        self.color = color
        space.add(self.body,self.shape)

    def draw(self):
        p1 = self.body.local_to_world(self.shape.a)
        p2 = self.body.local_to_world(self.shape.b)
        pygame.draw.line(screen, self.color, p1, p2, self.radius*2)

class star():
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.collision_rect = None

    def draw(self):
        self.collision_rect = pygame.Rect((self.x - 10, self.y - 10), (20, 20))
        #pygame.draw.rect(screen, (255, 0, 0), self.collision_rect)
        pygame.draw.circle(screen, (204, 204, 0), (self.x, self.y), 10)

pygame.init()
font = pygame.font.SysFont("comicsansms", 50)
font_big = pygame.font.SysFont("comicsansms", 100)
font_massive = pygame.font.SysFont("comicsansms", 150)
font_small = pygame.font.SysFont("comicsansms", 40)

screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

space = pymunk.Space()

dynamics = []
main_circle = (dynamic_circle(space, screen_width/2, 100, 50, (green_color)))

static_segments = []
static_circles = []

current_star = star(-100, -100)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            cx, cy = pygame.mouse.get_pos()
            #+dynamics.append(dynamic_circle(space, cx, cy, 50, (blue_color)))
            print(cx, cy)

    mx, my = pygame.mouse.get_pos()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_q]:
        pygame.quit()
    if keys[pygame.K_SPACE]:
        gravity = (0, 500)
    if keys[pygame.K_e]:
        static_segments.append(static_segment(space, mx, my, 10, (0, -100), (0, 100), red_color))
    if keys[pygame.K_r]:
        static_segments.append(static_segment(space, mx, my, 10, (-100, 0), (100, 0), red_color))
    if keys[pygame.K_t]:
        static_segments.append(static_segment(space, mx, my, 10, (-100, 0), (100, -100), red_color))
    if keys[pygame.K_y]:
        static_segments.append(static_segment(space, mx, my, 10, (-100, 0), (100, 100), red_color))
    if keys[pygame.K_w]:
        static_circles.append(static_circle(space, mx, my, 15, red_color))
    if stage == 0 and stage_1 == False:
        static_segments.append(static_segment(space, 0, screen_height / 2 + 540, 350, (-100, 0), (2000, 0), (0, 154, 23)))
        # HOUSE
        create_house(350, screen_height / 2 + 140)

        create_house(650, screen_height / 2 + 140)

        create_house(1050, screen_height / 2 + 140)

        create_house(1350, screen_height / 2 + 140)

        create_house(1750, screen_height / 2 + 140)
    if keys[pygame.K_1] or stage == 1:
        stage_1 = True
        stage_2 = False
        stage_3 = False
        stage_4 = False
        gravity = (0, 0)
        main_circle.change_pos((screen_width/2, 100), (0, 0))
        for dynamic in dynamics:
            space.remove(dynamic.shape)
            dynamics.remove(dynamic)
        for static in static_segments:
            space.remove(static.shape)
            static_segments.remove(static)
        for static in static_circles:
            space.remove(static.shape)
            static_circles.remove(static)
        #if len(space.bodies) == 1:
        stage = 0
        static_segments.append(static_segment(space, 0, screen_height/2+540, 350, (-100, 0), (2000, 0), (0, 154, 23)))
        #HOUSE
        create_house(350, screen_height/2+140)

        create_house(650, screen_height/2+140)

        create_house(1050, screen_height/2+140)

        create_house(1350, screen_height/2+140)

        create_house(1750, screen_height/2+140)

        #STAR
        current_star = star(screen_width/1.03, screen_height/1.6)
    if keys[pygame.K_2] or stage == 2:
        stage_2 = True
        stage_1 = True
        stage_3 = False
        stage_4 = False
        gravity = (0, 0)
        main_circle.change_pos((screen_width / 2, 100), (0, 0))
        for dynamic in dynamics:
            space.remove(dynamic.shape)
            dynamics.remove(dynamic)
        for static in static_segments:
            space.remove(static.shape)
            static_segments.remove(static)
        for static in static_circles:
            space.remove(static.shape)
            static_circles.remove(static)
        if len(space.shapes) < 2:
            stage = 0
        if stage == 0:
            static_segments.append(static_segment(space, 0, screen_height / 2 + 540, 350, (-100, 0), (2000, 0), (0, 154, 23)))

            # HOUSE
            create_house(350, screen_height / 2 + 140)

            create_house(650, screen_height / 2 + 140)

            create_house(1050, screen_height / 2 + 140)

            create_house(1350, screen_height / 2 + 140)

            create_house(1750, screen_height / 2 + 140)

            # STAR
            current_star = star(screen_width / 1.03, screen_height / 1.6)
    if keys[pygame.K_3] or stage == 3:
        stage_3 = True
        stage_1 = True
        stage_2 = True
        stage_4 = False
        gravity = (0, 0)
        main_circle.change_pos((screen_width / 2, 100), (0, 0))
        for dynamic in dynamics:
            space.remove(dynamic.shape)
            dynamics.remove(dynamic)
        for static in static_segments:
            space.remove(static.shape)
            static_segments.remove(static)
        for static in static_circles:
            space.remove(static.shape)
            static_circles.remove(static)
        if len(space.shapes) < 2:
            stage = 0
        if stage == 0:
            static_segments.append(static_segment(space, 0, screen_height/2+540, 350, (-100, 0), (2000, 0), (0, 154, 23)))
            static_segments.append(static_segment(space, 500, screen_height/2-200, 25, (-100, 0), (100, 0), (0, 154, 23)))
            static_segments.append(static_segment(space, 1320, screen_height/2-100, 25, (-100, 0), (100, 0), (0, 154, 23)))

            create_house(350, screen_height / 2 + 140)

            create_house(650, screen_height / 2 + 140)

            create_house(1050, screen_height / 2 + 140)

            create_house(1350, screen_height / 2 + 140)

            create_house(1750, screen_height / 2 + 140)

            create_house(550, screen_height / 2 - 275)

            create_house(1370, screen_height / 2 - 175)

            # STAR
            current_star = star(screen_width / 1.03, screen_height / 1.6)
    if keys[pygame.K_4] or stage == 4:
        stage_4 = True
        stage_1 = True
        stage_2 = True
        stage_3 = True
        gravity = (0, 0)
        main_circle.change_pos((screen_width / 2, 100), (0, 0))
        for dynamic in dynamics:
            space.remove(dynamic.shape)
            dynamics.remove(dynamic)
        for static in static_segments:
            space.remove(static.shape)
            static_segments.remove(static)
        for static in static_circles:
            space.remove(static.shape)
            static_circles.remove(static)
        if len(space.shapes) < 2:
            stage = 0
        if stage == 0:
            static_segments.append(static_segment(space, 0, screen_height/2+540, 350, (-100, 0), (2000, 0), (0, 154, 23)))
            static_circles.append(static_circle(space, -100, screen_height/2+300, 500, (0, 154, 23)))

            create_house(650, screen_height / 2 + 140)

            create_house(1050, screen_height / 2 + 140)

            create_house(1350, screen_height / 2 + 140)

            create_house(1750, screen_height / 2 + 140)

            # STAR
            current_star = star(screen_width / 4, screen_height / 1.6)

    #screen.fill((128, 206, 225))
    screen.fill((119, 158, 203))

    main_circle.draw()
    for dynamic in dynamics:
        dynamic.draw()
    for static_segment_object in static_segments:
        static_segment_object.draw()
    for static_circle_object in static_circles:
        static_circle_object.draw()
    current_star.draw()

    if get_collision(current_star.collision_rect, main_circle.collision_rect):
        if stage_1 == True and stage_2 == False:
            stage = 2
        if stage_2 == True and stage_3 == False:
            stage = 3
        if stage_3 == True and stage_4 == False:
            stage = 4
        #   current_star = star(random.randint(0, screen_width), random.randint(0, 730))

    space.step(1/35)
    space.gravity = gravity

    if stage_1 == False:
        Main = font_big.render("Crayon Physics", bool(1), (255, 255, 255))
        screen.blit(Main, (screen_width / 3.1, screen_height / 5))
        Play = font_big.render("Play", bool(1), (255, 255, 255))
        Play_massive = font_massive.render("Play", bool(1), (255, 255, 255))
        if cx > 881 and cx < 1052:
            if cy > 389 and cy < 498:
                stage = 1
        if mx > 881 and mx < 1052 and my > 389 and my < 498:
            screen.blit(Play_massive, (screen_width / 2.3, screen_height / 3.2))
        else:
            screen.blit(Play, (screen_width / 2.2, screen_height / 3))
    if stage_1 == True and stage_2 == False:
        tutorial_label_1 = font.render("The objective of the game is to get the green circle to the gold circle", bool(1), (255, 255, 255))
        screen.blit(tutorial_label_1, (screen_width / 20, 250))
        tutorial_label_2 = font.render("Hold down 'w' and move your cursor to create a path for the circle to move", bool(1), (255, 255, 255))
        screen.blit(tutorial_label_2, (screen_width / 20, 350))
        tutorial_label_3 = font.render("Click space once you are done creating your path to test it out",bool(1), (255, 255, 255))
        screen.blit(tutorial_label_3, (screen_width / 20, 450))
        tutorial_label_4 = font_small.render("Hold down 1 to reset the level", bool(1),(255, 255, 255))
        screen.blit(tutorial_label_4, (10, 10))
    if stage_2 == True and stage_3 == False:
        tutorial_label_1 = font_small.render("Try holding down the keys 'e', 'r', 't' and 'y', they each give you different shapes to use",bool(1), (255, 255, 255))
        screen.blit(tutorial_label_1, (screen_width / 50, 250))
        tutorial_label_2 = font_small.render("Hold down 2 to reset the level", bool(1), (255, 255, 255))
        screen.blit(tutorial_label_2, (10, 10))
    if stage_3 == True and stage_4 == False:
        tutorial_label_1 = font_small.render("Hold down 3 to reset the level", bool(1),(255, 255, 255))
        screen.blit(tutorial_label_1, (10, 10))
    if stage_4 == True:
        tutorial_label_1 = font_small.render("Hold down 4 to reset the level", bool(1),(255, 255, 255))
        screen.blit(tutorial_label_1, (10, 10))

    pygame.display.update()
    clock.tick(60)