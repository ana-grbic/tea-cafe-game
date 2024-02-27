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
            pygame.draw.rect(self.screen, (190, 130, 85), (50, 50, 200, 300))

            font = pygame.font.Font(None, 24)
            y_pos = 70
            for item, count in self.inventory_items.items():
                if count > 0:
                    text = f"{item} x{count}"
                    text_surface = font.render(text, True, (0, 0, 0))
                    self.screen.blit(text_surface, (60, y_pos))
                    y_pos += 30

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
        self.item_rects = {}

    def toggle_visibility(self):
        self.visible = not self.visible

    def add_item(self, item):
        if item in self.inventory:
            self.inventory[item] += 1
        else:
            self.inventory[item] = 1

    def draw(self):
        if self.visible:
            pygame.draw.rect(self.screen, (190, 130, 85), (300, 200, 600, 300))
            
            font = pygame.font.Font(None, 24)
            x_pos = 320
            y_pos = 220
            for item, count in self.inventory.items():
                if count > 0:
                    text = f"{item} x{count}"
                    text_surface = font.render(text, True, (0, 0, 0))
                    item_rect = text_surface.get_rect(topleft=(x_pos, y_pos))
                    self.item_rects[item] = item_rect
                    self.screen.blit(text_surface, (x_pos, y_pos))
                    y_pos += 30

    def handle_click(self, mouse_pos):
        for item, rect in self.item_rects.items():
            if rect.collidepoint(mouse_pos):
                if item == "Leaf":
                    if self.inventory.get("Leaf", 0) > 0:
                        self.inventory["Leaf"] -= 1
                        self.inventory["Tea"] = self.inventory.get("Tea", 0) + 1

class Counter:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen, camera_x, camera_y):
        adjusted_x = self.rect.x - camera_x
        adjusted_y = self.rect.y - camera_y
        pygame.draw.rect(screen, (210, 88, 55), (adjusted_x, adjusted_y, self.rect.width, self.rect.height))