#!/usr/bin/env python3
import sys
from wikidata.entity import EntityId
from wikidata_tree_generator.generate_from_yaml import generate_from_yaml

if __name__ == '__main__':
    generate_from_yaml(sys.argv[1], EntityId(sys.argv[2]), sys.argv[3])
