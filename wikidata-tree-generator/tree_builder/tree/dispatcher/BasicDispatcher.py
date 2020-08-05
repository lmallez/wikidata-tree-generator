#!/usr/bin/env python3
from wikidata.entity import EntityId

from tree_builder.tree.dispatcher.Dispatcher import Dispatcher


class BasicDispatcher(Dispatcher):
    def compute(self, entity_ids: [EntityId], method, depth=0):
        for entity_id in entity_ids:
            method(entity_id, depth)
