import threading
import time
import random
from colorama import Fore, Style

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
            print(f"{Fore.LIGHTBLACK_EX}Queue is full. Producer is waiting.{Style.RESET_ALL}\n")
            return False
        elif self.is_empty():
            self.front = self.rear = 0
        else:
            self.rear = (self.rear + 1) % self.size
        self.queue[self.rear] = item
        print(f"{Fore.GREEN}Produced item {item}. Queue: {self.queue}{Style.RESET_ALL}\n")
        return True

    def dequeue(self):
        if self.is_empty():
            print(f"{Fore.LIGHTBLACK_EX}Queue is empty. Consumer is waiting.{Style.RESET_ALL}\n")
            return None
        elif self.front == self.rear:
            item = self.queue[self.front]
            self.queue[self.front] = None  # Remove o item da fila
            self.front = self.rear = -1
            print(f"{Fore.RED}Consumed item {item}. Queue: {self.queue}{Style.RESET_ALL}\n")
            return item
        else:
            item = self.queue[self.front]
            self.queue[self.front] = None  # Remove o item da fila
            self.front = (self.front + 1) % self.size
            print(f"{Fore.RED}Consumed item {item}. Queue: {self.queue}{Style.RESET_ALL}\n")
            return item

mutex = threading.Lock()
size = int(input("Digite o tamanho da fila: "))
queue = CircularQueue(size)  

class Producer(threading.Thread):
    def run(self):
        global mutex, queue
        while True:
            mutex.acquire()
            if not queue.is_full():
                item = random.randint(1, 100)  # Item produzido
                queue.enqueue(item)
            mutex.release()
            time.sleep(1)

class Consumer(threading.Thread):
    def run(self):
        global mutex, queue
        while True:
            mutex.acquire()
            if not queue.is_empty():
                item = queue.dequeue()
            mutex.release()
            time.sleep(1)

# Criando threads de produtor e consumidor
producers = [Producer() for _ in range(3)]  # Número de produtores
consumers = [Consumer() for _ in range(2)]  # Número de consumidores

# Iniciando as threads
for producer in producers:
    producer.start()
for consumer in consumers:
    consumer.start()

# Esperando as threads terminarem
for producer in producers:
    producer.join()
for consumer in consumers:
    consumer.join()
