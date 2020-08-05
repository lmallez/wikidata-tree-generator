#!/usr/bin/env python3
from threading import Thread

from Configuration import ThreadConfiguration
from Database import Database
from entity_filler.EntityFiller import EntityFiller
from entity_filler.property_fetcher.PropertyFetcher import PropertyFetcher
from logger.Logger import Logger, Color
from tree_builder.PlacerBuilder import PlaceBuilder


class ThreadedEntityFiller(EntityFiller):
    def __init__(self, properties: list, character_database: Database, property_fetcher: PropertyFetcher, place_builder: PlaceBuilder, logger: Logger, thread_configuration: ThreadConfiguration):
        super().__init__(properties, character_database, property_fetcher, place_builder, logger)
        self.entity_queue = []
        self.thread_configuration = thread_configuration

    def __next_entity(self):
        return self.entity_queue.pop(0)

    def thread_entity(self, entity, thread_id=0):
        self.logger.log("Filler {:>4} | {:>10}\n".format(thread_id, entity.id), end='')
        self.process_entity(entity)
        if self.entity_queue:
            self.thread_entity(self.__next_entity(), thread_id)

    def process(self):
        self.entity_queue = [v for _, v in self.entity_database.cache.items()]
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
