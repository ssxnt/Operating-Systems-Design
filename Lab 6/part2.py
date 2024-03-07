# student name: Sant Sumetpong
# student number: 24821563

import multiprocessing as mp
import random  # is used to cause some randomness
import time  # is used to cause some delay to simulate thinking or eating times


def philosopher(id: int, chopstick: list):
    """
       implements a thinking-eating philosopher
       id is used to identifier philosopher #id (id is between 0 to numberOfPhilosophers-1)
       chopstick is the list of semaphores associated with the chopsticks
    """

    def eatForAWhile():  # simulates philosopher eating time with a random delay
        print(f"DEBUG: philosopher{id} eating")
        time.sleep(round(random.uniform(.1, .3), 2))  # a random delay (100 to 300 ms)

    def thinkForAWhile():  # simulates philosopher thinking time with a random delay
        print(f"DEBUG: philosopher{id} thinking")
        time.sleep(round(random.uniform(.1, .3), 2))  # a random delay (100 to 300 ms)

    for _ in range(6):  # to make testing easier, instead of a forever loop we use a finite loop
        leftChopstick = id
        rightChopstick = (id + 1) % 5  # 5 is number of philosophers

        while True:
            chopstick[leftChopstick].acquire(block=False)
            if chopstick[leftChopstick].acquire(block=False):
                print(f"DEBUG: philosopher{id} has chopstick{leftChopstick}")
                chopstick[rightChopstick].acquire(block=False)
                if chopstick[rightChopstick].acquire(block=False):
                    print(f"DEBUG: philosopher{id} has chopstick{rightChopstick}")
                    break
                else:
                    chopstick[leftChopstick].release()
            time.sleep(round(random.uniform(.1, .3), 2))  # a random delay (100 to 300 ms)

        # to simplify, try statement not used here

        eatForAWhile()  # use this line as is

        print(f"DEBUG: philosopher{id} is to release chopstick{rightChopstick}")
        chopstick[rightChopstick].release()
        print(f"DEBUG: philosopher{id} is to release chopstick{leftChopstick}")
        chopstick[leftChopstick].release()

        thinkForAWhile()  # use this line as is


if __name__ == "__main__":
    semaphoreList = list()  # this list will hold one semaphore per chopstick
    numberOfPhilosophers = 5

    for i in range(numberOfPhilosophers):
        semaphoreList.append(mp.Semaphore(1))  # one semaphore per chopstick

    philosopherProcessList = list()
    for i in range(numberOfPhilosophers):  # instantiate all processes representing philosophers
        philosopherProcessList.append(mp.Process(target=philosopher, args=(i, semaphoreList)))
    for j in range(numberOfPhilosophers):  # start all child processes
        philosopherProcessList[j].start()
    for k in range(numberOfPhilosophers):  # join all child processes
        philosopherProcessList[k].join()