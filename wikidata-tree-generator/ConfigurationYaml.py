#!/usr/bin/env python3
import yaml

from Configuration import Configuration, TreeMethod, ExportFormat
from models.CharacterEntity import Properties


class ConfigurationYaml:
    __str_tree_method = {
        "ANCESTORS": TreeMethod.ANCESTORS,
        "DESCENDANTS": TreeMethod.DESCENDANTS,
        "FULL": TreeMethod.FULL,
        "CLASSIC": TreeMethod.CLASSIC,
    }

    __str_export_format = {
        "GEDCOM": ExportFormat.GEDCOM,
    }

    __str_properties = {
        "DATE_DEATH": Properties.DATE_DEATH,
        "DATE_BIRTH": Properties.DATE_BIRTH,
        "FAMILY_NAME": Properties.FAMILY_NAME,
        "GIVEN_NAME": Properties.GIVEN_NAME,
        "IS_HUMAN": Properties.IS_HUMAN,
        "PLACE_BIRTH": Properties.PLACE_BIRTH,
        "PLACE_DEATH": Properties.PLACE_DEATH,
        "SEX": Properties.SEX,
    }

    def __init__(self, config_path: str):
        self.config_path = config_path
        self.content = self.load_config(config_path)

    @staticmethod
    def load_config(config_path):
        with open(config_path, 'r') as stream:
            content = yaml.safe_load(stream)
        if not content['wikidata_to_gedcom']:
            raise
        return content['wikidata_to_gedcom']

    def _content_get(self, names, types):
        content = self.content
        for name in names:
            if not name in content:
                return None
            content = content[name]
        if type(content) not in types:
            raise
        return content

    def _content_get_raise(self, names, types):
        content = self._content_get(names, types)
        if content is None:
            raise
        return content

    def _content_get_default(self, names, types, default):
        content = self._content_get(names, types)
        if content is None:
            return default
        return content

    def create_configuration(self) -> Configuration:
        configuration = Configuration()
        method = self._content_get_raise(['tree', 'method'], [str])
        if method not in self.__str_tree_method.keys():
            raise
        configuration.tree_configuration.method = self.__str_tree_method[method]
        configuration.tree_configuration.generation_limit = self._content_get_default(['tree', 'generation_limit'], [int], 10)
        configuration.tree_configuration.load_fathers = self._content_get_default(['tree', 'load_fathers'], [bool], True)
        configuration.tree_configuration.load_mothers = self._content_get_default(['tree', 'load_mothers'], [bool], True)
        configuration.tree_configuration.load_men_children = self._content_get_default(['tree', 'load_men_children'], [bool], True)
        configuration.tree_configuration.load_women_children = self._content_get_default(['tree', 'load_women_children'], [bool], True)

        configuration.thread_configuration.enable = self._content_get_default(['thread', 'enable'], [bool], False)
        if configuration.thread_configuration.enable:
            configuration.thread_configuration.max_thread = self._content_get_default(['thread', 'max'], [int], 10)

        format = self._content_get_raise(['export', 'format'], [str])
        if format not in self.__str_export_format.keys():
            raise
        configuration.export_configuration.format = self.__str_export_format[format]
        configuration.export_configuration.export_men = self._content_get_default(['export', 'export_men'], [bool], True)
        configuration.export_configuration.export_women = self._content_get_default(['export', 'export_women'], [bool], True)

        properties = self._content_get_default(['properties'], [list], [])
        configuration.properties = []
        for property in properties:
            if (type(property) is not str) or (property not in self.__str_properties.keys()):
                raise
            configuration.properties.append(self.__str_properties[property])

        return configuration
