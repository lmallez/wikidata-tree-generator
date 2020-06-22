#!/usr/bin/env python3
from threading import Thread

from Config import Config
from Database import Database
from WikidataFetcher import WikidataFetcher
from entity_filler.EntityFiller import EntityFiller
from logger.Logger import Logger, Color
from tree_builder.PlacerBuilder import PlaceBuilder


class ThreadedEntityFiller(EntityFiller):
    def __init__(self, config: Config, entity_database: Database, place_database: Database,
                 wikidata: WikidataFetcher, place_builder: PlaceBuilder, logger: Logger):
        super().__init__(config, entity_database, place_database, wikidata, place_builder, logger)
        self.entity_queue = []
        self.logger = logger

    def __next_entity(self):
        return self.entity_queue.pop(0)

    def thread_entity(self, entity, thread_id=0):
        self.logger.log("Filler {} | {:>10}".format(thread_id, entity.id))
        self.process_entity(entity)
        if self.entity_queue:
            self.thread_entity(self.__next_entity(), thread_id)

    def process(self):
        self.entity_queue = [v for _, v in self.entity_database.cache.items()]
        threads = []
        for i in range(0, self.config.max_thread):
            if not self.entity_queue:
                break
            threads.append(Thread(target=self.thread_entity, args=[self.__next_entity(), i]))
        self.logger.log("ThreadedEntityFiller : {}/{} threads created, {} entities left".format(
            len(threads), self.config.max_thread, len(self.entity_queue)), Color.HEADER)
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
