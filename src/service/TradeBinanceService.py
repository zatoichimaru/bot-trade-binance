# -*- coding: utf-8 -*-
import os
import json
import pprint
from typing import Dict
from infra.lib.Validate import Validate
from infra.lib.WebSocket import WebSocket

class TradeBinanceService(WebSocket,Validate):
    def __init__(self, url:str) -> None:
        self._websocket = WebSocket(url)
        self._validate = Validate()

