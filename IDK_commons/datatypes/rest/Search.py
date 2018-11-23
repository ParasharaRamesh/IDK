from IDK_commons import utils

class SearchRequest:
    def __init__(self,searchquery,searchtype):
        self.searchquery = searchquery
        self.searchtype = searchtype

class SearchResponse:
    def __init__(self,minifiedQuestions):
        self.minifiedQuestions = minifiedQuestions