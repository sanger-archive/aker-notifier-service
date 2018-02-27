#! /usr/bin/env python
"""Subscribes to an events_notifications queue and sends notifications when receiving messages."""

import argparse
import json
import logging
import logging.config
import os
import pika
import sys
import traceback
import yaml
from contextlib import closing
from daemon import DaemonContext, pidfile
from functools import partial
from notifier import consts
from notifier import Config, Message, Notify, Rule

logger = logging.getLogger(__name__)


def configure_logging(env):
    logging_config_path = '{!s}/{!s}/logging_{!s}.yml'.format(
        os.path.dirname(os.path.realpath(__file__)),
        consts.PATH_CONFIG,
        env)
    with open(logging_config_path) as stream:
        try:
            config_file = yaml.load(stream)
            logging.config.dictConfig(config_file)
        except yaml.YAMLError as e:
            print(e)

    if env in (consts.ENV_DEV, consts.ENV_TEST):
        logger.setLevel('DEBUG')
    else:
        logger.setLevel('INFO')


def on_message(channel, method_frame, header_frame, body, env, config):
    """Check the rules for the message (event) and acknowledge (or nack) if the message has been
    processed or not.
    """
    notify = Notify(env, config)
    try:
        logger.info('Processing message: {!s}'.format(method_frame.delivery_tag))
        logger.debug('Message body: {!s}'.format(body))
        # We need to decode the body to be able to read the JSON
        decoded_body = body.decode('utf-8')
        message = Message.from_json(decoded_body)
        logger.debug('message: {!s}'.format(message))
        rule = Rule(env=env, config=config, message=message)
        rule.check_rules()
        channel.basic_ack(delivery_tag=method_frame.delivery_tag)
    except Exception:
        traceback.print_exc(file=sys.stderr)
        try:
            # Nack the message and try to requeue it
            channel.basic_nack(delivery_tag=method_frame.delivery_tag, requeue=False)

            logger.exception('Error processing message. Not acknowledging.')

            # Notify the devs that a message failed
            notify.send_email(subject=consts.SBJ_MSG_FAILED,
                              to=[config.contact.email_dev_team],
                              from_address=config.email.from_address,
                              template='notification_dev',
                              data={'message': body, 'traceback': traceback.format_exc()})
        except Exception:
            traceback.print_exc(file=sys.stderr)
            logger.exception('Failed to nack message.')

            # Notify devs that nack failed
            notify.send_email(subject=consts.SBJ_NACK_FAILED,
                              to=[config.contact.email_dev_team],
                              from_address=config.email.from_address,
                              template='notification_dev',
                              data={'message': body, 'traceback': traceback.format_exc()})


def main():
    # Extract arguments from the CLI
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('env', help='environment (e.g. development)', nargs='?', default=None)
    args = parser.parse_args()

    env = args.env or os.getenv(consts.ENV_VAR_APP, default=consts.ENV_DEV)

    if env not in (consts.ENV_DEV, consts.ENV_TEST, consts.ENV_STAGING, consts.ENV_PROD):
        raise ValueError('Unrecognised environment: {!r}'.format(env))

    # Get the config for this environment
    config_file_path = '{!s}/{!s}/{!s}.cfg'.format(os.path.dirname(os.path.realpath(__file__)),
                                                   consts.PATH_CONFIG, env)

    # Get the config
    config = Config(config_file_path)

    # Daemonize the script
    with DaemonContext(
            working_directory=os.getcwd(),
            stdout=open(config.process.stdout_log, 'a'),
            stderr=open(config.process.stderr_log, 'a'),
            pidfile=pidfile.PIDLockFile(config.process.pidfile)):

        configure_logging(env)

        logger.info('Using: {!s}'.format(config_file_path))

        on_message_partial = partial(on_message, env=env, config=config)

        credentials = pika.PlainCredentials(config.broker.user, config.broker.password)
        parameters = pika.ConnectionParameters(host=config.broker.host,
                                               port=config.broker.port,
                                               virtual_host=config.broker.virtual_host,
                                               credentials=credentials)
        with closing(pika.BlockingConnection(parameters=parameters)) as connection:
            channel = connection.channel()
            # Exchanges and queues are created using configuration and not at run-time
            # Configure a basic consumer
            channel.basic_consume(consumer_callback=on_message_partial,
                                  queue=config.broker.queue,
                                  consumer_tag='aker-events-notifier')
            try:
                logger.info('Listening on queue: {!s}...'.format(config.broker.queue))
                channel.start_consuming()
            finally:
                channel.stop_consuming()


if __name__ == '__main__':
    main()
