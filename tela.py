import sys
import pygame
from linha import Linha

pygame.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
FPS = 60

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jogo da Velha")
clock = pygame.time.Clock()

lin = Linha()
player = "x"

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Pegamos a posição e convertemos para índice da matriz (0, 1 ou 2)
            pos = pygame.mouse.get_pos()
            x = pos[0] // 200
            y = pos[1] // 200

            # Usamos o método set_cell_value que criamos
            # Ele retorna True se a jogada for válida (espaço vazio)
            if lin.set_cell_value(x, y, player):
                # Só trocamos o jogador se a jogada foi bem sucedida
                if player == "x":
                    player = "o"
                else:
                    player = "x"

    screen.fill((0, 0, 0))

    lin.draw(screen)
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()