# -*- coding: utf-8 -*-
import os
import json
import re
import asyncio
import requests
from typing import Dict
from infra.lib.Api import Api
from domain.report.ReportQueue import ReportQueue
from infra.lib.Validate import Validate

class ApiReportService(Api, Validate):
    def __init__(self) -> None:
        self._api = Api()
        self._validate = Validate()
        self._header:dict = {
            'mz-internal-app': '1',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type,Authorization',
            'Access-Control-Allow-Methods': 'GET,PUT,POST,DELETE'
        }

        self._url:str = "{}/company/{}/mailing/{}/report/{}"


    async def post(self, jsonData:str=None) -> dict:
        try:
            mailerDataJson:dict = None
            regex = re.compile(r'\D')

            if(self._validate.is_json(jsonData) == False):
                return mailerDataJson

            jsonDataLoads = json.loads(jsonData)
            reportQueueInstance = ReportQueue(**jsonDataLoads)

            if(isinstance(reportQueueInstance, ReportQueue) == False):
                raise Exception("{} - Fail formart json schema queue".format(__class__))

            period:int = regex.sub('', jsonDataLoads['period'])
            self._url = self._url.format(os.environ['API_MAILER_URL'], jsonDataLoads['company_id'], jsonDataLoads['mailing_id'], period)
            response = await self._api.send_request('POST', self._url, self._header)

            if(self._validate.is_json(response) == False):
                raise Exception("{} - Fail formart json mailer is void".format(__class__)) 
            
            mailerDataJson = json.loads(response)

            return mailerDataJson

        except Exception as error:
            raise Exception("{} - Fail request POST mailer report [{}]".format(__class__, error))



