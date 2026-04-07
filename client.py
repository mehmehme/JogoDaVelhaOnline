import sys
import pygame
import threading
import socket
from linha import Linha

pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Jogo da Velha - SERVIDOR (Chuva)")
clock = pygame.time.Clock()

background = pygame.transform.scale(pygame.image.load("icon/nublado.jpg"), (600, 600))

HOST = '127.0.0.1'
PORT = 65432
conn = None
connection_status = False
lin = Linha()
player = "o"
turno = False  # Começa esperando o X

def thread_receber():
    global turno, connection_status
    while True:
        try:
            data = conn.recv(1024).decode()
            if data:
                parts = data.split('-')
                x, y, symbol = int(parts[0]), int(parts[1]), parts[2]
                # Sincroniza com a lógica da classe Linha
                lin.set_cell_value(x, y, symbol)
                turno = True  # Recebeu a jogada, agora é a vez dele
                print(f"Recebido: {x}, {y}")
        except:
            connection_status = False
            break

def iniciar_conexao():
    global conn, connection_status
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(1)
    print("Aguardando conexão do Cliente...")
    conn, addr = server.accept()
    connection_status = True
    print("Conectado!")
    threading.Thread(target=thread_receber, daemon=True).start()

threading.Thread(target=iniciar_conexao, daemon=True).start()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN and connection_status and turno:
            pos = pygame.mouse.get_pos()
            cX, cY = pos[0] // 200, pos[1] // 200
            if lin.set_cell_value(cX, cY, player):
                conn.send(f"{cX}-{cY}-{player}".encode())
                turno = False

    screen.blit(background, (0, 0))
    lin.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()