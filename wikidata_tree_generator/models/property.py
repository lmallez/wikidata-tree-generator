#!/usr/bin/env python3
from dataclasses import dataclass

from wikidata.entity import EntityId


@dataclass
class Property:
    value: object
    to_load = False
    sources = None


@dataclass
class PropertyToLoad:
    loader: EntityId
    value: object = None
    to_load = True
