# -*- coding: utf-8 -*-
import os
import json
import asyncio
from typing import Dict
from infra.lib.Api import Api
from infra.lib.Validate import Validate

class ApiTradeService(Api, Validate):
    def __init__(self) -> None:
        self._api = Api()
        self._validate = Validate()
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



