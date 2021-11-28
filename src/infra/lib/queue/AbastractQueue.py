from abc import ABC, abstractmethod
from typing import Any, Collection, List, NoReturn

class AbastractQueue(ABC):
    
    QUANTITY_QUEUE_LIMIT:int = 1
    TIMOUT_LIMIT:int = 10
    TIMER_WAIT:int = 5
    MAX_RETRIES:int = 5
    EXCHANGE_TYPE:dict = {
        'direct':'direct',
        'fanout':'fanout',
        'headers':'headers',
        'topic':'topic'
    }

    def __init__(self, queue_url:str) -> None:
        self._config:str = queue_url
        self._queue_url:str = queue_url
        self._connection:tuple = None
        self._channel:tuple = None
        self._total:int = 0
        self._body:list = []
        self._countRentries:int = 0
        self._queue:tuple = None
        self.connection()

    @staticmethod
    @abstractmethod  
    def connection(cls) -> None:
        raise NotImplementedError

    @abstractmethod
    def declare(cls, queue_name:str, exchange_name:str=None) -> bool:
        raise NotImplementedError

    @abstractmethod 
    def publish(cls, body:str, queue_name:str, exchange_name:str=None) -> bool:
        raise NotImplementedError

    @abstractmethod  
    def getTotal(cls) -> int:
        raise NotImplementedError

    @abstractmethod  
    def receive(cls, queue_name:str, quantity:int) -> List[Any]:
        raise NotImplementedError
