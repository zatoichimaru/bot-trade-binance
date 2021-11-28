# -*- coding: utf-8 -*-
from typing import Any, List
import pika
import time
from .AbastractQueue import AbastractQueue

class RabbitMQ(AbastractQueue):
    
    def connection(self) -> None:
        try:
            if(isinstance(self._connection, RabbitMQ) == False):
                self._connection = pika.BlockingConnection(pika.URLParameters(self._queue_url))
                self._channel = self._connection.channel()
                self._statusConnection = True
    
        except KeyboardInterrupt:
            self._channel.stop_consuming()
            self._connection.close()

        except (pika.exceptions.ConnectionClosedByBroker, pika.exceptions.AMQPConnectionError):
            time.sleep(self.TIMOUT_LIMIT)
            self._countRentries += 1
            
            if(self._countRentries <= self.MAX_RETRIES):
                self.connection()
            else:
                raise Exception("{} - Fail RabbitMQ connecting".format(__class__))

    def declare(self, queue_name:str, exchange_name:str=None) -> bool:
        try:
            if(not queue_name or self._statusConnection == False):
               return False
                
            self._queue = self._channel.queue_declare(
                queue=queue_name,
                exclusive=False,
                auto_delete=False,
                durable=True
            )

            if(exchange_name is not None or len(exchange_name) > 0):
                self._channel.exchange_declare(
                    exchange=exchange_name,
                    exchange_type=self.EXCHANGE_TYPE['direct'],
                    passive=False,
                    durable=True,
                    auto_delete=False
                )

                self._channel.queue_bind(
                    exchange=exchange_name,
                    queue=queue_name
                )

            self._channel.confirm_delivery()
            time.sleep(self.TIMER_WAIT)
            return True
        
        except:
            return False

    def publish(self, body:any, queue_name:str, exchange_name:str=None) -> bool:
        try:
            if(not queue_name or not body):
                raise Exception("{} - Fail receive field queue_name/body is null".format(__class__))

            if(not exchange_name):
                exchange_name = ''
            
            self.connection()

            self._channel.basic_publish(
                exchange=exchange_name,
                routing_key=queue_name,
                body=body,
                properties=pika.BasicProperties(
                    delivery_mode=2
                ),
                mandatory=True
            )

            self._channel.cancel()
            self._connection.close()
            time.sleep(self.TIMER_WAIT)
            return True

        except pika.exceptions.UnroutableError:
            self.publish(body, queue_name, exchange_name)

        except (pika.exceptions.ConnectionClosed, pika.exceptions.ChannelClosed):
            self._connection.close()
    
    def getTotal(self) -> int:
        if self._queue.method.message_count: 
            self._total = int(self._queue.method.message_count)
            return self._total

        time.sleep(self.TIMER_WAIT)
        return self._total

    def receive(self, queue_name:str, quantity:int=1) -> List[Any]: 
        try:
            if(not queue_name):
                raise Exception("{} - Fail receive field queue_name is null".format(__class__))

            self.connection()
            
            for method_frame, properties, body in self._channel.consume(queue_name):
                if not body:
                    break
            
                self._channel.basic_ack(method_frame.delivery_tag)
                self._body.append(body.decode())

                if method_frame.delivery_tag == quantity:
                    break

            self._channel.cancel()
            self._connection.close()
            time.sleep(self.TIMER_WAIT)
            return self._body
            
        except (pika.exceptions.ConnectionClosed, pika.exceptions.ChannelClosed):
            self._connection.close()
            self.receive(queue_name, quantity)