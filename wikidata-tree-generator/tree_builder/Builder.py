#!/usr/bin/env python3
from wikidata.entity import Entity, EntityId
from logger.Logger import Logger


class Builder:
    def __init__(self, logger: Logger):
        self.logger = logger

    def get_property(self, entity: Entity, property_id: EntityId):
        if property_id not in entity.data['claims']:
            self.logger.error(
                '{}: {} ({}) -> property {} not found'.format(self.__class__.__name__, entity.id, entity.label,
                                                              property_id))
            raise
        return entity.data['claims'][property_id]
