import pygame
from support import import_sprite
from settings import GRAVITY, JUMP_SPEED


class Player(pygame.sprite.Sprite):
	def __init__(self, pos, sound_manager=None):
		super().__init__()
		self.sound_manager = sound_manager
		self._import_character_assets()
		self.frame_index = 0
		self.animation_speed = 0.15
		self.image = self.animations["idle"][self.frame_index]
		self.rect = self.image.get_rect(topleft=pos)
		self.mask = pygame.mask.from_surface(self.image)

		# player movement
		self.direction = pygame.math.Vector2(0, 0)
		self.speed = 5
		self.jump_move = JUMP_SPEED

		# player status
		self.life = 5
		self.game_over = False
		self.win = False
		self.status = "idle"
		self.facing_right = True
		self.on_ground = False
		self.on_ceiling = False
		self.on_left = False
		self.on_right = False
		self.jumping = False

	# gets all the images needed for animating specific player actions
	def _import_character_assets(self):
		character_path = "Sprites/player/"
		self.animations = {
			"idle": [],
			"walk": [],
			"jump": [],
			"fall": [],
			"lose": [],
			"win": []
		}
		for animation in self.animations.keys():
			full_path = character_path + animation
			self.animations[animation] = import_sprite(full_path)

	# animates the player actions
	def _animate(self):
		animation = self.animations[self.status]
		if not animation:
			return

		# loop over frame index
		self.frame_index += self.animation_speed
		if self.frame_index >= len(animation):
			self.frame_index = 0
		image = animation[int(self.frame_index)]
		image = pygame.transform.scale(image, (35, 50))
		if self.facing_right:
			self.image = image
		else:
			flipped_image = pygame.transform.flip(image, True, False)
			self.image = flipped_image

		# set the rect
		if self.on_ground and self.on_right:
			self.rect = self.image.get_rect(bottomright=self.rect.bottomright)
		elif self.on_ground and self.on_left:
			self.rect = self.image.get_rect(bottomleft=self.rect.bottomleft)
		elif self.on_ground:
			self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
		elif self.on_ceiling and self.on_right:
			self.rect = self.image.get_rect(topright=self.rect.topright)
		elif self.on_ceiling and self.on_left:
			self.rect = self.image.get_rect(bottomleft=self.rect.topleft)
		elif self.on_ceiling:
			self.rect = self.image.get_rect(midtop=self.rect.midtop)

	# handles movement inputs from the active keys set
	def _get_input(self, keys_pressed):
		if "right" in keys_pressed and "left" not in keys_pressed:
			self.direction.x = 1
			self.facing_right = True
		elif "left" in keys_pressed and "right" not in keys_pressed:
			self.direction.x = -1
			self.facing_right = False
		else:
			self.direction.x = 0

	def _jump(self):
		self.direction.y = self.jump_move
		self.jumping = True
		if self.sound_manager:
			self.sound_manager.play("jump", .35)

	def jump_cut(self):
		if self.jumping and self.direction.y < 0:
			self.direction.y *= 0.45

	# identifies player action
	def _get_status(self):
		if self.direction.y < 0:
			self.status = "jump"
		elif self.direction.y > 1:
			self.status = "fall"
		elif self.direction.x != 0:
			self.status = "walk"
		else:
			self.status = "idle"

	# update the player's state
	def update(self, keys_pressed):
		self._get_status()
		if self.life > 0 and not self.game_over:
			self._get_input(keys_pressed)
		elif self.game_over and self.win:
			self.direction.x = 0
			self.status = "win"
		else:
			self.direction.x = 0
			self.status = "lose"
		self._animate()