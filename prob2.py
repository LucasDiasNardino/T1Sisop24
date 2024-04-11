import threading
import time
import random
from colorama import Fore, Style
from lamport import LamportMutex  

class Cannibal(threading.Thread):
    def __init__(self, index, servings, table, mutex, cook):
        threading.Thread.__init__(self)
        self.index = index
        self.servings = servings
        self.table = table
        self.mutex = mutex
        self.cook = cook

    def run(self):
        while True:
            time.sleep(random.uniform(0, 3))
            
            # Tenta pegar porções da mesa
            self.mutex.lock(self.index)
            if self.table.value > 0:
                servings_to_take = min(self.servings, self.table.value)
                print(f'Canibal {self.index} pegou {servings_to_take} porções.\tPorções restantes: {self.table.value - servings_to_take}.')
                self.table.value -= servings_to_take
            else:
                print(f'{Fore.RED}Sem porções disponíveis. Canibal {self.index} acordou o cozinheiro.{Style.RESET_ALL}')
                self.cook.wake_up()
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
        self.mutex = threading.Lock()
        self.cond = threading.Condition(self.mutex)

    def run(self):
        while True:
            with self.cond:
                print('\nCozinheiro dormindo...')
                self.cond.wait()
            
                print('\nCozinheiro acordou.')
                self.table.value = self.servings
                print(f'{Fore.GREEN}Cozinheiro colocou {self.servings} porções na mesa.{Style.RESET_ALL}')
                self.cond.notify_all()  # Notifica os canibais que mais porções estão disponíveis

    def wake_up(self):
        with self.cond:
            self.cond.notify()

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
        self.value = initial

# Criando objetos de semáforo e cozinheiro
table = Semaphore(M)
cook = Cook(table, servings)

# Criando threads para os canibais
canibais = [Cannibal(i, random.randint(1, 3), table, mutex, cook) for i in range(N)]

# Iniciando as threads
for canibal in canibais:
    canibal.start()
cook.start()

# Esperando as threads terminarem
for canibal in canibais:
    canibal.join()
cook.join()
