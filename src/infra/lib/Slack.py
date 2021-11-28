from infra.lib.Api import Api
from typing import List
from typeguard import typechecked
import json
import asyncio

@typechecked
class Slack:

    TEMPLATE_SLACK:List[dict] = [
        {
            'warning': { 'color': '#ffae42', 'error_type': 'Warning', 'icon': ':warning:'},
            'error': { 'color': '#ff0000', 'error_type': 'Error', 'icon': ':bangbang:' },
        }
    ]

    def __init__(self, config: dict) -> None:
        self._api = Api()
        self._config:dict = config

    async def notify_failure(self, type_error:str, title:str, message:any):
        try:

            if(len(type_error) == 0 or len(title) == 0 or len(message) ==0):
                raise Exception("{} - Failure needs these fields that are required: [type_error, title, message]".format(__class__))

            template = self.TEMPLATE_SLACK

            print("template--------------------", template)

            payload = {
                'icon_emoji': template[1][type_error]['icon'],
                'username': self._config.get('SLACK_APP') + '({})'.format(self._config.get('APP_ENV')),
                'channel': self._config.get('SLACK_CHANNEL'),
                'attachments': template
            }

            print("payload--------------------", payload)


            # self._url = self._url.format(self._config.get('SLACK_URL'), payload)
            #response = await self._api.send_request('POST', self._config.get('SLACK_URL'), None, json.dump(payload))

            #return response['data']['status']
                    
        except Exception as error:
            print("ERRROOOOOOOOOO SLACK>>>>", error)