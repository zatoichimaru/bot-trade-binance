import os
import json
from typing import List
from uuid import uuid4
from infra.lib.email.Sendgrid import Sendgrid
from domain.report.ReportMail import ReportMail
from service.ElasticSearchService import ElasticSearchService
from datetime import datetime
from uuid import UUID
from infra.lib.slack import slack
from typeguard import typechecked


@typechecked
class MailService(ReportMail):
    def __init__(self, config: dict, company_id: UUID, mailing_id: UUID, body_report: str, recipients:List[str]) -> None:
        self._config = config
        self._sendgrid = Sendgrid(config)
        self._sendgrid_data = {}
        self._data = ReportMail(company_id, mailing_id, body_report, recipients)

    @property
    def sendgrid_data(self):
        return self._sendgrid_data

    @property
    def sendgrid_data(self):
        return self._sendgrid_data

    @property
    def recipients(self):
        return self._data.recipients

    async def build(self):
        """
        Create All data structure to sendgrid payload by mailing
        """
        email_body = self._data.body_report

        self._sendgrid_data = {
            'from': {
                'email': str(os.environ.get('MAIL_FROM'))
            },
            'subject': str(os.environ.get('SUBJECT_MAIL')),
            'content': [{
                'type': 'text/html',
                'value': email_body
            }],
            'personalizations': []
        }

        return self

    def create_personalizations(self, recipients: list):
        """ Create personalizations for all recipients """
        return list(map(self._personalize, recipients))

    def _personalize(self, recipient: str):
        """
        Create email personalization for recipient
        """
        return {
            'to': [{
                'email': recipient,
            }]
        }

    async def send_mail(self) -> bool:
        try:
            mail = await self.build()

            mail._sendgrid_data['personalizations'] = self.create_personalizations(mail.recipients)

            status, content = await self._sendgrid.send(mail.sendgrid_data)
            jsonData = json.dumps({"level": "info", "status": status, "content": str(content), "created_at": str(datetime.now())})
            elastic = ElasticSearchService(self._config.get('ELASTICSEARCH_URL'),self._config.get('ELASTICSEARCH_PORT'),self._config.get('ELASTIC_USERNAME'),self._config.get('ELASTIC_PASSWORD'))
            elastic.post(str(self._config.get('ELASTICSEARCH_INDEX_NAME')), self._config.get('ELASTICSEARCH_DOCUMENT_TYPE'), str(uuid4()), jsonData)
            return  status
        except Exception as e:
            jsonData = json.dumps({"level": "error", "created_at": str(datetime.now()), 'error': repr(e)})
            elastic = ElasticSearchService(self._config.get('ELASTICSEARCH_URL'),self._config.get('ELASTICSEARCH_PORT'),self._config.get('ELASTIC_USERNAME'),self._config.get('ELASTIC_PASSWORD'))
            elastic.post(str(self._config.get('ELASTICSEARCH_INDEX_NAME')), self._config.get('ELASTICSEARCH_DOCUMENT_TYPE'),  str(uuid4()), jsonData)

            message = {}
            message['body'] = "company_id => {} \nmailing_id => {}".format(self._data.company_id, self._data.mailing_id)
            message['error'] = "error => {} ".format(repr(e))

            slack.notify_failure(self._config, message, True)
            return False