#!/usr/bin/env python3
from threading import Thread
from wikidata_tree_generator.configuration import ThreadConfiguration
from wikidata_tree_generator.database import Database
from wikidata_tree_generator.logger.logger import Logger, Color
from .database_filler import DatabaseFiller
from .entity_filler import EntityFiller


class ThreadedDatabaseFiller(DatabaseFiller):
    def __init__(self, entity_filler: EntityFiller, database: Database, logger: Logger, thread_configuration: ThreadConfiguration):
        super().__init__(entity_filler, database, logger)
        self.entity_queue = []
        self.thread_configuration = thread_configuration

    def print(self, entity, thread_id=0):
        self.logger.log("Filler {:>4} | {:>10}".format(thread_id, entity.id))

    def __next_entity(self):
        return self.entity_queue.pop(0)

    def thread_entity(self, entity, thread_id=0):
        self.print(entity, thread_id)
        self.entity_filler.load(entity)
        if self.entity_queue:
            self.thread_entity(self.__next_entity(), thread_id)

    def process(self):
        self.entity_queue = [v for _, v in self.database.cache.items()]
        threads = []
        for i in range(0, self.thread_configuration.max_thread):
            if not self.entity_queue:
                break
            threads.append(Thread(target=self.thread_entity, args=[self.__next_entity(), i]))
        self.logger.log("ThreadedEntityFiller : {}/{} threads created, {} entities left".format(
            len(threads), self.thread_configuration.max_thread, len(self.entity_queue)), Color.HEADER)
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
