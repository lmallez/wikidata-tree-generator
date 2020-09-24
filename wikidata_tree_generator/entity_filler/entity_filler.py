from typing import Dict

from wikidata_tree_generator.builder.fetcher.property_fetcher import PropertyFetcher
from wikidata_tree_generator.logger import Logger
from wikidata_tree_generator.macros.character_properties import PropertyToLoad, Property, PropertyMeta
from wikidata_tree_generator.models import Entity, Properties


class EntityFiller:
    def __init__(self, logger: Logger, property_fetcher: PropertyFetcher, properties: [Properties], property_metas: Dict[Properties, PropertyMeta]):
        self.properties = properties
        self.logger = logger
        self.fetcher = property_fetcher
        self.property_metas = property_metas

    def load_property(self, meta, prop: PropertyToLoad):
        prop.value = self.fetcher.get(prop.loader, meta.value_type)

    def load_properties(self, meta, props: [Property]):
        for prop in props:
            self.load_property(meta, prop)

    def load(self, entity: Entity):
        for property_tag in self.properties:
            meta = self.property_metas[property_tag]
            if not meta.to_load or not entity.has_property(property_tag):
                continue
            prop = entity.get_property(property_tag)
            if meta.value_multiple:
                self.load_properties(meta, prop)
            else:
                self.load_property(meta, prop)
