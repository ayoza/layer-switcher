import pygame, character

from vector import Vec2d as Vector

class Enemy(character.Character):
	group = []
	blue = "enemyBlue"
	yellow = "enemyYellow"
	red = "enemyRed"

	def __init__(self, game, gMap, enemyType, pos, layer):
		super(Enemy, self).__init__(game, gMap, enemyType, pos, layer)

		self.inProximity = False

		if self.type in [Enemy.yellow, Enemy.red]:
			self.moveSpeed = 450
			self.jumpSpeed = -550
			self.jumpTimerLimit = 0.25
			self.swimSpeed = -250

		Enemy.group.append(self)

	def die(self, game):
		self.spawn()

	def update(self, game, dt):
		in_x = abs(self.position.centerx - game.player.position.centerx) < game.halfResolution[0]
		in_y = abs(self.position.centery - game.player.position.centery) < game.halfResolution[1]
		self.inProximity = in_x and in_y

		update = True

		if self.type == Enemy.blue:
			if self.inProximity and self.layer == game.player.layer:

				self.movingLeft = game.player.position.centerx < self.position.centerx
				self.movingRight = game.player.position.centerx > self.position.centerx

				if game.player.position.centery < self.position.centery:
					self.holdJump = True

					if self.resting:
						self.jump()

				if game.player.position.centery > self.position.centery and self.holdJump:
					self.holdJump = False

			elif self.resting and self.velocity.x == 0:
				update = False

		if self.type == Enemy.yellow:
			if self.inProximity:

				if game.player.position.centerx < self.position.centerx:
					self.moveLeft(dt)

				elif game.player.position.centerx > self.position.centerx:
					self.moveRight(dt)

				if game.player.position.centery < self.position.centery:
					self.holdJump = True

					if self.resting:
						self.jump()

				if game.player.position.centery > self.position.centery and self.holdJump:
					self.holdJump = False

			elif self.resting and self.velocity.x == 0:
				update = False

		if self.type == Enemy.red:
			if self.inProximity:

				if game.player.layer > self.layer:
					self.toFront(game)
				elif game.player.layer < self.layer:
					self.toBack(game)

				if game.player.position.centerx < self.position.centerx:
					self.moveLeft(dt)

				elif game.player.position.centerx > self.position.centerx:
					self.moveRight(dt)

				if game.player.position.centery < self.position.centery:
					self.holdJump = True

					if self.resting:
						self.jump()

				if game.player.position.centery > self.position.centery and self.holdJump:
					self.holdJump = False

			elif self.resting and self.velocity.x == 0:
				update = False

		if update:
			super(Enemy, self).update(game, dt)
