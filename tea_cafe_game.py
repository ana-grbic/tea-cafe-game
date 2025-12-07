from game_classes import *
from game_functions import *
import sys
import pygame
import math
import time
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
GRID_WIDTH, GRID_HEIGHT = screen.get_size()
GRID_WIDTH = math.floor(GRID_WIDTH / TILE_SIZE)
GRID_HEIGHT = math.floor(GRID_HEIGHT / TILE_SIZE) * 2
SCREEN_WIDTH = GRID_WIDTH * TILE_SIZE
SCREEN_HEIGHT = GRID_HEIGHT * TILE_SIZE / 2
TILE_SIZE = 64

class MainWindow:
    def __init__(self):
        pygame.init()

        # pygame window
        pygame.display.set_caption("Tea Café")
        self.clock = pygame.time.Clock()

        # initialise texts
        pygame.font.init()
        self.font = pygame.font.Font(None, 30)
        self.show_text = False
        self.text_start_time = 0

        # map dimensions
        self.camera_offset_x, self.camera_offset_y = 0, 0

        # initialise inventory
        shared_inventory = {"Leaf": 0, "Tea": 0}
        self.inventory_screen = InventoryScreen(screen, shared_inventory)

        # initialise counter screen
        self.counter_screen = CounterInteractionScreen(screen, shared_inventory)

        # initialise coin
        self.coin = Coin(screen)

        # initialise shop
        self.shop = Shop(screen)

        self.walls = [
            # x, y, width, height
            # cafe walls
            Wall(2, 10, 6, 1), # top left
            Wall(10, 10, 12, 1), # top right
            Wall(2, 10, 1, 12), # left
            Wall(21, 10, 1, 12), # right
            Wall(2, 21, 6, 1), # bottom left
            Wall(10, 21, 12, 1), # bottom right
            # garden walls
            Wall(2, 2, 20, 1), # top
            Wall(2, 2, 1, 8), # left
            Wall(21, 2, 1, 8), # right
        ]

        self.chairs = [
            Chair(16, 15), # top
            Chair(15, 16), # left
            Chair(17, 16), # right
            Chair(16, 17), # bottom
        ]

        initial_customer = Customer(9, 27, screen)
        self.customers = []
        self.customers.append(initial_customer)
        self.spawn_interval = random.randint(1200, 7200)
        self.spawn_timer = 0

        self.table = Table(16, 16)
        
        self.plants = Plant(4, 4)

        self.counter = Counter(3, 13, 4, 1)

        self.character = Character(10 * TILE_SIZE, 12 * TILE_SIZE, TILE_SIZE, TILE_SIZE)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        running = False
                    case pygame.KEYDOWN:
                        if event.key == pygame.K_e and not self.counter_screen.visible:
                            self.inventory_screen.toggle_visibility()
                        elif event.key == pygame.K_ESCAPE:
                            running = False
                    case pygame.MOUSEBUTTONDOWN:
                        mouse_x, mouse_y = pygame.mouse.get_pos()

                        match event.button:
                            case 1: # left mouse button
                                if distance_to_object(self.character, self.plants) <= TILE_SIZE * 2 and self.plants.rect.collidepoint(mouse_x - self.camera_offset_x, mouse_y - self.camera_offset_y):
                                    self.show_text = True
                                    self.text_start_time = time.time()
                                    self.inventory_screen.add_item("Leaf")
                                elif self.counter_screen.visible:
                                    self.counter_screen.handle_click(pygame.mouse.get_pos())
                                elif self.inventory_screen.visible:
                                    self.inventory_screen.hold_item(pygame.mouse.get_pos())
                            case 3: # right mouse button
                                if self.counter_screen.visible:
                                    self.counter_screen.toggle_visibility()
                                elif any(customer.text_box_open for customer in self.customers):
                                    for customer in self.customers:
                                        customer.text_box_open = False
                                elif distance_to_object(self.character, self.counter) <= TILE_SIZE * 2 and self.counter.rect.collidepoint(mouse_x - self.camera_offset_x, mouse_y + self.camera_offset_y) and not self.inventory_screen.visible:
                                    self.counter_screen.toggle_visibility()
                                elif self.shop.icon_rect.collidepoint(mouse_x, mouse_y):
                                    if self.shop.open:
                                        self.shop.open = False
                                    else:
                                        self.shop.open = True
                                for customer in self.customers:
                                    if distance_to_object(self.character, customer) <= TILE_SIZE * 3 and customer.rect.collidepoint(mouse_x - self.camera_offset_x, mouse_y + self.camera_offset_y) and customer.sitting and not customer.received:
                                        if self.inventory_screen.item_held is not None:
                                            customer.receive_item(self.inventory_screen.item_held, self.coin)
                                            self.inventory_screen.item_held = None
                                            customer.text_box_open = True
                                        customer.text_box_open = True

            if not self.counter_screen.visible and not any(customer.text_box_open for customer in self.customers):
                keys = pygame.key.get_pressed()
                dx = (keys[pygame.K_d] - keys[pygame.K_a]) * 4
                dy = (keys[pygame.K_s] - keys[pygame.K_w]) * 4

            new_rect = self.character.rect.move(dx, dy)

            collision = False
            for wall in self.walls:
                if new_rect.colliderect(wall.rect):
                    collision = True
                    break

            for chair in self.chairs:
                if new_rect.colliderect(chair.rect):
                    collision = True
                    break

            if new_rect.colliderect(self.plants.rect):
                collision = True

            if new_rect.colliderect(self.counter.rect):
                collision = True

            if new_rect.colliderect(self.table.rect):
                collision = True

            for customer in self.customers:
                if new_rect.colliderect(customer.rect) and customer.sitting:
                    collision = True

            if not collision:
                self.character.move(dx, dy)

            # update camera position based on character
            self.camera_offset_x = max(min(self.character.rect.x - SCREEN_WIDTH // 2, GRID_WIDTH * TILE_SIZE - SCREEN_WIDTH), 0)
            self.camera_offset_y = max(min(self.character.rect.y - SCREEN_HEIGHT // 2, GRID_HEIGHT * TILE_SIZE - SCREEN_HEIGHT), 0)

            screen.fill((198, 192, 156))

            # draw walls
            for wall in self.walls:
                wall.draw(screen, self.camera_offset_x, self.camera_offset_y)

            # draw chairs
            for chair in self.chairs:
                chair.draw(screen, self.camera_offset_x, self.camera_offset_y)

            # draw plants
            self.plants.draw(screen, self.camera_offset_x, self.camera_offset_y)

            # draw counter            
            self.counter.draw(screen, self.camera_offset_x, self.camera_offset_y)

            # draw table
            self.table.draw(screen, self.camera_offset_x, self.camera_offset_y)

            # draw character
            self.character.draw(screen, self.camera_offset_x, self.camera_offset_y)

            # spawn customer
            self.spawn_timer += 1
            if self.spawn_timer >= self.spawn_interval and any(chair.available for chair in self.chairs):
                new_customer = Customer(9, 27, screen)
                self.customers.append(new_customer)
                self.spawn_timer = 0

            # draw customer
            for customer in self.customers:
                customer.draw(screen, self.camera_offset_x, self.camera_offset_y)
                if customer.chair_chosen == None:
                    customer.chair_chosen = customer.find_available_chair(self.chairs)
                    chair_x, chair_y = self.chairs[customer.chair_chosen].x, self.chairs[customer.chair_chosen].y
                    self.obstacles = obstacle_list(self.walls, self.chairs, self.table, self.chairs[customer.chair_chosen])
                    customer.path = find_path(customer.spawn_point, (chair_x, chair_y), self.obstacles)
                else:
                    customer.update()
                    if not customer.path and not customer.received:
                        customer.sitting = True
                        customer.wants_to_receive = True

            for customer in self.customers:
                if customer.text_box_open:
                    customer.draw_text_box(screen)
                if customer.leave_timer == 0 and not customer.path:
                    chair_x, chair_y = self.chairs[customer.chair_chosen].x, self.chairs[customer.chair_chosen].y
                    self.obstacles = obstacle_list(self.walls, self.chairs, self.table, self.chairs[customer.chair_chosen])
                    customer.path = find_path((chair_x, chair_y), customer.spawn_point, self.obstacles)
                    self.sitting = False
                if customer.leave_timer == 0 and customer.rect.x == customer.spawn_point[0] * TILE_SIZE and customer.rect.y == customer.spawn_point[1] * TILE_SIZE:
                    self.chairs[customer.chair_chosen].available = True
                    customer.left = True
                elif customer.leave_timer != 0 and customer.received:
                    customer.leave_timer -= 1
                
            self.customers = [customer for customer in self.customers if not customer.left]

            # draw inventory
            if not self.counter_screen.visible:
                self.inventory_screen.draw()

            # draw counter screen
            if not self.inventory_screen.visible:
                self.counter_screen.draw()

            # draw coin
            self.coin.draw(GRID_WIDTH)

            # draw shop
            self.shop.draw()

            if self.show_text:
                text_surface = self.font.render("Leaf in inventory!", True, (63, 77, 52))
                text_rect = text_surface.get_rect(center=(self.character.rect.centerx,
                                                self.character.rect.centery - TILE_SIZE))  # text above the character
                screen.blit(text_surface, text_rect)  # text on the screen

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