import argparse
from dataclasses import dataclass
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup


@dataclass(frozen=True)
class ScraperArguments:
    links: list[str]
    data_path: str = "data"  # Default value


def get_arguments() -> ScraperArguments:
    parser = argparse.ArgumentParser(
        description="Process a named argument and multiple links."
    )

    # Define the parameterized argument (e.g., --name value)
    parser.add_argument(
        "--data_path", help="An optional named parameter.", default="./data"
    )

    # Define positional arguments for links
    parser.add_argument("links", nargs="*", help="List of links.")

    args = parser.parse_args()
    return ScraperArguments(args.links, args.data_path)


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


def main():
    args = get_arguments()

    # Create data directory if it does not exist
    Path(args.data_path).mkdir(parents=True, exist_ok=True)

    for link in args.links:
        t = parse(link)
        if not t:
            print(f"Failed {link}")
            continue
        df = table_to_df(t)
        new_filename = Path(args.data_path, f"{link.split('/')[-1]}.csv")
        df_to_csv(df, new_filename)
        print(f"Success {link}\n{new_filename}")
    print("All done")


if __name__ == "__main__":
    main()
