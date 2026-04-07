import sys
import pygame
import threading
import socket
from linha import Linha

pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Jogo da Velha - CLIENTE (Sol)")
clock = pygame.time.Clock()

background = pygame.transform.scale(pygame.image.load("icon/ceu.jpg"), (600, 600))

HOST = '127.0.0.1'
PORT = 65432
meia = None
connection_status = False
lin = Linha()
player = "x"
turno = True  # O Cliente (X) começa

def thread_receber():
    global turno, connection_status
    while True:
        try:
            data = meia.recv(1024).decode()
            if data:
                parts = data.split('-')
                x, y, symbol = int(parts[0]), int(parts[1]), parts[2]
                lin.set_cell_value(x, y, symbol)
                turno = True
                print(f"Recebido: {x}, {y}")
        except:
            connection_status = False
            break

def conectar():
    global meia, connection_status
    meia = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        meia.connect((HOST, PORT))
        connection_status = True
        print("Conectado ao Servidor!")
        threading.Thread(target=thread_receber, daemon=True).start()
    except:
        print("Erro ao conectar.")

threading.Thread(target=conectar, daemon=True).start()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN and connection_status and turno:
            pos = pygame.mouse.get_pos()
            cX, cY = pos[0] // 200, pos[1] // 200
            if lin.set_cell_value(cX, cY, player):
                meia.send(f"{cX}-{cY}-{player}".encode())
                turno = False

    screen.blit(background, (0, 0))
    lin.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()