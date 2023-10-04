import os
import re
import datetime
import bibtexparser
from pathlib import Path
from urllib.request import urlopen


authors_folders = [x[0] for x in os.walk('content/authors')]

dblp_urls = []

for author_folder in authors_folders:
    index_filename = os.path.join(author_folder, '_index.md')
    if Path(index_filename).is_file():
        with open(index_filename, 'r') as index_file:
            content = index_file.read()
            search = re.search("- icon: dblp\n.*\n.*link\: ?(.*)", content)
            if search:
                dblp_urls.append(search.group(1))


joined_bibs = ''

for url in dblp_urls:
    print("importing " + url)
    url_bib = url.replace(".html", ".bib?param=1")
    output = urlopen(url_bib).read()
    joined_bibs += output.decode('utf-8')


library = bibtexparser.loads(joined_bibs)


def is_recent(entry):
    return int(entry.get('year')) >= datetime.date.today().year - 5


library.entries = filter(is_recent, library.entries)

with open('recent_bibtex.bib', 'w') as bibtex_file:
    bibtexparser.dump(library, bibtex_file)
