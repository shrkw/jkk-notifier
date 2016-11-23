#!/bin/env python
# encoding: UTF-8

import sendgrid
import os
from sendgrid.helpers.mail import *

import logging
from .logger import handler
logger = logging.getLogger(__name__)
logger.addHandler(handler)

def send(recipient, subject, body):
    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email(os.environ.get('MAIL_SENDER'))
    subject = subject
    to_email = Email(recipient)
    content = Content("text/plain", body)
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    logger.info(response.status_code)
    logger.info(response.body)
    logger.info(response.headers)
