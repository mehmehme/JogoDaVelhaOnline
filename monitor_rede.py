import time

class MonitorDesempenho:
    def __init__(self):
        self.start_time = time.time()
        self.pacotes_enviados = 0
        self.pacotes_recebidos = 0
        self.total_bytes_sent = 0
        self.total_bytes_received = 0
        
        # Categorias para o experimento do TCC
        self.categorias = {f"{i}kb": {'enviados': 0, 'recebidos': 0, 'latencias': []} 
                           for i in [1, 10, 20, 30, 40, 50, 60]}
        
        self.latencies = []
        self.last_click_time = 0
        self.frame_times = []
        self.last_frame_tick = time.time()

    def registrar_envio(self, data, tam):
        cat = f"{tam}kb"
        self.pacotes_enviados += 1
        self.total_bytes_sent += len(str(data).encode())
        self.last_click_time = time.time()
        
        if cat in self.categorias:
            self.categorias[cat]['enviados'] += 1

    def registrar_recebimento(self, data, tam):
        cat = f"{tam}kb"
        self.pacotes_recebidos += 1
        self.total_bytes_received += len(str(data).encode())
        
        if self.last_click_time > 0:
            latencia = (time.time() - self.last_click_time) * 1000
            self.latencies.append(latencia) # Global
            if cat in self.categorias:
                self.categorias[cat]['recebidos'] += 1
                self.categorias[cat]['latencias'].append(latencia) # Por categoria
            self.last_click_time = 0

    def tick_frame(self):
        agora = time.time()
        duration = (agora - self.last_frame_tick) * 1000
        self.frame_times.append(duration)
        self.last_frame_tick = agora
        if len(self.frame_times) > 60: self.frame_times.pop(0)

    def calcular_metricas(self):
        tempo_total = time.time() - self.start_time
        if tempo_total <= 0: tempo_total = 1
        
        taxa_envio = self.total_bytes_sent / tempo_total
        taxa_recebimento = self.total_bytes_received / tempo_total
        
        print("\n" + "="*60)
        print(f"RELATÓRIO GERAL | Tempo: {tempo_total:.1f}s")
        print(f"Upload: {taxa_envio:.2f} B/s | Download: {taxa_recebimento:.2f} B/s")
        print("-" * 60)
        print(f"{'CARGA':<10} | {'ENV':<6} | {'REC':<6} | {'PERDA %':<10} | {'LATÊNCIA'}")
        
        for cat, d in self.categorias.items():
            env = d['enviados']
            rec = d['recebidos']
            perda = ((env - rec) / env * 100) if env > 0 else 0
            avg_lat = sum(d['latencias'])/len(d['latencias']) if d['latencias'] else 0
            print(f"{cat:<10} | {env:<6} | {rec:<6} | {perda:>8.2f}% | {avg_lat:>6.1f}ms")
        print("="*60 + "\n")