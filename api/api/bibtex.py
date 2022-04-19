# style from bibtex to other

from bibtexparser.bparser import BibTexParser

# bibtex_str = """@article{10.2307/1969529,
#  ISSN = {0003486X},
#  URL = {http://www.jstor.org/stable/1969529},
#  author = {John Nash},
#  journal = {Annals of Mathematics},
#  number = {2},
#  pages = {286--295},
#  publisher = {Annals of Mathematics},
#  title = {Non-Cooperative Games},
#  urldate = {2022-04-19},
#  volume = {54},
#  year = {1951}
# }"""

def bibtex_load(bibtex_str):
    parser = BibTexParser()
    parser.ignore_nonstandard_types = False
    parser.homogenize_fields = False
    parser.common_strings = False
    bib_database = bibtexparser.loads(bibtex_str, parser)
    return bib_database

def bibtex_dump(bib_database):
    bibtex_str = bibtexparser.dumps(bib_database)
    return bibtex_str