#!/bin/env python
# encoding: UTF-8

import sendgrid
import os
from sendgrid.helpers.mail import *
from jinja2 import Environment, PackageLoader

import logging
from .logger import handler
logger = logging.getLogger(__name__)
logger.addHandler(handler)

env = Environment(loader=PackageLoader('jkk', 'templates'))
sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))

def send_search_result(recipient, subject, param):
    from_email = Email(os.environ.get('MAIL_SENDER'))
    subject = subject
    to_email = Email(recipient)
    template = env.get_template('search_result.html.j2')
    body = template.render(**param)
    content = Content("text/html", body)
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    logger.info(response.status_code)
    logger.info(response.body)
    logger.info(response.headers)
