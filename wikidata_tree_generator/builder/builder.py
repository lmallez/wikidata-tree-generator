#!/usr/bin/env python3
from typing import Dict, Callable

from wikidata.entity import Entity as WikidataEntity, EntityId

from wikidata_tree_generator.logger import Logger
from .extractor import PropertyNotFoundException, extract_property
from ..macros.property_meta import PropertyMeta, ExtractType
from ..models import Entity
from ..models.property import Property


class Builder:
    def __init__(self, logger: Logger, properties=None, property_metas=None):
        if property_metas is None:
            property_metas = {}
        if properties is None:
            properties = []
        self.logger = logger
        self.properties = properties
        self.property_metas = property_metas

    # TODO : move to extractor ?
    @staticmethod
    def get_property(entity: WikidataEntity, property_id: EntityId):
        if property_id not in entity.data['claims']:
            raise PropertyNotFoundException()
        return entity.data['claims'][property_id]

    def extract_all(self, _, property_meta: PropertyMeta, wiki_properties) -> Property:
        return extract_property(property_meta, wiki_properties)

    def extract_single(self, entity: WikidataEntity, property_meta: PropertyMeta, wiki_properties) -> Property:
        # if len(wikidata_properties) == 0:
        #     raise PropertyNotFoundException(entity.id, property_meta.wikidata_id)
        if len(wiki_properties) > 1:
            self.logger.error('{}: {} -> has multiple {} ({})'.format(self.__class__.__name__, entity.id, property_meta.tag, property_meta.wikidata_id))
        # TODO : select the correct property to take
        return extract_property(property_meta, wiki_properties[0])

    def extract_multiple(self, _, property_meta: PropertyMeta, wiki_properties) -> [Property]:
        return [extract_property(property_meta, wiki_property) for wiki_property in wiki_properties]

    def extract_property(self, entity: WikidataEntity, property_meta: PropertyMeta):
        # if property_meta.value_type not in extract_property_methods.keys():
        #     raise
        wiki_properties = self.get_property(entity, property_meta.wikidata_id)
        if not wiki_properties:
            raise PropertyNotFoundException(entity.id, property_meta.wikidata_id)
        return extract_type_methods[property_meta.extract_type](self, entity, property_meta, wiki_properties)

    @staticmethod
    def create_new(entity: WikidataEntity) -> Entity:
        return Entity(entity.id, str(entity.label))

    def build(self, entity: WikidataEntity):
        build_entity = self.create_new(entity)
        for to_extract_property in self.properties:
            meta = self.property_metas[to_extract_property]
            try:
                build_entity.properties[to_extract_property] = self.extract_property(entity, meta)
            except PropertyNotFoundException:
                self.logger.error(
                    '{}: {} ({}) -> property {} ({}) not found'.format(
                        self.__class__.__name__, entity.id, entity.label, meta.tag, meta.wikidata_id)
                )
        return build_entity


extract_type_methods: Dict[ExtractType, Callable] = {
    ExtractType.ALL: Builder.extract_all,
    ExtractType.SINGLE: Builder.extract_single,
    ExtractType.MULTIPLE: Builder.extract_multiple,
}
