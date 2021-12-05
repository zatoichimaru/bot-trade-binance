# -*- coding: utf-8 -*-
import os
import json
import asyncio
from typing import Dict
from binance.client import Client
from binance.enums import *
from infra.lib.Api import Api
from infra.lib.Validate import Validate

class ApiTradeService(Api, Validate, Client):
    def __init__(self, api_key:str, api_secret:str, idiom:str="us") -> None:
        self._api = Api()
        self._validate = Validate()
        self._client = Client(api_key, api_secret, tld=idiom)
        self._header:dict = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type,Authorization',
            'Access-Control-Allow-Methods': 'GET,PUT,POST,DELETE'
        }

        self._url:str = ""


    async def post(self, jsonData:str=None) -> dict:
        try:
        
            pass
        except Exception as error:
            raise Exception("{} - Fail request post [{}]".format(__class__, error))



