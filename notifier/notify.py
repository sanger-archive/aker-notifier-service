from .consts import *
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader, select_autoescape
import os
from smtplib import SMTP


class Notify:
    """Notify users using multiple methods of notification e.g. email, SMS, etc."""

    def __init__(self, env, config):
        """Init the class with the environment and config for the environment."""
        self._env = env
        self._config = config
        self._jinja_env = Environment(
            loader=FileSystemLoader(
                os.path.join(os.path.abspath(os.path.dirname(__file__)), 'templates')),
            autoescape=select_autoescape(['html', ]))

    def send_email(self, subject, from_address, to, template, data):
        """Curate and send an email."""
        with SMTP(host=self._config.email.smtp_host,
                  port=self._config.email.smtp_port) as smtp:
            # Login to SMTP server
            smtp.login(user=self._config.email.smtp_username,
                       password=self._config.email.smtp_password)

            msg = MIMEMultipart('alternative')

            template_html = self._jinja_env.get_template(template + '.html')
            template_txt = self._jinja_env.get_template(template + '.txt')

            # Record the MIME types of both parts - text/plain and text/html.
            part1 = MIMEText(template_txt.render(data), 'plain')
            part2 = MIMEText(template_html.render(data), 'html')

            # Attach parts into message container.
            # According to RFC 2046, the last part of a multipart message, in this case
            # the HTML message, is best and preferred.
            msg.attach(part1)
            msg.attach(part2)

            msg['Subject'] = subject
            msg['From'] = from_address
            msg['To'] = ', '.join(to)
            smtp.send_message(msg)
            smtp.quit()
