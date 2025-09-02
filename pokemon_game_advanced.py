import pygame
import random
from pokemon_a_star import Bot
from game_animations import GameAnimations

class Pokemon:
    def __init__(self):
        pygame.init()
        
        display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.load_images()
        self.new_game()
        
        self.height = len(self.maze)
        self.width = len(self.maze[0])
        self.scale = self.images[0].get_width()

        window_height = self.scale * self.height
        window_width = self.scale * self.width
        self.window = pygame.display.set_mode((window_width, window_height + self.scale))
        self.animations = GameAnimations(self)
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
                square = self.maze[y][x]
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
    
    def generate_map(self, x, y):
        self.visited[y][x] = True
        self.maze[2*y+1][2*x+1] = 0  # Mark current cell as floor
        
        directions = ([(0, -1), (1, 0), (0, 1), (-1, 0)])  # N, E, S, W
        random.shuffle(directions)
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height and not self.visited[ny][nx]:
                # Remove wall between (x,y) and (nx,ny)
                self.maze[y + ny + 1][x + nx + 1] = 0
                self.generate_map(nx, ny)
        
    def new_game(self):
        self.points = 0
        self.rocket_points = 0
        self.width = 6
        self.height = 4
        
        self.maze_display_width = self.width * 2 + 1
        self.maze_display_height = self.height * 2 + 1
        self.maze = [[1 for _ in range(self.maze_display_width)] for _ in range(self.maze_display_height)]
        # Mark visited cells
        self.visited = [[False for _ in range(self.width)] for _ in range(self.height)]
        self.generate_map(1,1)
        
        self.maze[1][1] = 3
        
        self.bot = Bot(3, 11)
        self.apples = []
        for _ in range(30):
            x_pos = random.randint(1, 6)
            y_pos = random.randint(1, 12)
            if self.maze[x_pos][y_pos] not in [1, 2, 3, 4]:
                self.maze[x_pos][y_pos] = 2
                self.apples.append([x_pos, y_pos])
        print(self.apples)
    
        self.moves = 0
    
    def find_ash(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.maze[y][x] == 3:
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
                if self.maze[ash_y_new][ash_x_new] != 1:
                    if self.maze[ash_y_new][ash_x_new] == 2:
                        self.points += 1
                    
                    self.maze[ash_y_old][ash_x_old] = 0
                    self.maze[ash_y_new][ash_x_new] = 3 
        except TypeError:
            self.status = "YOU LOSE"
            print("GAME OVER")
    
    def win_criteria(self):
        self.apple_count = 0
        for row in range(self.height):
            for col in range(self.width):
                if self.maze[row][col] == 2:
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
        current_level = 1
        max_level = 3
        clock = pygame.time.Clock()
        while True:
            if current_level == 1:
                game_speed = 2
            elif current_level == 2:
                game_speed = 4
            elif current_level == 3:
                game_speed = 6
            else:
                game_speed = 6
            
            self.check_events() # Check for events before drawing
            
            old_x, old_y = self.bot.x, self.bot.y
            
            # Move the bot
            self.bot.move(self.maze, list(map(tuple, self.apples))) # Convert to tuples for find_nearest_apple
            
            new_x, new_y = self.bot.x, self.bot.y
            
            # Clear old position
            if 0 <= old_x < self.height and 0 <= old_y < self.width and self.maze[old_x][old_y] == 5:
                self.maze[old_x][old_y] = 0
                
            # Update new position
            if 0 <= new_x < self.height and 0 <= new_y < self.width:
                if self.maze[new_x][new_y] == 2:  # If bot landed on apple
                    self.rocket_points += 1
                    for i, apple in enumerate(self.apples):
                        if tuple(apple) == (new_x, new_y):
                            self.apples.pop(i)
                            break
                self.maze[new_x][new_y] = 5
          
            self.draw_window()
            self.moves += 1
            clock.tick(game_speed)
            self.win_criteria()
            
            if self.status == "YOU WIN" and current_level == 1:
                if current_level < max_level:
                    self.animations.level_complete_animation(current_level)
                    current_level += 1
                    #self.animations.reset_for_next_level()
                    self.animations.next_level_animation(current_level)
                else:
                    self.animations.game_complete_animation()
                    break

if __name__ == "__main__":
    Pokemon()