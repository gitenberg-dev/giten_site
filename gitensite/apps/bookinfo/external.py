import requests
from cachecontrol import CacheControl
from lxml import etree

request_session = requests.session()
cached_session = CacheControl(request_session)

#These functions take a Book object as an argument, and return either a URL if a result is found, or an empty string if there is no result

def librivox_api(book):
    if "," in book.author.name:
        author_last = book.author.name[0:book.author.name.index(",")]
    else:
        author_last = book.author.name

    result = cached_session.get("https://librivox.org/api/feed/audiobooks/", params={"author": author_last, "limit": 500, "format": "json"})
    
    try:
        result_json = result.json()
    except:
        return ""

    if not "books" in result_json:
        return ""

    books = result_json["books"]
    for x in books:
        if "gutenberg.org" in x["url_text_source"] and x["url_text_source"].endswith("/" + str(book.book_id)):
            return x["url_librivox"]
    
    for x in books:
        if book.title == x["title"]:
            return x["url_librivox"]
    
    return ""
    
def standard_ebooks_api(book):
    opds = cached_session.get("https://standardebooks.org/opds/all")

    try:
        tree = etree.fromstring(opds.content)
    except:
        return ""

    for entry in tree.iter("{http://www.w3.org/2005/Atom}entry"):
        for source in entry.iter("{http://purl.org/dc/elements/1.1/}source"):
            if "gutenberg" in source.text and source.text.endswith("/" + str(book.book_id)):
                return entry.find("{http://www.w3.org/2005/Atom}id").text
    
    return ""


api_sources = {"Librivox": librivox_api, "Standard Ebooks": standard_ebooks_api}

#This function calls each function in the api_sources dict, and returns a new dict containing the results
def getExternalLinks(book):
    ret = {}
    
    for source in api_sources:
        result = api_sources[source](book)

        if len(result) > 0:
            ret[source] = result
    
    return ret
