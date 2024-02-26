from game_classes import Character, InventoryScreen, Wall, Plant, CounterInteractionScreen, Counter
import sys
import pygame
import math
import time

class MainWindow:
    def __init__(self):
        pygame.init()

        # pygame window
        window_width, window_height = 1200, 700
        self.screen = pygame.display.set_mode((window_width, window_height))
        pygame.display.set_caption("Tea Café")
        self.clock = pygame.time.Clock()

        # initialise texts
        pygame.font.init()
        self.font = pygame.font.Font(None, 30)
        self.show_text = False
        self.text_start_time = 0

        # map dimensions
        self.map_width, self.map_height = 1200, 1400
        self.camera_offset_x, self.camera_offset_y = 0, 0

        # initialise inventory
        shared_inventory = {"Leaf": 0}
        self.inventory_screen = InventoryScreen(self.screen, shared_inventory)

        # initialise counter screen
        self.counter_screen = CounterInteractionScreen(self.screen, shared_inventory)

        self.walls = [
            # x, y, width, height
            # cafe walls
            Wall(100, 500, 300, 40), # top left
            Wall(500, 500, 600, 40), # top right
            Wall(100, 500, 40, 600), # left
            Wall(1060, 500, 40, 600), # right
            Wall(100, 1060, 300, 40), # bottom left
            Wall(500, 1060, 600, 40), # bottom right
            # garden walls
            Wall(100, 100, 1000, 20), # top
            Wall(100, 100, 20, 400), # left
            Wall(1080, 100, 20, 400), # right
        ]
        
        self.plants = [
            Plant(200, 200, 20, 20),
        ]

        self.counter = Counter(140, 650, 200, 40)

        self.character = Character(575, 800, 50, 50)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e and not self.counter_screen.visible:
                        self.inventory_screen.toggle_visibility()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if event.button == 1:  # left mouse button

                        # distance between character and plants
                        for plant in self.plants:
                            plant_center_x = plant.rect.x + plant.rect.width / 2
                            plant_center_y = plant.rect.y + plant.rect.height / 2
                            distance = math.sqrt((self.character.rect.centerx - plant_center_x)**2 +
                                                 (self.character.rect.centery - plant_center_y)**2)

                            if distance <= 50 and plant.rect.collidepoint(mouse_x - self.camera_offset_x, mouse_y - self.camera_offset_y):
                                self.show_text = True
                                self.text_start_time = time.time()
                                self.inventory_screen.add_item("Leaf")

                    elif event.button == 3:  # right mouse button      
                        if self.counter.rect.collidepoint(mouse_x - self.camera_offset_x, mouse_y + self.camera_offset_y) and not self.inventory_screen.visible:
                            self.counter_screen.toggle_visibility()
                        elif self.counter_screen.visible:
                            self.counter_screen.toggle_visibility()
                
            keys = pygame.key.get_pressed()
            dx = (keys[pygame.K_d] - keys[pygame.K_a]) * 4
            dy = (keys[pygame.K_s] - keys[pygame.K_w]) * 4

            new_rect = self.character.rect.move(dx, dy)

            collision = False
            for wall in self.walls:
                if new_rect.colliderect(wall.rect):
                    collision = True
                    break

            for plant in self.plants:
                if new_rect.colliderect(plant.rect):
                    collision = True
                    break

            if new_rect.colliderect(self.counter.rect):
                collision = True

            if not collision:
                self.character.move(dx, dy)

            # update camera position based on character
            window_width, window_height = 1200, 700
            self.camera_offset_x = max(min(self.character.rect.x - window_width // 2, self.map_width - window_width), 0)
            self.camera_offset_y = max(min(self.character.rect.y - window_height // 2, self.map_height - window_height), 0)

            self.screen.fill((198, 192, 156))  # screen colour

            # draw walls
            for wall in self.walls:
                wall.draw(self.screen, self.camera_offset_x, self.camera_offset_y)

            # draw plants
            for plant in self.plants:
                plant.draw(self.screen, self.camera_offset_x, self.camera_offset_y)

            # draw counter            
            self.counter.draw(self.screen, self.camera_offset_x, self.camera_offset_y)

            # draw character
            self.character.draw(self.screen, self.camera_offset_x, self.camera_offset_y)

            # draw inventory
            if not self.counter_screen.visible:
                self.inventory_screen.draw()

            # draw counter screen
            if not self.inventory_screen.visible:
                self.counter_screen.draw()

            if self.show_text:
                text_surface = self.font.render("Leaf in inventory!", True, (63, 77, 52))
                text_rect = text_surface.get_rect(center=(self.character.rect.centerx,
                                                self.character.rect.centery - 50))  # text above the character
                self.screen.blit(text_surface, text_rect)  # text on the screen

            # text hide time
            if time.time() - self.text_start_time > 2:
                self.show_text = False

            # update Pygame display
            pygame.display.flip()

            # cap frame rate at 60 FPS
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    window = MainWindow()
    window.run()