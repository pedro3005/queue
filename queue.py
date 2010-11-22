#!/usr/bin/env python

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
    add item1 [item2, item3, ...] -- adds the items to the queue
    next -- grabs an item from the queue and puts it as pending
    reset -- moves all pending items back to the queue
    done [item1, item2, ...] -- without arguments, removes the first pending item.
    print -- prints your queues (main and pending)
    clear -- clears the main queue'''
        
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
            next_key = main.next()
            pending.put(next_key)
            print "{0}".format(next_key)
        except QueueError:
            print "Queue is empty! Try adding something"
    
    elif sys.argv[0] == "reset":
        if len(pending) < 1:
            print "There is nothing on the pending queue."
        else:
            main = Queue(*(queue_to_list(pending) + queue_to_list(main)))
    
    elif sys.argv[0] == "done":
        if argc == 1:
            pending.next() # it gets thrown away, so essentially removing
        else:
            for item in sys.argv[1:]:
                try:
                    pending.remove(item)
                except QueueError:
                    print "Could not find {0}".format(item)
    
    elif sys.argv[0] == "print":
        print '''Here is your main queue:
{0}
And here are your pending items:
{1}'''.format(main, pending)

    elif sys.argv[0] == "clear":
        main = Queue()
    
    cPickle.dump([main, pending], outfd)
    outfd.close()
