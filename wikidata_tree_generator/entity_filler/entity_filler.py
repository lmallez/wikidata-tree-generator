#!/usr/bin/env python3
from wikidata_tree_generator.builder.fetcher import PropertyFetcher
from wikidata_tree_generator.logger import Logger
from ..macros.property_meta import PropertyList, PropertyTag
from ..models.property import Property, PropertyToLoad
from ..models.entity import Entity


class EntityFiller:
    def __init__(self, logger: Logger, property_fetcher: PropertyFetcher, property_tags: [PropertyTag], property_metas: PropertyList):
        self.property_tags = property_tags
        self.logger = logger
        self.fetcher = property_fetcher
        self.property_metas = property_metas

    def load_property(self, meta, prop: PropertyToLoad):
        prop.value = self.fetcher.get(prop.loader, meta.value_type)

    def load_properties(self, meta, props: [Property]):
        for prop in props:
            self.load_property(meta, prop)

    def load(self, entity: Entity):
        for property_tag in self.property_tags:
            meta = self.property_metas[property_tag]
            if not meta.to_load or not entity.has_property(property_tag):
                continue
            prop = entity.get_property(property_tag)
            if meta.value_multiple:
                self.load_properties(meta, prop)
            else:
                self.load_property(meta, prop)
