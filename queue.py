#!/usr/bin/env python

import sys
import cPickle
import subprocess
import os.path

class QueueError(Exception):
    pass

class Queue(object):
    def __init__(self, *args):
        self.queue = []
        for arg in args:
            self.put(arg)
    def put(self, element):
        self.queue.insert(0, element)
    def remove(self, element):
        try:
            self.queue.remove(element)
        except ValueError:
            raise QueueError("Could not find element {0}!".format(element))
    def next(self):
        try:
            return self.queue.pop()
        except IndexError:
            raise QueueError("Empty queue!")
    def to_list(self):
        return [self.next() for i in range(len(self))]
    def __str__(self):
        return repr(self.queue)
    def __len__(self):
        return len(self.queue)

def exit(status):
    if os.path.isfile(".queue-lock"):
        subprocess.call(["rm", ".queue-lock"])
    sys.exit(status)

if __name__ == "__main__":
    
    while os.path.isfile(".queue-lock"):
        pass
    
    subprocess.call(["touch", ".queue-lock"])
    
    try:
        main, pending = cPickle.load(open(".queue_data"))
    except: # failed somehow to open and de-serialize the data.
            # could be practically any exception, so it is a bare 'except: '
        main = Queue()
        pending = Queue()
    
    sys.argv.pop(0) # remove the useless './queue.py' part
    argc = len(sys.argv)
    
    if argc == 0:
       exit(1)
        
    elif sys.argv[0] == "add":
        if argc == 1:
            exit(1)
        else:
            for item in sys.argv[1:]:
                main.put(item)
    
    elif sys.argv[0] == "next":
        try:
            next_key = main.next()
            pending.put(next_key)
            print "{0}".format(next_key)
        except QueueError:
            exit(1)
    
    elif sys.argv[0] == "reset":
        if len(pending) < 1:
            exit(1)
        else:
            main = Queue(*(pending.to_list() + main.to_list()))
    
    elif sys.argv[0] == "done":
        if argc == 1:
            pending.next() # it gets thrown away, so essentially removing
        else:
            for item in sys.argv[1:]:
                try:
                    pending.remove(item)
                except QueueError:
                    pass
    
    elif sys.argv[0] == "print":
        print ", ".join(main.queue)
        print ", ".join(pending.queue)

    elif sys.argv[0] == "clear":
        main = Queue()
    
    outfd = open(".queue_data", "w")
    cPickle.dump([main, pending], outfd)
    outfd.close()

    exit(0)

