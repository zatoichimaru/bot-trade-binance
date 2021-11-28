# -*- coding: utf-8 -*-
from uuid import UUID
from datetime import datetime

class ReportQueue:
    def __init__(self, company_id:UUID, mailing_id:UUID, is_test_message:bool, scheduled_at:datetime, period:str) -> None:
        self.company_id = company_id
        self.mailing_id = mailing_id
        self.is_test_message = is_test_message == 'true' and True or False
        self.scheduled_at = datetime.strptime(scheduled_at,'%Y-%m-%d %H:%M:%S').date()
        self.period = period