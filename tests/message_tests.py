import dateutil.parser
import unittest
from collections import namedtuple
from datetime import datetime
from notifier import consts
from notifier import Message


class MessageTests(unittest.TestCase):

    FakeMessage = namedtuple('FakeMessage', 'event_type timestamp user_identifier metadata')
    _fake_message = FakeMessage(event_type=consts.EVENT_SUB_CREATED,
                                timestamp=datetime.now().isoformat(),
                                user_identifier='test@sanger.ac.uk',
                                metadata={'sample_custodian': 'sc@sanger.ac.uk'})

    def test_init(self):
        message = Message(event_type=self._fake_message.event_type,
                          timestamp=dateutil.parser.parse(self._fake_message.timestamp),
                          user_identifier=self._fake_message.user_identifier,
                          metadata=self._fake_message.metadata)

        self.assertEqual(message.event_type, self._fake_message.event_type)
        self.assertEqual(message.timestamp.isoformat(), self._fake_message.timestamp)
        self.assertEqual(message.user_identifier, self._fake_message.user_identifier)
        self.assertEqual(message.metadata, self._fake_message.metadata)

    def test_from_json(self):
        message_as_json = '''
            {{
                "event_type":"{}",
                "timestamp":"{}",
                "user_identifier":"{}",
                "metadata":{{
                    "{}":"{}"
                }}
            }}'''.format(self._fake_message.event_type,
                         self._fake_message.timestamp,
                         self._fake_message.user_identifier,
                         list(self._fake_message.metadata.keys())[0],
                         self._fake_message.metadata['sample_custodian'])

        message = Message.from_json(message_as_json)
        self.assertEqual(message.event_type, self._fake_message.event_type)
        self.assertEqual(message.timestamp.isoformat(), self._fake_message.timestamp)
        self.assertEqual(message.user_identifier, self._fake_message.user_identifier)
        self.assertEqual(message.metadata, self._fake_message.metadata)
