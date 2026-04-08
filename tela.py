import sys
import random
import pygame
import threading
import socket
from linha import Linha
from monitor_rede import MonitorDesempenho 

# Configurações Globais
TAMANHO_TESTE_ATUAL = 60  # 1, 10, 20, 30, 40, 50 ou 60
PROBABILIDADE_PERDA = 0.1 

pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Jogo da Velha - CLIENTE")
clock = pygame.time.Clock()

# Tente carregar a imagem, se falhar usa cor sólida para não dar erro
try:
    background = pygame.transform.scale(pygame.image.load("icon/ceu.jpg"), (600, 600))
except:
    background = pygame.Surface((600, 600))
    background.fill((135, 206, 235))

ultimo_relatorio = pygame.time.get_ticks()
HOST = '127.0.0.1'
PORT = 65432
meia = None
connection_status = False
lin = Linha()
monitor = MonitorDesempenho()
player = "x"
turno = True

def simular_rede(pacote):
    if random.random() < PROBABILIDADE_PERDA:
        return None  
    return pacote

def thread_receber():
    global turno, connection_status
    while True:
        try:
            # Buffer grande para suportar os payloads de 60kb
            raw_data = meia.recv(1024*75).decode()
            if not raw_data: break
            
            data = simular_rede(raw_data)
            
            if data:
                # Passando os dois argumentos que o monitor agora espera
                monitor.registrar_recebimento(data, TAMANHO_TESTE_ATUAL)
                parts = data.split('-')
                x, y, symbol = int(parts[0]), int(parts[1]), parts[2]
                lin.set_cell_value(x, y, symbol)
                turno = True
                print(f"Recebido: {x},{y}")
            else:
                print("⚠️ PACOTE PERDIDO! Jogue novamente.")
                turno = True 
        except Exception as e:
            print(f"Erro na recepção: {e}")
            connection_status = False
            break

def conectar():
    global meia, connection_status
    meia = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        meia.connect((HOST, PORT))
        connection_status = True
        print("Conectado!")
        threading.Thread(target=thread_receber, daemon=True).start()
    except:
        print("Erro de conexão.")

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
                payload = "A" * (TAMANHO_TESTE_ATUAL * 1024)
                msg = f"{cX}-{cY}-{player}-{payload}"
                try:
                    meia.send(msg.encode())
                    monitor.registrar_envio(msg, TAMANHO_TESTE_ATUAL)
                    turno = False
                except:
                    connection_status = False

    screen.blit(background, (0, 0))
    lin.draw(screen)
    pygame.display.flip()
    clock.tick(60)
    monitor.tick_frame() 

    agora = pygame.time.get_ticks()
    if agora - ultimo_relatorio > 5000: 
        monitor.calcular_metricas()
        ultimo_relatorio = agora

pygame.quit()