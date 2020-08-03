#!/usr/bin/env python3
from Configuration import ExportConfiguration
from Database import Database
from logger import Logger
from macros.WikidataProperties import Sex
from models.CharacterEntity import Properties, CharacterEntity


class Exporter:
    def __init__(self, database: Database, properties: list, configuration: ExportConfiguration, logger: Logger):
        self.database = database
        self.properties = properties
        self.configuration = configuration
        self.logger = logger

    def allow_export(self, character: CharacterEntity) -> bool:
        if not character.has_property(Properties.SEX):
            return True
        sex = character.get_property(Properties.SEX)
        return (sex == Sex.MALE and self.configuration.export_men) or (sex == Sex.FEMALE and self.configuration.export_women)

    def export(self, output_file: str):
        pass
