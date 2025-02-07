# rit-schedule-scraper
This scraper is made specifically to scrape table from the rit bus schedule site and generate csv file.


## package manager
This tool uses [uv](https://docs.astral.sh/uv/) for managing python environments and dependencies. Download uv from the link [here](https://docs.astral.sh/uv/getting-started/installation/).

## setup project
You can clone this repository and initiate uv by running `uv sync`. Once successfully installed the dependencies, you can run `uv run main.py <link_1> <link_2> ...`.

## command line arguments
* `uv run main.py -h`: Help command. Shows more detailed and accurate description of the command line arguments.
* `uv run main.py [links]`: Scrapes from each links and saves the table in the csv file in the `data` directory.
* `uv run main.py --data_path <directory_path> [links]`: Same as above, but saves the csv in `directory_path`.