import argparse
from tabulate import tabulate
from constants import Aggregation
from csv_functions import read_csv, parse_filter_args, aggregate_file, filter_file


def main():
    parser = argparse.ArgumentParser(description="CSV parser")
    parser.add_argument("file_path", help="Path to file")
    parser.add_argument("--where", help="Filter")
    parser.add_argument("--aggregate", help="Aggregation")

    args = parser.parse_args()

    try:
        headers, rows = read_csv(args.file_path)
    except FileNotFoundError:
        print(f"Error: File {args.filepath} not found")
        return
    except Exception as e:
        print(f"Error: {e}")
        return

    if args.where:
        filter_params = parse_filter_args(args.where)
        if not filter_params:
            print("Invalid filter args format. Try '<column_name><operator><value>'")
            return
        column, op, value = filter_params
        if column not in headers:
            print(f"Error: Column {column} not found in file")
            return
        rows = filter_file(rows, column, op, value)

    if args.aggregate:
        agg_parts = args.aggregate.split(":")
        if len(agg_parts) != 2 or any([len(x) == 0 for x in agg_parts]):
            print("Invalid aggregation format. Try '<agg_type>:<column_name>'")
            return
        agg_type_str, column = agg_parts
        if column not in headers:
            print(f"Error: Column {column} not found in file")
            return
        try:
            agg_type = Aggregation.from_string(agg_type_str)
        except ValueError:
            print(f"Error: Unknown aggregation type {agg_type_str}")
            return

        result = aggregate_file(rows, column, agg_type)
        if "error" in result:
            print(result["error"])
        else:
            print(tabulate([result.values()], headers=result.keys(), tablefmt="grid"))
    else:
        if rows:
            print(tabulate(rows, headers="keys", tablefmt="grid"))
        else:
            print("No data")


if __name__ == "__main__":
    main()
