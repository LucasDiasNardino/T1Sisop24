import threading
import time
import random
from colorama import Fore, Style
from lamport import LamportMutex  # Importa a classe LamportMutex do arquivo lamport.py

class CircularQueue:
    def __init__(self, size):
        self.size = size
        self.queue = [None] * size
        self.front = self.rear = -1

    def is_full(self):
        return (self.rear + 1) % self.size == self.front

    def is_empty(self):
        return self.front == -1

    def enqueue(self, item):
        if self.is_full():
            print(f"{Fore.LIGHTBLACK_EX}Fila está cheia. Produtor está aguardando.{Style.RESET_ALL}\n")
            return False
        elif self.is_empty():
            self.front = self.rear = 0
        else:
            self.rear = (self.rear + 1) % self.size
        self.queue[self.rear] = item
        print(f"{Fore.GREEN}Item produzido: {item}. Fila: {self.queue}{Style.RESET_ALL}\n")
        return True

    def dequeue(self):
        if self.is_empty():
            print(f"{Fore.LIGHTBLACK_EX}Fila está vazia. Consumidor está aguardando.{Style.RESET_ALL}\n")
            return None
        elif self.front == self.rear:
            item = self.queue[self.front]
            self.queue[self.front] = None  # Remove o item da fila
            self.front = self.rear = -1
            print(f"{Fore.RED}Item consumido: {item}. Fila: {self.queue}{Style.RESET_ALL}\n")
            return item
        else:
            item = self.queue[self.front]
            self.queue[self.front] = None  # Remove o item da fila
            self.front = (self.front + 1) % self.size
            print(f"{Fore.RED}Item consumido: {item}. Fila: {self.queue}{Style.RESET_ALL}\n")
            return item

tamanho_fila = int(input("Digite o tamanho da fila: \n"))
queue = CircularQueue(tamanho_fila)  
qtProdutores = int(input("Digite a quantidade de produtores: \n"))
qtConsumidores = int(input("Digite a quantidade de consumidores: \n"))

mutex = LamportMutex(qtProdutores+qtConsumidores)  # Altere para o número adequado de threads

class Produtor(threading.Thread):
    def run(self):
        global mutex, queue
        while True:
            mutex.lock(threading.get_ident() % 5)
            if not queue.is_full():
                item = random.randint(1, 100)  # Item produzido
                queue.enqueue(item)
            mutex.unlock(threading.get_ident() % 5)
            time.sleep(1)

class Consumidor(threading.Thread):
    def run(self):
        global mutex, queue
        while True:
            mutex.lock(threading.get_ident() % 5)
            if not queue.is_empty():
                item = queue.dequeue()
            mutex.unlock(threading.get_ident() % 5)
            time.sleep(1)

# Criando threads de produtor e consumidor
produtores = [Produtor() for _ in range(qtProdutores)]  # Número de produtores
consumidores = [Consumidor() for _ in range(qtConsumidores)]  # Número de consumidores

# Iniciando as threads
for produtor in produtores:
    produtor.start()
for consumidor in consumidores:
    consumidor.start()

# Esperando as threads terminarem
for produtor in produtores:
    produtor.join()
for consumidor in consumidores:
    consumidor.join()
