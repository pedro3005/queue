#!/usr/bin/env python2

import sys
import cPickle

class QueueError(Exception):
    pass

class Queue:
    def __init__(self, *args):
        self.queue = []
        for arg in args:
            self.put(arg)
    def put(self, element):
        self.queue.insert(0, element)
    def next(self):
        try:
            return self.queue.pop()
        except IndexError:
            raise QueueError("Empty queue!")
    def __str__(self):
        return repr(self.queue)
    def __len__(self):
        return len(self.queue)

def queue_to_list(queue):
    return [queue.next() for i in range(len(queue))]

def queue(qlist):
    '''Converts a list object to a queue.'''
    return Queue(*qlist)

if __name__ == "__main__":
    
    try:
        main, pending = cPickle.load(open(".queue_data"))
    except: # failed somehow to open and de-serialize the data.
            # could be practically any exception, so it is a bare 'except: '
        print '''Failed to load the queue data, creating a new one...
Everything's fine, though you did lose anything you might have stored.'''
        main = Queue()
        pending = Queue()
    finally:
        outfd = open(".queue_data", "w")
    
    sys.argv.pop(0) # remove the useless './queue.py' part
    argc = len(sys.argv)
    
    if argc == 0:
        print '''Welcome to queue.py! Commands:
    ./queue.py add item1 [item2, item3, ...]
    ./queue.py next
    ./queue.py reset'''
        
    elif sys.argv[0] == "add":
        if argc == 1:
            print '''You're doing it wrong!
The right way is:
    ./queue.py add item1 [item2, item3, ...]'''
        else:
            for item in sys.argv[1:]:
                main.put(item)
    
    elif sys.argv[0] == "next":
        try:
            next = main.next()
            pending.put(next)
            print "Next is {0}. it has been added to the pending queue.".format(next)
        except QueueError:
            print "Queue is empty! Try adding something"
    
    elif sys.argv[0] == "reset":
        if len(pending) < 1:
            print "There is nothing on the pending queue."
        else:
            main = Queue(*(queue_to_list(pending) + queue_to_list(main)))
    
    cPickle.dump([main, pending], outfd)
    outfd.close()
