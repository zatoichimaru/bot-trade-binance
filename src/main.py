# -*- coding: utf-8 -*-
import sys
import asyncio
import os
from threading import Thread
from service.ServiceRunMailer import ServiceRunMailer
from service.NoticeService import NoticeService

config:dict = {
    'RABBITMQ_DEFAULT_URL': os.environ['RABBITMQ_DEFAULT_URL'],
    'QUEUE_EXCHANGE': os.environ['QUEUE_EXCHANGE'],
    'QUEUE_NAME': os.environ['QUEUE_NAME'].split(","),
    'APP_ENV': os.environ['APP_ENV'],
    'API_MAILER_URL': os.environ['API_MAILER_URL'],
    'RABBITMQ_SENDER_URL': os.environ['RABBITMQ_SENDER_URL'],

    'APP_ENV': os.environ['APP_ENV'],
    'SLACK_URL': os.environ['SLACK_URL'],
    'SLACK_CHANNEL': os.environ['SLACK_CHANNEL'],
    'SLACK_APP': os.environ['SLACK_APP'],
    'ELASTICSEARCH_URL': os.environ['ELASTICSEARCH_URL'],
    'API_KEY': os.environ['API_KEY'],
    'ELASTICSEARCH_PORT': os.environ['ELASTICSEARCH_PORT'],
    'ELASTICSEARCH_INDEX_NAME': os.environ['ELASTICSEARCH_INDEX_NAME'],
    'ELASTICSEARCH_DOCUMENT_TYPE': os.environ['ELASTICSEARCH_DOCUMENT_TYPE'],
    'ELASTIC_USERNAME': os.environ['ELASTIC_USERNAME'],
    'ELASTIC_PASSWORD': os.environ['ELASTIC_PASSWORD']
}

async def main(config:dict):

    await NoticeService(config).notify('warning', 'test-notify', '{"company_id":"1321321231231231231"}', "EXCEPTION ERROR")
    #while True:
        
        #thread_receive = Thread(target=asyncio.run, daemon=True, args=(ServiceRunMailer(config).run(),), name="queue-mailer")
        #thread_receive.start()
        #thread_receive.join()
        #print("---------------- RUNNER MAILER PEDING REPORT SENDING -----------------")


if __name__ == '__main__':
    try:
        asyncio.run(main(config))

    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)