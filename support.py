from os import walk
import os
import pygame

def import_sprite(path):
    surface_list = []
    for root, _, img_files in walk(path):
        for image in sorted(img_files):
            if image.endswith(('.png', '.jpg', '.jpeg', '.gif')):
                full_path = os.path.join(root, image)
                img_surface = pygame.image.load(full_path).convert_alpha()
                surface_list.append(img_surface)
    return surface_list