from threading import Thread, Lock
import time
import random

# Variáveis compartilhadas
clock = 0
timestamp_self = 0
solicitacoes = {}  # Dicionário para armazenar as solicitações recebidas de outros processos
liberado = True  # Indica se o processo está na seção crítica ou não
mutex = Lock()  # Mutex para garantir acesso exclusivo à seção crítica

# Função para atualizar o relógio lógico local
def incrementar_clock():
    global clock
    with mutex:
        clock += 1

# Função para gerar um carimbo de tempo
def gerar_timestamp():
    global timestamp_self
    with mutex:
        timestamp_self = clock
        incrementar_clock()

# Função para enviar solicitação de entrada na seção crítica
def solicitar_entrada():
    gerar_timestamp()
    for processo in solicitacoes.keys():
        enviar_mensagem(processo, timestamp_self)

# Função para receber uma solicitação de outro processo
def receber_solicitacao(timestamp_received, processo):
    solicitacoes[processo] = timestamp_received
    enviar_resposta(processo)

# Função para enviar uma mensagem
def enviar_mensagem(processo, timestamp):
    # Simulação de envio de mensagem
    time.sleep(random.uniform(0, 0.1))
    receber_resposta(processo, timestamp)

# Função para enviar mensagem de resposta
def enviar_resposta(processo):
    enviar_mensagem(processo, timestamp_self)

# Função para verificar se é seguro entrar na seção crítica
def verificar_seguranca():
    for processo, timestamp in solicitacoes.items():
        if (timestamp, processo) < (timestamp_self, 'self'):
            return False
    return True

# Função para entrar na seção crítica
def entrar_secao_critica():
    global liberado
    while not verificar_seguranca():
        time.sleep(0.01)
    with mutex:
        liberado = False
        print(f"Processo {timestamp_self} entrando na seção crítica")
        time.sleep(1)  # Simulação de tarefa na seção crítica
        liberado = True
        print(f"Processo {timestamp_self} saindo da seção crítica")
        for processo in solicitacoes.keys():
            enviar_mensagem(processo, float('inf'))

# Função para receber uma mensagem de liberação de outro processo
def receber_liberacao(processo):
    solicitacoes[processo] = float('inf')

# Função principal do processo
def principal():
    global liberado
    while True:
        time.sleep(random.uniform(0, 0.5))
        if liberado:
            solicitar_entrada()
            entrar_secao_critica()

# Função para simular o envio de mensagem (thread separada)
def receber_resposta(processo, timestamp):
    time.sleep(random.uniform(0, 0.1))
    receber_solicitacao(timestamp, processo)

# Simulação de vários processos
for i in range(5):
    solicitacoes[i] = float('inf')  # Inicializa as solicitações com infinito

# Criando e inicializando os processos
threads = []
for i in range(5):
    t = Thread(target=principal)
    threads.append(t)

# Iniciando os processos
for t in threads:
    t.start()

# Aguardando a finalização dos processos
for t in threads:
    t.join()

print("Fim da execução")
