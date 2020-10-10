#!/usr/bin/env python3
from wikidata_tree_generator.configuration import ExportConfiguration
from wikidata_tree_generator.database import Database
from wikidata_tree_generator.logger import Logger, Color
from wikidata_tree_generator.macros import PropertyTag
from wikidata_tree_generator.macros.wikidata import Sex
from wikidata_tree_generator.models import Character


class ExportPropertyException(BaseException):
    pass


class Exporter:
    def __init__(self, database: Database, properties: list, configuration: ExportConfiguration, logger: Logger):
        self.database = database
        self.properties = properties
        self.configuration = configuration
        self.logger = logger

    def allow_export(self, character: Character) -> bool:
        if not character.has_property(PropertyTag.SEX):
            return True
        sex = character.get_property(PropertyTag.SEX).value
        return (sex == Sex.MALE and self.configuration.export_men) or (sex == Sex.FEMALE and self.configuration.export_women)

    def export(self, output_file: str):
        pass

    def log(self, entity_nbr: int, export_format: str, output_file: str):
        self.logger.log("{} : {} entities exported in {} to {}".format(self.__class__.__name__, entity_nbr, export_format, output_file), color=Color.HEADER)
