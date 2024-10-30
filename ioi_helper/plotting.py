import matplotlib.pyplot as plt
from .scraping import get_year_data
from numpy import linspace, arange


plt.style.use("seaborn-v0_8-dark")


def plot_shadow(n_participants, min_score, max_score, color, ax):
    all_x = range(1, n_participants)
    ax.fill_between(all_x, min_score, max_score, color=color, alpha=0.3)


def plot_prize_vs_score(year):
    fig, ax = plt.subplots()
    participants = get_year_data(year)
    participants = participants[participants["Rank"] != "Guest"]
    golden = participants[participants["Award"] == "Gold"]
    silver = participants[participants["Award"] == "Silver"]
    bronze = participants[participants["Award"] == "Bronze"]
    no_award = participants.drop(golden.index).drop(silver.index).drop(bronze.index)

    min_gold = golden["Score"].min()
    max_gold = golden["Score"].max()
    min_silver = silver["Score"].min()
    max_silver = silver["Score"].max()
    min_bronze = bronze["Score"].min()
    max_bronze = bronze["Score"].max()

    gold_label = f"Gold ({min_gold} - {max_gold})"
    silver_label = f"Silver ({min_silver} - {max_silver})"
    bronze_label = f"Bronze ({min_bronze} - {max_bronze})"

    ax.scatter(golden["Rank"], golden["Score"], label=gold_label, color="gold", s=10)
    ax.scatter(
        silver["Rank"], silver["Score"], label=silver_label, color="silver", s=10
    )
    ax.scatter(bronze["Rank"], bronze["Score"], label=bronze_label, color="brown", s=10)
    ax.scatter(
        no_award["Rank"], no_award["Score"], label="No Award", color="gray", s=10
    )
    participants["Rank"] = participants["Rank"].astype(int)
    n_positions = int(participants["Rank"].max())

    plot_shadow(n_positions, min_gold, max_gold, "gold", ax)
    plot_shadow(n_positions, min_silver, max_silver, "silver", ax)
    plot_shadow(n_positions, min_bronze, max_bronze, "brown", ax)

    ax.set_xlabel("Rank")
    ax.set_ylabel("Score")
    ax.set_xticks(linspace(0, n_positions + 2, 10))
    ax.set_yticks(arange(0, 601, 100))
    ax.set_title(f"IOI {year} Participants ({len(participants)} contestants)")
    ax.legend()
    plt.show()
