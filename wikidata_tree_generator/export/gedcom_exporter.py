#!/usr/bin/env python3
from dataclasses import dataclass, field
from datetime import datetime
from typing import Union
from gedcom.element.element import Element
from wikidata_tree_generator.configuration import ExportConfiguration
from wikidata_tree_generator.database import Database
from wikidata_tree_generator.logger import Logger
from wikidata_tree_generator.macros.wikidata import Sex
from wikidata_tree_generator.models import Place, Date, Character
from .exporter import ExportPropertyException, Exporter
from ..macros import PropertyTag
from ..models.entity import EntityException

HEADER = '0 HEAD\n1 SOUR Wikidata to Gedcom\n2 VERS 5.1.1\n2 NAME Wikidata to Gedcom\n1 DATE {}\n2 TIME {}\n1 SUBM @SUBM@\n1 FILE {}\n1 GEDC\n2 VERS 5.5.1\n2 FORM LINEAGE-LINKED\n1 CHAR UTF-8\n1 LANG English\n0 @SUBM@ SUBM\n1 NAME\n1 ADDR\n'

FOOTER = '0 TRLR\n'


class GedcomDate:
    # TODO : complete class
    def __init__(self, year: int, month=None, day=None) -> None:
        self.year = year
        self.month = month
        self.day = day

    gedcom_month = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']

    def __str__(self) -> str:
        string = ''
        if self.day:
            string += str(self.day) + ' '
        if self.month and self.month > 0:
            string += self.gedcom_month[self.month - 1] + ' '
        return string + str(self.year)


class GedcomBetweenDate:
    def __init__(self, start, stop):
        self.start = start
        self.stop = stop

    def __str__(self) -> str:
        return 'BET {} AND {}'.format(str(self.start), str(self.stop))


def create_between_gedcom_date(year, around, offset=0):
    year = int(year / around) * around + offset
    return GedcomBetweenDate(GedcomDate(year), GedcomDate(year + around - 1))


class GedcomDateException(BaseException):
    pass


def create_gedcom_date(date: Date) -> Union[GedcomDate, GedcomBetweenDate]:
    if date.precision < 6 or date.precision > 11:
        raise GedcomDateException()
    return [
        lambda x: create_between_gedcom_date(int(x[1:5]), 1000, offset=1),
        lambda x: create_between_gedcom_date(int(x[1:5]), 100, offset=1),
        lambda x: create_between_gedcom_date(int(x[1:5]), 10),
        lambda x: GedcomDate(int(x[1:5]), int(x[6:8])),
        lambda x: GedcomDate(int(x[1:5]), int(date.time[6:8]), int(date.time[9:11])),
    ][date.precision - 7](date.time)


class GedcomExporter(Exporter):
    @dataclass()
    class Family:
        family_id: str
        children_ids: list = field(default_factory=list)
        father_id: int = None
        mother_id: int = None

    def __init__(self, database: Database, properties: list, configuration: ExportConfiguration, logger: Logger):
        super().__init__(database, properties, configuration, logger)
        self.elements = {}
        self.families = {}
        for property_tag in self.properties:
            if property_tag not in export_gedcom_property_methods.keys():
                self.properties.remove(property_tag)
                self.logger.error('{}: Property {} cannot and will not be exported'.format(self.__class__.__name__, property_tag))

    def create_character_element(self, character: Character):
        element = Element(0, '@{}@'.format(character.id), 'INDI', '')
        element.new_child_element('NAME', '', str(character.label))
        for property_tag in self.properties:
            try:
                export_gedcom_property_methods[property_tag](self, character, element)
            except (ExportPropertyException, EntityException):
                self.logger.error('{}: {} is impossible to export'.format(self.__class__.__name__, property_tag))
        self.create_family(character)
        self.elements[character.id] = element

    @staticmethod
    def get_create_child_by_tag(element: Element, tag: str):
        childs = element.get_child_elements()
        for child in childs:
            if child.get_tag() == tag:
                return child
        return element.new_child_element(tag)

    def export_sex(self, character: Character, element: Element):
        sex = character.get_property(PropertyTag.SEX).value
        if sex != Sex.UNDEFINED:
            element.new_child_element('SEX', '', {Sex.MALE: 'M', Sex.FEMALE: 'F'}[sex])

    def export_date_birth(self, character: Character, element: Element):
        birth = character.get_property(PropertyTag.DATE_BIRTH).value
        if birth is None:
            raise ExportPropertyException()
        birth_element = self.get_create_child_by_tag(element, 'BIRT')
        birth_element.new_child_element('DATE', '', str(create_gedcom_date(birth)))

    def export_date_death(self, character: Character, element: Element):
        death = character.get_property(PropertyTag.DATE_DEATH).value
        if death is None:
            raise ExportPropertyException()
        death_element = self.get_create_child_by_tag(element, 'DEAT')
        death_element.new_child_element('DATE', '', str(create_gedcom_date(death)))

    def export_place_birth(self, character: Character, element: Element):
        place_birth = character.get_property(PropertyTag.PLACE_BIRTH)
        if place_birth is None:
            raise ExportPropertyException()
        birth_element = self.get_create_child_by_tag(element, 'BIRT')
        self.__export_place(place_birth.value, birth_element)

    def export_place_death(self, character: Character, element: Element):
        place_death = character.get_property(PropertyTag.PLACE_DEATH)
        if place_death is None:
            raise ExportPropertyException()
        death_element = self.get_create_child_by_tag(element, 'DEAT')
        self.__export_place(place_death.value, death_element)

    @staticmethod
    def __export_place(place: Place, event: Element):
        plac_element = event.new_child_element('PLAC', '', place.label)
        coordinates = place.get_property(PropertyTag.COORDINATE_LOCATION).value
        if coordinates.latitude and coordinates.longitude:
            map_element = plac_element.new_child_element('MAP')
            map_element.new_child_element('LATI', '', '{}{}'.format('N' if coordinates.latitude > 0 else 'S', abs(coordinates.latitude)))
            map_element.new_child_element('LONG', '', '{}{}'.format('E' if coordinates.longitude > 0 else 'W', abs(coordinates.longitude)))

    def export_given_name(self, character: Character, element: Element):
        givens = character.get_property(PropertyTag.GIVEN_NAME)
        if givens is None:
            raise ExportPropertyException()
        name_element = self.get_create_child_by_tag(element, 'NAME')
        name_element.new_child_element('GIVN', '', ' '.join([given.value.label for given in givens]))

    def export_family_name(self, character: Character, element: Element):
        families = character.get_property(PropertyTag.FAMILY_NAME)
        if families is None:
            raise ExportPropertyException()
        name_element = self.get_create_child_by_tag(element, 'NAME')
        name_element.new_child_element('SURN', '', ' '.join([family.value.label for family in families]))

    def create_family(self, character: Character):
        if not character.has_property(PropertyTag.MOTHER) and not character.has_property(PropertyTag.FATHER):
            return
        family_id = '{}//{}'.format(
            character.get_property(PropertyTag.MOTHER) if character.has_property(PropertyTag.MOTHER) else "",
            character.get_property(PropertyTag.FATHER) if character.has_property(PropertyTag.FATHER) else ""
        )
        if family_id in self.families.keys():
            self.families[family_id].children_ids.append(character.id)
        else:
            family = self.Family('FAM{}'.format(len(self.families.keys())))
            if character.has_property(PropertyTag.MOTHER) and character.get_property(
                    PropertyTag.MOTHER).loader in self.database.cache.keys():
                family.mother_id = character.get_property(PropertyTag.MOTHER).loader
            if character.has_property(PropertyTag.FATHER) and character.get_property(
                    PropertyTag.FATHER).loader in self.database.cache.keys():
                family.father_id = character.get_property(PropertyTag.FATHER).loader
            family.children_ids.append(character.id)
            self.families[family_id] = family

    def create_family_element(self, family: Family):
        element = Element(0, '@{}@'.format(family.family_id), 'FAM', '')
        if family.father_id and family.father_id in self.elements.keys():
            element.new_child_element('HUSB', '', '@{}@'.format(family.father_id))
            self.elements[family.father_id].new_child_element('FAMS', '', '@{}@'.format(family.family_id))
        if family.mother_id and family.mother_id in self.elements.keys():
            element.new_child_element('WIFE', '', '@{}@'.format(family.mother_id))
            self.elements[family.mother_id].new_child_element('FAMS', '', '@{}@'.format(family.family_id))
        for child_id in family.children_ids:
            if child_id in self.database.cache.keys():
                element.new_child_element('CHIL', '', '@{}@'.format(child_id))
                self.elements[child_id].new_child_element('FAMC', '', '@{}@'.format(family.family_id))
        self.elements[family.family_id] = element

    def print_element(self, file, element: Element, depth=0):
        gedcom_string = element.to_gedcom_string()
        file.write(gedcom_string)
        for child in element.get_child_elements():
            self.print_element(file, child, depth=depth + 1)

    def write_gedcom(self, output_file, elements):
        file = open(output_file, "w+", encoding="utf8")
        time = datetime.now()
        file.write(HEADER.format(
            time.strftime("%d %b %Y"),
            time.strftime("%H:%M:%S"),
            output_file
        ))
        for element in elements:
            self.print_element(file, element)
        file.write(FOOTER)
        file.close()

    def export(self, output_file: str):
        character_nbr = 0
        for character in self.database.cache.values():
            if self.allow_export(character):
                self.create_character_element(character)
                character_nbr += 1
        for family in self.families.values():
            self.create_family_element(family)
        self.write_gedcom(output_file, self.elements.values())
        self.elements = {}
        self.families = {}
        self.log(character_nbr, 'GEDCOM', output_file)


# TODO : replace this by a more abstract thing
export_gedcom_property_methods = {
    PropertyTag.SEX: GedcomExporter.export_sex,
    PropertyTag.DATE_BIRTH: GedcomExporter.export_date_birth,
    PropertyTag.DATE_DEATH: GedcomExporter.export_date_death,
    PropertyTag.GIVEN_NAME: GedcomExporter.export_given_name,
    PropertyTag.FAMILY_NAME: GedcomExporter.export_family_name,
    PropertyTag.PLACE_BIRTH: GedcomExporter.export_place_birth,
    PropertyTag.PLACE_DEATH: GedcomExporter.export_place_death,
}
