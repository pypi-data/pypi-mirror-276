import datetime
from collections.abc import Mapping
from decimal import Decimal
from typing import Literal, NewType, Required, TypeAlias, TypedDict

from . import enums as e

Age = NewType("Age", int)
AgencyCode = NewType("AgencyCode", str)
AvailabilityOpen = NewType("AvailabilityOpen", int)
AvailabilityRequest = NewType("AvailabilityRequest", int)
BrandCode = NewType("BrandCode", str)
DayAllocationIndex = NewType("DayAllocationIndex", int)
DayAllocationLevel = NewType("DayAllocationLevel", int)
Identifier = NewType("Identifier", str)  # [A-Za-z0-9\.\-_|\+]+
ISO3166Country = NewType("ISO3166Country", str)  # [A-Z]{2}
Key = NewType("Key", str)  # [A-Za-z0-9\.\-_|\+]+
LanguageText = NewType("LanguageText", str)  # Indicates localised text.
LayerLevel = NewType("LayerLevel", int)
Token = NewType("Token", str)  # [\S]{1,128}  # Usually used for Class attribute
Name = NewType("Name", str)  # [A-Za-z0-9]+
Offset = NewType("Offset", int)
OWGS84Latitude = NewType("OWGS84Latitude", float)  # -90.0 to 90.0
OWGS84Longitude = NewType("OWGS84Longitude", float)  # -180.0 to 180.0
SeparatorLeft = NewType("SeparatorLeft", str)
SeparatorRight = NewType("SeparatorRight", str)
ShortServiceAnnotation = NewType("ShortServiceAnnotation", str)  # 1-50 characters
SimpleNodeIataAirportCode = NewType("SimpleNodeIataAirportCode", str)
SourceAttribute = NewType("SourceAttribute", str)
StringSlice = NewType("StringSlice", tuple[int, int | None])

_AbsoluteConditionAppliedBy = tuple[Literal[e.Absolute.AppliedBy], str]
_AbsoluteConditionDayBase = tuple[Literal[e.Absolute.DayBase], tuple[SourceAttribute, int | Literal[e.X.x]]]
_AbsoluteConditionPersonBase = tuple[Literal[e.Absolute.PersonBase], int]
AbsoluteCondition = _AbsoluteConditionAppliedBy | _AbsoluteConditionDayBase | _AbsoluteConditionPersonBase

AccommodationCategory = tuple[Literal[0, 1, 2, 3, 4, 5, 6], Literal[0, 5]] | tuple[Literal[7], Literal[0]]

class BookingOffsetCondition(TypedDict, total=False):
    min: int
    max: int

class DateCondition(TypedDict, total=False):
    min: datetime.date
    max: datetime.date
    dates: tuple[datetime.date, ...]

_DayImpactDate = tuple[Literal[e.DayImpact.Date], tuple[e.DayType, SourceAttribute, DateCondition]]
_DayImpactDayIndex = tuple[Literal[e.DayImpact.DayIndex], tuple[SourceAttribute, tuple[tuple[e.DayIndex, int], ...]]]
DayImpact = _DayImpactDate | _DayImpactDayIndex

class DurationCondition(TypedDict, total=False):
    durations: tuple[int, ...]
    min: datetime.timedelta
    max: datetime.timedelta

_MatchElement = tuple[Literal[e.Match.Element], tuple[e.MatchElement, SourceAttribute]]
_MatchTag = tuple[Literal[e.Match.Tag], tuple[SourceAttribute, Token]]
Match = _MatchElement | _MatchTag

class PersonAge(TypedDict, total=False):
    max: int

class PersonCount(TypedDict, total=False):
    filter: tuple[Literal[e.PersonFilter.Impact], tuple[SourceAttribute, Token, tuple[str, ...]]]
    min: int

class PersonIndex(TypedDict, total=False):
    from_: int
    indices: tuple[int, ...]
    until: int

_PersonImpactAge = tuple[Literal[e.PersonImpact.Age], tuple[SourceAttribute, PersonAge]]
_PersonImpactIndex = tuple[Literal[e.PersonImpact.Index], tuple[SourceAttribute, PersonIndex]]
_PersonImpactGender = tuple[Literal[e.PersonImpact.Genders], tuple[SourceAttribute, tuple[e.PersonGender, ...]]]
PersonImpact = _PersonImpactAge | _PersonImpactIndex | _PersonImpactGender

_ConditionAndOr = tuple[Literal[e.Condition.And, e.Condition.Or], tuple["ConditionGroup", ...]]
_ConditionNot = tuple[Literal[e.Condition.Not], "ConditionGroup"]
_ConditionAirports = tuple[Literal[e.Condition.Airports], tuple[SourceAttribute, e.AirportType, tuple[str, ...]]]
_ConditionBookingDateOffset = tuple[Literal[e.Condition.BookingDateOffset], tuple[SourceAttribute, BookingOffsetCondition]]
_ConditionConditionalTags = tuple[Literal[e.Condition.ConditionalTags], tuple[SourceAttribute, Token, tuple[str, ...]]]
_ConditionDate = tuple[Literal[e.Condition.Date], tuple[e.DayType, SourceAttribute, DateCondition]]
_ConditionDayImpact = tuple[Literal[e.Condition.DayImpact], DayImpact]
_ConditionDuration = tuple[Literal[e.Condition.Duration], tuple[SourceAttribute, DurationCondition]]
_ConditionImpact = tuple[Literal[e.Condition.Impact], tuple[SourceAttribute, Token, tuple[str, ...]]]
_ConditionImply = tuple[Literal[e.Condition.Imply], tuple["ConditionGroup", "ConditionGroup"]]
_ConditionKeys = tuple[Literal[e.Condition.Keys], tuple[SourceAttribute, str, e.DayAllocation | None]]
_ConditionMatchEqual = tuple[Literal[e.Condition.MatchEqual], tuple[Match, ...]]
_ConditionPersonCount = tuple[Literal[e.Condition.PersonCount], tuple[SourceAttribute, PersonCount]]
_ConditionPersonImpact = tuple[Literal[e.Condition.PersonImpact], PersonImpact]
_ConditionTags = tuple[Literal[e.Condition.Tags], tuple[SourceAttribute, Token, tuple[str, ...], StringSlice]]
ConditionGroup: TypeAlias = _ConditionAndOr | _ConditionNot | _ConditionAirports | _ConditionBookingDateOffset | _ConditionConditionalTags | _ConditionDayImpact | _ConditionDate | _ConditionDuration | _ConditionImpact | _ConditionImply | _ConditionKeys | _ConditionMatchEqual | _ConditionPersonCount | _ConditionPersonImpact | _ConditionTags

_DayStateClosed = tuple[Literal[e.DayState.Closed]]
_DayStateOpen = tuple[Literal[e.DayState.Open], AvailabilityOpen | None]
DayState = _DayStateClosed | _DayStateOpen

_DefaultDayStateClosed = tuple[Literal[e.DefaultDayState.Closed]]
_DefaultDayStateOpen = tuple[Literal[e.DefaultDayState.Open], AvailabilityOpen | None]
DefaultDayState = _DefaultDayStateClosed | _DefaultDayStateOpen

class DefaultDayStateExtra(TypedDict, total=False):
    check_out: AvailabilityRequest | None

Availability = tuple[datetime.date, datetime.date, tuple[DefaultDayState, DefaultDayStateExtra], Mapping[Key, tuple[Offset, DayState]]]
Availabilities = tuple[ConditionGroup | None, Mapping[Key, Availability]]

_BookingParameterDate = tuple[Literal[e.BookingParameter.Date], e.DayType, SourceAttribute, e.DateFormat]
_BookingParameterPersonAge = tuple[Literal[e.BookingParameter.PersonAge], e.AgeType, e.DateFormat]
_BookingParameterTag = tuple[Literal[e.BookingParameter.Tag], SourceAttribute, Token]
_BookingParameterValue = tuple[Literal[e.BookingParameter.Value], str]
BookingParameterParam = _BookingParameterDate | _BookingParameterPersonAge | _BookingParameterTag | _BookingParameterValue

_CombinableWhenCode = tuple[Literal[e.CombinableWhen.Code], Identifier]
_CombinableWhenOr = tuple[Literal[e.CombinableWhen.Or], tuple["CombinableWhen", ...]]
CombinableWhen = _CombinableWhenCode | _CombinableWhenOr

class BookingParameter(TypedDict):
    field: e.Field
    index: int
    name: Name
    params: BookingParameterParam
    sep: tuple[SeparatorLeft, SeparatorRight]

_BookingGroupBookingParameter = tuple[Literal[e.BookingGroup.Parameter], BookingParameter]
_BookingGroupCondition = tuple[Literal[e.BookingGroup.Condition], ConditionGroup]
BookingGroupCondition = _BookingGroupBookingParameter | _BookingGroupCondition
BookingGroup = tuple[e.BookingGroupArea, SourceAttribute, tuple[BookingGroupCondition, ...], e.EvaluationBase | None]

DayAllocationStartEnd = tuple[DayAllocationLevel, SourceAttribute, e.DayReference, e.Shift]
_DayAllocationStart = tuple[Literal[e.DayAllocationPart.Start], DayAllocationStartEnd]
_DayAllocationEnd = tuple[Literal[e.DayAllocationPart.End], DayAllocationStartEnd]
DayAllocation = _DayAllocationStart | _DayAllocationEnd

_OccupancyPerson = tuple[Literal[e.Occupancy.Person], "OccupancyPerson"]
Occupancy = _OccupancyPerson

OptionalBookableAddonType = tuple[e.OptionalBookableAddonType, ShortServiceAnnotation]

_ParameterSetDistributorIdentificationGroup = tuple[Literal[e.ParameterSet.DistributorIdentificationGroup], e.CrsSystem, AgencyCode, BrandCode]
_ParameterSetDistributionChannel = tuple[Literal[e.ParameterSet.DistributionChannel], e.DistributionChannel]
_ParameterSetSalesChannel = tuple[Literal[e.ParameterSet.SalesChannel], e.SalesChannel]
_ParameterSetSalesMarket = tuple[Literal[e.ParameterSet.SalesMarket], ISO3166Country]
ParameterSet = _ParameterSetDistributorIdentificationGroup | _ParameterSetDistributionChannel | _ParameterSetSalesChannel | _ParameterSetSalesMarket

RuleDefinedComponent = tuple[e.Role, Name, DayAllocationLevel]
RuleOnewayFlightComponent = tuple[Name, DayAllocationIndex, DayAllocationLevel]
RuleSellingAccomComponent = tuple[Name, DayAllocationIndex]
RuleCombiComponent = tuple[e.Role, Name, DayAllocationIndex, tuple[RuleDefinedComponent, ...]]

_ComponentAccommodation = tuple[Literal[e.Component.Accommodation], tuple[RuleSellingAccomComponent, ...]]
_ComponentCombiComponent = tuple[Literal[e.Component.CombiComponent], RuleCombiComponent]
_ComponentDefinedComponent = tuple[Literal[e.Component.DefinedComponent], RuleDefinedComponent]
_ComponentOnewayFlight = tuple[Literal[e.Component.OnewayFlight], RuleOnewayFlightComponent]
Component = _ComponentAccommodation | _ComponentCombiComponent | _ComponentDefinedComponent | _ComponentOnewayFlight

_TagsDict = Mapping[Token, tuple[str, ConditionGroup | None]]
TagsDict = Mapping[Key, _TagsDict]

class Geocode(TypedDict):
    latitude: OWGS84Latitude
    longitude: OWGS84Longitude
    accuracy_km: int

class Geo(TypedDict, total=False):
    geocode: Geocode

class Address(TypedDict, total=False):
    city: LanguageText
    country: LanguageText
    geo: Geo
    phone: str
    street: str
    zip: str

class AccommodationInfo(TypedDict, total=False):
    giata: tuple[str, str]
    geonames: tuple[str, str]

class Combinatorics(TypedDict, total=False):
    code: tuple[Identifier, str]
    level: int
    when: CombinableWhen

class PriceItem(TypedDict, total=False):
    absolute: tuple[Decimal, tuple[AbsoluteCondition, ...]]
    combinatorics: Mapping[tuple[Identifier, LayerLevel], Combinatorics]
    condition: ConditionGroup

class Property(TypedDict, total=False):
    address: Address
    board_name: LanguageText
    board_type: e.BoardType
    city: tuple[LanguageText, ...]
    condition: ConditionGroup
    included_services: tuple[e.GeneralIncludedService, ...]
    info: AccommodationInfo
    name: LanguageText
    official_category: AccommodationCategory
    operator_category: AccommodationCategory
    optional_addons: tuple[OptionalBookableAddonType, ...]
    unit_facilities: tuple[e.UnitFacilities, ...]
    unit_name: LanguageText
    unit_types: tuple[e.UnitType, ...]

class Board(TypedDict, total=False):
    booking: tuple[BookingGroup, ...]
    properties: Mapping[Key, tuple[Property, ...]]
    tags: TagsDict

class SellingUnit(TypedDict, total=False):
    booking: Required[tuple[BookingGroup, ...]]
    occupancy: Required[Mapping[Key, tuple[Occupancy, ...]]]
    tags: TagsDict

class Unit(TypedDict, total=False):
    properties: Mapping[Key, tuple[Property, ...]]
    selling_units: Required[Mapping[Key, SellingUnit]]
    tags: TagsDict

class SellingAccom(TypedDict, total=False):
    board: Mapping[Key, Board]
    booking: tuple[BookingGroup, ...]
    filter: Mapping[Key, ConditionGroup]
    price_items: Mapping[Key, Mapping[Token, tuple[PriceItem, ...]]]
    tags: TagsDict
    unit: Mapping[Key, Unit]

class Accommodation(TypedDict, total=False):
    airports: tuple[SimpleNodeIataAirportCode, ...]
    availabilities: Mapping[Key, Availabilities]
    properties: Mapping[Key, tuple[Property, ...]]
    selling: Required[Mapping[Key, SellingAccom]]
    tags: TagsDict

class BookingClass(TypedDict, total=False):
    availabilities: Mapping[Key, Availabilities]

class Brand(TypedDict, total=False):
    booking: tuple[BookingGroup, ...]
    tags: TagsDict

class _DefineComponent(TypedDict, total=False):
    booking: tuple[BookingGroup, ...]
    components: Required[tuple[Component, ...]]
    filter: Mapping[Key, ConditionGroup]

DefineComponent = tuple[e.Role, _DefineComponent]

class Oneway(TypedDict, total=False):
    arrival: Required[SimpleNodeIataAirportCode]
    booking_class: Required[Mapping[Key, BookingClass]]
    departure: Required[SimpleNodeIataAirportCode]
    filter: Mapping[Key, ConditionGroup]

class Flights(TypedDict, total=False):
    oneway: Mapping[Key, Oneway]

class GlobalValue(TypedDict):
    params: Mapping[Key, ParameterSet]

class OccupancyPerson(TypedDict, total=False):
    count: int
    max_age: PersonAge
    min_age: PersonAge

class Product(TypedDict, total=False):
    components: Required[tuple[Component, ...]]
    day_allocation: tuple[DayAllocation, ...]
    filters: Mapping[Key, ConditionGroup]
    tags: TagsDict

class Products(TypedDict, total=False):
    globals: Mapping[Key, GlobalValue]
    product: Mapping[Key, tuple[e.ProductType, Product]]

class PropertyGroup(TypedDict, total=False):
    info: tuple[str, str]
