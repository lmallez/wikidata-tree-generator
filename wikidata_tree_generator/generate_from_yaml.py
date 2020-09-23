#!/usr/bin/env python3
import sys

from wikidata.entity import EntityId
from wikidata_tree_generator.configuration.reader import YamlConfigurationReader
from wikidata_tree_generator.launcher_creator import LauncherCreator


def generate_from_yaml(configuration_path: str, entity_id: EntityId, output_path: str):
    try:
        configuration = YamlConfigurationReader(configuration_path).create_configuration()
        module = LauncherCreator(configuration)
        launcher = module.get_launcher()
        launcher.execute(entity_id, output_path)
    except YamlConfigurationReaderException as exception:
        print(exception, file=sys.stderr)
