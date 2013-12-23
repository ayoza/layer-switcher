#!/usr/bin/env python

import pygame, game

class Main(object):

	def __init__(self):
		objClock = pygame.time.Clock()
		fps = 120.
		resolution = (1280, 720)
		icon = pygame.image.load("assets/icons/icon.png")
		pygame.display.set_icon(icon)
		pygame.display.set_caption("Layer Switcher", "Layer Switcher")
		objScreen = pygame.display.set_mode(resolution)
		font = pygame.font.Font("assets/ARLRDBD.ttf", 30)
		objGame = game.Game(objScreen, objClock, fps, font, resolution)

if __name__ == "__main__":
	pygame.init()
	Main()
