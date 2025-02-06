import pygame
import random

class Pokemon:
    def __init__(self):
        pygame.init()
        
        display = pygame.display.set_mode((640, 480))
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

        time_text_render = self.game_font.render(f"Time Remainig: {self.time_text}", True, (0, 0, 255))
        self.window.blit(time_text_render, (150, self.height * self.scale + 10))
        
        pygame.display.flip()

    def new_game(self):
        self.points = 0
        self.ball_count = 0
        self.map = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 3, 1, 0, 0, 0, 0, 1, 0, 4, 0, 0, 0, 1],
                    [1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1],
                    [1, 0, 0, 4, 0, 0, 0, 1, 0, 1, 1, 5, 0, 1],
                    [1, 0, 0, 0, 0, 4, 0, 1, 0, 1, 0, 0, 0, 1],
                    [1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1],
                    [1, 0, 0, 0, 0, 0, 0, 4, 0, 1, 0, 0, 0, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
        
        for _ in range(10):
            x_pos = random.randint(1, 6)
            y_pos = random.randint(1, 12)
            if self.map[x_pos][y_pos] not in [1, 2, 3, 4]:
                self.map[x_pos][y_pos] = 2
    
        self.moves = 0
    
    def find_ash(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.map[y][x] == 3: # Ash is represented by '3'
                    return (y,x)
        return None
    
    def find_rocket(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.map[y][x] == 5:  # Enemy is represented by '4'
                    return (y, x)
        return None
    '''
    def find_cat(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.map[y][x] == 4:  # Enemy is represented by '4'
                    return (y, x)
        return None
    '''
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                self.counter -= 1
                self.time_text = str(self.counter).rjust(3) if self.counter > 0 else 'GAME OVER'
                if self.counter == 0:
                    print("GAME OVER")
                    pygame.quit()
                    exit()
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.move(0, -1)  # Move left
                elif event.key == pygame.K_RIGHT:
                    self.move(0, 1)  # Move right
                elif event.key == pygame.K_UP:
                    self.move(-1, 0)  # Move up
                elif event.key == pygame.K_DOWN:
                    self.move(1, 0)  # Move down
                    
    def move(self, y_offset, x_offset): #
        ash_y_old, ash_x_old = self.find_ash()
        ash_y_new = ash_y_old + y_offset
        ash_x_new = ash_x_old + x_offset

        # Check boundaries and obstacles
        if 0 <= ash_y_new < self.height and 0 <= ash_x_new < self.width:
            if self.map[ash_y_new][ash_x_new] != 1: 
                if self.map[ash_y_new][ash_x_new] == 2:
                    self.points += 1
                if self.map[ash_y_new][ash_x_new] in [4, 5]:
                    print("GAME OVER")
                    pygame.quit()
                    exit()
                # Update map to reflect movement - WHY & HOW
                self.map[ash_y_old][ash_x_old] = 0  # Old position
                self.map[ash_y_new][ash_x_new] = 3  # New position
                
        if self.game_solved():
            print("WELL DONE")
            #return
            pygame.quit()
            exit()
    
    def move_team_rocket(self):
        enemy_y, enemy_x = self.find_rocket()
        
        possible_moves = [(0, 1), (0, -1)]
        
        random_move = random.choice(possible_moves)
        y_offset, x_offset = random_move
        
        enemy_y_new = enemy_y + y_offset
        enemy_x_new = enemy_x + x_offset
        
        if 0 <= enemy_y_new < self.height and 0 <= enemy_x_new < self.width:
            if self.map[enemy_y_new][enemy_x_new] != 1:
                self.map[enemy_y][enemy_x] = 0
                self.map[enemy_y_new][enemy_x_new] = 5
    
    def move_all_cats(self):
        ''' CHANGE THIS FUNCTION TO A LOWER LEVEL'''
        enemy_positions = [(y, x) for y in range(self.height) for x in range(self.width) if self.map[y][x] == 4]
        
        for y, x in enemy_positions:
            possible_moves = []
            
            for dy, dx in [(-1, 0), (1, 0)]:  # Up, Down, Left, Right
                ny, nx = y + dy, x + dx
                if 0 <= ny < self.height and 0 <= nx < self.width and self.map[ny][nx] != 1:
                    possible_moves.append((ny, nx))
                    
                if possible_moves:
                    new_y, new_x = random.choice(possible_moves)
                    self.map[y][x] = 0  # Clear old position
                    self.map[new_y][new_x] = 4  # Update to new position
                    
    def game_solved(self):
        for row in self.map:
            if 2 in row:
                return False
        return True
        
    def main_loop(self):
        clock = pygame.time.Clock()
        while True:
            self.check_events() # Check for events before drawing
            
            if self.moves % 20 == 0:
                self.move_all_cats()
                self.move_team_rocket()
                
            self.draw_window()
            self.moves += 1
            clock.tick(30)

if __name__ == "__main__":
    Pokemon()