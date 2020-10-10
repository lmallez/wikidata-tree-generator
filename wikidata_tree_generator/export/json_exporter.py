#!/usr/bin/env python3
import json
from json import JSONEncoder
from typing import Dict, Callable

from wikidata.multilingual import MultilingualText
from .exporter import Exporter, ExportPropertyException
from ..macros.export.json import json_property_tag_str
from ..macros.property_meta import PropertyMeta, character_property_metas, property_metas_by_type
from ..macros.wikidata import Sex
from ..models import Character, Place, Name, Date
from ..models.entity import EntityException
from ..models.place import CoordinateLocation
from ..models.property import Property, PropertyToLoad


class MultilingualEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, MultilingualText):
            return str(o)
        return o.__dict__


class JsonExporter(Exporter):
    @staticmethod
    def export_sex(prop: Property):
        if prop.value == Sex.UNDEFINED:
            raise ExportPropertyException()
        return {Sex.MALE: 'male', Sex.FEMALE: 'female'}[prop.value]

    @staticmethod
    def export_value(prop: Property):
        return prop.value

    @staticmethod
    def export_loader(prop: PropertyToLoad):
        return prop.loader

    @staticmethod
    def export_multiple_value(props: [Property]):
        return [JsonExporter.export_value(prop) for prop in props]

    @staticmethod
    def export_multiple_loader(props: [Property]):
        return [JsonExporter.export_loader(prop) for prop in props]

    @staticmethod
    def export_entity(prop: [Property]):
        entity = prop.value
        export_character = {'id': entity.id, 'label': entity.label}
        if len(entity.properties.items()) > 0:
            export_character['properties'] = {}
            for tag, entity_property in entity.properties.items():
                if not entity_property or type(prop.value) not in property_metas_by_type.keys():
                    continue
                export_character['properties'][json_property_tag_str[tag]] = JsonExporter.export_property(entity_property, property_metas_by_type[type(prop.value)][tag])
        return export_character

    @staticmethod
    def export_property(prop: [Property], meta: PropertyMeta):
        method = json_export_by_type[meta.value_type]
        if meta.value_multiple:
            return [method(p) for p in prop]
        return method(prop)

    def get_exportable_character(self, character: Character) -> dict:
        export_character = {'id': character.id, 'label': character.label}
        for property_tag in self.properties:
            try:
                meta = character_property_metas[property_tag]
                export_character[json_property_tag_str[property_tag]] = self.export_property(character.get_property(property_tag), meta)
            except EntityException:
                self.logger.error('{}: {} is impossible to export'.format(self.__class__.__name__, property_tag))
        return export_character

    def export(self, output_file: str):
        export_characters = dict(filter(lambda x: self.allow_export(x[1]), self.database.cache.items()))
        export_characters = {key: self.get_exportable_character(character) for key, character in export_characters.items()}
        file = open(output_file, "w+")
        json.dump(export_characters, file, cls=MultilingualEncoder, indent=4)
        file.close()
        self.log(len(export_characters), 'JSON', output_file)


json_export_by_type: Dict[type, Callable] = {
    bool: JsonExporter.export_value,
    Sex: JsonExporter.export_sex,
    Date: JsonExporter.export_value,
    Character: JsonExporter.export_loader,
    Place: JsonExporter.export_entity,
    Name: JsonExporter.export_entity,
    CoordinateLocation: JsonExporter.export_value,
}
