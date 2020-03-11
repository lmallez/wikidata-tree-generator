#!/usr/bin/env python3

from wikidata.client import Client
from wikidata.entity import EntityId, Entity


class WikidataFetcherService(Client):
    def get(self, entity_id: EntityId, load: bool = True) -> Entity:
        return super().get(entity_id, load)
