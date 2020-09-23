#!/usr/bin/env python3
from wikidata.entity import Entity, EntityId
from wikidata_tree_generator.logger import Logger


class PropertyNotFoundException(BaseException):
    def __init__(self, entity_id: EntityId, property_id: EntityId):
        self.entity_id = entity_id
        self.property_id = property_id


class Builder:
    def __init__(self, logger: Logger):
        self.logger = logger

    def get_property(self, entity: Entity, property_id: EntityId):
        if property_id not in entity.data['claims']:
            self.logger.error('{}: {} ({}) -> property {} not found'.format(self.__class__.__name__, entity.id, entity.label, property_id))
            raise PropertyNotFoundException(entity.id, property_id)
        return entity.data['claims'][property_id]
