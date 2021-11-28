# -*- coding: utf-8 -*-
from typing import Any, Dict, List
import json
import asyncio
from infra.lib.Slack import Slack
from service.ElasticSearchService import ElasticSearchService
from typeguard import typechecked
from datetime import datetime

@typechecked
class NoticeService(ElasticSearchService,Slack):

    def __init__(self, config: dict) -> None:
        self._config:dict = config
        self._slack:str = Slack(config)
        #self._elasticSearchService = ElasticSearchService(self._config.get('ELASTICSEARCH_URL'), self._config.get('ELASTICSEARCH_PORT'), self._config.get('ELASTIC_USERNAME'), self._config.get('ELASTIC_PASSWORD'))

    async def notify(self, type_error:str, title:str, body:any, content_error:any) -> None:
        message = {
            'body': "{}".format(repr(body)),
            'error': "{}".format(repr(content_error)) 
        }

        await self._slack.notify_failure(type_error, title, message) 
        jsonData = json.dumps({"level": "error", "created_at": str(datetime.now()), 'error': repr(content_error)})
        #self._elasticSearchService.post(str(self._config.get('ELASTICSEARCH_INDEX_NAME')), self._config.get('ELASTICSEARCH_DOCUMENT_TYPE'),  str(uuid4()), jsonData)
