import datetime
import json
import logging
from collections.abc import MutableSequence
from decimal import Decimal
from pathlib import Path
from types import MappingProxyType as MPT
from typing import Literal, Mapping, overload

from lxml import etree

from . import enums as e
from . import typedefs as t

ROOT_PATH = Path(__file__).parent.parent
NS = MPT({None: "http://otds-group.org/otds"})
PREFIX = "{http://otds-group.org/otds}"

def validate(xml_path: Path, xsd_path: Path) -> etree._ElementTree:
    xml_doc = etree.parse(xml_path)

    if __debug__:
        xmlschema_doc = etree.parse(xsd_path)
        xmlschema = etree.XMLSchema(xmlschema_doc)
        if not xmlschema.validate(xml_doc):
            raise ValueError(xmlschema.error_log.last_error)  # type: ignore[attr-defined]

    return xml_doc

_COMPONENT_NAME_LOOKUP = MPT({
    e.ProductType.AccommodationOnly: "Accommodation",
    e.ProductType.OnewayFlightOnly: "OnewayFlight",
    e.ProductType.ReturnFlightOnly: "ReturnFlight",
    e.ProductType.FlightAccommodation: "CombiComponent",
    e.ProductType.Addon: "Addon"
})
_NAME_COMPONENT_LOOKUP = MPT({v: k for k, v in _COMPONENT_NAME_LOOKUP.items()})

class OTDS:
    def __init__(self) -> None:
        self._accommodations: dict[t.Key, t.Accommodation] = {}
        self._brands: dict[t.Key, t.Brand] = {}
        self._defined_components: dict[t.Key, t.DefineComponent] = {}
        self._flights: t.Flights = {}
        self._products: t.Products = {"product": {}}
        self._accommodations_price_items: dict[t.Key, dict[t.Token, tuple[t.PriceItem, ...]]] = {}

    @property
    def accommodations(self) -> MPT[t.Key, t.Accommodation]:
        return MPT(self._accommodations)

    def parse(self, path: Path) -> None:
        xml = validate(path, ROOT_PATH / "schema" / "otds.xsd")
        otds = xml.getroot()
        update_mode = self.get_update_mode(otds)
        if update_mode is e.UpdateMode.New:
            if self._accommodations or self._products != {"product": {}}:
                raise ValueError("Would overwrite all content")
        if update_mode is e.UpdateMode.Delete:
            raise NotImplementedError()

        for elem in otds.iterchildren():
            if elem.tag == f"{PREFIX}Brands":
                self.parse_brands(elem)
            elif elem.tag == f"{PREFIX}DefinedComponents":
                self.parse_combi_components(elem)
            elif elem.tag == f"{PREFIX}Flights":
                self.parse_flights(elem)
            elif elem.tag == f"{PREFIX}Accommodations":
                self.parse_accomodations(elem)
            elif elem.tag == f"{PREFIX}Products":
                self.parse_products(elem)
            else:
                raise NotImplementedError(elem.tag)

    def parse_accomodation(self, accommodation: etree._Element) -> None:
        update_mode = self.get_update_mode(accommodation)
        if update_mode is e.UpdateMode.New:
            if accommodation.attrib["Key"] in self._accommodations:
                raise ValueError("Would overwrite accommodation")
        elif update_mode is e.UpdateMode.Delete:
            raise NotImplementedError()
        key = t.Key(accommodation.attrib["Key"])
        accom = self._accommodations.setdefault(key, {"selling": {}})
        properties: dict[t.Key, tuple[t.Property, ...]] = {}
        for elem in accommodation.iterchildren():
            if elem.tag == f"{PREFIX}Tags":
                self.parse_tags(elem, accom.setdefault("tags", {}))
            elif elem.tag == f"{PREFIX}Properties":
                self.parse_properties(elem, properties)
            elif elem.tag == f"{PREFIX}SellingAccom":
                self.parse_selling_accom(elem, accom["selling"])
            elif elem.tag == f"{PREFIX}CatchmentAirports":
                if elem.get("UpdateMode", "New") != "New":
                    raise NotImplementedError()
                assert elem.text
                accom["airports"] = tuple(t.SimpleNodeIataAirportCode(c) for c in elem.text.split())
            elif elem.tag == f"{PREFIX}Availabilities":
                self.parse_availabilities(elem, accom.setdefault("availabilities", {}))
            else:
                raise NotImplementedError(elem.tag)
        if properties:
            accom["properties"] = MPT(properties)

    def parse_accomodations(self, accommodations: etree._Element) -> None:
        update_mode = self.get_update_mode(accommodations)
        if update_mode is e.UpdateMode.New:
            if self._accommodations:
                raise ValueError("Would overwrite all accommodations")
        elif update_mode is e.UpdateMode.Delete:
            raise NotImplementedError()
        for elem in accommodations.iterchildren():
            if elem.tag == f"{PREFIX}Accommodation":
                self.parse_accomodation(elem)
            elif elem.tag == f"{PREFIX}PriceItems":
                self.parse_price_items(elem, self._accommodations_price_items)
            else:
                raise NotImplementedError(elem.tag)

    def parse_address(self, addr: etree._Element, addr_dict: t.Address) -> None:
        for elem in addr.iterchildren():
            if elem.tag == f"{PREFIX}Street":
                assert elem.text
                addr_dict["street"] = elem.text
            elif elem.tag == f"{PREFIX}ZipCode":
                assert elem.text
                addr_dict["zip"] = elem.text
            elif elem.tag == f"{PREFIX}City":
                if elem.get("lang", "de") != "de":
                    raise NotImplementedError()
                if "city" in addr_dict:
                    raise NotImplementedError()
                assert elem.text
                addr_dict["city"] = t.LanguageText(elem.text)
            elif elem.tag == f"{PREFIX}Country":
                if elem.get("lang", "de") != "de":
                    raise NotImplementedError()
                if "country" in addr_dict:
                    raise NotImplementedError()
                assert elem.text
                addr_dict["country"] = t.LanguageText(elem.text)
            elif elem.tag == f"{PREFIX}Phone":
                assert elem.text
                addr_dict["phone"] = elem.text
            elif elem.tag == f"{PREFIX}GeoInfo":
                self.parse_geoinfo(elem, addr_dict.setdefault("geo", {}))
            else:
                raise NotImplementedError()

    def parse_age_condition(self, person_age: etree._Element) -> tuple[t.SourceAttribute, t.PersonAge]:
        if person_age.get("DayAllocation") is not None:
            raise NotImplementedError()
        if person_age.get("EvaluationMode", "Any") != "Any":
            raise NotImplementedError()
        src = t.SourceAttribute(person_age.attrib["Source"])

        conds: t.PersonAge = {}
        for elem in person_age.iterchildren():
            if elem.tag == f"{PREFIX}Max":
                assert elem.text
                conds["max"] = int(elem.text)
            else:
                raise NotImplementedError(elem.tag)
        return (src, conds)

    def parse_airport_condition(self, airports: etree._Element) -> tuple[t.SourceAttribute, e.AirportType, tuple[str, ...]]:
        src = t.SourceAttribute(airports.attrib["Source"])
        a_type = e.AirportType(airports.attrib["AirportType"])
        assert airports.text
        return (src, a_type, tuple(airports.text.split()))

    def parse_availabilities(self, availabilities: etree._Element, avail_dict: dict[t.Key, t.Availabilities]) -> None:
        update_mode = self.get_update_mode(availabilities)
        if update_mode is not e.UpdateMode.New:
            raise NotImplementedError()

        avail: dict[t.Key, t.Availability] = {}
        cond = None
        for elem in availabilities.iterchildren():
            if elem.tag == f"{PREFIX}Availability":
                self.parse_availability(elem, avail)
            elif elem.tag == f"{PREFIX}Condition":
                conds = self.parse_condition_group(elem)
                assert len(conds) == 1
                cond = conds[0]
            else:
                assert False
        key = t.Key(availabilities.attrib["Key"])
        avail_dict[key] = (cond, MPT(avail))

    def parse_availability(self, availability: etree._Element, avail_dict: dict[t.Key, t.Availability]) -> None:
        update_mode = self.get_update_mode(availability)
        if update_mode is not e.UpdateMode.New:
            raise NotImplementedError()

        start = datetime.date.fromisoformat(availability.attrib["StartDate"])
        end = datetime.date.fromisoformat(availability.attrib["EndDate"])

        state: dict[t.Key, tuple[t.Offset, t.DayState]] = {}
        default = None
        for elem in availability.iterchildren():
            if elem.tag == f"{PREFIX}DefaultDayState":
                default = self.parse_default_day_state(elem)
            elif elem.tag == f"{PREFIX}DayState":
                self.parse_day_state(elem, state)
            else:
                assert False

        assert default is not None
        key = t.Key(availability.attrib["Key"])
        avail_dict[key] = (start, end, default, MPT(state))

    def parse_board(self, board: etree._Element, board_dict: dict[t.Key, t.Board]) -> None:
        update_mode = self.get_update_mode(board)
        if update_mode is not e.UpdateMode.New:
            raise NotImplementedError()

        b: t.Board = {}
        for elem in board.iterchildren():
            if elem.tag == f"{PREFIX}Tags":
                self.parse_tags(elem, b.setdefault("tags", {}))
            elif elem.tag == f"{PREFIX}Booking":
                b["booking"] = self.parse_booking(elem)
            elif elem.tag == f"{PREFIX}Properties":
                self.parse_properties(elem, b.setdefault("properties", {}))
            else:
                raise NotImplementedError(elem.tag)
        key = t.Key(board.attrib["Key"])
        board_dict[key] = MPT(b)

    def parse_booking(self, booking: etree._Element) -> tuple[t.BookingGroup, ...]:
        update_mode = self.get_update_mode(booking)
        assert update_mode is not e.UpdateMode.Merge
        if update_mode is not e.UpdateMode.New:
            raise NotImplementedError()
        bookings = []
        for elem in booking.iterchildren():
            if elem.tag == f"{PREFIX}BookingGroup":
                #bookings.append((e.Booking.Group, *self.parse_booking_group(elem)))
                bookings.append(self.parse_booking_group(elem))
            else:
                raise NotImplementedError()
        return tuple(bookings)

    def parse_booking_class(self, booking_class: etree._Element, booking_dict: dict[t.Key, t.BookingClass]) -> None:
        update_mode = self.get_update_mode(booking_class)
        if update_mode is not e.UpdateMode.New:
            raise NotImplementedError()

        booking: t.BookingClass = {}
        for elem in booking_class.iterchildren():
            if elem.tag == f"{PREFIX}Availabilities":
                self.parse_availabilities(elem, booking.setdefault("availabilities", {}))
            else:
                raise NotImplementedError(elem.tag)
        key = t.Key(booking_class.attrib["Key"])
        booking_dict[key] = MPT(booking)

    def parse_booking_group(self, booking_group: etree._Element) -> t.BookingGroup:
        if booking_group.get("Priority", 0) != 0:
            raise NotImplementedError()
        if booking_group.get("Class") is not None:
            raise NotImplementedError()
        _base = booking_group.get("EvaluationBase")
        eval_base = None if _base is None else e.EvaluationBase(_base)
        area = e.BookingGroupArea(booking_group.attrib["Area"])
        source = t.SourceAttribute(booking_group.get("Source", "ThisComponent"))
        conds: list[t.BookingGroupCondition] = []
        for elem in booking_group.iterchildren():
            if elem.tag == f"{PREFIX}BookingParameter":
                conds.append((e.BookingGroup.Parameter, self.parse_booking_parameter(elem)))
            elif elem.tag == f"{PREFIX}Condition":
                cond_group = self.parse_condition_group(elem)
                assert len(cond_group) == 1
                conds.append((e.BookingGroup.Condition, cond_group[0]))
            else:
                raise NotImplementedError(elem.tag)
        return (area, source, tuple(conds), eval_base)

    def parse_booking_offset_condition(self, date_offset: etree._Element) -> tuple[t.SourceAttribute, t.BookingOffsetCondition]:
        source = t.SourceAttribute(date_offset.attrib["Source"])
        conds: t.BookingOffsetCondition = {}
        for elem in date_offset.iterchildren():
            if elem.tag == f"{PREFIX}Min":
                assert elem.text
                conds["min"] = int(elem.text)
            elif elem.tag == f"{PREFIX}Max":
                assert elem.text
                conds["max"] = int(elem.text)
            else:
                assert False
        return (source, conds)

    def parse_booking_parameter(self, booking_parameter: etree._Element) -> t.BookingParameter:
        pad_length = int(booking_parameter.get("PadLength", 0))
        left_sep = t.SeparatorLeft(booking_parameter.get("LeftSeparator", ""))
        right_sep = t.SeparatorRight(booking_parameter.get("RightSeparator", ""))
        if booking_parameter.get("PadOrientation", "Right") != "Right":
            raise NotImplementedError()
        if booking_parameter.get("Padding", " ") != " ":
            raise NotImplementedError()
        if booking_parameter.get("PadCondition", "Always") != "Always":
            raise NotImplementedError()

        params: list[t.BookingParameterParam] = []
        for elem in booking_parameter.iterchildren():
            if elem.tag == f"{PREFIX}Value":
                assert elem.text
                params.append((e.BookingParameter.Value, elem.text.ljust(pad_length)))
            elif elem.tag == f"{PREFIX}Date":
                day_type = e.DayType(elem.attrib["DayType"])
                source = t.SourceAttribute(elem.get("Source", "ThisComponent"))
                date_format = e.DateFormat(elem.get("DateFormat", "[D01][M01][Y01]"))
                params.append((e.BookingParameter.Date, day_type, source, date_format))
            elif elem.tag == f"{PREFIX}PersonAge":
                age_type = e.AgeType(elem.get("AgeType", "TravelAge"))
                date_format = e.DateFormat(elem.get("DateFormat", "[D01][M01][Y01]"))
                params.append((e.BookingParameter.PersonAge, age_type, date_format))
            elif elem.tag == f"{PREFIX}Tag":
                if elem.get("DayAllocation") is not None:
                    raise NotImplementedError()
                if elem.get("EvaluationMode", "Any") != "Any":
                    raise NotImplementedError()
                if elem.get("Offset", 0) != 0:
                    raise NotImplementedError()
                if elem.get("Length") is not None:
                    raise NotImplementedError()
                if elem.get("TagValueType") is not None:
                    raise NotImplementedError()
                src = t.SourceAttribute(elem.attrib["Source"])
                params.append((e.BookingParameter.Tag, src, t.Token(elem.attrib["Class"])))
            else:
                raise NotImplementedError(elem.tag)
        return MPT({
            "field": e.Field(booking_parameter.attrib["Field"]),
            "index": int(booking_parameter.get("Index", 0)),
            "name": t.Name(booking_parameter.get("Name", "Default")),
            "params": tuple(params),
            "sep": (left_sep, right_sep)
        })

    def parse_brand(self, brand: etree._Element) -> None:
        update_mode = self.get_update_mode(brand)
        if update_mode is not e.UpdateMode.New:
            raise NotImplementedError()

        details: t.Brand = {}
        for elem in brand.iterchildren():
            if elem.tag == f"{PREFIX}Booking":
                details["booking"] = self.parse_booking(elem)
            elif elem.tag == f"{PREFIX}Tags":
                self.parse_tags(elem, details.setdefault("tags", {}))
            else:
                raise NotImplementedError(elem.tag)
        key = t.Key(brand.attrib["Key"])
        self._brands[key] = details

    def parse_brands(self, brands: etree._Element) -> None:
        update_mode = self.get_update_mode(brands)
        if update_mode is e.UpdateMode.New:
            if self._brands:
                raise ValueError("Would overwrite all brands")
        if update_mode is e.UpdateMode.Delete:
            raise NotImplementedError()

        for elem in brands.iterchildren():
            if elem.tag == f"{PREFIX}Brand":
                self.parse_brand(elem)
            else:
                assert False

    def parse_combi_components(self, defined_components: etree._Element) -> None:
        update_mode = self.get_update_mode(defined_components)
        if update_mode is not e.UpdateMode.New:
            raise NotImplementedError()

        for elem in defined_components.iterchildren():
            assert elem.tag == f"{PREFIX}DefineComponent"
            self.parse_define_component_rules(elem, self._defined_components)

    @overload
    def parse_combinable_when(self, combinable_when: etree._Element, _multi: Literal[True]) -> tuple[t.CombinableWhen, ...]:
        ...
    @overload
    def parse_combinable_when(self, combinable_when: etree._Element, _multi: Literal[False] = ...) -> t.CombinableWhen:
        ...
    def parse_combinable_when(self, combinable_when: etree._Element, _multi: bool = False) -> tuple[t.CombinableWhen, ...] | t.CombinableWhen:
        conds: list[t.CombinableWhen] = []
        for elem in combinable_when.iterchildren():
            if elem.tag == f"{PREFIX}CombinationCode":
                if elem.get("Component") is not None:
                    raise NotImplementedError()
                if elem.get("Source") is not None:
                    raise NotImplementedError()
                group = t.Identifier(elem.get("Group", "Default"))
                conds.append((e.CombinableWhen.Code, group))
            elif elem.tag == f"{PREFIX}Or":
                conds.append((e.CombinableWhen.Or, self.parse_combinable_when(elem, _multi=True)))
            else:
                raise NotImplementedError(elem.tag)
        assert conds
        assert _multi or len(conds) == 1
        return tuple(conds) if _multi else conds[0]

    def parse_combinatorics(self, combinatorics: etree._Element, combi_dict: dict[tuple[t.Identifier, t.LayerLevel], t.Combinatorics]) -> None:
        lname = t.Identifier(combinatorics.get("LayerName", "Default"))
        llevel = t.LayerLevel(int(combinatorics.get("LayerLevel", 0)))
        key = (lname, llevel)
        assert key not in combi_dict
        c: t.Combinatorics = {}
        for elem in combinatorics.iterchildren():
            if elem.tag == f"{PREFIX}CombinationCode":
                group = t.Identifier(elem.get("Group", "Default"))
                assert elem.text
                c["code"] = (group, elem.text)
            elif elem.tag == f"{PREFIX}CombinationLevel":
                assert elem.text
                c["level"] = int(elem.text)
            elif elem.tag == f"{PREFIX}CombinableWhen":
                c["when"] = self.parse_combinable_when(elem)
            else:
                raise NotImplementedError(elem.tag)
        combi_dict[key] = MPT(c)

    def parse_components(self, components: etree._Element, product_type: e.ProductType) -> tuple[t.Component, ...]:
        update_mode = self.get_update_mode(components)
        assert update_mode is not e.UpdateMode.Merge
        if update_mode is not e.UpdateMode.New:
            raise NotImplementedError()

        comps: list[t.Component] = []
        for elem in components.iterchildren():
            if elem.tag == f"{PREFIX}Accommodation":
                comps.append((e.Component.Accommodation, self.parse_rule_accommodation_component(elem, product_type)))
            elif elem.tag == f"{PREFIX}CombiComponent":
                comps.append((e.Component.CombiComponent, self.parse_rule_combi_component(elem, product_type)))
            elif elem.tag == f"{PREFIX}DefinedComponent":
                comps.append((e.Component.DefinedComponent, self.parse_rule_defined_component(elem, product_type)))
            elif elem.tag == f"{PREFIX}OnewayFlight":
                _name = elem.get("Name")
                if _name is None:
                    raise NotImplementedError()
                name = t.Name(_name)
                _day_alloc = elem.get("DayAllocationIndex")
                if _day_alloc is None:
                    _day_alloc = "0"  # TODO: The following default values are used depending on the component context:
                day_alloc_index = t.DayAllocationIndex(int(_day_alloc))
                day_alloc_lvl = t.DayAllocationLevel(int(elem.get("DayAllocationLevel", 0)))
                comps.append((e.Component.OnewayFlight, (name, day_alloc_index, day_alloc_lvl)))
            else:
                raise NotImplementedError(elem.tag)
        return tuple(comps)

    def parse_condition_group(self, condition: etree._Element) -> tuple[t.ConditionGroup, ...]:
        cond: list[t.ConditionGroup] = []
        for elem in condition.iterchildren():
            if elem.tag == f"{PREFIX}Or":
                cond.append((e.Condition.Or, self.parse_condition_group(elem)))
            elif elem.tag == f"{PREFIX}And":
                cond.append((e.Condition.And, self.parse_condition_group(elem)))
            elif elem.tag == f"{PREFIX}Not":
                not_cond = self.parse_condition_group(elem)
                assert len(not_cond) == 1
                cond.append((e.Condition.Not, not_cond[0]))
            elif elem.tag == f"{PREFIX}Airports":
                cond.append((e.Condition.Airports, self.parse_airport_condition(elem)))
            elif elem.tag == f"{PREFIX}BookingDateOffset":
                cond.append((e.Condition.BookingDateOffset, self.parse_booking_offset_condition(elem)))
            elif elem.tag == f"{PREFIX}ConditionalTags":
                cond.append((e.Condition.ConditionalTags, self.parse_conditional_tag_condition(elem)))
            elif elem.tag == f"{PREFIX}Date":
                cond.append((e.Condition.Date, self.parse_date_condition(elem)))
            elif elem.tag == f"{PREFIX}DayImpact":
                cond.append((e.Condition.DayImpact, self.parse_day_impact(elem)))
            elif elem.tag == f"{PREFIX}Duration":
                cond.append((e.Condition.Duration, self.parse_duration_condition(elem)))
            elif elem.tag == f"{PREFIX}Impact":
                cond.append((e.Condition.Impact, self.parse_impact(elem)))
            elif elem.tag == f"{PREFIX}Imply":
                cond.append((e.Condition.Imply, self.parse_imply(elem)))
            elif elem.tag == f"{PREFIX}Keys":
                cond.append((e.Condition.Keys, self.parse_key_condition(elem)))
            elif elem.tag == f"{PREFIX}MatchEqual":
                cond.append((e.Condition.MatchEqual, self.parse_match(elem)))
            elif elem.tag == f"{PREFIX}PersonCount":
                cond.append((e.Condition.PersonCount, self.parse_person_count_condition(elem)))
            elif elem.tag == f"{PREFIX}PersonImpact":
                cond.append((e.Condition.PersonImpact, self.parse_person_impact(elem)))
            elif elem.tag == f"{PREFIX}Tags":
                cond.append((e.Condition.Tags, self.parse_tag_condition(elem)))
            else:
                raise NotImplementedError(elem.tag)
        return tuple(cond)

    def parse_conditional_tag(self, cond_tag: etree._Element) -> tuple[t.Token, str, t.ConditionGroup]:
        _tag = cond_tag.find(f"{PREFIX}Tag")
        _cond = cond_tag.find(f"{PREFIX}Condition")
        assert _tag is not None and _cond is not None
        c, v = self.parse_tag(_tag)
        cond = self.parse_condition_group(_cond)
        assert len(cond) == 1
        return c, v, cond[0]

    def parse_conditional_tag_condition(self, tags: etree._Element) -> tuple[t.SourceAttribute, t.Token, tuple[str, ...]]:
        if tags.get("DayAllocation", "All") != "All":  # Do not understand: The Default is "All" if the condition is not one of the following:
            raise NotImplementedError()
        if tags.get("EvaluationMode", "Any") != "Any":
            raise NotImplementedError()
        if tags.get("Offset", 0) != 0:
            raise NotImplementedError()
        if tags.get("Length") is not None:
            raise NotImplementedError()
        src = t.SourceAttribute(tags.attrib["Source"])
        assert tags.text
        return (src, t.Token(tags.attrib["Class"]), tuple(tags.text.split()))

    def parse_content_info(self, info: etree._Element, info_dict: t.AccommodationInfo) -> None:
        for elem in info.iterchildren():
            if elem.tag == f"{PREFIX}Reference":
                system = elem.attrib["ReferenceSystem"].lower()
                assert system in {"giata", "geocodes"}
                typ = elem.attrib["ReferenceType"]
                info_dict[system] = (typ, elem.text)  # type: ignore[literal-required]
            else:
                raise NotImplementedError()

    def parse_date_condition(self, date: etree._Element) -> tuple[e.DayType, t.SourceAttribute, t.DateCondition]:
        source = t.SourceAttribute(date.attrib["Source"])
        dt = e.DayType(date.get("DayType", "Stay"))
        conds: t.DateCondition = {}
        for elem in date.iterchildren():
            if elem.tag == f"{PREFIX}Min":
                assert elem.text
                conds["min"] = datetime.date.fromisoformat(elem.text)
            elif elem.tag == f"{PREFIX}Max":
                assert elem.text
                conds["max"] = datetime.date.fromisoformat(elem.text)
            elif elem.tag == f"{PREFIX}Dates":
                assert elem.text
                conds["dates"] = tuple(datetime.date.fromisoformat(d) for d in elem.text.split())
            else:
                assert False
        return (dt, source, MPT(conds))

    def parse_day_allocation(self, day_allocation: etree._Element) -> tuple[t.DayAllocation, ...]:
        update_mode = self.get_update_mode(day_allocation)
        assert update_mode is not e.UpdateMode.Merge
        if update_mode is not e.UpdateMode.New:
            raise NotImplementedError()

        allocs: list[t.DayAllocation] = []
        for elem in day_allocation.iterchildren():
            if elem.tag == f"{PREFIX}DayAllocationStart":
                allocs.append((e.DayAllocationPart.Start, self.parse_day_allocation_start(elem)))
            elif elem.tag == f"{PREFIX}DayAllocationEnd":
                allocs.append((e.DayAllocationPart.End, self.parse_day_allocation_end(elem)))
            else:
                assert False
        return tuple(allocs)

    def _parse_day_allocation(self, day_alloc: etree._Element, day_ref_default: str) -> t.DayAllocationStartEnd:
        if day_alloc.get("Offset", 0) != 0:
            raise NotImplementedError()

        source = t.SourceAttribute(day_alloc.get("Source", "Product"))
        day_ref = e.DayReference(day_alloc.get("DayReference", day_ref_default))
        level = t.DayAllocationLevel(int(day_alloc.get("DayAllocationLevel", 0)))
        shift = e.Shift(day_alloc.get("Shift", "None"))
        return (level, source, day_ref, shift)

    def parse_day_allocation_end(self, day_alloc: etree._Element) -> t.DayAllocationStartEnd:
        return self._parse_day_allocation(day_alloc, "CheckOut")

    def parse_day_allocation_start(self, day_alloc: etree._Element) -> t.DayAllocationStartEnd:
        return self._parse_day_allocation(day_alloc, "CheckIn")

    def parse_day_impact(self, day_impact: etree._Element) -> t.DayImpact:
        if day_impact.get("ImpactExecutionOrder", "BeforeCombinatorics") != "BeforeCombinatorics":
            raise NotImplementedError()
        for elem in day_impact.iterchildren():
            if elem.tag == f"{PREFIX}Date":
                return (e.DayImpact.Date, self.parse_date_condition(elem))
            elif elem.tag == f"{PREFIX}DayIndex":
                return (e.DayImpact.DayIndex, self.parse_day_index_condition(elem))
            else:
                raise NotImplementedError()
        assert False

    def parse_day_index_condition(self, day_index: etree._Element) -> tuple[t.SourceAttribute, tuple[tuple[e.DayIndex, int], ...]]:
        if day_index.get("Repeat") is not None:
            raise NotImplementedError()
        if day_index.get("IntervalType", "Stay") != "Stay":
            raise NotImplementedError()
        src = t.SourceAttribute(day_index.attrib["Source"])

        conds = []
        for elem in day_index.iterchildren():
            if elem.tag == f"{PREFIX}Indices":
                assert elem.text
                conds.append((e.DayIndex.Indices, int(elem.text)))
            elif elem.tag == f"{PREFIX}Until":
                assert elem.text
                conds.append((e.DayIndex.Until, int(elem.text)))
            else:
                raise NotImplementedError(elem.tag)
        return (src, tuple(conds))

    def parse_day_state(self, day_state: etree._Element, state_dict: dict[t.Key, tuple[t.Offset, t.DayState]]) -> None:
        update_mode = self.get_update_mode(day_state)
        assert update_mode is not e.UpdateMode.Merge
        if update_mode is not e.UpdateMode.New:
            raise NotImplementedError()

        state: t.DayState | None = None
        for elem in day_state.iterchildren():
            if elem.tag == f"{PREFIX}Closed":
                state = (e.DayState.Closed,)
            elif elem.tag == f"{PREFIX}Open":
                state = (e.DayState.Open, t.AvailabilityOpen(int(elem.text)) if elem.text else None)
            else:
                raise NotImplementedError(elem.tag)
        assert state is not None
        key = t.Key(day_state.attrib["Key"])
        offset = t.Offset(int(day_state.attrib["Offset"]))
        state_dict[key] = (offset, state)

    def parse_default_day_state(self, default_day_state: etree._Element) -> tuple[t.DefaultDayState, t.DefaultDayStateExtra]:
        update_mode = self.get_update_mode(default_day_state)
        assert update_mode is not e.UpdateMode.Merge
        if update_mode is not e.UpdateMode.New:
            raise NotImplementedError

        state: t.DefaultDayState | None = None
        extra: t.DefaultDayStateExtra = {}
        for elem in default_day_state.iterchildren():
            if elem.tag == f"{PREFIX}Closed":
                state = (e.DefaultDayState.Closed,)
            elif elem.tag == f"{PREFIX}Open":
                state = (e.DefaultDayState.Open, t.AvailabilityOpen(int(elem.text)) if elem.text else None)
            elif elem.tag == f"{PREFIX}CheckOut":
                if elem.get("State", "Open") != "Open":
                    raise NotImplementedError()
                extra["check_out"] = t.AvailabilityRequest(int(elem.text)) if elem.text else None
            else:
                raise NotImplementedError(elem.tag)
        assert state is not None
        return (state, extra)

    def parse_define_component_rules(self, define_component: etree._Element, components_dict: dict[t.Key, t.DefineComponent]) -> None:
        update_mode = self.get_update_mode(define_component)
        if update_mode is not e.UpdateMode.New:
            raise NotImplementedError()

        if define_component.get("DayAllocationIndex") is not None:
            raise NotImplementedError()
        role = e.Role(define_component.attrib["Role"])
        product_type = _NAME_COMPONENT_LOOKUP[define_component.attrib["Role"]]

        comp: t._DefineComponent = {"components": ()}
        for elem in define_component.iterchildren():
            if elem.tag == f"{PREFIX}Booking":
                comp["booking"] = self.parse_booking(elem)
            elif elem.tag == f"{PREFIX}Components":
                comp["components"] = self.parse_components(elem, product_type)
            elif elem.tag == f"{PREFIX}Filter":
                self.parse_filter_simple_node(elem, comp.setdefault("filter", {}))
            else:
                assert False
        key = t.Key(define_component.attrib["Key"])
        if "filter" in comp:
            comp["filter"] = MPT(comp["filter"])
        components_dict[key] = (role, comp)

    def parse_duration_condition(self, duration: etree._Element) -> tuple[t.SourceAttribute, t.DurationCondition]:
        source = t.SourceAttribute(duration.attrib["Source"])
        du = e.DurationUnit(duration.get("DurationUnit", "Nights"))

        def delta(elem: etree._Element) -> datetime.timedelta:
            assert elem.text
            value = int(elem.text)
            if du is e.DurationUnit.Nights:
                return datetime.timedelta(days=value)
            elif du is e.DurationUnit.Hours:
                return datetime.timedelta(hours=value)
            elif du is e.DurationUnit.Minutes:
                return datetime.timedelta(minutes=value)
            elif du is e.DurationUnit.Weeks:
                return datetime.timedelta(weeks=value)
            assert False

        conds: t.DurationCondition = {}
        for elem in duration.iterchildren():
            if elem.tag == f"{PREFIX}Min":
                conds["min"] = delta(elem)
            elif elem.tag == f"{PREFIX}Max":
                conds["max"] = delta(elem)
            elif elem.tag == f"{PREFIX}Durations":
                assert elem.text
                conds["durations"] = tuple(int(x) for x in elem.text.split())
            else:
                raise NotImplementedError(elem.tag)
        return (source, conds)

    def parse_empty_tag_condition(self, tag: etree._Element) -> tuple[t.SourceAttribute, t.Token]:
        if tag.get("DayAllocation", "All") != "All":  # Do not understand: The Default is "All" if the condition is not one of the following:
            raise NotImplementedError()
        if tag.get("EvaluationMode", "Any") != "Any":
            raise NotImplementedError()
        if tag.get("Offset", 0) != 0:
            raise NotImplementedError()
        if tag.get("Length") is not None:
            raise NotImplementedError()
        if tag.get("TagValueType", "String") != "String":
            raise NotImplementedError()

        src = t.SourceAttribute(tag.attrib["Source"])
        return (src, t.Token(tag.attrib["Class"]))

    def parse_filter_simple_node(self, filt: etree._Element, filter_dict: dict[t.Key, t.ConditionGroup]) -> None:
        update_mode = self.get_update_mode(filt)
        assert update_mode is not e.UpdateMode.Merge
        if update_mode is not e.UpdateMode.New:
            raise NotImplementedError()
        key = t.Key(filt.get("Key", "default"))
        conds = self.parse_condition_group(filt)
        assert len(conds) == 1
        filter_dict[key] = conds[0]  # TODO(OTDS2+): Key must exist

    def parse_flights(self, flights: etree._Element) -> None:
        update_mode = self.get_update_mode(flights)
        if update_mode is e.UpdateMode.New:
            if self._flights:
                raise ValueError("Would overwrite all flights")
        elif update_mode is e.UpdateMode.Delete:
            raise NotImplementedError()
        for elem in flights.iterchildren():
            if elem.tag != f"{PREFIX}OnewayFlights":
                raise NotImplementedError(elem.tag)
            self.parse_oneway_flights(elem, self._flights.setdefault("oneway", {}))

    def parse_general_included_services(self, included_services: etree._Element) -> tuple[e.GeneralIncludedService, ...]:
        if included_services.get("Class") is not None:
            raise NotImplementedError()
        services = []
        for elem in included_services.iterchildren():
            assert elem.tag == f"{PREFIX}GeneralIncludedService"
            if elem.get("lang", "de") != "de":
                raise NotImplementedError()
            if elem.get("ShortServiceAnnotation") is not None:
                raise NotImplementedError()
            services.append(e.GeneralIncludedService(elem.text))
        return tuple(services)

    def parse_geoinfo(self, geo: etree._Element, geo_dict: t.Geo) -> None:
        for elem in geo.iterchildren():
            if elem.tag == f"{PREFIX}GeoCode":
                lat = elem.findtext(f"{PREFIX}Latitude")
                long = elem.findtext(f"{PREFIX}Longitude")
                if not lat or not long:  # Why?! "As this information is optional, the value can be empty"
                    raise NotImplementedError()
                acc = elem.findtext(f"{PREFIX}Accuracy")
                assert acc
                geo_dict["geocode"] = {
                    "latitude": t.OWGS84Latitude(float(lat)),
                    "longitude": t.OWGS84Longitude(float(long)),
                    "accuracy_km": int(acc)
                }
            else:
                raise NotImplementedError()

    def parse_global_value(self, global_value: etree._Element, globals_dict: dict[t.Key, t.GlobalValue]) -> None:
        update_mode = self.get_update_mode(global_value)
        if update_mode is not e.UpdateMode.New:
            raise NotImplementedError()

        value: t.GlobalValue = {"params": {}}
        for elem in global_value.iterchildren():
            if elem.tag == f"{PREFIX}ParameterSet":
                self.parse_parameter_set(elem, value["params"])
            else:
                raise NotImplementedError(elem.tag)
        assert value["params"]
        key = t.Key(global_value.attrib["Key"])
        globals_dict[key] = value

    def parse_global_values(self, global_values: etree._Element, products_dict: t.Products) -> None:
        update_mode = self.get_update_mode(global_values)
        if update_mode is not e.UpdateMode.New:
            raise NotImplementedError()

        g: dict[t.Key, t.GlobalValue] = {}
        for elem in global_values.iterchildren():
            assert elem.tag == f"{PREFIX}GlobalValue"
            self.parse_global_value(elem, g)
        assert g
        products_dict["globals"] = MPT(g)

    def parse_impact(self, impact: etree._Element) -> tuple[t.SourceAttribute, t.Token, tuple[str, ...]]:
        if impact.get("ImpactExecutionOrder", "BeforeCombinatorics") != "BeforeCombinatorics":
            raise NotImplementedError()
        cond = None
        for elem in impact.iterchildren():
            assert cond is None
            if elem.tag == f"{PREFIX}ConditionalTags":
                cond = self.parse_conditional_tag_condition(elem)
            else:
                raise NotImplementedError()
        assert cond is not None
        return cond

    def parse_imply(self, imply: etree._Element) -> tuple[t.ConditionGroup, t.ConditionGroup]:
        _if = imply.find(f"{PREFIX}If")
        _then = imply.find(f"{PREFIX}Then")
        assert _if is not None and _then is not None
        if_cond = self.parse_condition_group(_if)
        assert len(if_cond) == 1
        then_cond = self.parse_condition_group(_then)
        assert len(then_cond) == 1
        return (if_cond[0], then_cond[0])

    def parse_key_condition(self, keys: etree._Element) -> tuple[t.SourceAttribute, str, e.DayAllocation | None]:
        src = t.SourceAttribute(keys.attrib["Source"])
        _day_alloc = keys.get("DayAllocation")
        day_alloc = None if _day_alloc is None else e.DayAllocation(_day_alloc)
        if keys.get("EvaluationMode", "Any") != "Any":
            raise NotImplementedError()
        assert keys.text
        return (src, keys.text, day_alloc)

    def parse_match(self, match_equal: etree._Element) -> tuple[t.Match, ...]:
        elems: list[t.Match] = []
        for elem in match_equal.iterchildren():
            if elem.tag == f"{PREFIX}Element":
                elems.append((e.Match.Element, self.parse_match_element(elem)))
            elif elem.tag == f"{PREFIX}Tag":
                elems.append((e.Match.Tag, self.parse_empty_tag_condition(elem)))
            else:
                raise NotImplementedError(elem.tag)
        assert len(elems) >= 2
        return tuple(elems)

    def parse_match_element(self, element: etree._Element) -> tuple[e.MatchElement, t.SourceAttribute]:
        if element.get("DayAllocation") is not None:
            raise NotImplementedError()
        if element.get("EvaluationMode", "Any") != "Any":
            raise NotImplementedError()

        src = t.SourceAttribute(element.attrib["Source"])
        return (e.MatchElement(element.text), src)

    def parse_occupancy(self, occupancy: etree._Element, occupancies: dict[t.Key, tuple[t.Occupancy, ...]]) -> None:
        update_mode = self.get_update_mode(occupancy)
        assert update_mode is not e.UpdateMode.Merge
        if update_mode is not e.UpdateMode.New:
            raise NotImplementedError()

        occ: list[t.Occupancy] = []
        for elem in occupancy.iterchildren():
            if elem.tag == f"{PREFIX}Person":
                occ.append((e.Occupancy.Person, self.parse_occupancy_person(elem)))
            else:
                raise NotImplementedError(elem.tag)
        key = t.Key(occupancy.attrib["Key"])
        occupancies[key] = tuple(occ)

    def parse_occupancy_person(self, person: etree._Element) -> t.OccupancyPerson:
        if person.get("MatchAvailability") is not None:
            raise NotImplementedError()

        conds = {}
        for elem in person.iterchildren():
            if elem.tag == f"{PREFIX}Count":
                assert elem.text
                conds["count"] = int(elem.text)
            elif elem.tag == f"{PREFIX}MaxAge":
                assert elem.text
                conds["max_age"] = t.Age(int(elem.text))
            elif elem.tag == f"{PREFIX}MinAge":
                assert elem.text
                conds["min_age"] = t.Age(int(elem.text))
            else:
                raise NotImplementedError(elem.tag)
        return MPT(conds)

    def parse_oneway(self, one_way_flight: etree._Element, flights_dict: dict[t.Key, t.Oneway]) -> None:
        update_mode = self.get_update_mode(one_way_flight)
        if update_mode is e.UpdateMode.New:
            if one_way_flight.attrib["Key"] in flights_dict:
                raise ValueError("Would overwrite flight.")
        elif update_mode is e.UpdateMode.Delete:
            raise NotImplementedError()

        key = t.Key(one_way_flight.attrib["Key"])
        flight = flights_dict.setdefault(key, {"booking_class": {}})
        for elem in one_way_flight.iterchildren():
            if elem.tag == f"{PREFIX}ArrivalAirport":
                if self.get_update_mode(elem) is not e.UpdateMode.New:
                    raise NotImplementedError()
                assert elem.text
                flight["arrival"] = t.SimpleNodeIataAirportCode(elem.text)
            elif elem.tag == f"{PREFIX}DepartureAirport":
                if self.get_update_mode(elem) is not e.UpdateMode.New:
                    raise NotImplementedError()
                assert elem.text
                flight["departure"] = t.SimpleNodeIataAirportCode(elem.text)
            elif elem.tag == f"{PREFIX}Filter":
                self.parse_filter_simple_node(elem, flight.setdefault("filter", {}))
            elif elem.tag == f"{PREFIX}BookingClass":
                self.parse_booking_class(elem, flight["booking_class"])
            else:
                raise NotImplementedError(elem.tag)

    def parse_oneway_flights(self, one_way_flights: etree._Element, flights_dict: dict[t.Key, t.Oneway]) -> None:
        update_mode = self.get_update_mode(one_way_flights)
        if update_mode is e.UpdateMode.New:
            if flights_dict:
                raise ValueError("Would overwrite all one way flights.")
        elif update_mode is e.UpdateMode.Delete:
            raise NotImplementedError()
        for elem in one_way_flights.iterchildren():
            assert elem.tag == f"{PREFIX}OnewayFlight"
            self.parse_oneway(elem, flights_dict)

    def parse_optional_bookable_addon_types(self, addon_types: etree._Element) -> tuple[t.OptionalBookableAddonType, ...]:
        if addon_types.get("Class") is not None:
            raise NotImplementedError()

        addons: list[t.OptionalBookableAddonType] = []
        for elem in addon_types.iterchildren():
            assert elem.tag == f"{PREFIX}OptionalBookableAddonType"
            if elem.get("lang", "de") != "de":
                raise NotImplementedError()
            teaser_text = t.ShortServiceAnnotation(elem.get("ShortTeaserText", ""))
            addons.append((e.OptionalBookableAddonType(elem.text), teaser_text))
        return tuple(addons)

    def parse_parameter_set(self, parameter_set: etree._Element, params_dict: dict[t.Key, t.ParameterSet]) -> None:
        update_mode = self.get_update_mode(parameter_set)
        assert update_mode is not e.UpdateMode.Merge
        if update_mode is not e.UpdateMode.New:
            raise NotImplementedError()

        param: t.ParameterSet | None = None
        agency = brand = crs = None
        for elem in parameter_set.iterchildren():
            if elem.tag == f"{PREFIX}AgencyCode":
                assert elem.text
                agency = t.AgencyCode(elem.text)
            elif elem.tag == f"{PREFIX}BrandCode":
                assert elem.text
                brand = t.BrandCode(elem.text)
            elif elem.tag == f"{PREFIX}CrsSystem":
                crs = e.CrsSystem(elem.text)
            elif elem.tag == f"{PREFIX}DistributionChannel":
                param = (e.ParameterSet.DistributionChannel, e.DistributionChannel(elem.text))
            elif elem.tag == f"{PREFIX}SalesChannel":
                param = (e.ParameterSet.SalesChannel, e.SalesChannel(elem.text))
            elif elem.tag == f"{PREFIX}SalesMarket":
                assert elem.text
                param = (e.ParameterSet.SalesMarket, t.ISO3166Country(elem.text))
            else:
                raise NotImplementedError(elem.tag)
        if all(x is not None for x in (agency, brand, crs)):
            assert crs and agency and brand
            param = (e.ParameterSet.DistributorIdentificationGroup, crs, agency, brand)
        assert param is not None
        key = t.Key(parameter_set.attrib["Key"])
        params_dict[key] = param

    def parse_person_count_condition(self, person_count: etree._Element) -> tuple[t.SourceAttribute, t.PersonCount]:
        if person_count.get("DayAllocation") is not None:
            raise NotImplementedError()
        if person_count.get("EvaluationMode", "Any") != "Any":
            raise NotImplementedError()
        src = t.SourceAttribute(person_count.attrib["Source"])

        conds: t.PersonCount = {}
        for elem in person_count.iterchildren():
            if elem.tag == f"{PREFIX}Min":
                assert elem.text
                conds["min"] = int(elem.text)
            elif elem.tag == f"{PREFIX}PersonFilter":
                conds["filter"] = self.parse_person_filter_condition(elem)
            else:
                raise NotImplementedError(elem.tag)
        return (src, MPT(conds))

    def parse_person_filter_condition(self, person_filter: etree._Element) -> tuple[Literal[e.PersonFilter.Impact], tuple[t.SourceAttribute, t.Token, tuple[str, ...]]]:
        cond: tuple[Literal[e.PersonFilter.Impact], tuple[t.SourceAttribute, t.Token, tuple[str, ...]]] | None = None
        for elem in person_filter.iterchildren():
            assert cond is None
            if elem.tag == f"{PREFIX}Impact":
                cond = (e.PersonFilter.Impact, self.parse_impact(elem))
            else:
                raise NotImplementedError(elem.tag)
        assert cond is not None
        return cond

    def parse_person_genders_condition(self, person_genders: etree._Element) -> tuple[t.SourceAttribute, tuple[e.PersonGender, ...]]:
        if person_genders.get("DayAllocation") is not None:
            raise NotImplementedError()
        if person_genders.get("EvaluationMode", "Any") != "Any":
            raise NotImplementedError()
        src = t.SourceAttribute(person_genders.attrib["Source"])

        assert person_genders.text
        values = tuple(e.PersonGender(v) for v in person_genders.text.split())
        return (src, values)

    def parse_person_impact(self, person_impact: etree._Element) -> t.PersonImpact:
        if person_impact.get("ImpactExecutionOrder", "BeforeCombinatorics") != "BeforeCombinatorics":
            raise NotImplementedError()

        cond: t.PersonImpact | None = None
        for elem in person_impact.iterchildren():
            assert cond is None
            if elem.tag == f"{PREFIX}PersonAge":
                cond = (e.PersonImpact.Age, self.parse_age_condition(elem))
            elif elem.tag == f"{PREFIX}PersonIndex":
                cond = (e.PersonImpact.Index, self.parse_person_index_condition(elem))
            elif elem.tag == f"{PREFIX}PersonGenders":
                cond = (e.PersonImpact.Genders, self.parse_person_genders_condition(elem))
            else:
                raise NotImplementedError(elem.tag)
        assert cond is not None
        return cond

    def parse_person_index_condition(self, person_index: etree._Element) -> tuple[t.SourceAttribute, t.PersonIndex]:
        if person_index.get("DayAllocation") is not None:
            raise NotImplementedError()
        if person_index.get("EvaluationMode", "Any") != "Any":
            raise NotImplementedError()
        src = t.SourceAttribute(person_index.attrib["Source"])

        conds: t.PersonIndex = {}
        for elem in person_index.iterchildren():
            if elem.tag == f"{PREFIX}From":
                assert elem.text
                conds["from_"] = int(elem.text)
            elif elem.tag == f"{PREFIX}Indices":
                assert elem.text
                conds["indices"] = tuple(int(t) for t in elem.text.split())
            elif elem.tag == f"{PREFIX}Until":
                assert elem.text
                conds["until"] = int(elem.text)
            else:
                raise NotImplementedError(elem.tag)
        return (src, MPT(conds))

    def parse_price_impact_absolute(self, absolute: etree._Element) -> tuple[Decimal, tuple[t.AbsoluteCondition, ...]]:
        value = None
        conds: list[t.AbsoluteCondition] = []
        for elem in absolute.iterchildren():
            if elem.tag == f"{PREFIX}Value":
                assert elem.text
                value = Decimal(elem.text)
            elif elem.tag == f"{PREFIX}DayBase":
                conds.append((e.Absolute.DayBase, self.parse_price_impact_base_value(elem)))
            elif elem.tag == f"{PREFIX}PersonBase":
                if elem.text == "x":
                    raise NotImplementedError()
                assert elem.text
                conds.append((e.Absolute.PersonBase, int(elem.text)))
            elif elem.tag == f"{PREFIX}AppliedBy":
                if elem.get("Component") is not None:
                    raise NotImplementedError()
                if elem.get("Source") is not None:
                    raise NotImplementedError()
                if elem.get("LogicalRelation", "Or") != "Or":
                    raise NotImplementedError()
                assert elem.text
                conds.append((e.Absolute.AppliedBy, elem.text))
            else:
                raise NotImplementedError(elem.tag)
        assert value is not None
        return (value, tuple(conds))

    def parse_price_impact_base_value(self, day_base: etree._Element) -> tuple[t.SourceAttribute, int | Literal[e.X.x]]:
        source = t.SourceAttribute(day_base.get("Source", "ThisComponent"))
        if day_base.get("IntervalType", "Stay") != "Stay":
            raise NotImplementedError()
        if day_base.text == "x":
            return (source, e.X.x)
        assert day_base.text
        return (source, int(day_base.text))

    def parse_price_item(self, price_item: etree._Element, price_dict: dict[t.Token, MutableSequence[t.PriceItem]]) -> None:
        p: t.PriceItem = {}
        for elem in price_item.iterchildren():
            if elem.tag == f"{PREFIX}Absolute":
                p["absolute"] = self.parse_price_impact_absolute(elem)
            elif elem.tag == f"{PREFIX}Combinatorics":
                self.parse_combinatorics(elem, p.setdefault("combinatorics", {}))
            elif elem.tag == f"{PREFIX}Condition":
                conds = self.parse_condition_group(elem)
                assert len(conds) == 1
                p["condition"] = conds[0]
            else:
                raise NotImplementedError(elem.tag)
        price_dict.setdefault(t.Token(price_item.attrib["Class"]), []).append(p)

    def parse_price_items(self, price_items: etree._Element, prices_dict: dict[t.Key, dict[t.Token, tuple[t.PriceItem, ...]]]) -> None:
        update_mode = self.get_update_mode(price_items)
        assert update_mode is not e.UpdateMode.Merge
        if update_mode is not e.UpdateMode.New:
            raise NotImplementedError()

        p: dict[t.Token, MutableSequence[t.PriceItem]] = {}
        for elem in price_items.iterchildren():
            if elem.tag == f"{PREFIX}PriceItem":
                self.parse_price_item(elem, p)
            else:
                raise NotImplementedError(elem.tag)
        key = t.Key(price_items.attrib["Key"])
        prices_dict[key] = {k: tuple(v) for k, v in p.items()}

    def parse_product(self, product: etree._Element, product_dict: dict[t.Key, tuple[e.ProductType, t.Product]]) -> None:
        update_mode = self.get_update_mode(product)
        if update_mode is not e.UpdateMode.New:
            raise NotImplementedError()

        product_type = e.ProductType(product.attrib["ProductType"])
        p: t.Product = {"components": ()}
        for elem in product.iterchildren():
            if elem.tag == f"{PREFIX}Tags":
                self.parse_tags(elem, p.setdefault("tags", {}))
            elif elem.tag == f"{PREFIX}Components":
                p["components"] = self.parse_components(elem, product_type)
            elif elem.tag == f"{PREFIX}DayAllocation":
                p["day_allocation"] = self.parse_day_allocation(elem)
            elif elem.tag == f"{PREFIX}Filter":
                self.parse_filter_simple_node(elem, p.setdefault("filters", {}))
            else:
                raise NotImplementedError(elem.tag)
        assert "components" in p
        key = t.Key(product.attrib["Key"])
        product_dict[key] = (product_type, p)

    def parse_products(self, products: etree._Element) -> None:
        update_mode = self.get_update_mode(products)
        if update_mode is not e.UpdateMode.New:
            raise NotImplementedError()

        for elem in products.iterchildren():
            if elem.tag == f"{PREFIX}GlobalValues":
                self.parse_global_values(elem, self._products)
            elif elem.tag == f"{PREFIX}Product":
                self.parse_product(elem, self._products["product"])
            else:
                raise NotImplementedError(elem.tag)

    def parse_properties(self, properties: etree._Element, properties_dict: dict[t.Key, tuple[t.Property, ...]]) -> None:
        update_mode = self.get_update_mode(properties)
        assert update_mode is not e.UpdateMode.Merge
        if update_mode is not e.UpdateMode.New:
            raise NotImplementedError()
        p = []
        for elem in properties.iterchildren():
            assert elem.tag == f"{PREFIX}PropertyGroup"
            p.append(self.parse_property_group(elem))
        key = t.Key(properties.attrib["Key"])
        properties_dict[key] = tuple(p)

    def parse_property_group(self, property_group: etree._Element) -> t.Property:
        if property_group.get("Priority", 0) != 0:
            raise NotImplementedError()
        property: t.Property = {}
        city = []
        for elem in property_group.iterchildren():
            if elem.tag == f"{PREFIX}AccommodationCity":
                if elem.get("lang", "de") != "de":
                    raise NotImplementedError()
                if "city" in property:
                    raise NotImplementedError()
                assert elem.text
                city.append(t.LanguageText(elem.text))
            elif elem.tag == f"{PREFIX}AccommodationType":
                if elem.text != "Hotel":
                    raise NotImplementedError()
                #property["type"] = AccommodationType(elem.text)
            elif elem.tag == f"{PREFIX}AccommodationName":
                if elem.get("lang", "de") != "de":
                    raise NotImplementedError()
                if "name" in property:
                    raise NotImplementedError()
                assert elem.text
                property["name"] = t.LanguageText(elem.text)
            elif elem.tag == f"{PREFIX}AccommodationInfo":
                self.parse_content_info(elem, property.setdefault("info", {}))
            elif elem.tag == f"{PREFIX}AccommodationOfficialCategory":
                assert elem.text
                value = [int(i) for i in elem.text.strip().split(".")]
                if len(value) == 1:
                    value.append(0)
                property["official_category"] = tuple(value)  # type: ignore[typeddict-item]
            elif elem.tag == f"{PREFIX}AccommodationOperatorCategory":
                assert elem.text
                value = [int(i) for i in elem.text.strip().split(".")]
                if len(value) == 1:
                    value.append(0)
                property["operator_category"] = tuple(value)  # type: ignore[typeddict-item]
            elif elem.tag == f"{PREFIX}AccommodationAddress":
                self.parse_address(elem, property.setdefault("address", {}))
            elif elem.tag == f"{PREFIX}BoardName":
                if elem.get("lang", "de") != "de":
                    raise NotImplementedError()
                if "board_name" in property:
                    raise NotImplementedError()
                assert elem.text
                property["board_name"] = t.LanguageText(elem.text)
            elif elem.tag == f"{PREFIX}BoardType":
                property["board_type"] = e.BoardType(elem.text)
            elif elem.tag == f"{PREFIX}UnitFacilities":
                assert elem.text
                property["unit_facilities"] = tuple(e.UnitFacilities(t) for t in elem.text.split())
            elif elem.tag == f"{PREFIX}UnitName":
                if elem.get("lang", "de") != "de":
                    raise NotImplementedError()
                if "unit_name" in property:
                    raise NotImplementedError()
                assert elem.text
                property["unit_name"] = t.LanguageText(elem.text)
            elif elem.tag == f"{PREFIX}UnitType":
                assert elem.text
                property["unit_types"] = tuple(e.UnitType(t) for t in elem.text.split())
            elif elem.tag == f"{PREFIX}GeneralIncludedServices":
                property["included_services"] = self.parse_general_included_services(elem)
            elif elem.tag == f"{PREFIX}Condition":
                conds = self.parse_condition_group(elem)
                assert len(conds) == 1
                property["condition"] = conds[0]
            elif elem.tag == f"{PREFIX}OptionalBookableAddonTypes":
                property["optional_addons"] = self.parse_optional_bookable_addon_types(elem)
            else:
                raise NotImplementedError(elem.tag)
        if city:
            property["city"] = tuple(city)
        return MPT(property)

    def parse_rule_accommodation_component(self, component: etree._Element, product_type: e.ProductType) -> tuple[t.RuleSellingAccomComponent, ...]:
        _name = component.get("Name")
        if any(component.get(a) is not None for a in ("Name", "DayAllocationIndex")):
            raise NotImplementedError()
        """if _name is None:
            _name = _COMPONENT_NAME_LOOKUP[product_type]
        name = t.Name(_name)

        _day_alloc = component.get("DayAllocationIndex")
        if _day_alloc is None:
            day_alloc = _COMPONENT_DAY_ALLOC_LOOKUP[product_type]
        else:
            day_alloc = int(_day_alloc)"""

        if component.get("DayAllocationLevel", 0) != 0:
            raise NotImplementedError()

        accoms = []
        for elem in component.iterchildren():
            if elem.tag == f"{PREFIX}SellingAccom":
                accoms.append(self.parse_rule_selling_accom_component(elem))
            else:
                assert False

        return tuple(accoms)

    def parse_rule_combi_component(self, combi: etree._Element, product_type: e.ProductType) -> t.RuleCombiComponent:
        # No idea what this is for, the element doesn't even have a Key...
        update_mode = self.get_update_mode(combi)
        assert update_mode is not e.UpdateMode.Merge
        if update_mode is not e.UpdateMode.New:
            raise NotImplementedError()

        _name = combi.get("Name")
        if _name is None:
            raise NotImplementedError()
        name = t.Name(_name)
        _day_alloc = combi.get("DayAllocationIndex")
        if _day_alloc is None:
            raise NotImplementedError()
        day_alloc_index = t.DayAllocationIndex(int(_day_alloc))
        if combi.get("DayAllocationLevel", 0) != 0:
            raise NotImplementedError()

        comps: list[t.RuleDefinedComponent] = []
        for elem in combi.iterchildren():
            if elem.tag == f"{PREFIX}DefinedComponent":
                #comps.append((e.Component.DefinedComponent, self.parse_rule_defined_component(elem, product_type)))
                comps.append(self.parse_rule_defined_component(elem, product_type))
            else:
                raise NotImplementedError(elem.tag)

        role = e.Role(combi.attrib["Role"])
        return (role, name, day_alloc_index, tuple(comps))

    def parse_rule_defined_component(self, component: etree._Element, product_type: e.ProductType) -> t.RuleDefinedComponent:
        _name = component.get("Name")
        if _name is None:
            _name = _COMPONENT_NAME_LOOKUP[product_type]  # TODO: Check this...
        name = t.Name(_name)

        if component.get("DayAllocationIndex") is not None:
            raise NotImplementedError()

        day_alloc_lvl = t.DayAllocationLevel(int(component.get("DayAllocationLevel", 0)))
        role = e.Role(component.attrib["UseRole"])
        return (role, name, day_alloc_lvl)

    def parse_rule_selling_accom_component(self, selling_accom: etree._Element) -> t.RuleSellingAccomComponent:
        _name = selling_accom.get("Name")
        if _name is None:
            raise NotImplementedError()
        name = t.Name(_name)

        _day_alloc = selling_accom.get("DayAllocationIndex")
        if _day_alloc is None:
            raise NotImplementedError()
        day_alloc_index = t.DayAllocationIndex(int(_day_alloc))

        if selling_accom.get("DayAllocationLevel", 0) != 0:
            raise NotImplementedError()

        return name, day_alloc_index

    def parse_selling_accom(self, selling_accom: etree._Element, selling: dict[t.Key, t.SellingAccom]) -> None:
        update_mode = self.get_update_mode(selling_accom)
        if update_mode is not e.UpdateMode.New:
            raise NotImplementedError()

        sell: t.SellingAccom = {}
        for elem in selling_accom.iterchildren():
            if elem.tag == f"{PREFIX}Tags":
                self.parse_tags(elem, sell.setdefault("tags", {}))
            elif elem.tag == f"{PREFIX}Booking":
                sell["booking"] = self.parse_booking(elem)
            elif elem.tag == f"{PREFIX}Filter":
                self.parse_filter_simple_node(elem, sell.setdefault("filter", {}))
            elif elem.tag == f"{PREFIX}Board":
                self.parse_board(elem, sell.setdefault("board", {}))
            elif elem.tag == f"{PREFIX}PriceItems":
                self.parse_price_items(elem, sell.setdefault("price_items", {}))
            elif elem.tag == f"{PREFIX}Unit":
                self.parse_unit(elem, sell.setdefault("unit", {}))
            else:
                raise NotImplementedError(elem.tag)
        key = t.Key(selling_accom.attrib["Key"])
        selling[key] = MPT(sell)

    def parse_selling_unit(self, selling_unit: etree._Element, selling: dict[t.Key, t.SellingUnit]) -> None:
        update_mode = self.get_update_mode(selling_unit)
        if update_mode is not e.UpdateMode.New:
            raise NotImplementedError()

        sell: t.SellingUnit = {"booking": (), "occupancy": {}}
        for elem in selling_unit.iterchildren():
            if elem.tag == f"{PREFIX}Tags":
                self.parse_tags(elem, sell.setdefault("tags", {}))
            elif elem.tag == f"{PREFIX}Booking":
                sell["booking"] = self.parse_booking(elem)
            elif elem.tag == f"{PREFIX}Occupancy":
                self.parse_occupancy(elem, sell.setdefault("occupancy", {}))
            else:
                raise NotImplementedError(elem.tag)
        key = t.Key(selling_unit.attrib["Key"])
        selling[key] = MPT(sell)

    def parse_tag_condition(self, tags: etree._Element) -> tuple[t.SourceAttribute, t.Token, tuple[str, ...], t.StringSlice]:
        if tags.get("DayAllocation", "All") != "All":  # Do not understand: The Default is "All" if the condition is not one of the following:
            raise NotImplementedError()
        if tags.get("EvaluationMode", "Any") != "Any":
            raise NotImplementedError()
        src = t.SourceAttribute(tags.attrib["Source"])
        # Convert these to slice indexes, so they can be compared with value[start:end].
        start = int(tags.get("Offset", 0))
        length = tags.get("Length")
        end = None if length is None else start + int(length)
        slc = t.StringSlice((start, end))
        assert tags.text
        return (src, t.Token(tags.attrib["Class"]), tuple(tags.text.split()), slc)

    def parse_tag(self, tag: etree._Element) -> tuple[t.Token, str]:
        if tag.get("TagValueType", "String") != "String":
            raise NotImplementedError()
        assert tag.text
        return (t.Token(tag.attrib["Class"]), tag.text)

    def parse_tags(self, tags: etree._Element, tags_dict: dict[t.Key, Mapping[t.Token, tuple[str, t.ConditionGroup | None]]]) -> None:
        update_mode = self.get_update_mode(tags)
        assert update_mode is not e.UpdateMode.Merge
        if update_mode is not e.UpdateMode.New:
            raise NotImplementedError()
        tags_: dict[t.Token, tuple[str, t.ConditionGroup | None]] = {}  # TODO(OTDS2+): Key must exist
        for elem in tags.iterchildren():
            if elem.tag == f"{PREFIX}Tag":
                k, v = self.parse_tag(elem)
                tags_[k] = (v, None)
            elif elem.tag == f"{PREFIX}ConditionalTag":
                k, v, c = self.parse_conditional_tag(elem)
                tags_[k] = (v, c)
            else:
                assert False
        key = t.Key(tags.get("Key", "default"))
        tags_dict[key] = MPT(tags_)

    def parse_unit(self, unit: etree._Element, unit_dict: dict[t.Key, t.Unit]) -> None:
        update_mode = self.get_update_mode(unit)
        if update_mode is not e.UpdateMode.New:
            raise NotImplementedError()

        u: t.Unit = {"selling_units": {}}
        for elem in unit.iterchildren():
            if elem.tag == f"{PREFIX}Tags":
                self.parse_tags(elem, u.setdefault("tags", {}))
            elif elem.tag == f"{PREFIX}Properties":
                self.parse_properties(elem, u.setdefault("properties", {}))
            elif elem.tag == f"{PREFIX}SellingUnit":
                self.parse_selling_unit(elem, u.setdefault("selling_units", {}))
            else:
                raise NotImplementedError(elem.tag)
        key = t.Key(unit.attrib["Key"])
        unit_dict[key] = MPT(u)

    def get_update_mode(self, elem: etree._Element) -> e.UpdateMode:
        return e.UpdateMode(elem.get("UpdateMode", "New"))
