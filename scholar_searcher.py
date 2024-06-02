"""
This module is designed to be run as a side script.
It fetches links from Google Scholar and returns
them as a JSON object. The links are then used to provide
the articles which are then used to provide the user
with the information they need.
"""
import os
from typing import Any

from dotenv import load_dotenv  # pip install python-dotenv
from serpapi import GoogleSearch  # pip install

# load api_key from .env file
load_dotenv()
api_key = os.getenv("api_key")


def searcher(query: str) -> dict[Any, Any]:
    """
    This function takes in a query and returns a JSON object
    containing the links to the articles.
    """

    params: dict[str, str] = {
      "api_key": f"{api_key}",
      "engine": "google_scholar",
      "q": f"{query}",
    }

    search = GoogleSearch(params)

    results = search.get_dict()

    if "organic_results" in results.keys():
        new_results = results["organic_results"]
        # new_results is now a list of dicts...
        # convert it to a dict
        new_results = {i: new_results[i] for i in range(0, len(new_results))}
        return new_results

    return results


def link_parser(links: dict) -> list[str]:
    """
    This function takes in a list or a dict, and
    searches for the link key in the dict and returns
    a list of links.
    """

    wanted_links: list[str] = []

    # Go through the nested inner dictionaries looking for link key
    # if found, append the value to the wanted_links list
    for key in links.keys():
        if isinstance(links[key], dict):
            for inner_key in links[key].keys():
                if inner_key == "link":
                    wanted_links.append(links[key][inner_key])

    return wanted_links


def main():
    query: str = '''Sharma, A., Modak, S., & Sridhar, E. (2019). Data
                    visualization and stock market and prediction.
                    International Research Journal of Engineering
                    and Technolog,6(9), 2037-2040.'''

    json_obj: dict = searcher(query)

    print(link_parser(json_obj))


if __name__ == "__main__":
    main()
