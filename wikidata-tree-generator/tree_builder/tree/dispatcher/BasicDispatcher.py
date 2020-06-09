#!/usr/bin/env python3
from wikidata.entity import EntityId

from tree_builder.tree.dispatcher.Dispatcher import Dispatcher


class BasicDispatcher(Dispatcher):
    def compute(self, entity_ids: [EntityId], method, prof=0, branch=0):
        for entity_id in entity_ids:
            method(entity_id, prof, branch)
            branch += 1
