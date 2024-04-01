from threading import Thread, Semaphore
import time
import random

class Cozinheiro(Thread):
    def __init__(self, travessa, M, clock):
        super().__init__()
        self.travessa = travessa
        self.M = M
        self.clock = clock

    def run(self):
        while True:
            with self.travessa.mutex:
                if self.travessa.quantidade == 0:
                    print("\nA travessa está vazia. O cozinheiro está preparando mais porções...")

                    self.travessa.reabastecer(self.M)
                else:
                    print("A travessa ainda tem porções. O cozinheiro está dormindo...")
            time.sleep(2)

class Canibal(Thread):
    def __init__(self, nome, travessa, clock):
        super().__init__()
        self.nome = nome
        self.travessa = travessa
        self.clock = clock

    def run(self):
        while True:
            time.sleep(random.uniform(1, 3))  # Tempo para comer
            self.clock.incrementar()
            with self.clock.mutex:
                timestamp_self = self.clock.valor
            with self.travessa.mutex:
                print(f"Canibal {self.nome} está aguardando para se servir.")
                while self.travessa.quantidade == 0:
                    if self.clock.valor < timestamp_self:
                        break
                if self.travessa.quantidade > 0:
                    self.travessa.servir(self.nome)
                else:
                    print(f"Canibal {self.nome} desistiu de esperar.")
            time.sleep(random.uniform(0.5, 1))

class Travessa:
    def __init__(self, M):
        self.mutex = Semaphore(1)
        self.quantidade = 0
        self.M = M

    def servir(self, nome):
        self.quantidade -= 1
        print(f"Canibal {nome} está se servindo. Restam {self.quantidade} porções na travessa.")

    def reabastecer(self, M):
        self.quantidade = M
        print(f"\nA travessa foi reabastecida com {M} porções.")

class Clock:
    def __init__(self):
        self.mutex = Semaphore(1)
        self.valor = 0

    def incrementar(self):
        with self.mutex:
            self.valor += 1

def main(N, M):
    clock = Clock()
    travessa = Travessa(M)
    cozinheiro = Cozinheiro(travessa, M, clock)
    cozinheiro.start()

    canibais = []
    for i in range(N):
        canibal = Canibal(i+1, travessa, clock)
        canibais.append(canibal)
        canibal.start()

    cozinheiro.join()
    for canibal in canibais:
        canibal.join()

if __name__ == "__main__":
    N = int(input("Digite o número de canibais: "))
    M = int(input("Digite o número de porções que a travessa comporta: "))
    main(N, M)
