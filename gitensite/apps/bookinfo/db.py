from gitensite.apps.bookinfo.models import Author, Book

import yaml as PyYAML
def default_ctor(loader, tag_suffix, node):
    return tag_suffix + ' ' + node.value
PyYAML.add_multi_constructor('!lcc', default_ctor)
PyYAML.add_multi_constructor('!lcsh', default_ctor)

def addBookFromYaml(yaml):
    obj = PyYAML.safe_load(yaml)

    (book,created) = Book.objects.get_or_create(book_id=int(obj['identifiers']['gutenberg']), repo_name=obj['_repo'])

    if "creator" in obj and "author" in obj["creator"]:
        (author, created) = Author.objects.get_or_create(name=obj["creator"]["author"]["agent_name"])
        if "birthdate" in obj["creator"]["author"]:
            author.birth_year = obj["creator"]["author"]["birthdate"]
        if "deathdate" in obj["creator"]["author"]:
            author.death_year = obj["creator"]["author"]["deathdate"]
        book.author = author
        author.save()

    book.title = obj["title"]
    book.language = obj["language"] if isinstance(obj["language"], str) else 'mul'
    book.gutenberg_type = obj["gutenberg_type"]
    if "gutenberg_bookshelf" in obj:
        if type(obj["gutenberg_bookshelf"]) is str:
            book.gutenberg_bookshelf = obj["gutenberg_bookshelf"]
        else:
            book.gutenberg_bookshelf = ";".join(obj["gutenberg_bookshelf"])
    if "subjects" in obj:
        if type(obj["subjects"]) is str:
            book.subjects = obj["subjects"]
        else:
            subjectList = [x[1] for x in obj["subjects"]]
            book.subjects = ";".join(subjectList)
    
    book.yaml = yaml
    book.save()

    return True