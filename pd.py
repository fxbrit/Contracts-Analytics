import json
from operator import itemgetter

import edlib
import matplotlib.pyplot as plt
import pandas


def manipulate_csv(filename):
    data_frame = pandas.read_csv(filename)
    s = data_frame["functions"].value_counts()
    s.to_csv("distinct_functions.csv")
    return len(s)


def create_plot():
    indexes = []
    matches = []
    columns = []
    functions = []
    erc20_stopwords = (
        get_stopwords()
    )  # list of mandatory rules and events for erc20 standard
    with open("analytics.json") as json_file:
        data = json.load(json_file)
    sorted_data = sorted(
        data, key=itemgetter("identical"), reverse=True
    )  # by changing key you can sort differently elements from .json
    for d in sorted_data:
        spl_df = d["functions"].split()
        result_df = [word for word in spl_df if word not in erc20_stopwords]
        is_variation = False
        final_df = " ".join(result_df)
        if len(final_df) == 0:
            continue
        for f in functions:
            spl_f = f.split()
            result_f = [word for word in spl_f if word not in erc20_stopwords]
            final_f = " ".join(result_f)
            if get_difference(final_df, final_f) <= 50:
                is_variation = True
                separator()
                print(f"{final_df} ---> grouped into ---> {final_f}")
                ind = int(functions.index(f)) * 2 + 1
                new_sim = matches[ind] + d["similar"]
                matches[ind] = new_sim
                separator()
                break
        if is_variation == True:
            continue
        else:
            functions.append(d["functions"])
            separator()
            print(f'[-] index: {d["index"]} - {final_df}')
            separator()
            indexes.append(d["index"])
            indexes.append(d["index"])
            matches.append(d["identical"])
            matches.append(d["similar"])
            columns.append("identical fuctions")
            columns.append("similar functions (matching >= 50%)")
        if len(indexes) == 20:
            break
    layout = {"index": indexes, "matches": matches, "columns": columns}
    data_frame = pandas.DataFrame(layout)
    pivot_t = data_frame.pivot(index="index", columns="columns", values="matches")
    print("\n\n")
    print(pivot_t)
    colors = [(0.85, 0.55, 0.35), (0.35, 0.60, 0.8)]
    pivot_t.loc[
        :, ["identical fuctions", "similar functions (matching >= 50%)"]
    ].plot.bar(stacked=True, color=colors, figsize=(10, 7))
    plt.show()


def get_difference(function_1, function_2):
    length = len(function_1)
    align = edlib.align(function_1, function_2)["editDistance"]
    difference_coeff = align * 100 / length
    rounded = round(int(round(difference_coeff, 0)), -1)
    return rounded


def separator():
    print("-----------------------------------------------------")


def get_stopwords():
    stopwords = [
        "allowance",
        "Approval",
        "approve",
        "balanceOf",
        "totalSupply",
        "transfer",
        "Transfer",
        "transferFrom",
    ]
    return stopwords
