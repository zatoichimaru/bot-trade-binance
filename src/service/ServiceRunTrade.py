# -*- coding: utf-8 -*-
import os
import json
import asyncio
from .ApiTradeService import ApiTradeService
from infra.lib.Validate import Validate
from typeguard import typechecked


@typechecked
class ServiceRunTrade(ApiTradeService, Validate):

    def __init__(self, config:dict) -> None:
        self._config = config
        self._apiService = ApiTradeService()
        self._validate = Validate()

    async def run(self) -> None:
        try:
            
            pass

        except Exception as error:
            pass


   