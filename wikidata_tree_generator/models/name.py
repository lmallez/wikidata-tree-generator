#!/usr/bin/env python3
from dataclasses import dataclass
from wikidata.entity import EntityId


@dataclass
class Name:
    id: EntityId
    name: str = None
