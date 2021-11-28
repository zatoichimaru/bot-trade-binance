# -*- coding: utf-8 -*-
import os
import json
from infra.lib.ElasticSearch import ElasticSearch

class ElasticSearchService(ElasticSearch):

    def __init__(self, hostname:str, port:str, username:str, password:str) -> None:
        self._elasticSearch = ElasticSearch(hostname, port, username, password)

    def post(self, index:str, doc_type:str, id:str, body:any) -> bool:
        try:
            self._elasticSearch.create_index(index)
            return self._elasticSearch.create_document(index, doc_type, id, body) == True

        except Exception as error:
            return { "status" : False, "message": error }
