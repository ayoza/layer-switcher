import pygame, utils, particles, enemy

from vector import Vec2d as Vector
util = utils.Utils()

class Viewport(object):

	def __init__(self, game, x, y):
		self.position = Vector(x, y)
		self.resolution = Vector(game.resolution)
		self.halfResolution = Vector(game.halfResolution)
		self.rect = pygame.rect.Rect(self.position - self.halfResolution, self.resolution)
		self.update(game, x, y)

	def update(self, game, x, y):
		vec = Vector(x - self.position.x, y - self.position.y) * 0.05
		if vec.length < 0.05:
			vec = Vector(0, 0)

		self.position += vec
		self.resolution = Vector(game.resolution)
		self.rect = pygame.rect.Rect(self.position - self.halfResolution, self.resolution)

		if self.rect.x < 0:
			self.rect.x = 0

		if self.rect.x > game.map.width - self.resolution.x:
			self.rect.x = game.map.width - self.resolution.x

		if self.rect.y < 0:
			self.rect.y = 0

		if self.rect.y > game.map.height - self.resolution.y:
			self.rect.y = game.map.height - self.resolution.y

		game.player.rect.x = game.player.position.x - self.rect.x
		game.player.rect.y = game.player.position.y - self.rect.y

		game.player.cdBar = pygame.rect.Rect(
			(game.player.rect.left, game.player.rect.bottom + 2),
			(util.remap(game.player.layerCooldown, 0, 0.5, 0, game.player.rect.width), 5)
		)

		for gEnemy in enemy.Enemy.group:
			gEnemy.rect.x = gEnemy.position.x - self.rect.x
			gEnemy.rect.y = gEnemy.position.y - self.rect.y

		for group in particles.Particles.groups:
			group.setOffset(self.rect.topleft)

		if game.map.background:
			bgx = -util.remap(self.rect.x, 0, game.map.width - self.resolution.x, 0, game.map.bgSize[0] - self.resolution.x)
			bgy = -util.remap(self.rect.y, 0, game.map.height - self.resolution.y, 0, game.map.bgSize[1] - self.resolution.y)
			game.map.bgOffset = (bgx, bgy)

		for layer in game.map.totalLayers:
			for block in layer:
				block.rect.x = block.x - self.rect.x
				block.rect.y = block.y - self.rect.y
