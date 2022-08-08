import math
import two_body_simulation as tbs
import time
import pygame


class TwoBodyController:

    def __init__(self, m1, m2, eccentricity=0.7):
        self.m1 = m1
        self.m2 = m2
        self.q = m1/m2
        self.u = [1, 1, 0, 0]
        self.eccentricity = eccentricity
        self.positions = tbs.TwoBodyModel(1, 0, 0, 0)

    def initial_velocity(self):
        return math.sqrt((1 + self.q)*(1 + self.eccentricity))


    def update_position(self):
        time_step = 0.15
        self.runge_kutta(time_step, self.u)
        self.calculate_new_position()
        print(math.sqrt(math.pow(self.positions.position_1_x - self.positions.position_2_x, 2) +
                        math.pow(self.positions.position_1_y - self.positions.position_2_y, 2)))

    def calculate_new_position(self):
        r = 1
        a1 = (self.m2/(self.m2 + self.m1))*r
        a2 = (self.m1/(self.m2 + self.m1))*r
        self.positions.position_1_x = -a1 * self.u[0]
        self.positions.position_1_y = -a1 * self.u[1]
        self.positions.position_2_x = a2 * self.u[0]
        self.positions.position_2_y = a2 * self.u[1]

    def derivative(self):
        du = [0, 0, 0, 0]
        m = self.u[0], self.u[1]
        mm = math.sqrt(math.pow(m[0], 2) + math.pow(m[1], 2))
        for i in range(2):
            du[i] = self.u[i + 2]
            du[i + 2] = (-(1 + self.q)*m[i])/math.pow(mm, 3)
        return du

    def runge_kutta(self, h, u):
        a = [h/2, h/2, h, 0]
        b = [h/6, h/3, h/3, h/6]
        u0 = []
        ut = []
        dimension = len(self.u)
        for i in range(dimension):
            u0.append(u[i])
            ut.append(0)
        for i in range(4):
            du = self.derivative()
            for j in range(dimension):
                u[i] = u0[i] + a[j] * du[i]
                ut[i] = ut[i] + b[j] * du[i]
        for i in range(dimension):
            u[i] = u0[i] + ut[i]

d = TwoBodyController(5, 15)


def player(x1,y1,x2,y2):
    screen.blit(image_1, (x1, y1))
    screen.blit(image_2, (x2, y2))

pygame.init()
screen = pygame.display.set_mode((900, 600))
pygame.display.set_caption("Two Body Simulation")

image_1 = pygame.image.load("ven.png")
image_1 = pygame.transform.scale(image_1, (d.m1*10, d.m1*10))


image_2 = pygame.image.load("jup.png")
image_2 = pygame.transform.scale(image_2, (d.m2*10, d.m2*10))

running = True
while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    img1_x = d.positions.position_1_x + 300
    img1_y = d.positions.position_1_y + 200

    img2_x = d.positions.position_2_x + 300
    img2_y = d.positions.position_2_y + 200
    player(img1_x, img1_y, img2_x, img2_y)
    time.sleep(0.02)
    d.update_position()
    pygame.display.update()









