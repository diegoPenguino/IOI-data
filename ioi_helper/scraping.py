from requests import get as get_url
from bs4 import BeautifulSoup
import pandas as pd
from os import path, makedirs

first_IOI = 1989
current_year = 2024  # UPDATE next year
directory_contests = "data/contests"
directory_admin = "data/administration"


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
    if year_data_exists(year):
        return pd.read_csv(f"{directory_contests}/annual/{year}_data.csv")
    makedirs(directory_contests + "/annual", exist_ok=True)
    data = scrape_year_data(year, number_of_tasks)
    data.to_csv(
        f"{directory_contests}/annual/{year}_data.csv", index=False, encoding="utf-8"
    )
    return data


def scrape_year_data(year: int, number_of_tasks=None):
    url = f"https://stats.ioinformatics.org/results/{year}"
    page = get_url(url)
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
    if all_data_exists():
        return pd.read_csv(f"{directory_contests}/IOI_data.csv")
    makedirs(directory_contests, exist_ok=True)
    data = scrape_all_data()
    data.to_csv(f"{directory_contests}/IOI_data.csv", index=False, encoding="utf-8")

    return data


def scrape_all_data():
    years = range(first_IOI, current_year + 1)
    all_years_data = []

    for year in years:
        print(f"Scraping {year}", end="\r")
        df = get_year_data(year, 8)
        df.insert(0, "Year", year)
        all_years_data.append(df)

    print(" " * 50, end="\r")
    all_years_data = pd.concat(all_years_data, ignore_index=True)
    return all_years_data


def scrape_administration_by_year(year):
    url = f"https://stats.ioinformatics.org/administration/{year}"
    page = get_url(url)
    soup = BeautifulSoup(page.content, "html.parser")

    members = soup.find_all("a", class_="delegationmember")

    data = []
    for member in members:
        info = member.find_all("div")
        member_data = [val.text for val in info]
        data.append(member_data)

    df = pd.DataFrame(data, columns=["Name", "Role"])
    return df


def get_administration_by_year(year):
    if admin_annual_exists(year):
        return pd.read_csv(f"{directory_admin}/annual/administration_{year}.csv")
    df = scrape_administration_by_year(year)
    makedirs(directory_admin + "/annual", exist_ok=True)
    df.to_csv(f"{directory_admin}/annual/administration_{year}.csv", index=False)
    return df


def scrape_all_administration():
    years = range(first_IOI, current_year + 1)
    all_years = []

    for year in years:
        print(f"Scraping {year}", end="\r")
        year_data = get_administration_by_year(year)
        year_data.insert(0, "Year", year)
        all_years.append(year_data)

    print(" " * 50, end="\r")
    data = pd.concat(all_years, ignore_index=True)
    return data


def get_all_administration():
    if all_admin_exists():
        return pd.read_csv(f"{directory_admin}/administration.csv")
    makedirs(directory_admin, exist_ok=True)
    data = scrape_all_administration()
    data.to_csv(f"{directory_admin}/administration.csv", index=False)
    return data


def year_data_exists(year: int) -> bool:
    return path.exists(f"{directory_contests}/annual/{year}_data.csv")


def all_data_exists() -> bool:
    return path.exists(f"{directory_contests}/IOI_data.csv")


def admin_annual_exists(year):
    return path.exists(f"{directory_admin}/annual/administration_{year}.csv")


def all_admin_exists():
    return path.exists(f"{directory_admin}/administration.csv")
