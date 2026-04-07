import pygame
import os

try:
    letraX = pygame.image.load(os.path.join('icon',"sol.png"))
    letraO = pygame.image.load(os.path.join('icon',"chuva.png"))
    letraX = pygame.transform.scale(letraX, (100, 100))
    letraO = pygame.transform.scale(letraO, (100, 100))
except:
    print("Erro ao carregar imagens. Verifique a pasta 'icon'.")

class Linha:
    def __init__(self):
        self.grid_lines = [((0,200), (600,200)), 
                            ((0,400), (600,400)), 
                           ((200,0), (200,600)), 
                           ((400,0), (400,600))]
        self.grid = [[None for x in range(3)] for y in range(3)]
        self.game_over = False

    def draw(self, screen):
        for line in self.grid_lines:
            pygame.draw.line(screen, (255,255,255), line[0], line[1], 5)

        for y in range(3):
            for x in range(3):
                if self.grid[y][x] == "x":
                    screen.blit(letraX, (x*200 + 50, y*200 + 50))
                elif self.grid[y][x] == "o":
                    screen.blit(letraO, (x*200 + 50, y*200 + 50))

    def set_cell_value(self, x, y, player):
        if self.grid[y][x] is None and not self.game_over:
            self.grid[y][x] = player
            self.check_win(player)
            return True 
        return False

    def check_win(self, player):

        for i in range(3):
            # Linhas
            if self.grid[i][0] == self.grid[i][1] == self.grid[i][2] == player:
                self.won(player)
            # Colunas
            if self.grid[0][i] == self.grid[1][i] == self.grid[2][i] == player:
                self.won(player)

        # Diagonais
        if self.grid[0][0] == self.grid[1][1] == self.grid[2][2] == player:
            self.won(player)
        if self.grid[0][2] == self.grid[1][1] == self.grid[2][0] == player:
            self.won(player)

    def won(self, player):
        self.game_over = True