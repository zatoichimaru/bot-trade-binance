# -*- coding: utf-8 -*-
import os
import json
import asyncio
from .ApiReportService import ApiReportService
from infra.lib.Validate import Validate
from typeguard import typechecked


@typechecked
class ServiceRunTrade(ApiReportService, Validate):

    def __init__(self, config:dict) -> None:
        self._config = config
        self._apiService = ApiReportService()
        self._validate = Validate()

    async def run(self) -> None:
        try:
            
            pass

        except Exception as error:
            pass


   