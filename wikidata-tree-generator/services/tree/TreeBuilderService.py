#!/usr/bin/env python3
from wikidata.entity import EntityId

from services.CharacterFetcherService import CharacterFetcherService
from services.tree.AncestorsTreeBuilderService import AncestorsTreeBuilderService
from services.tree.DescandantsTreeBuilderService import DescandantsTreeBuilderService


class TreeBuilderService:
    def __init__(self, fetcher: CharacterFetcherService,
                 a_tree_builder: AncestorsTreeBuilderService,
                 d_tree_builder: DescandantsTreeBuilderService):
        self.fetcher = fetcher
        self.loads_entities = []
        self.a_tree_builder = a_tree_builder
        self.d_tree_builder = d_tree_builder

    def build_tree(self, entity_id: EntityId):
        self.a_tree_builder.build_tree(entity_id)
        self.d_tree_builder.build_tree(entity_id)
