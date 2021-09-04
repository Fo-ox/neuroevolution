import pygame
import random
import sys
import math

width = 1024
height = 1024
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
		self.car_sprite = pypgame.image.load("carImg/" + random.choice(self.car_sprites) + ".png")
		self.car_sprite = pypgame.transform.scale(self.car_sprite,
			(math.floor(self.car_sprite.get_size([0]/1.5), math.floor(self.car_sprite.get_size()[1]/1.5))))

		self.car = self.car_sprite

		# pos & center
		self.pos = [650,922]
		self.compute_center()


	def compute_center(self):
		self.center = (self.pos[0] + (self.car.get_size()[0]/2), self.pos[1] + (self.car.get_size()[1]/2))

	def draw(self, screen):
		screen.blit(self.car, self.pos)
		self.draw_radars(screen)

	def draw_center(self, screen):
		pypgame.draw.circle(screen, (0,72,186), (math.floor(self.center[0]), math.floor(self.center[1])), 5)

	def compute_radars(self, degree, road):
		length = 0
		x = int(self.center[0] + math.cos(math.radians(360 - (self.angle + degree))) * length)
		y = int(self.center[1] + math.cos(math.radians(360 - (self.angle + degree))) * length)

		while not road.get_at((x, y) == bg and length < 360):
			length += 1
			x = int(self.center[0] + math.cos(math.radians(360 - (self.angle + degree))) * length)
			y = int(self.center[1] + math.cos(math.radians(360 - (self.angle + degree))) * length)

		dist = int(math.sqrt(math.pow(x - self.center[0], 2) + math.pow(y - self.center[1], 2)))
		self.radars.append([(x, y), dist])

	def draw_radars(self, screen):
		for r in self.radars:
			p, d = r
			pypgame.draw.line(screen, (158,232,55), self.center, p, 1)
			pypgame.draw.circle(screen, (158,232,55), p, 5)


	def compute_collision_points(self):
		self.compute_center()
		lw, lh = 65

		lt = [self.center[0] + math.cos(math.radians(360 - (self.angle + 20))) * lw,
		      self.center[1] + math.sin(math.radians(360 - (self.angle + 20))) * lh]
		rt = [self.center[0] + math.cos(math.radians(360 - (self.angle + 160))) * lw,
		      self.center[1] + math.sin(math.radians(360 - (self.angle + 160))) * lh]

		lb = [self.center[0] + math.cos(math.radians(360 - (self.angle + 200))) * lw,
		      self.center[1] + math.sin(math.radians(360 - (self.angle + 200))) * lh]
		rb = [self.center[0] + math.cos(math.radians(360 - (self.angle + 340))) * lw,
		      self.center[1] + math.sin(math.radians(360 - (self.angle + 340))) * lh]

		self.collision_points = []

	def draw_collision_points(self, road):
		pass

	def check_collision(self, road):
		pass

	def rotate(self, angle):
		orig_rect = self.car_sprite.get_rect()
		rot_image = pypgame.transform.rotate(self.car_sprite, angle)
		rot_rect = orig_rect.copy()
		rot_rect.center = rot_image.get_rect().center
		rot_image = rot_image.subsurface(rot_rect).copy()

		self.car = rot_image




# TEST THIS
if __name__ == "__main__":
	pypgame.init()
	screen = pypgame.display.set_mode((width, height))
	clock = pypgame.time.Clock()

	road = pypgame.image.load("roadImg/road-1.png")

	c = Car()
	c.angle = 0

	while  True:
		for event in pypgame.event.get():
			if event.type == pypgame.QUIT:
				sys.exit(0)

			screen.blit(road, (0,0))

			c.angle -= 1
			c.rotate(c.angle)

			c.radars = []
			for d in range(-90, 120, 45):
				c.compute_radars(d, road)

			c.compute_collision_points()

			c.draw()
			c.draw_center()
			c.draw_collision_points()

			pypgame.display.flip()
			clock.tick(0)





