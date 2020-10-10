#!/usr/bin/env python3
from dataclasses import field, dataclass

from wikidata.entity import EntityId

from wikidata_tree_generator.macros import PropertyTag


class EntityException(BaseException):
    pass


@dataclass
class Entity:
    id: EntityId
    label: str
    properties: dict = field(default_factory=dict)
    PROPERTIES = []

    def has_property(self, entity_property: PropertyTag):
        return entity_property in self.properties.keys()

    def get_property(self, entity_property: PropertyTag):
        if not self.has_property(entity_property):
            raise EntityException()
        return self.properties[entity_property]
