from gitenberg.metadata.pandata import Pandata

from gitensite.apps.bookinfo.models import Author, Book, Cover

def default_ctor(loader, tag_suffix, node):
    return tag_suffix + ' ' + node.value

def addBookFromYaml(yaml):
    if isinstance(yaml, Pandata):
        obj = yaml.metadata
    else:
        pandata = Pandata(None)
        pandata.load(yaml)
        obj = pandata.metadata

    (book,created) = Book.objects.get_or_create(book_id=int(obj['identifiers']['gutenberg']))

    creator = None
    if "creator" in obj:
        creator = obj["creator"]
    elif "metadata" in obj and "creator" in obj.metadata:
        creator = obj.metadata["creator"]
    if creator is not None and "author" in creator:
        (author, created) = Author.objects.get_or_create(name=creator["author"]["agent_name"])
        if "birthdate" in creator["author"]:
            author.birth_year = creator["author"]["birthdate"]
        if "deathdate" in creator["author"]:
            author.death_year = creator["author"]["deathdate"]
        book.author = author
        author.save()
    
    if "cover" in obj:
        num_existing_covers = len(list(Cover(book=book).objects.all()))
        (cover, created) = Cover.objects.get_or_create(link=obj["cover"])
        cover.book = book
        cover.default_cover = (num_existing_covers == 0)

    book.title = obj["title"]
    book.language = obj["language"] if isinstance(obj["language"], str) else 'mul'
    
    if "description" in obj:
        book.description = obj["description"]
    if "gutenberg_type" in obj:
        book.gutenberg_type = obj["gutenberg_type"]
    elif "metadata" in obj and "gutenberg_type" in obj.metadata:
        book.gutenberg_type = obj.metadata["gutenberg_type"]
    
    bookshelf = None
    if "gutenberg_bookshelf" in obj:
        bookshelf = obj["gutenberg_bookshelf"]
    elif "metadata" in obj and "gutenberg_bookshelf" in obj.metadata:
        bookshelf = obj.metadata["gutenberg_bookshelf"]

    if bookshelf is not None:
        if type(bookshelf) is str:
            book.gutenberg_bookshelf = bookshelf
        else:
            book.gutenberg_bookshelf = ";".join(bookshelf)
    
    subjects = None
    if "subjects" in obj:
        subjects = obj["subjects"]
    elif "metadata" in obj and "subjects" in obj.metadata:
        subjects = obj.metadata["subjects"]

    if subjects is not None:
        if type(subjects) is str:
            book.subjects = subjects
        else:
            if len(subjects) > 0:
                if type(subjects[0]) is str:
                    book.subjects = ";".join(subjects)
                else:
                    subjectList = [x[1] for x in subjects]
                    book.subjects = ";".join(subjectList)
        
    book.yaml = yaml
    book.save()

    return True