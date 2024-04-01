import threading
import time
import random

class JantarDosCanibais:

    def __init__(self, n, m):
        self.n_canibais = n
        self.m_porcoes = m
        self.travessa = 0
        self.mutex = threading.Semaphore(1)
        self.sinal_canibal = threading.Semaphore(0)
        self.sinal_cozinheiro = threading.Semaphore(0)

    def servir_na_travessa(self):
        self.mutex.acquire()
        if self.travessa == 0:
            print("Travessa vazia! Acordando o cozinheiro...")
            self.mutex.release()
            self.sinal_cozinheiro.release()
            self.sinal_canibal.acquire()  # Aguarda até que o cozinheiro encha a travessa
            self.mutex.acquire()
        self.travessa -= 1
        print("Canibal se serviu da travessa. Porções restantes:", self.travessa)
        self.mutex.release()

    def encher_travessa(self):
        self.mutex.acquire()
        print("Enchendo a travessa com", self.m_porcoes, "porções.")
        self.travessa = self.m_porcoes
        self.mutex.release()
        self.sinal_canibal.release()

    def canibal(self):
        while True:
            self.servir_na_travessa()
            time.sleep(random.randint(1, 3))  # Tempo que o canibal demora para comer

    def cozinheiro(self):
        while True:
            self.sinal_cozinheiro.acquire()
            self.encher_travessa()



def main():
    n = int(input("Digite o número de canibais: "))
    m = int(input("Digite o número de porções que a travessa comporta: "))

    jantar = JantarDosCanibais(n, m)

    threads = []
    for _ in range(n):
        t = threading.Thread(target=jantar.canibal)
        threads.append(t)
        t.start()

    t_cozinheiro = threading.Thread(target=jantar.cozinheiro)
    t_cozinheiro.start()

    for t in threads:
        t.join()

    t_cozinheiro.join()

if __name__ == "__main__":
    main()
