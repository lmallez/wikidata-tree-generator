#!/usr/bin/env python3
from threading import Thread
from wikidata.entity import EntityId
from tree_builder.tree.dispatcher.Dispatcher import Dispatcher


class ThreadExecute:
    def __init__(self, entity_queue):
        self.entity_queue = entity_queue

    def next_entity(self):
        return self.entity_queue.pop(0)

    def execute_thread(self, method, entity_id, prof):
        method(entity_id, prof)
        if self.entity_queue:
            self.execute_thread(method, self.next_entity(), prof)


class ThreadedDispatcher(Dispatcher):
    def __init__(self, max_thread):
        self.max_thread = max_thread
        self.thread_number = 0

    def start_thread(self, executer, method, entity_id, prof):
        executer.execute_thread(method, entity_id, prof)
        self.thread_number -= 1

    def compute(self, entity_ids: [EntityId], method, prof):
        if len(entity_ids) == 0:
            return
        if len(entity_ids) == 1:
            method(entity_ids[0], prof)
            return
        threads = []
        self_id = entity_ids[0]
        executer = ThreadExecute(entity_ids[1:])
        while self.thread_number < self.max_thread - 1 and executer.entity_queue:
            threads.append(Thread(target=self.start_thread, args=[executer, method, executer.next_entity(), prof]))
            self.thread_number += 1
        for thread in threads:
            thread.start()
        executer.execute_thread(method, self_id, prof)
        for thread in threads:
            thread.join()
