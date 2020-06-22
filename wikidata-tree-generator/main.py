#!/usr/bin/env python3
import sys
from wikidata.entity import EntityId
from ConfigurationYaml import ConfigurationYaml
from MainModule import MainModule

if __name__ == '__main__':
    configuration = ConfigurationYaml(sys.argv[1]).create_configuration()
    module = MainModule(configuration)
    launcher = module.get_generator()
    launcher.execute(EntityId(sys.argv[2]), sys.argv[3])
