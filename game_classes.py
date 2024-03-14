import sys
import pygame
import math
import time
import random
import json
TILE_SIZE = 50

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

class Customer:
    def __init__(self, x, y, screen):
        self.rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        self.x = x
        self.y = y
        self.screen = screen
        self.spawn_point = (9, 27)
        self.colour = None
        self.chair_chosen = None
        self.sitting = False
        self.text_box_open = False
        self.path = []
        self.counter = 49
        self.leave_timer = random.randint(1200, 3600)
        self.left = False
        with open('game_text.json') as f:
            self.texts = json.load(f)
        self.current_text = None
        self.wants_to_receive = False
        self.item_wanted = "Tea"

    def update(self, path):
        if self.counter == 0:
            next_node = path.pop(0)
        else:
            next_node = path[0]
        next_x, next_y = next_node
        if next_x * 50 > self.rect.x:
            self.rect.x = next_x * 50 - self.counter
        elif next_x * 50 < self.rect.x:
            self.rect.x = next_x * 50 + self.counter
        elif next_y * 50 > self.rect.y:
            self.rect.y = next_y * 50 - self.counter
        elif next_y * 50 < self.rect.y:
            self.rect.y = next_y * 50 + self.counter

    def receive_item(self, item, coins):
        if item == self.item_wanted:
            self.current_text = random.choice(self.texts.get("correct", []))
            coins.amount = coins.amount + 3
        else:
            self.current_text = random.choice(self.texts.get("incorrect", []))
        self.wants_to_receive = False
        print("doesnt wanna receive")

    def find_available_chair(self, chairs):
        available_chairs_indices = [i for i, chair in enumerate(chairs) if chair.available]
        if available_chairs_indices:
            random_chair = random.choice(available_chairs_indices)
            chairs[random_chair].available = False
            return random_chair
        else:
            return None

    def draw(self, screen, camera_x, camera_y):
        if self.colour == None:
            self.colour = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        adjusted_x = self.rect.x - camera_x
        adjusted_y = self.rect.y - camera_y
        pygame.draw.rect(screen, self.colour, (adjusted_x, adjusted_y, TILE_SIZE, TILE_SIZE))

    def draw_text_box(self, screen):
        pygame.draw.rect(self.screen, (190, 130, 85), (200, 500, 600, 150))
        pygame.draw.rect(self.screen, self.colour, (800, 400, 200, 250))

        if self.current_text == None:
            self.current_text = random.choice(self.texts.get("general tea requests", []))
            
        font = pygame.font.Font(None, 24)
        text_surface = font.render(self.current_text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(500, 575))
        screen.blit(text_surface, text_rect)
        
class InventoryScreen:
    def __init__(self, screen, inventory):
        self.screen = screen
        self.visible = False
        self.inventory_items = inventory
        self.item_rects = {}
        self.item_held = None

    def toggle_visibility(self):
        self.visible = not self.visible

    def add_item(self, item):
        self.inventory_items[item] += 1

    def draw(self):
        if self.visible:
            self.inventory_screen_rect = pygame.draw.rect(self.screen, (190, 130, 85), (50, 50, 200, 300))

            font = pygame.font.Font(None, 24)
            x_pos = 60
            y_pos = 70
            for item, count in self.inventory_items.items():
                if count > 0:
                    text = f"{item} x{count}"
                    text_surface = font.render(text, True, (0, 0, 0))
                    item_rect = text_surface.get_rect(topleft=(x_pos, y_pos))
                    self.item_rects[item] = item_rect
                    self.screen.blit(text_surface, (x_pos, y_pos))
                    y_pos += 30

        if self.item_held:
            mouse_pos = pygame.mouse.get_pos()
            item_rect = pygame.Rect(mouse_pos[0], mouse_pos[1], 20, 20)
            pygame.draw.rect(self.screen, (220, 105, 85), item_rect)

    def hold_item(self, mouse_pos):
        if self.item_held is not None and self.inventory_screen_rect.collidepoint(mouse_pos):
            self.inventory_items[self.item_held] += 1
            self.item_held = None
            return

        for item, rect in self.item_rects.items():
            if rect.collidepoint(mouse_pos):
                if self.inventory_items[item] > 0 and self.item_held == None:
                    self.inventory_items[item] -= 1
                    self.item_held = item

class Wall:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, width * TILE_SIZE, height * TILE_SIZE)
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, screen, camera_x, camera_y):
        adjusted_x = self.x * TILE_SIZE - camera_x
        adjusted_y = self.y * TILE_SIZE - camera_y
        pygame.draw.rect(screen, (205, 105, 65), (adjusted_x, adjusted_y, self.width * TILE_SIZE, self.height * TILE_SIZE))

    def get_points(self):
        points = set()

        for i in range(self.x, self.x + self.width):
            for j in range(self.y, self.y + self.height):
                points.add((i, j))

        return points

class Plant:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x * TILE_SIZE + TILE_SIZE/4, y * TILE_SIZE + TILE_SIZE/4, TILE_SIZE/2, TILE_SIZE/2)
        self.x = x
        self.y = y

    def draw(self, screen, camera_x, camera_y):
        adjusted_x = self.x * TILE_SIZE + TILE_SIZE/4 - camera_x
        adjusted_y = self.y * TILE_SIZE + TILE_SIZE/4 - camera_y
        pygame.draw.rect(screen, (63, 77, 52), (adjusted_x, adjusted_y, TILE_SIZE/2, TILE_SIZE/2))

class Table:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        self.x = x
        self.y = y

    def draw(self, screen, camera_x, camera_y):
        adjusted_x = self.x * TILE_SIZE - TILE_SIZE/5 - camera_x
        adjusted_y = self.y * TILE_SIZE - TILE_SIZE/5 - camera_y
        pygame.draw.rect(screen, (105, 80, 65), (adjusted_x, adjusted_y, TILE_SIZE * 7/5, TILE_SIZE * 7/5))

class Chair:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x * TILE_SIZE + TILE_SIZE/10, y * TILE_SIZE + TILE_SIZE/10, TILE_SIZE * 4/5, TILE_SIZE * 4/5)
        self.x = x
        self.y = y
        self.available = True

    def draw(self, screen, camera_x, camera_y):
        adjusted_x = self.x * TILE_SIZE + TILE_SIZE/10 - camera_x
        adjusted_y = self.y * TILE_SIZE + TILE_SIZE/10 - camera_y
        pygame.draw.rect(screen, (105, 90, 65), (adjusted_x, adjusted_y, TILE_SIZE * 4/5, TILE_SIZE * 4/5))

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
        self.rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, width * TILE_SIZE, height * TILE_SIZE)
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, screen, camera_x, camera_y):
        adjusted_x = self.x * TILE_SIZE - camera_x
        adjusted_y = self.y * TILE_SIZE - camera_y
        pygame.draw.rect(screen, (210, 88, 55), (adjusted_x, adjusted_y, self.width * TILE_SIZE, self.height * TILE_SIZE))

class Coin:
    def __init__(self, screen):
        self.screen = screen
        self.amount = 0

    def draw(self):
        self.inventory_screen_rect = pygame.draw.rect(self.screen, (250, 190, 75), (1125, 25, 40, 40))

        font = pygame.font.Font(None, 50)
        text_surface = font.render(str(self.amount), True, (0, 0, 0))
        self.screen.blit(text_surface, (1090, 30))