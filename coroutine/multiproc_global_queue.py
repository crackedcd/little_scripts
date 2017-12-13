from multiprocessing import Pool
# from multiprocessing.dummy import Pool
from multiprocessing import cpu_count
from multiprocessing import Manager

class A():
    
    def aa(self):
        result = []
        manager = Manager()
        for i in range(5):
            threading_pool = Pool(cpu_count() + 1)
            queue_list = manager.Queue()
            queue_count = manager.Queue()
            for j in range(5):
                threading_pool.apply_async(self.bb, args = (i, j, queue_list, queue_count))
            threading_pool.close()
            threading_pool.join()
            count = queue_count.qsize()
            while queue_list.qsize():
                result.append(queue_list.get())
            print("count: %s" % count)
        print(result)

    def bb(self, i, j, llist, count):
        llist.put([i, j])
        count.put(1)
        
    def cc(self):
        self.aa()

if __name__ == "__main__":
    a = A()
    a.aa()
