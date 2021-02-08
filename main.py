import time

from compare import run, to_json
from pd import create_plot, manipulate_csv


def main():
    """
    Please comment:
    1. manipulate_csv, if you already have distinct_functions.csv
    2. run and to_json, if you already have analytics.json (this operation is quite
       long, so don't run it unless you need to)
    """
    start = time.time()
    filename = "functions_and_variables.csv"
    # gets unique list of functions for the .csv
    l = manipulate_csv(filename)
    print(f"{l} contracts are unique.")
    # creates the .json with the analysis of your smart contracts
    similarities = run()
    to_json(similarities)
    # presents the results
    create_plot()
    end = time.time()
    print(f"\n[{end - start}]")


main()
