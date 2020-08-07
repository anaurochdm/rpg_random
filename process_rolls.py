import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from collections import Counter
from statistics import mean, mode


ROLLS_FILE = "rolls_so_far.txt"
USERS = ["macabreengel", "Saros", "Fyrefly", "ButtyMcButtox", "TheKwarg"]
DICE_ROLL_PREFIX = "Details:"
MIN_DIE = 1
MAX_DIE = 10
SUCCESS_THRESHOLD = 7


def line_contains_user(line: str) -> bool:
    return any(user in line for user in USERS)


def is_dice_roll_results(line: str) -> bool:
    return DICE_ROLL_PREFIX in line


def user_from_line(line: str) -> str:
    return line.split("]")[1].split(":")[0][1:]


def parse_dice_roll_result(line: str) -> list:
    return [
        int(i) for i in line.split("(")[1].split(")")[0].split() if int(i) <= MAX_DIE
    ]


def get_rolls_by_user(data: list) -> dict:

    rolls_by_user = {user: [] for user in USERS}

    for line in data:

        if line_contains_user(line):
            user = user_from_line(line)

        elif is_dice_roll_results(line):
            rolls_by_user[user] += parse_dice_roll_result(line)

    return rolls_by_user


def count_successes(roll_list: list) -> int:
    successes = 0
    for roll in roll_list:
        if roll == MAX_DIE:
            successes += 2
        elif roll >= SUCCESS_THRESHOLD:
            successes += 1
    return successes / len(roll_list) * 100


def apply_function_for_users(
    user_rolls: dict, result_col_name: str, function
) -> pd.DataFrame:
    df_dict = {"user": [], result_col_name: []}
    for user, list_of_rolls in user_rolls.items():
        df_dict["user"].append(user)
        df_dict[result_col_name].append(function(list_of_rolls))
    return pd.DataFrame(df_dict)


def transpose_to_rolls_dataframe(user_rolls: dict) -> pd.DataFrame:
    df_dict = {"user": [], "roll": [], "percent": []}
    for user, list_of_rolls in user_rolls.items():
        rolls = Counter(list_of_rolls)
        assert sum([v for k, v in rolls.items()]) == len(list_of_rolls)
        for number, percent in rolls.items():
            df_dict["user"].append(user)
            df_dict["roll"].append(number)
            df_dict["percent"].append(percent / len(list_of_rolls) * 100)
    return pd.DataFrame(df_dict)


def plot_rolls_by_user(user_rolls: pd.DataFrame) -> None:
    sns.set_style("ticks")
    g = sns.FacetGrid(user_rolls, col="user", height=5, aspect=1)
    g.map(plt.bar, "roll", "percent")
    plt.xticks(range(MIN_DIE, MAX_DIE + 1))
    plt.show()


def plot_bar_quantity_by_user(quantity_by_user: pd.DataFrame, quantity: str) -> None:
    sns.set_style("ticks")
    sns.barplot(
        y="user",
        x=quantity,
        data=quantity_by_user.sort_values(quantity, ascending=False),
    )
    plt.show()


def plot_scatter_quantity_by_user(quantity_by_user: pd.DataFrame, quantity: str) -> None:
    sns.set_style("ticks")
    sns.scatterplot(
        y="user",
        x=quantity,
        data=quantity_by_user.sort_values(quantity, ascending=False),
    )
    plt.show()
