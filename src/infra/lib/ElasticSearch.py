# -*- coding: utf-8 -*-
import json
import os
import time
from typing import Any
from elasticsearch import Elasticsearch as Elastic

class ElasticSearch(Elastic):
    MAX_RETRIES = 5
    TIMOUT_LIMIT = 10
    TIMOUT_LIMIT_ELASTIC = 60
    TIMER_WAIT = 2
    RETRY_ON_TIMEOUT = True

    def __init__(self, hostname:str, port:str, username:str, password:str) -> None:
        self._connection:tuple = None
        self._statusConnection:bool = False 
        self._hostname:str = hostname
        self._port:str = port
        self._username:str = username
        self._password:str = password
        self._countRentries:int = 0
        self.connection()

    def connection(self) -> None:
        try:
            if not self._connection:
                self._connection = Elastic([{'host': self._hostname, 'port': self._port}], 
                    http_auth=(self._username, self._password),
                    sniff_on_start=True,
                    sniff_on_connection_fail=True,
                    sniffer_timeout=self.TIMOUT_LIMIT_ELASTIC
                )
                self._statusConnection = True
            
            return self._statusConnection

        except Exception as error:
            time.sleep(self.TIMOUT_LIMIT)
            self._countRentries += 1
            if(self._countRentries <= self.MAX_RETRIES):
                self.connection()
            else:
                raise Exception("{} - Fail ElasticSearch connecting [{}]".format(__class__,error)) from None

    def info(self) -> json:
        return self._connection.info()

    def create_index(self, name_indice:str) -> bool:
        try:
            if self._statusConnection == True and name_indice is not None and self._connection.indices.exists(index=name_indice) == False:
                self._name_indice = name_indice
                self._connection.indices.create(index=name_indice)
                return True

            return False
        except:
            time.sleep(self.TIMOUT_LIMIT)
            return False

    def create_document(self, index:str, doc_type:str, id:str, body:dict) -> bool:
        try:
            if(self._statusConnection == False):
                return False
            
            self._connection.index(index=index, doc_type=doc_type, id=id, body=body)
            return True

        except Exception as error:
            raise Exception("{} - Fail ElasticSearch create document [{}]".format(__class__,error)) from None