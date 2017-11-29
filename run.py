#! /usr/bin/env python
"""Subscribes to an events_notifications queue and sends notifications when receiving messages."""

import argparse
import json
import os
import pika
import sys
import traceback
from contextlib import closing
from daemon import DaemonContext, pidfile
from functools import partial
from notifier import consts
from notifier import Config, Message, Notify, Rule


def on_message(channel, method_frame, header_frame, body, env, config):
    """Check the rules for the message (event) and acknowledge (or nack) if the message has been
    processed or not.
    """
    notify = Notify(env, config)
    try:
        print('method_frame.routing_key: {!s}'.format(method_frame.routing_key))
        print('method_frame.delivery_tag: {!s}'.format(method_frame.delivery_tag))
        print('body: {!s}'.format(body))
        message = Message.from_json(body)
        print('message: {!s}'.format(message))
        rule = Rule(env=env, config=config, message=message)
        rule.check_rules()
        channel.basic_ack(delivery_tag=method_frame.delivery_tag)
    except Exception:
        traceback.print_exc(file=sys.stderr)
        try:
            # Nack the message and try to requeue it
            channel.basic_nack(delivery_tag=method_frame.delivery_tag, requeue=False)

            print('Error processing message. Not acknowledging.')

            # Notify the devs that a message failed
            notify.send_email(subject=consts.SBJ_MSG_FAILED,
                              to=[config.contact.email_dev_team],
                              from_address=config.email.from_address,
                              template='notification_dev',
                              data={'message': body, 'traceback': traceback.format_exc()})
        except Exception:
            traceback.print_exc(file=sys.stderr)
            print('Failed to nack message.')

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
    print('Using: {!s}'.format(config_file_path))

    # Get the config
    config = Config(config_file_path)

    # Daemonize the script
    with DaemonContext(
            working_directory=os.getcwd(),
            stdout=open(config.process.log_file, 'w'),
            stderr=open(config.process.error_log, 'w'),
            pidfile=pidfile.PIDLockFile(config.process.pidfile)):

        on_message_partial = partial(on_message, env=env, config=config)

        credentials = pika.PlainCredentials(config.broker.user, config.broker.password)
        parameters = pika.ConnectionParameters(host=config.broker.host,
                                               port=config.broker.port,
                                               credentials=credentials)
        with closing(pika.BlockingConnection(parameters=parameters)) as connection:
            channel = connection.channel()
            # Declare the exchage (create it if it does not yet exist)
            # Currently not sure who should create the exchange and bindings etc. should each
            #   producer and the consumers assume they have been created? Should the consumers
            #   create if they do not yet exist?
            channel.exchange_declare(exchange=config.broker.exchange,
                                     exchange_type=config.broker.exchange_type,
                                     durable=True)
            # Declare the queue - not sure if it should happen here...
            channel.queue_declare(queue=config.broker.queue, durable=True)
            # Bind the queue to the exchange
            channel.queue_bind(queue=config.broker.queue, exchange=config.broker.exchange)
            # Configure a basic consumer
            channel.basic_consume(on_message_partial, config.broker.queue)
            try:
                print('Listening on queue: {!s}...'.format(config.broker.queue))
                channel.start_consuming()
            finally:
                channel.stop_consuming()


if __name__ == '__main__':
    main()
