class SearchResult:
    def __init__(self, search_result):
        self.search_result = search_result

    def __str__(self):
        return str(self.search_result)
    
    def __repr__(self):
        return repr(self.search_result)

    def __getattr__(self, attr):
        return getattr(self.search_result, attr)