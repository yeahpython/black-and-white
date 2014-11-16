import pickle
import os
#os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,0)

import pygame
from pygame import draw, Surface
if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

from math import cos, sin, floor

import random
import copy

import graphics

game_title = "black and white"
black = (0, 0, 0)
white = (255, 255, 255)
transparent = (200, 200, 200)

def initialization():
	pygame.init()
	pygame.display.set_mode(graphics.screen_size)
	pygame.display.set_caption(game_title)

def main_loop():

	'''these things only need to happen once'''
	screen = pygame.display.get_surface()
	screen.fill(black)

	clock = pygame.time.Clock()
	dt=0
	font = pygame.font.Font(None, 30)
	while 1:
		guam = World()

		#waves = Waves()
		#guam.add_child(waves)
		for z in range(2):
			island = Island(screen.get_size(), z, 10 + z * 13)
			guam.add_child(island)

			for x in range(5):
				s = int(random.random() * 20 + 10)
				triangle = Tree(screen.get_width() * random.random(), screen.get_height() * random.random(), island, s)
				guam.add_child(triangle)


			for j in range(2):
				tent = Tent([])
				

				x = (screen.get_width()-120) * random.random()
				y = (screen.get_height()) * random.random()

				for i in range(4):
					s = int(random.random() * 20 + 5)
					if i == 1 or i == 2:
						s += 10
					x += 30 * random.random()
					pole = Pole(x, y + 20 * random.random(), island, s)
					tent.poles.append(pole)
					guam.add_child(pole)

				guam.add_child(tent)



		while 1:
			dt = clock.tick(40)
			guam.update(dt)
			guam.render_to(screen)
			pygame.display.flip()
			pygame.event.pump()

			if pygame.event.get(pygame.QUIT):
				return 0

			if any(pygame.mouse.get_pressed()):
				break

class World(object):
	def __init__(self):
		self.objects = []
		self.surface = Surface(graphics.screen_size)
		self.name_accessible = {}

	def update(self, dt):
		for child in self.objects:
			child.update(dt)

	def add_child(self, child, name = "", depth = 0):
		self.objects.append(child)
		if name:
			self.name_accessible[name] = child

	def render_to(self, screen):
		screen.fill(black)
		for child in self.objects:
			child.render_to(screen)

class WorldObject(object):
	def __init__(self):
		self.buffer = 0
		self.buffer_needs_update = 1
		self.name = ""

	def render_to(self, screen):
		'''client-side'''
		if self.buffer_needs_update:
			self.update_buffer(screen.get_size())
			self.buffer_needs_update = 0
		screen.blit(self.buffer, (0, 0))


	def update_buffer(self, size):
		self.buffer = Surface(size)
		self.buffer.set_colorkey(transparent)
		self.buffer.fill(transparent)
		self.redraw()

	def redraw(self):
		pass

	def update(self, dt):
		pass

class Tent(WorldObject):
	def __init__(self, poles):
		self.poles = poles

	def render_to(self, screen):
		points = [(pole.x, pole.y - pole.size) for pole in self.poles]
		draw.polygon(screen, white, points)
		draw.lines(screen, white, True, points)

class SmallObject(WorldObject):
	def __init__(self, x, y):
		super(SmallObject, self).__init__()
		self.x = int(x)
		self.y = int(y)
		self.buffer_x = 15
		self.buffer_y = 15
		self.buffer_w = 30
		self.buffer_h = 30

	def render_to(self, screen):
		if self.buffer_needs_update:
			self.update_buffer((self.buffer_w, self.buffer_h))
			self.buffer_needs_update = 0
		screen.blit(self.buffer, (self.x - self.buffer_x, self.y - self.buffer_y))

class GravityObject(SmallObject):
	def __init__(self, x, y, island):
		super(GravityObject, self).__init__(x, y)
		self.vx = 0
		self.vy = 0
		self.island = island

	def update(self, dt):
		self.y += self.vy
		if self.island.heights and self.y >= self.island.heights[self.x]:
			self.y = self.island.heights[self.x]
			self.vy = 0
		else:
			self.vy += 2



class Loop(GravityObject):
	def __init__(self, x, y, island):
		super(Loop, self).__init__(x, y, island)
		self.pointlist = [(0,0), (5, -5), (-5, -5)]

	def redraw(self):
		offset_pointlist = [(self.buffer_x + x, self.buffer_y + y) for x, y in self.pointlist]
		draw.polygon(self.buffer, black, offset_pointlist)
		draw.lines(self.buffer, white, True, offset_pointlist)
	
	def update_buffer(self, size):
		self.buffer_w = max(x for x,y in self.pointlist) - min(x for x,y in self.pointlist) + 1
		self.buffer_h = max(y for x,y in self.pointlist) - min(y for x,y in self.pointlist) + 1
		self.buffer_x = - min(x for x,y in self.pointlist)
		self.buffer_y = - min(y for x,y in self.pointlist)
		super(Loop, self).update_buffer((self.buffer_w, self.buffer_h))

class Tree(Loop):
	def __init__(self, x, y, island, size):
		super(Tree, self).__init__(x, y, island)
		self.pointlist = []
		self.generate_points(size)
		self.size = size

	def generate_points(self, s):
		self.pointlist = [ (s*0.7*sin(t), s * 1.4 *( cos(t) - 2)) for t in range(6)]
		self.pointlist = [(x + random.random() * 10 - 5, y - random.random()*10) for x,y in self.pointlist]
		self.pointlist.extend([ (0, -1.2*s),(0,0), (0, -1.2*s)])

	def redraw(self):
		super(Tree, self).redraw()

class Pole(Loop):
	def __init__(self, x, y, island, size):
		super(Pole, self).__init__(x, y, island)
		self.pointlist = []
		self.generate_points(size)
		self.size = size

	def generate_points(self, s):
		self.pointlist = [(0, -s),(0, -s),(0,0)]

	def redraw(self):
		super(Pole, self).redraw()

class Island(WorldObject):
	def __init__(self, size, color, n = 20, ):
		super(Island, self).__init__()
		self.buffer = Surface(size)
		self.pointlist = []
		self.heights = []
		self.n = n
		self.color = color

	def redraw(self):
		self.pointlist = []
		self.heights = []
		if not self.pointlist:
			self.generate_terrain(self.buffer.get_size())

		if self.color:
			draw.polygon(self.buffer, white, self.pointlist)
		else:
			draw.polygon(self.buffer, black, self.pointlist)
		draw.lines(self.buffer, white, True, self.pointlist)
		#draw.lines(screen, [255, 0, 0], False, [(i, val) for i, val in enumerate(self.heights)])

	def generate_terrain(self, size):
		width, height = size
		scaling = 1.0 * width / self.n
		cumulative = [x * scaling for x in random_wander(self.n)]
		# turn heights into points
		self.pointlist = [(i * scaling, value + height - 300) for i, value in enumerate(cumulative) ]
		for x in range(width):
			i = floor(x / scaling)
			if i < 0:
				i = 0
			if i >= len(self.pointlist)-1:
				i = len(self.pointlist)-2
			remainder = x - i * scaling
			i = int(i)
			leftwidth, leftheight = self.pointlist[i]
			rightwidth, rightheight = self.pointlist[i + 1]
			h = leftheight + (rightheight - leftheight) * remainder / scaling
			self.heights.append(h)
		# add bottom right and bottom left
		self.pointlist.extend([size, (0, height)])

def random_wander(n):
	randomness = [random.random() - 0.5 for x in range(n)]
	cumulative = [0]
	for r in randomness:
		cumulative.append(cumulative[-1] + r)
	cumulative = [value - cumulative[-1] * i / n for i, value in enumerate(cumulative)]
	return cumulative



'''class Waves(WorldObject):
	def __init__(self):
		super(Island, self).__init__()

	def redraw(self):
		pointlist = [(x , 300 + 5 * sin(x / 50.0)) for x in range(screen.get_width())]
		draw.lines(self.buffer, white, False, pointlist)'''

def main():
	initialization()

	pygame.event.set_blocked(None)
	pygame.event.set_allowed(pygame.QUIT)

	main_loop()