from enum import Enum, auto


class Filter(Enum):
    EQ = auto()
    GT = auto()
    LT = auto()

    @staticmethod
    def from_string(op: str) -> "Filter":
        op_map = {
            "==": Filter.EQ,
            "=": Filter.EQ,
            ">": Filter.GT,
            "<": Filter.LT,
        }
        return op_map.get(op, None)


class Aggregation(Enum):
    AVG = auto()
    MIN = auto()
    MAX = auto()

    @staticmethod
    def from_string(agg: str) -> "Aggregation":
        agg_map = {
            "avg": Aggregation.AVG,
            "min": Aggregation.MIN,
            "max": Aggregation.MAX,
        }
        return agg_map.get(agg.lower(), None)
