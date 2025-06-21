from typing import Any, Dict, List, Optional, Tuple, Union
from constants import Aggregation, Filter
import csv


def read_csv(file_path: str) -> Tuple[List[str], List[Dict[str, Any]]]:
    with open(file_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []
        rows = [row for row in reader]
    return headers, rows


def filter_file(
    rows: List[Dict[str, Any]], column: str, operator: Filter, value: Any
) -> List[Dict[str, Any]]:
    filtered_rows = []
    for r in rows:
        r_value = r[column]
        if operator == Filter.EQ and r_value == value:
            filtered_rows.append(r)
        elif operator == Filter.LT:
            try:
                if float(r_value) < float(value):
                    filtered_rows.append(r)
            except ValueError:
                if r_value < value:
                    filtered_rows.append(r)
        elif operator == Filter.GT:
            try:
                if float(r_value) > float(value):
                    filtered_rows.append(r)
            except ValueError:
                if r_value > value:
                    filtered_rows.append(r)
    return filtered_rows


def aggregate_file(
    rows: List[Dict[str, Any]], column: str, agg: Aggregation
) -> Dict[str, Union[float, str]]:
    try:
        values = [float(row[column]) for row in rows]
    except ValueError:
        return {"error": f"Non-numeric value in column {column}"}

    if not values:
        return {"error": "Now rows to aggregate"}

    if agg == Aggregation.AVG:
        result = sum(values) / len(values)
    elif agg == Aggregation.MIN:
        result = min(values)
    elif agg == Aggregation.MAX:
        result = max(values)
    else:
        return {"error": f"Invalid aggregation type"}
    return {"column": column, "type": agg.name.lower(), "value": result}


def parse_filter_args(filter_args: Optional[str]) -> Optional[Tuple[str, Filter, str]]:
    if not filter_args:
        return None

    for op in ["==", "=", "<", ">"]:
        if op in filter_args:
            parts = filter_args.split(op)
            if len(parts) == 2 and all([len(x) != 0 for x in parts]):
                column = parts[0]
                value = parts[1]
                return column, Filter.from_string(op), value
    return None
