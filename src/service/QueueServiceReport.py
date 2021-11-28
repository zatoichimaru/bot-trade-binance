# -*- coding: utf-8 -*-
from typing import Any, Dict, List
import asyncio
from infra.lib.queue.RabbitMQ import RabbitMQ

class QueueServiceReport(RabbitMQ):

    def __init__(self, queue_url:str) -> None:
        self._queue_url:str = queue_url
        self._rabbitmq = RabbitMQ(self._queue_url)

    def declare(self, queue_name:str, exchange_name:str=None) -> bool:
        return self._rabbitmq.declare(queue_name, exchange_name)

    async def publish(self, body:any, queue_name:str, exchange:str='') -> bool:
        return self._rabbitmq.publish(body, queue_name, exchange) == True

    async def receive(self, queue_name:str, quantity:int=1) -> List[Any]: 
        return self._rabbitmq.receive(queue_name, quantity)

