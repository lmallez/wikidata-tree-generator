#!/usr/bin/env python3
from enum import Enum

wikidata_properties = {
    "sex": "P21",
    "father": "P22",
    "mother": "P25",
    "instance_of": "P31",
    "child": "P40",
    "family": "P53",
    "given_name": "P735",
    "family_name": "P734",
    "date_of_birth": "P569",
    "date_of_death": "P570",
    "place_of_birth": "P19",
    "place_of_death": "P20",
    "type_of_kinship": "P1039",
    "coordinate_location": "P625"
}

wikidata_entities = {
    "human": "Q5",
    "male": "Q6581097",
    "female": "Q6581072",
    "adopted": "Q20746725",
}


class Sex(Enum):
    MALE = 0
    FEMALE = 1
    UNDEFINED = 2
