from dataclasses import dataclass
from uuid import UUID
from typeguard import typechecked


@dataclass
@typechecked
class ReportMail:
    company_id: UUID
    mailing_id: UUID
    body_report: str
    recipients: list

    def __init__(self, company_id: UUID, mailing_id: UUID, body_report: str, recipients:list[str]):
        self.company_id = company_id
        self.mailing_id = mailing_id
        self.body_report = body_report
        self.recipients = recipients
