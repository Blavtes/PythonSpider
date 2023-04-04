import threading
from time import sleep
import os

a = 1


def music():
    global a
    print('a1', a)
    a = 1000
    for item in range(3):
        sleep(2)
        print(os.getpid(), '播放：3333')


t = threading.Thread(target=music)
t.start()

for i in range(4):
    sleep(1)
    print(os.getpid(), '播放： 4444')
t.join()
print('=' * 50)
print('a2', a)


def fun(sec, name):
    print('start')
    sleep(sec)
    print('%s over' % name)


jobs = []
for i in range(5):
    t = threading.Thread(target=fun, args=(2,), kwargs={'name': 'T%d' % i})  # 两种传参方法 顺序传参、关键帧传参
    jobs.append(t)
    t.start()
for t in jobs:
    t.join()
