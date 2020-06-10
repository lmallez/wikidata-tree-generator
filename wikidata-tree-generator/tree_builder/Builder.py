#!/usr/bin/env python3
from wikidata.entity import Entity, EntityId
from logger.LoggerService import LoggerService


class Builder:
    def __init__(self, logger: LoggerService):
        self.logger = logger

    def get_property(self, entity: Entity, property_id: EntityId):
        if property_id not in entity.data['claims']:
            self.logger.log('{}: {} ({}) -> property {} not found'.format(self.__class__.__name__, entity.id, entity.label, property_id))
            raise
        return entity.data['claims'][property_id]