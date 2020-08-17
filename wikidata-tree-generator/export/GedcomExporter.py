#!/usr/bin/env python3
from datetime import datetime
from typing import Union

from gedcom.element.element import Element

from Configuration import ExportConfiguration
from Database import Database
from export.Exporter import Exporter
from logger.Logger import Logger
from macros.WikidataProperties import Sex
from models.CharacterEntity import CharacterEntity, Properties
from models.Date import Date
from models.Place import Place

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


def create_gedcom_date(date: Date) -> Union[GedcomDate, GedcomBetweenDate]:
    if date.precision < 6 or date.precision > 11:
        raise
    return [
        lambda x: create_between_gedcom_date(int(x[1:5]), 1000, offset=1),
        lambda x: create_between_gedcom_date(int(x[1:5]), 100, offset=1),
        lambda x: create_between_gedcom_date(int(x[1:5]), 10),
        lambda x: GedcomDate(int(x[1:5]), int(x[6:8])),
        lambda x: GedcomDate(int(x[1:5]), int(date.time[6:8]), int(date.time[9:11])),
    ][date.precision - 7](date.time)


class GedcomExporter(Exporter):
    class Family:
        def __init__(self, family_id):
            self.id = family_id
            self.children_ids = []
            self.father_id = None
            self.mother_id = None

    def __init__(self, database: Database, properties: list, configuration: ExportConfiguration, logger: Logger):
        super().__init__(database, properties, configuration, logger)
        self.elements = {}
        self.families = {}

    def create_character_element(self, character: CharacterEntity):
        element = Element(0, '@{}@'.format(character.id), 'INDI', '')
        element.new_child_element('NAME', '', str(character[Properties.LABEL]))
        for field in self.properties:
            if field in field_method.keys():
                try:
                    field_method[field](self, character, element)
                except:
                    self.logger.error('{}: {} is impossible to export'.format(self.__class__.__name__, field))
        self.create_family(character)
        self.elements[character.id] = element

    @staticmethod
    def get_create_child_by_tag(element: Element, tag: str):
        childs = element.get_child_elements()
        for child in childs:
            if child.get_tag() == tag:
                return child
        return element.new_child_element(tag)

    def export_sex(self, character: CharacterEntity, element: Element):
        sex = character.get_property(Properties.SEX)
        if sex != Sex.UNDEFINED:
            element.new_child_element('SEX', '', ['M', 'F'][sex])

    def export_date_birth(self, character: CharacterEntity, element: Element):
        birth = character.get_property(Properties.DATE_BIRTH)
        if birth is None:
            raise
        birth_element = self.get_create_child_by_tag(element, 'BIRT')
        birth_element.new_child_element('DATE', '', str(create_gedcom_date(birth)))

    def export_date_death(self, character: CharacterEntity, element: Element):
        death = character.get_property(Properties.DATE_DEATH)
        if death is None:
            raise
        death_element = self.get_create_child_by_tag(element, 'DEAT')
        death_element.new_child_element('DATE', '', str(create_gedcom_date(death)))

    def export_place_birth(self, character: CharacterEntity, element: Element):
        place_birth = character.get_property(Properties.PLACE_BIRTH)
        if place_birth is None:
            raise
        birth_element = self.get_create_child_by_tag(element, 'BIRT')
        self.__export_place(place_birth, birth_element)

    def export_place_death(self, character: CharacterEntity, element: Element):
        place_death = character.get_property(Properties.PLACE_DEATH)
        if place_death is None:
            raise
        death_element = self.get_create_child_by_tag(element, 'DEAT')
        self.__export_place(place_death, death_element)

    @staticmethod
    def __export_place(place: Place, event: Element):
        plac_element = event.new_child_element('PLAC', '', place.name)
        map_element = plac_element.new_child_element('MAP')
        map_element.new_child_element('LATI', '',
                                      '{}{}'.format('N' if place.latitude > 0 else 'S', abs(place.latitude)))
        map_element.new_child_element('LONG', '',
                                      '{}{}'.format('E' if place.longitude > 0 else 'W', abs(place.longitude)))

    def export_given_name(self, character: CharacterEntity, element: Element):
        givens = character.get_property(Properties.GIVEN_NAME)
        if givens is None:
            raise
        name_element = self.get_create_child_by_tag(element, 'NAME')
        name_element.new_child_element('GIVN', '', ' '.join([given.name for given in givens]))

    def export_family_name(self, character: CharacterEntity, element: Element):
        families = character.get_property(Properties.FAMILY_NAME)
        if families is None:
            raise
        name_element = self.get_create_child_by_tag(element, 'NAME')
        name_element.new_child_element('SURN', '', ' '.join([family.name for family in families]))

    def create_family(self, character: CharacterEntity):
        if not character.has_property(Properties.MOTHER_ID) and not character.has_property(Properties.FATHER_ID):
            return
        family_id = '{}//{}'.format(
            character.get_property(Properties.MOTHER_ID) if character.has_property(Properties.MOTHER_ID) else "",
            character.get_property(Properties.FATHER_ID) if character.has_property(Properties.FATHER_ID) else ""
        )
        if family_id in self.families.keys():
            self.families[family_id].children_ids.append(character.id)
        else:
            family = self.Family('FAM{}'.format(len(self.families.keys())))
            if character.has_property(Properties.MOTHER_ID) and character.get_property(
                    Properties.MOTHER_ID) in self.database.cache.keys():
                family.mother_id = character.get_property(Properties.MOTHER_ID)
            if character.has_property(Properties.FATHER_ID) and character.get_property(
                    Properties.FATHER_ID) in self.database.cache.keys():
                family.father_id = character.get_property(Properties.FATHER_ID)
            family.children_ids.append(character.id)
            self.families[family_id] = family

    def create_family_element(self, family: Family):
        element = Element(0, '@{}@'.format(family.id), 'FAM', '')
        if family.father_id and family.father_id in self.elements.keys():
            element.new_child_element('HUSB', '', '@{}@'.format(family.father_id))
            self.elements[family.father_id].new_child_element('FAMS', '', '@{}@'.format(family.id))
        if family.mother_id and family.mother_id in self.elements.keys():
            element.new_child_element('WIFE', '', '@{}@'.format(family.mother_id))
            self.elements[family.mother_id].new_child_element('FAMS', '', '@{}@'.format(family.id))
        for child_id in family.children_ids:
            if child_id in self.database.cache.keys():
                element.new_child_element('CHIL', '', '@{}@'.format(child_id))
                self.elements[child_id].new_child_element('FAMC', '', '@{}@'.format(family.id))
        self.elements[family.id] = element

    def print_element(self, file, element: Element, depth=0):
        a = element.to_gedcom_string()
        file.write(a)
        for child in element.get_child_elements():
            self.print_element(file, child, depth=depth + 1)

    def write_gedcom(self, output_file, elements):
        f = open(output_file, "w+", encoding="utf8")
        dt = datetime.now()
        f.write(HEADER.format(
            dt.strftime("%d %b %Y"),
            dt.strftime("%H:%M:%S"),
            output_file
        ))
        for element in elements:
            self.print_element(f, element)
        f.write(FOOTER)
        f.close()

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


field_method = {
    Properties.SEX: GedcomExporter.export_sex,
    Properties.DATE_BIRTH: GedcomExporter.export_date_birth,
    Properties.DATE_DEATH: GedcomExporter.export_date_death,
    Properties.GIVEN_NAME: GedcomExporter.export_given_name,
    Properties.FAMILY_NAME: GedcomExporter.export_family_name,
    Properties.PLACE_BIRTH: GedcomExporter.export_place_birth,
    Properties.PLACE_DEATH: GedcomExporter.export_place_death,
}
