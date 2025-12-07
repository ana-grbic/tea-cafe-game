import sys
import pygame
import math
import time
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
TILE_SIZE = 64
GRID_WIDTH, GRID_HEIGHT = screen.get_size()
GRID_WIDTH = math.floor(GRID_WIDTH / TILE_SIZE) * 2
GRID_HEIGHT = math.floor(GRID_HEIGHT / TILE_SIZE) * 2

def distance_to_object(character, obj):
    char_x, char_y = character.rect.center
    dx = max(obj.rect.x, min(char_x, obj.rect.x + obj.rect.width)) - char_x
    dy = max(obj.rect.y, min(char_y, obj.rect.y + obj.rect.height)) - char_y
    return math.sqrt(dx ** 2 + dy ** 2)

def get_neighbors(current, obstacles):
    x, y = current
    neighbors = []
    possible_neighbors = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
    for neighbor in possible_neighbors:
        if neighbor[0] >= 0 and neighbor[0] < GRID_WIDTH and neighbor[1] >= 0 and neighbor[1] < GRID_HEIGHT:
            if neighbor not in obstacles:
                neighbors.append(neighbor)
    return neighbors

def find_path(start, end, obstacles):
    grid = {(x, y) for x in range(GRID_WIDTH) for y in range(GRID_HEIGHT)}
    open_list = [start]
    closed_list = []

    g_score = {node: float('inf') for node in grid}
    g_score[start] = 0

    parent = {}

    while open_list:
        current = min(open_list, key=lambda node: g_score[node])
        open_list.remove(current)
        
        if current == end:
            path = []
            while current in parent:
                path.insert(0, current)
                current = parent[current]
            return path
        
        closed_list.append(current)
        
        for neighbor in get_neighbors(current, obstacles):
            if neighbor in closed_list:
                continue
            
            tentative_g_score = g_score[current] + 1
            
            if tentative_g_score < g_score[neighbor]:
                parent[neighbor] = current
                g_score[neighbor] = tentative_g_score
                if neighbor not in open_list:
                    open_list.append(neighbor)
    return None

def obstacle_list(walls, chairs, table, destination_chair):
    obstacles = set()

    obstacles.update(walls[4].get_points())
    obstacles.update(walls[5].get_points())

    for chair in chairs:
        if chair != destination_chair:
            obstacles.add((chair.x, chair.y))

    obstacles.add((table.x, table.y))

    return obstacles