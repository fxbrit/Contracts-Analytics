import csv
import json

import edlib


def run():
    filename = "distinct_functions.csv"
    similarities = list()
    with open(filename, "r") as main_file:
        main_reader = csv.reader(main_file)
        for counter, main_row in enumerate(main_reader):
            to_compare = main_row[0].translate(
                str.maketrans({"[": "", "]": "", "'": "", ",": ""})
            )
            length = len(to_compare)
            if length == 0:
                continue
            layout = {
                "index": counter,
                "functions": to_compare,
                "total_matches": 0,
                "identical": int(main_row[1]),
                "similar": 0,
            }
            with open(filename, "r") as f:
                reader = csv.reader(f)
                for row in reader:
                    compare_row = row[0].translate(
                        str.maketrans({"[": "", "]": "", "'": "", ",": ""})
                    )
                    align = edlib.align(to_compare, compare_row)["editDistance"]
                    difference_coeff = align * 100 / length
                    rounded = round(int(round(difference_coeff, 0)), -1)
                    if rounded <= 30:  # max amount of difference
                        layout["total_matches"] += int(row[1])
            layout["similar"] = int(layout["total_matches"]) - int(layout["identical"])
            similarities.append(layout)
            print(f"Processed: {counter}", end="\r")
            if len(similarities) == 30000:
                break
    return similarities


def to_json(similarities):
    with open("analytics.json", "w") as fout:
        json.dump(similarities, fout, indent=4)


def categorize():
    filename = "functions_and_variables"
    with open(filename, "r"):
        print("hello")
