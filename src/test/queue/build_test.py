import os
from ...service.QueueServiceReport import QueueServiceReport
from ...service.ServiceRunMailer import ServiceRunMailer

config:dict = {
    'RABBITMQ_DEFAULT_URL': os.environ['RABBITMQ_DEFAULT_URL'],
    'QUEUE_EXCHANGE': os.environ['QUEUE_EXCHANGE'],
    'QUEUE_NAME': os.environ['QUEUE_NAME'].split(","),
    'RABBITMQ_DEFAULT_URL': os.environ['RABBITMQ_DEFAULT_URL']
}

def build_queue_name_and_exchange_test(config):
    assert QueueServiceReport(config['RABBITMQ_DEFAULT_URL']).declare(config['QUEUE_NAME'][0], config['QUEUE_EXCHANGE']) == True
    assert QueueServiceReport(config['RABBITMQ_DEFAULT_URL']).declare(config['QUEUE_NAME'][1], config['QUEUE_EXCHANGE']) == True
    assert QueueServiceReport(config['RABBITMQ_DEFAULT_URL']).declare(config['QUEUE_NAME'][2], config['QUEUE_EXCHANGE']) == True


def build_publish_queue_test(self):
    pass
    #jsonData = json.dumps({"company_id": "1217ca3c-7dbe-4be1-bce1-3ed5fedb7cef", "mailing_id": "fb81d954-fff5-44a8-b931-ef4f36a2809f", "is_test_message": "false", "scheduled_at":"2021-11-05 13:22:00", "period":"1h"})


    #await self._queueServiceReport.publish(jsonData, self._config['QUEUE_NAME'][0], self._config['QUEUE_EXCHANGE'])
    #print("//////////////////////////////////TESTE SEND QUEUE//////////////////////////////////////")
    #await asyncio.sleep(2)