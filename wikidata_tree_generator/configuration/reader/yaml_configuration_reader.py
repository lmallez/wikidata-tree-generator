#!/usr/bin/env python3
import yaml
from wikidata_tree_generator.configuration import TreeMethod, ExportFormat, Configuration
from wikidata_tree_generator.models.character import Properties


class YamlConfigurationReaderException(Exception):
    pass


class YamlConfigurationReader:
    __str_tree_method = {
        "ANCESTORS": TreeMethod.ANCESTORS,
        "DESCENDANTS": TreeMethod.DESCENDANTS,
        "FULL": TreeMethod.FULL,
        "CLASSIC": TreeMethod.CLASSIC,
    }

    __str_export_format = {
        "GEDCOM": ExportFormat.GEDCOM,
        "JSON": ExportFormat.JSON
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
    def __configuration_exception(message: str) -> YamlConfigurationReaderException:
        return YamlConfigurationReaderException("{}: {}".format(YamlConfigurationReader.__name__, message))

    @staticmethod
    def load_config(config_path):
        with open(config_path, 'r') as stream:
            content = yaml.safe_load(stream)
        if not content['wikidata_to_gedcom']:
            raise YamlConfigurationReader.__configuration_exception('invalid configuration (wikidata_to_gedcom not found)')
        return content['wikidata_to_gedcom']

    def _content_get(self, names, types):
        content = self.content
        for name in names:
            if not name in content:
                return None
            content = content[name]
        if type(content) not in types:
            raise self.__configuration_exception("expected type(s) for '{}' : {} got '{}'".format('/'.join(names), [x.__name__ for x in types], type(content).__name__))
        return content

    def _content_get_raise(self, names, types):
        content = self._content_get(names, types)
        if content is None:
            raise self.__configuration_exception("'{}' cannot be null".format('/'.join(names)))
        return content

    def _content_get_default(self, names, types, default):
        content = self._content_get(names, types)
        if content is None:
            return default
        return content

    def create_configuration(self) -> Configuration:
        configuration = Configuration()
        configuration.entity_cache = self._content_get_default(['entity_cache'], [bool], True)

        method = self._content_get_raise(['tree', 'method'], [str])
        if method not in self.__str_tree_method.keys():
            raise self.__configuration_exception('tree method {} does not exist\n\t(methods available : {})'.format(method, ', '.join(self.__str_tree_method.keys())))
        configuration.tree_configuration.method = self.__str_tree_method[method]
        configuration.tree_configuration.generation_limit = self._content_get_default(['tree', 'generation_limit'], [int], 10)
        configuration.tree_configuration.load_fathers = self._content_get_default(['tree', 'load_fathers'], [bool], True)
        configuration.tree_configuration.load_mothers = self._content_get_default(['tree', 'load_mothers'], [bool], True)
        configuration.tree_configuration.load_men_children = self._content_get_default(['tree', 'load_men_children'], [bool], True)
        configuration.tree_configuration.load_women_children = self._content_get_default(['tree', 'load_women_children'], [bool], True)
        configuration.tree_configuration.branch_cache = self._content_get_default(['tree', 'branch_cache'], [bool], True)

        configuration.thread_configuration.enable = self._content_get_default(['thread', 'enable'], [bool], False)
        if configuration.thread_configuration.enable:
            configuration.thread_configuration.max_thread = self._content_get_default(['thread', 'max'], [int], 10)

        export_format = self._content_get_raise(['export', 'format'], [str])
        if export_format not in self.__str_export_format.keys():
            raise self.__configuration_exception('export format {} does not exist\n\t(formats available : {})'.format(export_format, ', '.join(self.__str_export_format.keys())))
        configuration.export_configuration.format = self.__str_export_format[export_format]
        configuration.export_configuration.export_men = self._content_get_default(['export', 'export_men'], [bool], True)
        configuration.export_configuration.export_women = self._content_get_default(['export', 'export_women'], [bool], True)

        character_properties = self._content_get_default(['properties'], [list], [])
        configuration.properties = []
        for character_property in character_properties:
            if not isinstance(character_property, str) or (character_property not in self.__str_properties.keys()):
                raise self.__configuration_exception("character_property '{}' does not exist\n\t(properties available : {})".format(character_property, ', '.join(self.__str_properties.keys())))
            configuration.properties.append(self.__str_properties[character_property])

        return configuration
