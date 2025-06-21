import pytest
import csv
import os
from constants import Aggregation, Filter
from tempfile import NamedTemporaryFile
from csv_functions import filter_file, aggregate_file, parse_filter_args, read_csv


@pytest.fixture
def sample_file():
    data = [
        {"name": "Jordan", "team": "Chicago Bulls", "points": "50", "assists": "3.1"},
        {
            "name": "James",
            "team": "Los Angeles Lakers",
            "points": "25",
            "assists": "5.9",
        },
        {
            "name": "Harden",
            "team": "Los Angeles Clippers",
            "points": "36",
            "assists": "7.0",
        },
        {
            "name": "Doncic",
            "team": "Los Angeles Lakers",
            "points": "30",
            "assists": "5.0",
        },
    ]
    headers = ["name", "team", "points", "assists"]

    with NamedTemporaryFile(mode="w", delete=False, suffix=".csv") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)
        f.flush()
        yield f.name
    os.unlink(f.name)


def test_read_csv(sample_file):
    headers, rows = read_csv(sample_file)
    assert headers == ["name", "team", "points", "assists"]
    assert len(rows) == 4
    assert rows[2]["name"] == "Harden"


def test_filter_eq(sample_file):
    _, rows = read_csv(sample_file)
    filtered = filter_file(rows, "team", Filter.EQ, "Los Angeles Lakers")
    assert len(filtered) == 2
    assert all(row["team"] == "Los Angeles Lakers" for row in filtered)


def test_filter_lt(sample_file):
    _, rows = read_csv(sample_file)
    filtered = filter_file(rows, "points", Filter.LT, "35")
    assert len(filtered) == 2
    assert all(float(row["points"]) < 35 for row in filtered)


def test_filter_gt(sample_file):
    _, rows = read_csv(sample_file)
    filtered = filter_file(rows, "assists", Filter.GT, "5.0")
    assert len(filtered) == 2
    assert all(float(row["assists"]) > 5.0 for row in filtered)


def test_parse_filter_args():
    assert parse_filter_args("team==Los Angeles Lakers") == (
        "team",
        Filter.EQ,
        "Los Angeles Lakers",
    )
    assert parse_filter_args("points<35.0") == ("points", Filter.LT, "35.0")
    assert parse_filter_args("assists>5.0") == ("assists", Filter.GT, "5.0")
    assert parse_filter_args("invalid") is None


def test_aggregate_avg(sample_file):
    _, rows = read_csv(sample_file)
    result = aggregate_file(rows, "points", Aggregation.AVG)
    assert round(result["value"], 2) == 35.25


def test_aggregate_min(sample_file):
    _, rows = read_csv(sample_file)
    result = aggregate_file(rows, "assists", Aggregation.MIN)
    assert result["value"] == 3.1


def test_aggregate_max(sample_file):
    _, rows = read_csv(sample_file)
    result = aggregate_file(rows, "points", Aggregation.MAX)
    assert result["value"] == 50


def test_aggregate_non_numeric(sample_file):
    _, rows = read_csv(sample_file)
    result = aggregate_file(rows, "team", Aggregation.AVG)
    assert "error" in result
