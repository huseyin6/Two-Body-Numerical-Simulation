# imported library
import pygame
import time
import math


class TwoBodyView:

    # init function
    def __init__(self, body1_x, body1_y, body2_x, body2_y, mass_1, mass_2):
        self.body1_x = body1_x
        self.body1_y = body1_y
        self.body2_x = body2_x
        self.body2_y = body2_y
        self.mass_1 = mass_1
        self.mass_2 = mass_2
        pygame.init()
        pygame.display.set_caption("Two Body Simulation")
        self.screen = pygame.display.set_mode((900, 650))
        self.image_1 = pygame.image.load("ven.png")
        self.image_2 = pygame.image.load("jup.png")
        self.image_1 = pygame.transform.scale(self.image_1, (self.mass_1 * 5, self.mass_1 * 5))
        self.image_2 = pygame.transform.scale(self.image_2, (self.mass_2 * 5, self.mass_2 * 5))
        self.eccentricity = 0
        self.set_eccentricity()

    # to update the mass location which info comes from the main
    def set_body_coordinate(self, img1_x, img1_y, img2_x, img2_y):
        self.body1_x = 350 + img1_x*300
        self.body1_y = 300 + img1_y*10
        self.body2_x = 350 + img2_x*300
        self.body2_y = 300 + img2_y*10

    def set_eccentricity(self):
        self.eccentricity = math.sqrt(math.pow(self.body2_x - self.body1_x, 2) + math.pow(self.body2_y - self.body1_y, 2))

    def get_eccentricity(self):
        return self.eccentricity

    def set_body_mass(self, m1, m2):
        self.mass_1 = m1
        self.mass_2 = m2
        self.image_1 = pygame.transform.scale(self.image_1, (self.mass_1 * 5, self.mass_1 * 5))
        self.image_2 = pygame.transform.scale(self.image_2, (self.mass_2 * 5, self.mass_2 * 5))


    def player(self, x1, y1, x2, y2):
        self.screen.blit(self.image_1, (x1, y1))
        self.screen.blit(self.image_2, (x2, y2))


    def display_spirit(self, data, indicator):
        while True:
            print(self.body1_x, self.body1_y, self.body2_x, self.body2_y)
            self.screen.fill((0, 0, 0))
            if indicator >= len(data):
                return False
            else:
                color_red = (255, 100, 100)
                color_dark_red = (255, 10, 10)
                small_font = pygame.font.SysFont('Corbel', 25)
                text_stop = small_font.render("STOP", True, (255, 255, 255))
                mouse = pygame.mouse.get_pos()
                running = True
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if (10 <= mouse[0] <= 150) and (540 <= mouse[1] <= 580):
                            return False
                if (10 <= mouse[0] <= 150) and (540 <= mouse[1] <= 580):
                    pygame.draw.rect(self.screen, color_dark_red, [10, 540, 140, 40])
                else:
                    pygame.draw.rect(self.screen, color_red, [10, 540, 140, 40])
                self.screen.blit(text_stop, (40, 550))
                x_1 = (self.mass_2/(self.mass_2+self.mass_1))*float(data[indicator][0])*2
                y_1 = (self.mass_2/(self.mass_2+self.mass_1))*float(data[indicator][1])*100
                x_2 = (-self.mass_2/(self.mass_2+self.mass_1))*float(data[indicator][0])*2
                y_2 = (-self.mass_2/(self.mass_2+self.mass_1))*float(data[indicator][1])*100

                self.set_body_coordinate(x_1,y_1,x_2,y_2)
                self.player(self.body1_x, self.body1_y, self.body2_x, self.body2_y)
                self.set_eccentricity()
                pygame.display.update()
                indicator += 1


    def mass_plus(self):
        self.image_1 = pygame.image.load("ven.png")
        self.image_2 = pygame.image.load("jup.png")
        self.mass_1 += 2
        self.mass_2 += 2
        self.image_1 = pygame.transform.scale(self.image_1, (self.mass_1 * 10, self.mass_1 * 10))
        self.image_2 = pygame.transform.scale(self.image_2, (self.mass_2 * 10, self.mass_2 * 10))


    def mass_minus(self):
        self.image_1 = pygame.image.load("ven.png")
        self.image_2 = pygame.image.load("jup.png")
        self.mass_1 -= 1
        self.mass_2 -= 1
        self.image_1 = pygame.transform.scale(self.image_1, (self.mass_1 * 5, self.mass_1 * 5))
        self.image_2 = pygame.transform.scale(self.image_2, (self.mass_2 * 5, self.mass_2 * 5))

    def eccentricity_plus(self):
        if self.body1_x < self.body2_x:
            self.body1_x -= 10
            self.body2_x += 10
            if self.body1_y < self.body2_y:
                self.body1_y -= 10
                self.body2_y += 10
            else:
                self.body1_y += 10
                self.body2_y -= 10
        else:
            self.body1_x += 10
            self.body2_x -= 10
            if self.body1_y < self.body2_y:
                self.body1_y -= 10
                self.body2_y += 10
            else:
                self.body1_y += 10
                self.body2_y -= 10
            self.set_eccentricity()

    def eccentricity_minus(self):
        if self.body1_x > self.body2_x:
            self.body1_x -= 10
            self.body2_x += 10
            if self.body1_y < self.body2_y:
                self.body1_y -= 10
                self.body2_y += 10
            else:
                self.body1_y += 10
                self.body2_y -= 10
        else:
            self.body1_x += 10
            self.body2_x -= 10
            if self.body1_y > self.body2_y:
                self.body1_y -= 10
                self.body2_y += 10
            else:
                self.body1_y += 10
                self.body2_y -= 10
            self.set_eccentricity()

    def get_body1_coordinates(self):
        return self.body1_x, self.body1_y

    def get_body2_coordinates(self):
        return self.body2_x, self.body2_y

    # game loop
    def circulation(self, data):
        color_red = (255, 100, 100)
        color_dark_red = (255, 10, 10)

        color_light = (10, 10, 255)

        # dark shade of the button
        color_dark = (100, 100, 255)

        # defining a font
        small_font = pygame.font.SysFont('Corbel', 25)

        is_start = False

        # rendering a text written in
        # this font
        text_mass_plus = small_font.render('+Mass', True, (255, 255, 255))
        text_mass_minus = small_font.render('-Mass', True, (255, 255, 255))
        text_eccentricity_plus = small_font.render('+Eccentricity', True, (255, 255, 255))
        text_eccentricity_minus = small_font.render('-Eccentricity', True, (255, 255, 255))
        text_begin = small_font.render("START", True, (255, 255, 255))
        running = True
        while running:
            self.screen.fill((0, 0, 0))  # by RGB we set the screen color as black
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    margin = 100
                    if (margin <= mouse[0] <= (margin + 140)) and (0 <= mouse[1] <= 40):
                        self.mass_plus()
                    margin += 180
                    if (margin <= mouse[0] <= (margin + 140)) and (0 <= mouse[1] <= 40):
                        self.mass_minus()
                    margin += 180
                    if (margin <= mouse[0] <= (margin + 140)) and (0 <= mouse[1] <= 40):
                        self.eccentricity_plus()
                    margin += 180
                    if (margin <= mouse[0] <= (margin + 140)) and (0 <= mouse[1] <= 40):
                        self.eccentricity_minus()

                    # begin to the motion
                    if (380 <= mouse[0] <= 520) and (540 <= mouse[1] <= 580):
                        is_start = True
                        running = self.display_spirit(data, 0)
            mouse = pygame.mouse.get_pos()

            # button 1 text_mass_plus
            margin = 100
            if (margin <= mouse[0] <= (margin + 140)) and (0 <= mouse[1] <= 40):
                pygame.draw.rect(self.screen, color_light, [margin, 0, 140, 40])
            else:
                pygame.draw.rect(self.screen, color_dark, [margin, 0, 140, 40])

            # button 2 text_mass_minus
            margin += 180
            if (margin <= mouse[0] <= (margin + 140)) and (0 <= mouse[1] <= 40):
                pygame.draw.rect(self.screen, color_light, [margin, 0, 140, 40])
            else:
                pygame.draw.rect(self.screen, color_dark, [margin, 0, 140, 40])
                
            # button 3 text_ecc.._plus
            margin += 180
            if (margin <= mouse[0] <= (margin + 140)) and (0 <= mouse[1] <= 40):
                pygame.draw.rect(self.screen, color_light, [margin, 0, 140, 40])
            else:
                pygame.draw.rect(self.screen, color_dark, [margin, 0, 140, 40])

            # button 4 text_ecc..minus
            margin += 180
            if (margin <= mouse[0] <= (margin + 140)) and(0 <= mouse[1] <= 40):
                pygame.draw.rect(self.screen, color_light, [margin, 0, 140, 40])
            else:
                pygame.draw.rect(self.screen, color_dark, [margin, 0, 140, 40])

            # button 5 begin_to_orbit
            if (380 <= mouse[0] <= 520) and (540 <= mouse[1] <= 580):
                pygame.draw.rect(self.screen, color_dark_red, [380, 540, 140, 40])
            else:
                pygame.draw.rect(self.screen, color_red, [380, 540, 140, 40])


            # superimposing the text onto our button
            self.screen.blit(text_mass_plus, (120, 0))
            self.screen.blit(text_mass_minus, (310, 0))
            self.screen.blit(text_eccentricity_plus, (465, 0))
            self.screen.blit(text_eccentricity_minus, (650, 0))
            self.screen.blit(text_begin, (410, 550))
            self.player(self.body1_x, self.body1_y, self.body2_x, self.body2_y)

            pygame.display.update()