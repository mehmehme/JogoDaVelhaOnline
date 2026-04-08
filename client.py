import sys
import pygame
import threading
import socket
from linha import Linha

pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Jogo da Velha - SERVIDOR (Chuva)")
clock = pygame.time.Clock()

# Tenta carregar imagem, senão usa fundo cinza
try:
    background = pygame.transform.scale(pygame.image.load("icon/nublado.jpg"), (600, 600))
except:
    background = pygame.Surface((600, 600))
    background.fill((100, 100, 100))

HOST = '127.0.0.1'
PORT = 65432
conn = None
connection_status = False
lin = Linha()
player = "o"
turno = False 

# Variável para sabermos qual o tamanho do pacote que o cliente está testando
ultimo_payload_recebido = ""

def thread_receber():
    global turno, connection_status, ultimo_payload_recebido
    while True:
        try:
            # CORREÇÃO 1: Aumentar o buffer para suportar os testes de até 60kb
            raw_data = conn.recv(1024*75).decode() 
            if not raw_data:
                break
            
            parts = raw_data.split('-')
            if len(parts) >= 3:
                x, y, symbol = int(parts[0]), int(parts[1]), parts[2]
                
                # Se houver carga extra (os "AAAAA"), guardamos para devolver igual
                if len(parts) > 3:
                    ultimo_payload_recebido = parts[3]
                else:
                    ultimo_payload_recebido = ""

                lin.set_cell_value(x, y, symbol)
                turno = True 
                print(f"Recebido do Cliente: {x}, {y} (Tamanho: {len(raw_data)} bytes)")
        except Exception as e:
            print(f"Erro na recepção do servidor: {e}")
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
    print(f"Conectado a {addr}!")
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
                # CORREÇÃO 2: Devolver o pacote com o mesmo payload para o monitor medir
                msg = f"{cX}-{cY}-{player}-{ultimo_payload_recebido}"
                conn.send(msg.encode())
                turno = False

    screen.blit(background, (0, 0))
    lin.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()