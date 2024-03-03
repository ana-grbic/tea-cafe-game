import sys
import pygame
import math
import time
GRID_WIDTH = 120
GRID_HEIGHT = 140

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
            extended_neighbor = get_extended_neighbors(neighbor)
            if not any(n in obstacles for n in extended_neighbor):
                neighbors.append(neighbor)
    return neighbors

def get_extended_neighbors(current):
    x, y = current
    extended_neighbors = set()

    extended_neighbors.add(current)

    for i in range(int(x), int(x) + 5): # adjust number depending on how close you want the neighbor to obstacles
        for j in range(int(y), int(y) + 5):
            extended_neighbors.add((i, j))

    return extended_neighbors

def find_path(start, end, obstacles):
    print("path")
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

    def convert_to_grid_points(x, y, width, height):
        grid_points = set()
        for i in range(x // 10, (x + width) // 10 + 1):
            for j in range(y // 10, (y + height) // 10 + 1):
                grid_points.add((i, j))
        return grid_points

    obstacles.update(convert_to_grid_points(walls[4].rect.x, walls[4].rect.y, walls[4].rect.width, walls[4].rect.height))
    obstacles.update(convert_to_grid_points(walls[5].rect.x, walls[5].rect.y, walls[5].rect.width, walls[5].rect.height))

    for chair in chairs:
        if chair != destination_chair:
            obstacles.update(convert_to_grid_points(chair.rect.x, chair.rect.y, chair.rect.width, chair.rect.height))

    obstacles.update(convert_to_grid_points(table.rect.x, table.rect.y, table.rect.width, table.rect.height))

    #print(obstacles)
    return obstacles
