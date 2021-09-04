import pygame
import random
import sys
import math

width = 750
height = 750
bg = (176, 144, 104, 255)

class Car:

	# list of car

	car_sprites = ("purple", "red", "orange", "yellow", "green", "blue", "black", "grey", "white")

	def __init__(self):
		self.random_sprite()

		self.angle = 0
		self.speed = 5

		self.radars = []
		self.collision_points = []

		self.is_alive = True
		self.distance = 0
		self.time_spent = 0

	def random_sprite(self):
		self.car_sprite = pygame.image.load('car/' + random.choice(self.car_sprites) + '.png')
		self.car_sprite = pygame.transform.scale(self.car_sprite, (int(math.floor(self.car_sprite.get_size()[0]/2)), int(math.floor(self.car_sprite.get_size()[1]/2))))
		self.car = self.car_sprite

		# recompute
		self.pos = [62, 400]
		self.compute_center()


	def compute_center(self):
		self.center = (self.pos[0] + (self.car.get_size()[0]/2), self.pos[1] + (self.car.get_size()[1]/2))

	def draw(self, screen):
		screen.blit(self.car, self.pos)
		self.draw_radars(screen)

	def draw_center(self, screen):
		pygame.draw.circle(screen, (0,72,186), (int(math.floor(self.center[0])), int(math.floor(self.center[1]))), 5)
                           
	def compute_radars(self, degree, road):
		length = 0
		x = int(self.center[0] + math.cos(math.radians(360 - (self.angle + degree - 90))) * length)
		y = int(self.center[1] + math.sin(math.radians(360 - (self.angle + degree - 90))) * length)

		while not road.get_at((x, y)) == bg and length < 300:
			length = length + 1
			x = int(self.center[0] + math.cos(math.radians(360 - (self.angle + degree - 90))) * length)
			y = int(self.center[1] + math.sin(math.radians(360 - (self.angle + degree - 90))) * length)

		dist = int(math.sqrt(math.pow(x - self.center[0], 2) + math.pow(y - self.center[1], 2)))
		self.radars.append([(x, y), dist])

	def draw_radars(self, screen):
		for r in self.radars:
			p, d = r
			pygame.draw.line(screen, (183,235,70), self.center, p, 1)
			pygame.draw.circle(screen, (183,235,70), p, 5)


	def compute_collision_points(self):
		self.compute_center()
		lw = 40
		lh = 40

		lt = [self.center[0] + math.cos(math.radians(360 - (self.angle + 20 + 90 ))) * lw, self.center[1] + math.sin(math.radians(360 - (self.angle + 20 + 90))) * lh]
		rt = [self.center[0] + math.cos(math.radians(360 - (self.angle + 160 + 90))) * lw, self.center[1] + math.sin(math.radians(360 - (self.angle + 160 + 90))) * lh]
		lb = [self.center[0] + math.cos(math.radians(360 - (self.angle + 200 + 90))) * lw, self.center[1] + math.sin(math.radians(360 - (self.angle + 200 + 90))) * lh]
		rb = [self.center[0] + math.cos(math.radians(360 - (self.angle + 340 + 90))) * lw, self.center[1] + math.sin(math.radians(360 - (self.angle + 340 + 90))) * lh]

		self.collision_points = [lt, rt, lb, rb]

	def draw_collision_points(self, road):
		if not self.collision_points:
			self.compute_collision_points()

		for p in self.collision_points:
			if(road.get_at((int(p[0]), int(p[1]))) == bg):
				pygame.draw.circle(screen, (255,0,0), (int(p[0]), int(p[1])), 5)
			else:
				pygame.draw.circle(screen, (15,192,252), (int(p[0]), int(p[1])), 5)

	def check_collision(self, road):
		pass

	def rotate(self, angle):
		orig_rect = self.car_sprite.get_rect()
		rot_image = pygame.transform.rotate(self.car_sprite, angle)
		rot_rect = orig_rect.copy()
		rot_rect.center = rot_image.get_rect().center
		rot_image = rot_image.subsurface(rot_rect).copy()

		self.car = rot_image




# TEST THIS
if __name__ == "__main__":
	pygame.init()
	screen = pygame.display.set_mode((width, height))
	clock = pygame.time.Clock()

	road = pygame.image.load("roadImg/road-2.png")

	c = Car()
	c.angle = 0

	while  True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit(0)

		screen.blit(road, (0,0))

		c.angle -= 1
		c.rotate(c.angle)
        
		c.radars = []
		for d in range(-90, 120, 45):
			c.compute_radars(d, road)
            
		c.compute_collision_points()

		c.draw(screen)
		c.draw_center(screen)
		c.draw_collision_points(road)

		pygame.display.flip()
		clock.tick(0)