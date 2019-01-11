from multiprocessing import Value, Array, Process, Pool
import time, random
from multiprocessing import Process, Queue


class MyProcess():

    def __init__(self, enemy_list, queue):
        self.enemys = enemy_list
        self.q = queue

    def choose_enemy(self, q):
        index = random.randint(0, len(self.enemies) - 1)
        q.put(index)
        print(index)

    def process(self):
        p = Process(target=self.choose_enemy, args=[self.q])
        p.start()

