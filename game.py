import pygame
from settings import HEIGHT, WIDTH

pygame.font.init()


class Game:
	def __init__(self, screen):
		self.screen = screen
		self.font = pygame.font.SysFont("impact", 70)
		self.small_font = pygame.font.SysFont("impact", 30)
		self.hud_font = pygame.font.SysFont("impact", 26)
		self.message_color = pygame.Color("darkorange")
		self.sub_color = pygame.Color("white")
		self.lost_sound_played = False

	def reset_flags(self):
		self.lost_sound_played = False

	# if player ran out of life or fell below the platform
	def _game_lose(self, player, level_index, sound_manager=None):
		if not self.lost_sound_played and sound_manager:
			sound_manager.stop_music()
			sound_manager.play("gameover")
			self.lost_sound_played = True
		player.game_over = True
		player.win = False
		message = self.font.render('You Lose...', True, self.message_color)
		sub_message = self.small_font.render(
			f'Press Enter to Retry Level {level_index + 1}', True, self.sub_color
		)
		self.screen.blit(message, (WIDTH // 3 + 70, 70))
		self.screen.blit(sub_message, (WIDTH // 3 + 55, 150))

	# if player reaches the goal
	def _game_win(self, player, level_index, total_levels):
		player.game_over = True
		player.win = True
		is_final_level = (level_index + 1) >= total_levels
		if is_final_level:
			title_text = 'You Beat All Levels!'
			prompt_text = 'Press Enter to Play Again (Level 1)'
		else:
			title_text = f'Level {level_index + 1} Clear!'
			prompt_text = f'Press Enter for Level {level_index + 2}'

		message = self.font.render(title_text, True, self.message_color)
		sub_message = self.small_font.render(prompt_text, True, self.sub_color)
		self.screen.blit(message, (WIDTH // 4 + 30, 70))
		self.screen.blit(sub_message, (WIDTH // 4 + 65, 150))

	# checks if the game is over or not, and if win or lose
	def game_state(self, player, goal, level_index, total_levels, sound_manager=None):
		if player.life <= 0 or player.rect.y >= HEIGHT:
			self._game_lose(player, level_index, sound_manager=sound_manager)
		elif player.rect.colliderect(goal.rect):
			self._game_win(player, level_index, total_levels)

	def show_hud(self, player, level_index, total_levels):
		life_size = 30
		img_path = "Sprites/life/life.png"
		life_image = pygame.image.load(img_path).convert_alpha()
		life_image = pygame.transform.scale(life_image, (life_size, life_size))
		indent = 0
		for _ in range(max(0, player.life)):
			indent += life_size
			self.screen.blit(life_image, (indent, life_size))

		level_label = self.hud_font.render(
			f"Level {level_index + 1} / {total_levels}", True, self.sub_color
		)
		self.screen.blit(level_label, (WIDTH - 150, life_size))