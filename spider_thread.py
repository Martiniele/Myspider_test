# encoding: utf-8
import threading
from threading import Thread
from threading import Lock
from time import sleep
from random import randint

# 仓库有十个槽位
storehouse = [0] * 10
# 线程锁
lock = Lock()


class Producer(Thread):
    u"""生产者，依次往仓库里的十个槽位生产产品"""

    def __init__(self):
        super(Producer, self).__init__()

    def run(self):
        print "Producer starts producing...\n",
        x = 0
        while x < len(storehouse):
            # 获取锁
            lock.acquire()
            print "Producer is producing the No.%d product.\n" % x,
            storehouse[x] = 1
            print "Now, the storehouse is %s\n" % storehouse,
            # 释放锁
            lock.release()
            x += 1
            sleep(randint(1, 3))
        print "Producer has produced all the products!\n",


class Consumer(Thread):
    u"""消费者，依次消费仓库里十个槽位的产品，如果槽位还没有商品，则等待生产者生产"""

    def __init__(self):
        super(Consumer, self).__init__()

    def run(self):
        print "Consumer starts consuming...\n",
        x = 0
        while x < len(storehouse):
            print "Consumer wants to consume a product...\n",
            # 获取锁
            lock.acquire()
            if storehouse[x] <= 0:
                print "There are not any products, the consumer waits.\n",
            else:
                print "Consumer is consuming the No.%d product.\n" % x,
                storehouse[x] = -1
                print "Now, the storehouse is %s\n" % storehouse,
                x += 1
                # 释放锁
            lock.release()
            sleep(randint(1, 3))
        print "Consumer has consumed all the products!\n",


class SubThread(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self, name=name)

    # 重写父类的run方法
    def run(self):
        sleep(0.1)
        print 'Thread[%s] counter start...' % self.name
        counter(100)
        print 'Thread[%s] counter end.' % self.name


# 线程执行任务的函数
def counter(n):
    count = 0
    for i in xrange(n):
        i += 1
        count += i
    print 'n : %d, count : %d' % (n, count)


def main():
    for i in xrange(4):
        i += 1
        thd = SubThread('thread-' + str(i))
        thd.start()
        thd.join()  # 阻塞主线程，等待子线程先结束


print "Originally, the storehouse is ", storehouse

producer = Producer()
consumer = Consumer()
producer.start()
consumer.start()

# 阻塞线程，等待其他线程结束
producer.join()
consumer.join()

print "Finally, the storehouse is ", storehouse
