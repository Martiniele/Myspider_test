# coding: utf-8
import multiprocessing
import os
import time
from multiprocessing import Pool


class testClass():
    def upMethod(self):
        print '我是UP'
        time.sleep(1)

    def downMethod(self):
        print '我是DOWN'
        time.sleep(1)

    def multiProcess(self):
        p = Pool(2)
        aObj = p.apply_async(self, args=('up',))  # 这里是重点
        aObj = p.apply_async(self, args=('down',))  # 这里是重点
        p.close()
        p.join()

    def __call__(self, sign):  # 这里是重点
        if sign == 'up':
            return self.upMethod()
        elif sign == 'down':
            return self.downMethod()


# 线程执行任务的函数
def counter(n):
    count = 0
    for i in xrange(n):
        i += 1
        count += i
        time.sleep(0.01)
    print 'n : %d, count : %d' % (n, count)
    time.sleep(10)


def main():
    print 'main pid : %d, ppid : %d' % (os.getpid(), os.getppid())
    subPro = multiprocessing.Process(target=counter, args=(100,))
    subPro.start()
    subPro.join()  # 阻塞主进程，等待子进程先结束
    print 'subPro pid : %d, ppid : %d' % (subPro.pid, os.getpid())


if __name__ == '__main__':
    testObj = testClass()
    testObj.multiProcess()
    main()
