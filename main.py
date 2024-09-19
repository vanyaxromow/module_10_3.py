from threading import Thread, Lock
from random import randint
from time import sleep


class Bank(Thread):

    def __init__(self):
        super().__init__()
        self.balance = 0
        self.lock = Lock()
        # self.fl = 0
        # self.fl2 = 0

    def deposit(self):
        for i in range(100):
            # self.fl += 1 # если нужно знать количество итераций
            # print(self.fl)
            randint_num = randint(50, 500)
            self.balance += randint_num
            if self.balance >= 500 and self.lock.locked():
                self.lock.release()
            print(f"Пополнение: {randint_num}. Баланс: {self.balance} ")
        sleep(0.001)

    def take(self):
        for i in range(100):
            # self.fl2 += 1 # если нужно знать количество  итераций
            # print(self.fl2)
            randint_num = randint(50, 500)
            if randint_num > self.balance and self.lock.locked():
                break
            print(f'Запрос на {randint_num} ')
            if randint_num <= self.balance:
                self.balance -= randint_num
                print(f'Снятие: {randint_num}. Баланс: {self.balance} ')
            else:
                print(f'Запрос отклонён, недостаточно средств')
                self.lock.acquire()


bk = Bank()

# Т.к. методы принимают self, в потоки нужно передать сам объект класса Bank
th1 = Thread(target=Bank.deposit, args=(bk,))
th2 = Thread(target=Bank.take, args=(bk,))

th1.start()
th2.start()
th1.join()
th2.join()

print(f'Итоговый баланс: {bk.balance}')
