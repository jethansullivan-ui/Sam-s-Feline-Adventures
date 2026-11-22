import pygame
from settings import tile_size, WIDTH, GRAVITY, levels
from tile import Tile
from trap import Trap
from goal import Goal
from player import Player
from game import Game


class World:
	def __init__(self, world_data, screen, level_index=0, sound_manager=None):
		self.screen = screen
		self.sound_manager = sound_manager
		self.levels = levels
		self.current_level_index = level_index
		self.world_data = self.levels[self.current_level_index] if world_data is None else world_data
		self.world_shift = 0
		self.current_x = 0
		self.trap_cooldown = 0
		self.gravity = GRAVITY
		self.game = Game(self.screen)
		self._setup_world(self.world_data)

	# generates the world
	def _setup_world(self, layout):
		self.tiles = pygame.sprite.Group()
		self.traps = pygame.sprite.Group()
		self.player = pygame.sprite.GroupSingle()
		self.goal = pygame.sprite.GroupSingle()

		for row_index, row in enumerate(layout):
			for col_index, cell in enumerate(row):
				x, y = col_index * tile_size, row_index * tile_size
				if cell == "X":
					tile = Tile((x, y), tile_size)
					self.tiles.add(tile)
				elif cell == "t":
					tile = Trap((x + (tile_size // 4), y + (tile_size // 4)), tile_size // 2)
					self.traps.add(tile)
				elif cell == "P":
					player_sprite = Player((x, y), sound_manager=self.sound_manager)
					self.player.add(player_sprite)
				elif cell == "G":
					goal_sprite = Goal((x, y), tile_size)
					self.goal.add(goal_sprite)

	# resets only the level the player is currently on
	def reset_world(self):
		self.world_data = self.levels[self.current_level_index]
		self.world_shift = 0
		self.current_x = 0
		self.trap_cooldown = 0
		self.game.reset_flags()
		self._setup_world(self.world_data)
		if self.sound_manager:
			self.sound_manager.play_music(loops=-1, volume=0.35, force_restart=True)

	# loads a specific level by index
	def load_level(self, level_index):
		self.current_level_index = level_index % len(self.levels)
		self.world_data = self.levels[self.current_level_index]
		self.world_shift = 0
		self.current_x = 0
		self.trap_cooldown = 0
		self.game.reset_flags()
		self._setup_world(self.world_data)
		if self.sound_manager:
			self.sound_manager.play("savepoint")
			self.sound_manager.play_music(loops=-1, volume=0.35, force_restart=True)

	# advances to the next level; returns True if loaded, False if final level cleared
	def advance_level(self):
		if self.current_level_index + 1 < len(self.levels):
			self.load_level(self.current_level_index + 1)
			return True
		return False

	# world scroll when the player is walking towards left/right
	def _scroll_x(self):
		player = self.player.sprite
		player_x = player.rect.centerx
		direction_x = player.direction.x

		if player_x < WIDTH // 3 and direction_x < 0:
			self.world_shift = 8
			player.speed = 0
		elif player_x > WIDTH - (WIDTH // 3) and direction_x > 0:
			self.world_shift = -8
			player.speed = 0
		else:
			self.world_shift = 0
			player.speed = 3

	# add gravity for player to fall
	def _apply_gravity(self, player):
		player.direction.y += self.gravity
		player.rect.y += player.direction.y

	# prevents player from passing through objects horizontally
	def _horizontal_movement_collision(self):
		player = self.player.sprite
		player.rect.x += player.direction.x * player.speed

		for sprite in self.tiles.sprites():
			if sprite.rect.colliderect(player.rect):
				if player.direction.x < 0:
					player.rect.left = sprite.rect.right
					player.on_left = True
					self.current_x = player.rect.left
				elif player.direction.x > 0:
					player.rect.right = sprite.rect.left
					player.on_right = True
					self.current_x = player.rect.right
		if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
			player.on_left = False
		if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
			player.on_right = False

	# prevents player from passing through objects vertically
	def _vertical_movement_collision(self):
		player = self.player.sprite
		self._apply_gravity(player)

		for sprite in self.tiles.sprites():
			if sprite.rect.colliderect(player.rect):
				if player.direction.y > 0:
					player.rect.bottom = sprite.rect.top
					player.direction.y = 0
					player.on_ground = True
				elif player.direction.y < 0:
					player.rect.top = sprite.rect.bottom
					player.direction.y = 0
					player.on_ceiling = True
		if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
			player.on_ground = False
		if player.on_ceiling and player.direction.y > 0:
			player.on_ceiling = False

	# add consequences when player runs through traps
	def _handle_traps(self):
		if self.trap_cooldown > 0:
			return

		player = self.player.sprite
		for sprite in self.traps.sprites():
			if sprite.rect.colliderect(player.rect):
				if player.direction.x < 0 or player.direction.y > 0:
					player.rect.x += tile_size
				elif player.direction.x > 0 or player.direction.y > 0:
					player.rect.x -= tile_size
				player.life -= 1
				self.trap_cooldown = 30
				if self.sound_manager:
					self.sound_manager.play("damage")
				break

	# updating the game world from all changes committed
	def update(self, player_event):
		if self.trap_cooldown > 0:
			self.trap_cooldown -= 1

		self.tiles.update(self.world_shift)
		self.tiles.draw(self.screen)

		self.traps.update(self.world_shift)
		self.traps.draw(self.screen)

		self.goal.update(self.world_shift)
		self.goal.draw(self.screen)

		self._scroll_x()

		self._horizontal_movement_collision()
		self._vertical_movement_collision()
		self._handle_traps()
		self.player.update(player_event)
		self.game.show_hud(self.player.sprite, self.current_level_index, len(self.levels))
		self.player.draw(self.screen)

		self.game.game_state(
			self.player.sprite,
			self.goal.sprite,
			self.current_level_index,
			len(self.levels),
			sound_manager=self.sound_manager
		)