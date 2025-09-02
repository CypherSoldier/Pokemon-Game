# game_animations.py

import pygame
import colorsys

class GameAnimations:
    def __init__(self, game):
        self.game = game

    def level_complete_animation(self, level):
        self.game.window.fill((0, 0, 0))  # Black background
        font = pygame.font.Font(None, 74)
        text = font.render(f"Level {level} Complete!", True, (0, 255, 0))
        text_rect = text.get_rect(center=(self.game.window.get_width() // 2, self.game.window.get_height() // 2 - 50))

        points_font = pygame.font.Font(None, 36)
        points_text = points_font.render(f"Points: {self.game.rocket_points}", True, (255, 255, 255))
        points_rect = points_text.get_rect(center=(self.game.window.get_width() // 2, self.game.window.get_height() // 2 + 20))

        for i in range(60):
            self.game.window.fill((0, 0, 0))
            if i % 10 < 5:
                self.game.window.blit(text, text_rect)
            self.game.window.blit(points_text, points_rect)
            pygame.display.flip()
            pygame.time.wait(50)

    def next_level_animation(self, level):
        self.game.window.fill((0, 0, 50))
        font = pygame.font.Font(None, 74)
        text = font.render(f"Level {level}", True, (255, 255, 0))
        text_rect = text.get_rect(center=(self.game.window.get_width() // 2, self.game.window.get_height() // 2 - 30))

        speed_font = pygame.font.Font(None, 36)
        if level == 2:
            speed_text = speed_font.render("Speed Increased!", True, (255, 100, 100))
        elif level == 3:
            speed_text = speed_font.render("Maximum Speed!", True, (255, 50, 50))
        else:
            speed_text = speed_font.render("Get Ready!", True, (255, 255, 255))
        speed_rect = speed_text.get_rect(center=(self.game.window.get_width() // 2, self.game.window.get_height() // 2 + 30))

        for i in range(40):
            self.game.window.fill((0, 0, 50))
            alpha = min(255, i * 8)
            text.set_alpha(alpha)
            speed_text.set_alpha(alpha)
            self.game.window.blit(text, text_rect)
            self.game.window.blit(speed_text, speed_rect)
            pygame.display.flip()
            pygame.time.wait(50)

    def game_complete_animation(self):
        self.game.window.fill((50, 0, 50))
        font = pygame.font.Font(None, 74)
        text = font.render("GAME COMPLETE!", True, (255, 215, 0))
        text_rect = text.get_rect(center=(self.game.window.get_width() // 2, self.game.window.get_height() // 2 - 50))

        total_font = pygame.font.Font(None, 48)
        total_text = total_font.render(f"Total Points: {self.game.rocket_points}", True, (255, 255, 255))
        total_rect = total_text.get_rect(center=(self.game.window.get_width() // 2, self.game.window.get_height() // 2 + 20))

        for i in range(100):
            self.game.window.fill((50, 0, 50))
            color_shift = (i * 5) % 360
            rgb = colorsys.hsv_to_rgb(color_shift / 360.0, 1.0, 1.0)
            color = tuple(int(c * 255) for c in rgb)

            congratulations_text = font.render("CONGRATULATIONS!", True, color)
            congrats_rect = congratulations_text.get_rect(center=(self.game.window.get_width() // 2, self.game.window.get_height() // 2 - 100))

            self.game.window.blit(congratulations_text, congrats_rect)
            self.game.window.blit(text, text_rect)
            self.game.window.blit(total_text, total_rect)
            pygame.display.flip()
            pygame.time.wait(50)
    '''
    def reset_for_next_level(self):
        self.game.bot.x = 1
        self.game.bot.y = 1

        for i in range(self.game.height):
            for j in range(self.game.width):
                if self.game.maze[i][j] == 5:
                    self.game.maze[i][j] = 0

        self.game.generate_apples()
        self.game.status = ""
    '''