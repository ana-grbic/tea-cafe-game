import sys
import pygame
import math
import time

class Character:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen, camera_x, camera_y):
        adjusted_x = self.rect.x - camera_x
        adjusted_y = self.rect.y - camera_y
        pygame.draw.rect(screen, (110, 135, 130), (adjusted_x, adjusted_y, self.rect.width, self.rect.height))

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

class InventoryScreen:
    def __init__(self, screen, inventory):
        self.screen = screen
        self.visible = False
        self.inventory_items = inventory

    def toggle_visibility(self):
        self.visible = not self.visible

    def add_item(self, item):
        self.inventory_items[item] += 1

    def draw(self):
        if self.visible:
            pygame.draw.rect(self.screen, (245, 190, 170), (50, 50, 200, 300))

            # draw inventory items
            font = pygame.font.Font(None, 24)
            for i, (item, count) in enumerate(self.inventory_items.items()):
                if count > 0:
                    text = f"{item} x{count}"
                    text_surface = font.render(text, True, (210, 88, 55))
                    self.screen.blit(text_surface, (60, 70 + i * 30))

class Wall:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen, camera_x, camera_y):
        adjusted_x = self.rect.x - camera_x
        adjusted_y = self.rect.y - camera_y
        pygame.draw.rect(screen, (205, 105, 65), (adjusted_x, adjusted_y, self.rect.width, self.rect.height))

class Plant:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen, camera_x, camera_y):
        adjusted_x = self.rect.x - camera_x
        adjusted_y = self.rect.y - camera_y
        pygame.draw.rect(screen, (63, 77, 52), (adjusted_x, adjusted_y, self.rect.width, self.rect.height))

class CounterInteractionScreen:
    def __init__(self, screen, inventory):
        self.screen = screen
        self.visible = False
        self.inventory = inventory

    def toggle_visibility(self):
        self.visible = not self.visible

    def add_item(self, item):
        if item in self.inventory:
            self.inventory[item] += 1
        else:
            self.inventory[item] = 1

    def draw(self):
        if self.visible:
            pygame.draw.rect(self.screen, (200, 200, 200), (100, 100, 200, 300))
            
            font = pygame.font.Font(None, 24)
            y_pos = 120
            for item, count in self.inventory.items():
                if count > 0:
                    text = f"{item} x{count}"
                    text_surface = font.render(text, True, (0, 0, 0))
                    self.screen.blit(text_surface, (110, y_pos))
                    y_pos += 30

class Counter:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen, camera_x, camera_y):
        adjusted_x = self.rect.x - camera_x
        adjusted_y = self.rect.y - camera_y
        pygame.draw.rect(screen, (210, 88, 55), (adjusted_x, adjusted_y, self.rect.width, self.rect.height))