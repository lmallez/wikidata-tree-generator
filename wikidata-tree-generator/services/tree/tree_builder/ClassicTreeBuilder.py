#!/usr/bin/env python3
from wikidata.entity import EntityId

from services.ConfigService import ConfigService
from services.tree.dispatcher.Dispatcher import Dispatcher
from services.tree.tree_builder.AncestorsTreeBuilder import AncestorsTreeBuilder
from services.tree.tree_builder.DescandantsTreeBuilder import DescendantsTreeBuilder


class ClassicTreeBuilder:
    def __init__(self, ancestors_builder: AncestorsTreeBuilder, descendants_builder: DescendantsTreeBuilder):
        self.ancestors = ancestors_builder
        self.descendants = descendants_builder

    def compute(self, entity_id: EntityId):
        self.ancestors.compute(entity_id)
        self.descendants.compute(entity_id)
