# -*- coding: utf-8 -*-
import sys
import os
from threading import Thread
#from service.ServiceRunTrade import ServiceRunTrade
from service.TradeBinanceService import TradeBinanceService

config:dict = {
    'APP_ENV': os.environ['APP_ENV'],
    'WEBSOCKET_BINANCE_URL': os.environ['WEBSOCKET_BINANCE_URL']
}

def main(config:dict):
    url:str = "{}/ethusdt@kline_1m".format(config.get('WEBSOCKET_BINANCE_URL'))
    
    TradeBinanceService(url)

if __name__ == '__main__':
    try:
        main(config)

    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)