import os
import pygame


class SoundManager:
	def __init__(self, folder="Sound Effects"):
		self.folder = folder
		self.enabled = False
		self.sounds = {}
		self.music_path = None

		if not pygame.mixer.get_init():
			try:
				pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=256)
			except pygame.error as err:
				print(f"[SoundManager] Mixer init failed: {err}")
				return

		pygame.mixer.set_num_channels(16)
		self.enabled = True

		self.sounds = {
			"jump": self._load_sound("jump", [
				"maro-jump-sound-effect_1.wav",
				"mario-jump-sound-effect_1.wav",
				"jump.wav",
			]),
			"savepoint": self._load_sound("savepoint", [
				"savepoint.wav",
			]),
			"gameover": self._load_sound("gameover", [
				"game-over-frickbears-3.wav",
				"gameover.wav",
			]),
			"damage": self._load_sound("damage", [
				"deltarune-character-dies-meme.wav",
				"deltarune_dies.wav",
			]),
		}

		self.music_path = self._find_file([
			"Arcade Theme - Five Nights at Freddys_ Into the Pit (Soundtrack).wav",
			"arcade_theme.wav",
		])
		if not self.music_path:
			print(f"[SoundManager] Music file not found in '{self.folder}'")

	def _find_file(self, candidates):
		for name in candidates:
			path = os.path.join(self.folder, name)
			if os.path.isfile(path):
				return path
		return None

	def _load_sound(self, key, candidates):
		path = self._find_file(candidates)
		if not path:
			print(f"[SoundManager] Missing sound '{key}' in '{self.folder}'. Tried: {candidates}")
			return None
		try:
			snd = pygame.mixer.Sound(path)
			print(f"[SoundManager] Loaded '{key}' -> {path}")
			return snd
		except pygame.error as err:
			print(f"[SoundManager] Failed to load '{key}' ({path}): {err}")
			return None

	def play_music(self, loops=-1, volume=0.35, force_restart=False):
		if not self.enabled or not self.music_path:
			return
		try:
			if not force_restart and pygame.mixer.music.get_busy():
				pygame.mixer.music.set_volume(volume)
				return
			pygame.mixer.music.stop()
			pygame.mixer.music.load(self.music_path)
			pygame.mixer.music.set_volume(volume)
			pygame.mixer.music.play(loops)
			print(f"[SoundManager] Playing music -> {self.music_path}")
		except pygame.error as err:
			print(f"[SoundManager] Music play failed: {err}")

	def stop_music(self):
		if not self.enabled:
			return
		try:
			pygame.mixer.music.stop()
		except pygame.error:
			pass

	def play(self, key, volume=0.75):
		if not self.enabled:
			return
		snd = self.sounds.get(key)
		if snd:
			snd.set_volume(volume)
			snd.play()