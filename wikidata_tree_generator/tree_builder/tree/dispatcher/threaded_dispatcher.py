#!/usr/bin/env python3
from threading import Thread
from wikidata.entity import EntityId
from .dispatcher import Dispatcher


class ThreadExecute:
    def __init__(self, entity_queue):
        self.entity_queue = entity_queue

    def next_entity(self):
        return self.entity_queue.pop(0)

    def execute_thread(self, method, entity_id, depth):
        method(entity_id, depth)
        if self.entity_queue:
            self.execute_thread(method, self.next_entity(), depth)


class ThreadedDispatcher(Dispatcher):
    def __init__(self, max_thread):
        self.max_thread = max_thread
        self.thread_number = 0

    def start_thread(self, executer, method, entity_id, depth):
        executer.execute_thread(method, entity_id, depth)
        self.thread_number -= 1

    def compute(self, entity_ids: [EntityId], method, depth):
        if len(entity_ids) == 0:
            return
        if len(entity_ids) == 1:
            method(entity_ids[0], depth)
            return
        threads = []
        self_id = entity_ids[0]
        executer = ThreadExecute(entity_ids[1:])
        while self.thread_number < self.max_thread and executer.entity_queue:
            threads.append(Thread(target=self.start_thread, args=[executer, method, executer.next_entity(), depth]))
            self.thread_number += 1
        for thread in threads:
            thread.start()
        executer.execute_thread(method, self_id, depth)
        for thread in threads:
            thread.join()
