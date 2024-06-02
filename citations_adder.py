"""
This functions utilises the google scholar API to add citations to a list of
papers. It takes a paper and returns the paper with the
citations added.
"""
import os
from typing import Union

from scholarly import scholarly
from scholarly import ProxyGenerator


def get_proxy():
    """
    This function returns a proxy generator.
    """
    proxy = ProxyGenerator()
    proxy.FreeProxies()
    return proxy


def add_citations(paper):
    """
    This function takes a paper and returns the paper with the
    citations added.

    """
    # Get the paper
    paper = scholarly.search_pubs(paper)
    # Get the number of citations
    citations = paper.pub_parser
    # Print the number of citations
    print(citations)


def main():
    """
    This is the main function that is run when the file is run.
    """
    # Get the proxy
    proxy = get_proxy()
    # Set the proxy
    scholarly.use_proxy(proxy)

    paper: Union[str, bytes, os.PathLike[str], os.PathLike[bytes]] = "./\
    docx_files/selva.docx"

    add_citations(paper)


if __name__ == "__main__":
    main()
