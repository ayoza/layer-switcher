import pygame, sys, os, utils, animation, button, options, world, save, game
util = utils.Utils()

class Menu(object):

	def __init__(self, screen, clock, fps, resolution, version):
		self.screen = screen
		self.clock = clock
		self.fps = fps
		self.resolution = resolution
		self.halfResolution = (self.resolution[0] // 2, self.resolution[1] // 2)
		self.fullscreen = False
		self.version = version
		self.volume = pygame.mixer.music.get_volume()
		self.menuObj = None

		self.save = save.Save("opt")

		self.volume = float(self.save.get("volume"))
		if 0 <= self.volume <= 20:
			pygame.mixer.music.set_volume(self.volume * 0.05)

		self.fps = int(self.save.get("fps"))

		self.fullscreen = bool(int(self.save.get("fullscreen")))
		if self.fullscreen:
			pygame.display.set_mode(self.resolution, pygame.FULLSCREEN)

		self.running = True

		for anim in os.listdir("assets/characters/player"):
			info = anim[:anim.find(".")].split("+")
			if info[0] == "standingRight":
				self.logo = animation.Animation("assets/characters/player/%s" % anim, 50, 50, float(info[1]), float(info[2]))
				self.splice = self.logo.getSplice()

		self.background = pygame.image.load("assets/sprites/backgrounds/world1.png").convert_alpha()
		self.bgPos = (0, 0)

		self.smallFont = pygame.font.Font("assets/fonts/OpenSans-Semibold.ttf", 14)
		self.mediumFont = pygame.font.Font("assets/fonts/OpenSans-Semibold.ttf", 30)
		self.bigFont = pygame.font.Font("assets/fonts/OpenSans-Semibold.ttf", 72)

		self.mainText = self.bigFont.render("Layer Switcher", 1, (0, 0, 0))
		self.versionText = self.mediumFont.render(self.version, 1, (0, 0, 0))

		self.currentMenu = ""

		self.mainMenu()

		while self.running:
			dt = self.clock.tick(self.fps)
			pygame.display.set_caption("Layer Switcher %3d FPS" % (self.clock.get_fps()), "Layer Switcher")

			mouseTrigger = False

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.leave()

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						if self.currentMenu == "main":
							self.leave()
						else:
							self.mainMenu()

					if event.key == pygame.K_SPACE:
						if self.currentMenu == "main":
							world.World(self)
						elif self.currentMenu == "world":
							self.world.start()

					if self.currentMenu == "world":
						if event.key == pygame.K_a:
							if self.menuObj.mapIndex > 0:
								self.menuObj.mapDown()
							elif self.menuObj.worldIndex > 0:
								self.menuObj.worldDown()
								self.menuObj.mapIndex = len(self.menuObj.maps) - 2
								self.menuObj.mapUp()

						if event.key == pygame.K_d:
							if self.menuObj.mapIndex < len(self.menuObj.maps) - 1:
								self.menuObj.mapUp()
							elif self.menuObj.worldIndex < len(self.menuObj.worlds) - 1:
								self.menuObj.worldUp()

				if event.type == pygame.MOUSEBUTTONUP:
					if event.button == 1:
						mouseTrigger = True

			self.screen.fill((82, 246, 255))

			mPos = pygame.mouse.get_pos()

			self.bgPos = (
				-util.remap(mPos[0], 0, self.resolution[0], 0, self.background.get_width() - self.resolution[0]),
				-util.remap(mPos[1], 0, self.resolution[1], 0, self.background.get_height() - self.resolution[1])
			)

			self.screen.blit(self.background, self.bgPos)
			self.screen.blit(self.mainText, (self.halfResolution[0] - self.mainText.get_width() // 2, 100))
			self.screen.blit(self.versionText, (5, self.resolution[1] - self.versionText.get_height()))

			if self.currentMenu == "main":
				self.logo.update(dt * 0.001)
				self.screen.blit(self.splice, (self.halfResolution[0] - self.splice.get_width() // 2, 270))

			for butt in button.Button.group:
				butt.updateAndDraw(self.screen, mPos, mouseTrigger)

			pygame.display.flip()

	def mainMenu(self):
		self.currentMenu = "main"

		button.Button.group = []

		button.Button("big", self.mediumFont, "World", (0, self.resolution[1] - 330), self.resolution, lambda: world.World(self))
		button.Button("big", self.mediumFont, "Tutorial", (0, self.resolution[1] - 255), self.resolution, self.tutorial)
		button.Button("big", self.mediumFont, "Options", (0, self.resolution[1] - 180), self.resolution, lambda: options.Options(self))
		button.Button("big", self.mediumFont, "Quit", (0, self.resolution[1] - 105), self.resolution, self.leave)

		if int(self.save.get("displayTip")):
			button.Button("text", self.mediumFont, "Menu Haiku:", (self.halfResolution[0] - 250, self.halfResolution[1] - 150), self.resolution)
			button.Button("medium", self.smallFont, "SPACE makes you advance \\ESCAPE will help you go back \\A and D change map", 
				(self.halfResolution[0] - 250, self.halfResolution[1] - 100), self.resolution, self.hideTip, True)
			button.Button("text", self.smallFont, "Click to hide", (self.halfResolution[0] - 250, self.halfResolution[1] + 5), self.resolution)

	def hideTip(self):
		button.Button.group[-3:] = []
		self.save.set("displayTip", 0)

	def tutorial(self):
		game.Game(self, "Game", "Tutorial")

	def leave(self):
		self.running = False
		pygame.quit()
		sys.exit(0)
