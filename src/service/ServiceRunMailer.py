# -*- coding: utf-8 -*-
import os
import json
import asyncio
import re
from threading import Thread
from typing import Any, Dict, List, Sequence, TypeVar
from .QueueServiceReport import QueueServiceReport
from .ApiReportService import ApiReportService
from infra.lib.Validate import Validate
from typeguard import typechecked
#from infra.lib.Slack import Slack


@typechecked
class ServiceRunMailer(ApiReportService, QueueServiceReport, Validate):

    TIMER_WAIT:int = 5
    MAX_RETRIES:int = 5

    def __init__(self, config:dict) -> None:
        self._config = config
        self._apiService = ApiReportService()
        self._queueServiceReport = QueueServiceReport(self._config['RABBITMQ_DEFAULT_URL'])
        self._queueServiceReport.declare(self._config['QUEUE_NAME'][0], self._config['QUEUE_EXCHANGE'])
        self._queueServiceReport.declare(self._config['QUEUE_NAME'][2], self._config['QUEUE_EXCHANGE'])
        self._queueServiceReportSender = QueueServiceReport(self._config['RABBITMQ_SENDER_URL'])
        self._queueServiceReportSender.declare(self._config['QUEUE_NAME'][1])
        self._validate = Validate()
        self._queueResponse:dict = None

        self._return:dict = {
            'send_queue': False, 
            'get_queue': None, 
            'get_api_mailer_report': None
        }

        self._json_params:dict = {
            'company_id': None,
            'mailing_id': None,
            'is_test_message': 'false',
            'is_report': 'true'
        }

    """Execute run receive queue and get return api mailer report, after send new queue of the api sender"""
    async def run(self) -> None:
        try:
            
            if(not self._return['get_queue']):
                self._return['get_queue'] = await self._queueServiceReport.receive(self._config['QUEUE_NAME'][0])

                if(len(self._return['get_queue']) > 0):
                    return await self.run()
            else:
                return await self.retry()

        except Exception as error:
            pass
            #falta class notification add enviar no slack


    async def retry(self, retry_count:int=0):
        status:bool = False
        self.truncate_fields()

        try:

            if(retry_count >= self.MAX_RETRIES):
                await self._queueServiceReport.publish(self._return['get_queue'][0], self._config['QUEUE_NAME'][2], self._config['QUEUE_EXCHANGE'])
                status = True
                retry_count = 0
                self._return['get_queue'] = None
                #falta class notification add enviar no slack
                return [status, retry_count]            

            if(len(self._return['get_queue']) > 0 and self._validate.is_json(self._return['get_queue'][0]) == True):
                self._return['get_api_mailer_report'] = await self._apiService.post(self._return['get_queue'][0])
                await asyncio.sleep(self.TIMER_WAIT)

                if(not self._return['get_api_mailer_report'] 
                or self._return['get_api_mailer_report']['status'] == False
                or not self._return['get_api_mailer_report']['data']['success']):
                    retry_count += 1
                    return await self.retry(retry_count)
                    #falta class notification add enviar no slack

                self._json_params['company_id'] = self._return['get_api_mailer_report']['data']['data']['company']
                self._json_params['mailing_id'] = self._return['get_api_mailer_report']['data']['data']['mailing']

                if(not self._json_params['company_id'] or not self._json_params['company_id']):
                    retry_count += 1
                    return await self.retry(retry_count)
                    #falta class notification add enviar no slack

                await self._queueServiceReportSender.publish(json.dumps(self._json_params), self._config['QUEUE_NAME'][1])
                await asyncio.sleep(self.TIMER_WAIT)

                status = True
                retry_count = 0
                self._return['get_queue'] = None
                self.truncate_fields()

                return [status, retry_count]
            
        except Exception as error:
            #falta class notification add enviar no slack
            pass

    def truncate_fields(self):
        self._return['send_queue'] = False
        self._return['get_api_mailer_report'] = None
        self._json_params['company_id'] = None
        self._json_params['mailing_id'] = None
