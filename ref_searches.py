"""
Module documentation
"""
from ref_checkers import get_citations_and_references_dict
from ref_checkers import get_inline_citations_dict
from scholar_searcher import link_parser
from scholar_searcher import searcher


# Loop through all citations and references from the given imports
# and check if the citation is in the references
def ref_iterator() -> dict:
    """
    Function documentation
    """
    citations_and_references: dict = get_citations_and_references_dict()
    inline_citations: dict = get_inline_citations_dict()

    # Map the references to the sentences used as values in inline_citations
    new_stmt_ref: dict = {}

    for citation in inline_citations.keys():
        if citation in citations_and_references.keys():

            key_stmt = inline_citations[citation]
            val_stmt = citations_and_references[citation]

            new_stmt_ref[key_stmt] = val_stmt

    return new_stmt_ref


def get_ref_as_list() -> list:
    """Get the references as a list"""
    ref_dict = ref_iterator()

    return list(ref_dict.values())


def main():
    """Main function"""
    ref_list = get_ref_as_list()

    for ref in ref_list:
        if isinstance(ref, list):
            for item in ref:
                print(link_parser(searcher(item)))

        print(link_parser(searcher(ref[0])))


if __name__ == "__main__":
    main()
