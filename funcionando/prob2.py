import threading
import time
import random
from colorama import Fore, Style

class LamportMutex:
    def __init__(self, num_threads):
        self.ticket = [0] * num_threads
        self.turn = 0

    def lock(self, thread_id):
        # Solicita um ticket
        self.ticket[thread_id] = max(self.ticket) + 1

        # Espera até que seja o seu turno
        for i in range(len(self.ticket)):
            if i != thread_id:
                while self.ticket[i] != 0 and (self.ticket[i], i) < (self.ticket[thread_id], thread_id):
                    pass

    def unlock(self, thread_id):
        # Libera o recurso
        self.ticket[thread_id] = 0

class Cannibal(threading.Thread):
    def __init__(self, index, servings, table, mutex):
        threading.Thread.__init__(self)
        self.index = index
        self.servings = servings
        self.table = table
        self.mutex = mutex

    def run(self):
        while True:
            # Canibal com fome
            time.sleep(random.uniform(0, 3))
            
            # Tenta pegar porções da mesa
            self.mutex.lock(self.index)
            if self.table.value > 0:
                servings_to_take = min(self.servings, self.table.value)
                print(f'Canibal {self.index} pegou {servings_to_take} porções.\tPorções restantes: {self.table.value - servings_to_take}.')
                self.table.value -= servings_to_take
            else:
                print(f'{Fore.RED}Sem porções disponíveis. Canibal {self.index} acordou o cozinheiro.{Style.RESET_ALL}')
                self.mutex.unlock(self.index)
                continue
            self.mutex.unlock(self.index)

            # Canibal se alimenta
            time.sleep(random.uniform(1, 4))
            print(f'Canibal {self.index} terminou de comer.')

class Cook(threading.Thread):
    def __init__(self, table, servings):
        threading.Thread.__init__(self)
        self.table = table
        self.servings = servings

    def run(self):
        while True:
            # Cozinheiro dormindo
            print('\nCozinheiro dormindo...')
            time.sleep(random.uniform(2, 5))
            
            # Cozinheiro acorda e prepara mais porções
            print('\nCozinheiro acordou.')
            self.table.value = self.servings
            print(f'{Fore.GREEN}Cozinheiro colocou {self.servings} porções na mesa.{Style.RESET_ALL}')
            self.table.up()  # Notifica os canibais que mais porções estão disponíveis

# Função para ler entrada do usuário
def get_input():
    N = int(input("Digite o número de canibais: "))
    M = int(input("Digite a capacidade inicial da travessa: "))
    return N, M

# Definindo os parâmetros
N, M = get_input() # Número de canibais e Capacidade inicial da travessa
servings = 10 # Número de porções adicionadas pelo cozinheiro

# Inicializando mutex
mutex = LamportMutex(N)

# Inicializando semáforo contador para a mesa
class Semaphore:
    def __init__(self, initial):
        self.lock = threading.Condition(threading.Lock())
        self.value = initial

    def up(self):
        with self.lock:
            self.value += 1
            self.lock.notify()

    def down(self):
        with self.lock:
            while self.value <= 0:
                self.lock.wait()
            self.value -= 1
            self.lock.notify()  # Notificar os canibais que o recurso foi atualizado

table = Semaphore(M)

# Criando threads para os canibais e o cozinheiro
canibais = [Cannibal(i, random.randint(1, 3), table, mutex) for i in range(N)]
cozinheiro = Cook(table, servings)

# Iniciando as threads
for canibal in canibais:
    canibal.start()
cozinheiro.start()

# Esperando as threads terminarem
for canibal in canibais:
    canibal.join()
cozinheiro.join()
