import pygame
import heapq
import random

class Node:
    def __init__(self, x, y, parent=None):
        self.x = x
        self.y = y
        self.parent = parent
        self.g = 0  # Cost from start node
        self.h = 0  # Heuristic cost to apple
        self.f = 0  # Total cost (g + h)

    def __lt__(self, other):
        return self.f < other.f  # Allows priority queue sorting

def astar(grid, start, goal):
    open_list = []
    closed_set = set()
    start_node = Node(*start)
    
    heapq.heappush(open_list, (0, start_node))
    print(f"Starting A* from {start} to {goal}")
    while open_list:
        _, current = heapq.heappop(open_list)

        if (current.x, current.y) == goal:
            return reconstruct_path(current)

        closed_set.add((current.x, current.y))

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Up, Down, Left, Right
            nx, ny = current.x + dx, current.y + dy
            
            if not is_valid(nx, ny, grid) or (nx, ny) in closed_set:
                continue
            
            neighbor = Node(nx, ny, current)
            neighbor.g = current.g + 1
            neighbor.h = abs(nx - goal[0]) + abs(ny - goal[1])  # Manhattan Distance
            neighbor.f = neighbor.g + neighbor.h

            heapq.heappush(open_list, (neighbor.f, neighbor))
    print(f"No path found from {start} to {goal}")
    return None  # No path found

def reconstruct_path(node):
    path = []
    while node:
        path.append((node.x, node.y))
        node = node.parent
    return path[::-1]  # Reverse to get correct order

def is_valid(x, y, grid):
    return 0 <= x < len(grid) and 0 <= y < len(grid[0]) and grid[x][y] != 1  # Not a wall

class Bot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.path = []

    def find_nearest_apple(self, apples):
        if not apples:
            return None
        target = min(apples, key=lambda apple: abs(self.x - apple[0]) + abs(self.y - apple[1]))   # Manhattan distance
        print(f"Nearest apple chosen: {target}")
        return target

    def move(self, grid, apples):
        if not self.path:
            target = self.find_nearest_apple(apples)
            if target:
                self.path = astar(grid, (self.x, self.y), target)

        if self.path:
            next_step = self.path.pop(0)
            self.x, self.y = next_step

class Pokemon:
    def __init__(self):
        pygame.init()
        
        display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.load_images()
        self.new_game()
        
        self.height = len(self.map)
        self.width = len(self.map[0])
        self.scale = self.images[0].get_width()

        window_height = self.scale * self.height
        window_width = self.scale * self.width
        self.window = pygame.display.set_mode((window_width, window_height + self.scale))
        self.game_font = pygame.font.SysFont("Arial", 24)
        
        self.game_font = pygame.font.SysFont("Arial", 24)
        pygame.display.set_caption("Catch that Pokemon!")

        self.counter = 60
        self.time_text = str(self.counter).rjust(3)
        pygame.time.set_timer(pygame.USEREVENT, 1000)
        
        self.status = ""
 
        self.main_loop()
        
    def load_images(self):
        self.images = []
        
        for name in ["floor", "green_wall", "pokeball", "ash", "cat", "rocket"]:
            original_image = pygame.image.load(name + ".png")
            new_size = (70, 70)
            scaled_image = pygame.transform.scale(original_image, new_size)
            self.images.append(scaled_image)

    def draw_window(self):
        self.window.fill((255, 255, 255))

        for y in range(self.height): #
            for x in range(self.width):
                square = self.map[y][x]
                self.window.blit(self.images[square], (x * self.scale, y * self.scale))
        
        points_text = self.game_font.render(f"Points: {self.points}", True, (255, 0, 0))
        self.window.blit(points_text, (10, self.height * self.scale + 10))
        
        rocket_text = self.game_font.render(f"Points: {self.rocket_points}", True, (255, 0, 0))
        self.window.blit(rocket_text, (650, self.height * self.scale + 10))

        time_text_render = self.game_font.render(f"Time Remainig: {self.time_text}", True, (0, 0, 255))
        self.window.blit(time_text_render, (150, self.height * self.scale + 10))
        
        time_text_render = self.game_font.render(f"Status: {self.status}", True, (0, 0, 255))
        self.window.blit(time_text_render, (450, self.height * self.scale + 10))
        
        pygame.display.flip()

    def new_game(self):
        self.points = 0
        self.rocket_points = 0
        self.map = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 3, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
                    [1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1],
                    [1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1],
                    [1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1],
                    [1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1],
                    [1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
        
        self.bot = Bot(3, 11)
        self.apples = []
        for _ in range(30):
            x_pos = random.randint(1, 6)
            y_pos = random.randint(1, 12)
            if self.map[x_pos][y_pos] not in [1, 2, 3, 4]:
                self.map[x_pos][y_pos] = 2
                self.apples.append([x_pos, y_pos])
        print(self.apples)
    
        self.moves = 0
    
    def find_ash(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.map[y][x] == 3:
                    return (y, x)
                
        return None

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                self.counter -= 1
                self.time_text = str(self.counter).rjust(3) #if self.counter > 0 else 'GAME OVER'
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.move(0, -1)
                elif event.key == pygame.K_RIGHT:
                    self.move(0, 1)
                elif event.key == pygame.K_UP:
                    self.move(-1, 0)  # Move up
                elif event.key == pygame.K_DOWN:
                    self.move(1, 0)  # Move down
                    
    def move(self, y_offset, x_offset): #
        try:
            ash_y_old, ash_x_old = self.find_ash()
            ash_y_new = ash_y_old + y_offset
            ash_x_new = ash_x_old + x_offset
            
            if 0 <= ash_y_new < self.height and 0 <= ash_x_new < self.width:
                if self.map[ash_y_new][ash_x_new] != 1:
                    if self.map[ash_y_new][ash_x_new] == 2:
                        self.points += 1
                    
                    self.map[ash_y_old][ash_x_old] = 0
                    self.map[ash_y_new][ash_x_new] = 3 
        except TypeError:
            self.status = "YOU LOSE"
            print("GAME OVER")
    
    def win_criteria(self):
        self.apple_count = 0
        for row in range(self.height):
            for col in range(self.width):
                if self.map[row][col] == 2:
                    self.apple_count += 1
        
        if self.apple_count == 0:
            if self.points > self.rocket_points:
                self.status = "YOU WIN"
            elif self.points == self.rocket_points:
                self.status = "DRAW"
            elif self.counter == 0:
                self.status = "YOU LOSE"
            else:
                self.status = "YOU LOSE"
        
    def main_loop(self):
        clock = pygame.time.Clock()
        while True:
            self.check_events() # Check for events before drawing
            
            old_x, old_y = self.bot.x, self.bot.y
            
            # Move the bot
            self.bot.move(self.map, list(map(tuple, self.apples))) # Convert to tuples for find_nearest_apple
            
            new_x, new_y = self.bot.x, self.bot.y
            
            # Clear old position
            if 0 <= old_x < self.height and 0 <= old_y < self.width and self.map[old_x][old_y] == 5:
                self.map[old_x][old_y] = 0
                
            # Update new position
            if 0 <= new_x < self.height and 0 <= new_y < self.width:
                if self.map[new_x][new_y] == 2:  # If bot landed on apple
                    self.rocket_points += 1
                    for i, apple in enumerate(self.apples):
                        if tuple(apple) == (new_x, new_y):
                            self.apples.pop(i)
                            break
                self.map[new_x][new_y] = 5
          
            self.draw_window()
            self.moves += 1
            clock.tick(5)
            self.win_criteria()

if __name__ == "__main__":
    Pokemon()
