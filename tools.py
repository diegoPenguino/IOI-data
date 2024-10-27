import requests
from bs4 import BeautifulSoup
import pandas as pd
import time


def is_guest(participant: list):
    return not participant[0]


def no_country(participant: list):
    return not participant[2]


def check_irregularities(participant: list):
    if is_guest(participant):
        participant[0] = "Guest"
    if no_country(participant):
        participant[2] = "No country"
    return participant


def get_column_names(participant: list, number_of_tasks):
    task_number = 1
    column_names = ["Rank", "Name", "Country"]
    if number_of_tasks is not None:
        for i in range(number_of_tasks):
            column_names.append(f"Task_{i + 1}")
    else:
        for elem in participant:
            if "taskscore" in elem.get("class"):
                column_names.append(f"Task {task_number}")
                task_number += 1
    column_names.extend(["Score", "Rel_score(%)", "Award"])
    return column_names


def get_year_data(year: int, number_of_tasks=None):
    url = f"https://stats.ioinformatics.org/results/{year}"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    table = soup.find_all("table")[0]
    rows = table.find_all("tr")
    data = []
    for row in rows:
        cols = row.find_all("td")
        if cols == []:
            continue
        if not data:  # meaning first valid participant
            column_names = get_column_names(cols, number_of_tasks)
        participant = [elem.text.strip(" *%") for elem in cols]
        while len(participant) < len(column_names):
            participant.insert(-3, " ")
        data.append(check_irregularities(participant))

    df = pd.DataFrame(data, columns=column_names)
    df.replace("–", 0, inplace=True)

    return df


def get_all_data():
    first_IOI = 1989
    current_year = time.localtime().tm_year
    years = range(first_IOI, current_year + 1)
    all_years_data = pd.DataFrame()
    for year in years:
        print(f"Doing {year}", end="\r")
        df = get_year_data(year, 8)
        df.insert(0, "Year", year)

        if year == first_IOI:
            all_years_data = df.copy()
        else:
            all_years_data = pd.concat([all_years_data, df], ignore_index=True)
    print("Done!         ")
    return all_years_data
