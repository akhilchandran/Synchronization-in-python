import threading, time, os, signal, sys
import random

class Thread(threading.Thread):
    def __init__(self, target, *args):
        threading.Thread.__init__(self, target=target, args=args)
        self.start()

class Semaphore(threading._Semaphore):
    wait = threading._Semaphore.acquire   
    def signal(self, n=1):
        for i in range(n):
            self.release()

    def value(self):
        return self._Semaphore__value

    
def watcher():
    child = os.fork()
    if child == 0:
        return

    try:
        os.wait()
    except KeyboardInterrupt:
        print 'KeyBoardInterrupt'
        try:
            os.kill(child, signal.SIGKILL)
        except OSError:
            pass
    sys.exit()

class Shared:
    def __init__(self, start=7,capacity=15):
        self.product = Semaphore(start)
        self.buff = Semaphore(capacity-start)
        self.mutex = Semaphore(1)
        self.consumer = Semaphore(1)
        self.producer= Semaphore(1)
def consume(shared):
    shared.consumer.wait()
    shared.product.wait()
    shared.mutex.wait()
    print shared.product.value()
    shared.mutex.signal()
    shared.buff.signal()
    shared.consumer.signal()

def produce(shared):
    shared.producer.wait()
    shared.buff.wait()
    shared.mutex.wait()
    shared.product.signal()
    print shared.product.value()
    shared.mutex.signal()
    shared.producer.signal()
def event(shared, f, mu=1):
    while True:
        t = random.expovariate(1.0/mu)
        time.sleep(t)
        f(shared)
watcher()
shared = Shared()
fs = [consume]*5 + [produce]*7
threads = [Thread(event, shared, f) for f in fs]
for thread in threads: thread.join()

