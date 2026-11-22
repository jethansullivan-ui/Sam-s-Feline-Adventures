import pygame, sys
from settings import *
from world import World
from sound_manager import SoundManager

pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=256)
pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sam's Feline Adventures")


class Platformer:
	def __init__(self, screen, width, height):
		self.screen = screen
		self.clock = pygame.time.Clock()
		self.keys_pressed = set()

		self.sound_manager = SoundManager("Sound Effects")
		self.sound_manager.play_music(loops=-1, volume=0.35, force_restart=True)

		self.bg_img = pygame.image.load('Sprites/terrain/bg.png').convert()
		self.bg_img = pygame.transform.scale(self.bg_img, (width, height))

	def main(self):
		world = World(levels[0], self.screen, level_index=0, sound_manager=self.sound_manager)
		while True:
			self.screen.blit(self.bg_img, (0, 0))

			player = world.player.sprite

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_LEFT:
						self.keys_pressed.add("left")
					elif event.key == pygame.K_RIGHT:
						self.keys_pressed.add("right")
					elif event.key == pygame.K_UP:
						self.keys_pressed.add("up")
						if player and player.on_ground and not player.game_over:
							player._jump()
					elif event.key == pygame.K_RETURN:
						if player and player.game_over:
							if player.win:
								if not world.advance_level():
									world.load_level(0)
							else:
								world.reset_world()
							self.keys_pressed.clear()

				elif event.type == pygame.KEYUP:
					if event.key == pygame.K_LEFT:
						self.keys_pressed.discard("left")
					elif event.key == pygame.K_RIGHT:
						self.keys_pressed.discard("right")
					elif event.key == pygame.K_UP:
						self.keys_pressed.discard("up")
						if player:
							player.jump_cut()
							player.jumping = False

			world.update(self.keys_pressed)
			pygame.display.update()
			self.clock.tick(60)


if __name__ == "__main__":
	play = Platformer(screen, WIDTH, HEIGHT)
	play.main()