import sys

import pandas as pd
import requests
from bs4 import BeautifulSoup


def parse(url: str):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Extract all links from the page
    tables = [t for t in soup.find_all("table")]
    if not tables:
        print("Error: No tables found")
        return
    if len(tables) > 1:
        print("Error: Multiple tables found")
        return
    return tables[0]


def table_to_df(table):
    header = table.find_all("th")
    header = [ele.text.strip() for ele in header]

    rows = table.find_all("tr")
    data = []
    for row in rows:
        cols = row.find_all("td")
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])
    data = list(filter(lambda x: len(x) != 0, data))
    return pd.DataFrame(data, columns=header)


def df_to_csv(df, filename):
    df.to_csv(filename, index=False)


def main(*links):
    for link in links:
        t = parse(link)
        if not t:
            print(f"Failed {link}")
            continue
        df = table_to_df(t)
        new_filename = f"{link.split('/')[-1]}.csv"
        df_to_csv(df, new_filename)
        print(f"Success {link}\n{new_filename}")
    print("All done")


if __name__ == "__main__":
    main(*sys.argv[1:])
