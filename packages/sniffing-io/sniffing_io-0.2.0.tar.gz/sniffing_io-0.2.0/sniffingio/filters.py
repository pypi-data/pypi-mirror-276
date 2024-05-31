# filters.py

from typing import Iterable, Callable, ClassVar, Self
from dataclasses import dataclass, asdict
from abc import ABCMeta, abstractmethod

from dacite import from_dict

from scapy.all import Packet, sniff

__all__ = [
    "PacketFilterOperand",
    "PacketFilter",
    "PacketFilterIntersection",
    "PacketFilterOperator",
    "PacketFilterUnion",
    "PacketFilterNegation",
    "BasePacketFilterUnion",
    "BasePacketFilter",
    "StaticPacketFilter",
    "BasePacketFilterOperator",
    "BasePacketFilterIntersection",
    "format_packet_filters",
    "LivePacketFilter",
    "dump_packet_filter",
    "load_packet_filter",
    "PacketFilterValues",
    "Types",
    "Names",
    "pf",
    "pfv"
]

def wrap(value: str) -> str:

    if (" " in value) and not (value.startswith("(") and value.endswith(")")):
        value = f"({value})"

    return value

class Names:

    HOST = 'host'
    PORT = 'port'
    SRC = 'src'
    DST = 'dst'

class Types:

    TCP = 'tcp'
    UDP = 'udp'
    ICMP = 'icmp'
    SMTP = 'smtp'
    MAC = 'mac'

class BasePacketFilterOperator(metaclass=ABCMeta):

    @staticmethod
    def format_join(values: Iterable[str], joiner: str) -> str:

        if not values:
            return ""

        values = tuple(str(value) for value in values)

        if len(values) == 1:
            return wrap(values[0])

        data = f" {joiner} ".join(wrap(value) for value in values if value)

        return f"({data})"

class BasePacketFilterUnion(BasePacketFilterOperator, metaclass=ABCMeta):

    @classmethod
    def format_union(cls, values: Iterable[str]) -> str:

        return cls.format_join(values, joiner="or")

class BasePacketFilterIntersection(BasePacketFilterOperator, metaclass=ABCMeta):

    @classmethod
    def format_intersection(cls, values: Iterable[str]) -> str:

        return cls.format_join(values, joiner="and")

class BasePacketFilter(
    BasePacketFilterUnion,
    BasePacketFilterIntersection,
    metaclass=ABCMeta
):

    @abstractmethod
    def format(self) -> str:

        return ""

@dataclass(slots=True, frozen=True)
class PacketFilterOperand(BasePacketFilter, metaclass=ABCMeta):

    def __invert__(self) -> "PacketFilterOperand":

        if isinstance(self, PacketFilterNegation):
            return self.filter

        return PacketFilterNegation(self)

    def __or__(self, other: ...) -> "PacketFilterUnion":

        if isinstance(other, PacketFilterOperand):
            filters = []

            if isinstance(self, PacketFilterUnion):
                filters.extend(self.filters)

            else:
                filters.append(self)

            if isinstance(other, PacketFilterUnion):
                filters.extend(other.filters)

            else:
                filters.append(other)

            return PacketFilterUnion(tuple(filters))

        return NotImplemented

    def __and__(self, other: ...) -> "PacketFilterIntersection":

        if isinstance(other, PacketFilterOperand):
            filters = []

            if isinstance(self, PacketFilterIntersection):
                filters.extend(self.filters)

            else:
                filters.append(self)

            if isinstance(other, PacketFilterIntersection):
                filters.extend(other.filters)

            else:
                filters.append(other)

            return PacketFilterIntersection(tuple(filters))

        return NotImplemented

    @classmethod
    def load(cls, data: dict[str, ...]) -> Self:

        return from_dict(cls, data)

    def dump(self) -> dict[str, ...]:

        return asdict(self)

    @abstractmethod
    def match(self, packet: Packet) -> bool:

        pass

@dataclass(slots=True, frozen=True)
class StaticPacketFilter(PacketFilterOperand):

    filter: str

    def format(self) -> str:

        return self.filter

    def match(self, packet: Packet) -> bool:

        return len(sniff(offline=packet, filter=self.filter, verbose=0)) > 0

@dataclass(slots=True, frozen=True)
class PacketFilterOperator(PacketFilterOperand, metaclass=ABCMeta):

    filters: tuple[PacketFilterOperand, ...]

    def __len__(self) -> int:

        return len(self.filters)

@dataclass(slots=True, frozen=True)
class PacketFilterUnion(PacketFilterOperator, BasePacketFilterUnion):

    def format(self) -> str:

        return self.format_union((f.format() for f in self.filters or ()))

    def match(self, packet: Packet) -> bool:

        return any(f.match(packet) for f in self.filters)

@dataclass(slots=True, frozen=True)
class PacketFilterIntersection(PacketFilterOperator, BasePacketFilterIntersection):

    def format(self) -> str:

        return self.format_intersection((f.format() for f in self.filters or ()))

    def match(self, packet: Packet) -> bool:

        return all(f.match(packet) for f in self.filters)

@dataclass(slots=True, frozen=True)
class PacketFilterNegation(PacketFilterOperand):

    filter: PacketFilterOperand

    ATTRIBUTES: ClassVar[set[str]] = {'filter'}

    def format(self) -> str:

        data = self.filter.format()

        if not data:
            return ""

        return f"(not {data})"

    def match(self, packet: Packet) -> bool:

        return self.filter.match(packet)

def layers_names(packet: Packet) -> list[str]:

    names = [packet.name]

    while packet.payload:
        packet = packet.payload

        names.append(packet.name)

    return names

@dataclass(slots=True, frozen=True)
class PacketFilterValues[T](PacketFilterOperand):

    types: list[str] = None
    names: list[str] = None
    values: list[T] = None
    source_values: list[T] = None
    destination_values: list[T] = None
    attributes: dict[str, list[T]] = None

    @classmethod
    def load(cls, data: dict[str, list[T]]) -> "PacketFilterValues[T]":

        return from_dict(cls, data)

    def dump(self) -> dict[str, list[T]]:

        return asdict(self)

    @classmethod
    def format_values(cls, values: Iterable[str], key: str = None) -> str:

        if not values:
            return ""

        return cls.format_union(
            (
                " ".join((key, str(value)) if key else (str(value),))
                for value in values
                if value
            )
        )

    def format(self) -> str:

        values = [
            self.format_union(values)
            for values in (
                self.types,
                (
                    self.format_values(self.values, key=name)
                    for name in self.names or ['']
                ),
                (
                    self.format_values(
                        self.source_values, key=' '.join(['src', name])
                    )
                    for name in self.names or ['']
                ),
                (
                    self.format_values(
                        self.destination_values, key=' '.join(['dst', name])
                    )
                    for name in self.names or ['']
                )
            )
            if values
        ]

        values = [value for value in values if value]

        return self.format_intersection(values)

    def match(self, packet: Packet) -> bool:

        for layer in packet.layers():
            if (
                (self.types is not None) and
                (layer.name.lower() not in {n.lower() for n in self.types})
            ):
                return False

            if (
                self.attributes and
                not all(
                    hasattr(packet, attr) and
                    getattr(packet, attr) in values
                    for attr, values in self.attributes.items()
                )
            ):
                return False

            if hasattr(layer, 'src'):
                src = layer.src
                dst = layer.dst

            elif hasattr(layer, 'sport'):
                src = layer.sport
                dst = layer.dport

            else:
                continue

            sources = (self.values or []) + (self.source_values or [])
            destinations = (self.values or []) + (self.destination_values or [])

            if (
                (sources and (src not in sources)) or
                (destinations and (dst not in destinations))
            ):
                return False

        return True

@dataclass(slots=True, frozen=True, eq=False)
class PacketFilter(PacketFilterOperand):

    layers: list[PacketFilterValues] = None

    def match(self, packet: Packet) -> bool:

        for layer, layer_filter in zip(packet.layers(), self.layers):
            if layer_filter is None:
                continue

            layer_filter: PacketFilterValues

            if not layer_filter.match(layer):
                return False

        return True

    def format(self) -> str:

        return self.format_intersection(layer.format() for layer in self.layers)

def format_packet_filters(
        filters: BasePacketFilter | Iterable[BasePacketFilter],
        joiner: PacketFilterOperator = PacketFilterUnion
) -> str:

    if joiner is None:
        joiner = PacketFilterUnion

    if isinstance(filters, PacketFilterOperand):
        return filters.format()

    return joiner(tuple(filters)).format()

@dataclass(slots=True)
class LivePacketFilter:

    validator: Callable[[Packet], bool]

    disabled: bool = False

    def __call__(self, *args, **kwargs) -> bool:

        return self.validate(*args, **kwargs)

    def disable(self) -> None:

        self.disabled = True

    def enable(self) -> None:

        self.disabled = False

    def validate(self, packet: Packet) -> bool:

        if self.disabled:
            return True

        result = self.validator(packet)

        return result

PF = (
    PacketFilter |
    PacketFilterUnion |
    PacketFilterIntersection |
    PacketFilterNegation |
    StaticPacketFilter
)

def dump_packet_filter(data: PF) -> dict[str, ...]:

    return data.dump()

def load_packet_filter(data: PF | str | dict[str, ...]) -> PF:

    if isinstance(data, PacketFilterOperand):
        return data

    if isinstance(data, str):
        return StaticPacketFilter(data)

    return PacketFilterOperand.load(data)

pfv = PacketFilterValues
pf = PacketFilter
