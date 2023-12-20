class Data:
    def __init__(self,
                 title: str,
                 url: str,
                 desc: str,
                 created: str,
                 version: str = "",
                 relative_article: str = "",
                 authors=None) -> None:
        # Check if authors is None, and set it to an empty list if it is
        # authors can be a list of string array or dict array
        if authors is None:
            authors = [{}]
        self.title = title
        self.url = url
        self.authors = authors
        self.desc = desc
        self.created = created
        self.version = version
        self.relative_article = relative_article
