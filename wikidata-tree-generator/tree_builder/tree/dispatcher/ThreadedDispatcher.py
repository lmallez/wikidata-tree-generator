#!/usr/bin/env python3
from threading import Thread
from wikidata.entity import EntityId
from tree_builder.tree.dispatcher.Dispatcher import Dispatcher


class ThreadedDispatcher(Dispatcher):
    def __init__(self, max_thread):
        self.max_thread = max_thread
        self.thread_number = 0

    def compute(self, entity_ids: [EntityId], method, prof, branch):
        if len(entity_ids) == 0:
            return
        if len(entity_ids) == 1:
            method(entity_ids[0], prof, branch)
            return
        threads = []
        other_entities = []
        for entity_id in entity_ids:
            if self.thread_number < self.max_thread:
                threads.append(Thread(target=method, args=[entity_id, prof, branch]))
                branch += 1
                self.thread_number += 1
            else:
                other_entities.append(entity_id)
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        for entity_id in other_entities:
            method(entity_id, prof, branch)
            branch += 1
        self.thread_number -= len(threads)
