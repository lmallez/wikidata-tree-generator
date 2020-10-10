#!/usr/bin/env python3
from wikidata_tree_generator.configuration import TreeMethod, ExportFormat
from wikidata_tree_generator.macros.property import PropertyTag

# TODO : replace with configuration files

yaml_tree_method = {
    "ANCESTORS": TreeMethod.ANCESTORS,
    "DESCENDANTS": TreeMethod.DESCENDANTS,
    "FULL": TreeMethod.FULL,
    "CLASSIC": TreeMethod.CLASSIC,
}

yaml_export_format = {
    "GEDCOM": ExportFormat.GEDCOM,
    "JSON": ExportFormat.JSON,
}

yaml_property_tag = {
    "DATE_DEATH": PropertyTag.DATE_DEATH,
    "DATE_BIRTH": PropertyTag.DATE_BIRTH,
    "FAMILY_NAME": PropertyTag.FAMILY_NAME,
    "GIVEN_NAME": PropertyTag.GIVEN_NAME,
    "IS_HUMAN": PropertyTag.IS_HUMAN,
    "PLACE_BIRTH": PropertyTag.PLACE_BIRTH,
    "PLACE_DEATH": PropertyTag.PLACE_DEATH,
    "SEX": PropertyTag.SEX,
}
