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