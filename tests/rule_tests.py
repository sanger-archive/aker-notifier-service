import dateutil.parser
import unittest
from unittest import mock
from unittest.mock import Mock
from collections import namedtuple
from datetime import datetime
from notifier.consts import *
from notifier import Message, Notify, Rule
from .helper import config


class RulesTests(unittest.TestCase):

    FakeMessage = namedtuple('FakeMessage',
                             'event_type timestamp user_identifier metadata notifier_info')

    _fake_message = FakeMessage(event_type=None,
                                timestamp=datetime.now().isoformat(),
                                user_identifier='test@sanger.ac.uk',
                                metadata={'sample_custodian': 'sc@sanger.ac.uk'},
                                notifier_info={'work_plan_id': 1,
                                               'drs_study_code': 1234})

    def create_fake_generic_message(self, event_type):
        return self.FakeMessage(event_type,
                                timestamp=datetime.now().isoformat(),
                                user_identifier='test@sanger.ac.uk',
                                metadata={'sample_custodian': 'sc@sanger.ac.uk'},
                                notifier_info={'work_plan_id': 1,
                                               'drs_study_code': 1234})

    def test_init(self):
        rule = Rule(env='test_env', config='test_config', message=self._fake_message)
        self.assertEqual(rule._env, 'test_env')
        self.assertEqual(rule._config, 'test_config')
        self.assertEqual(rule._message, self._fake_message)
        self.assertIsInstance(rule._notify, Notify)

    def test_manifest_create_triggered(self):
        message = self.create_fake_generic_message(EVENT_MAN_CREATED)
        rule = Rule(env='test', config='test', message=message)

        rule._on_manifest_create = Mock()
        rule._on_manifest_received = Mock()
        rule._on_work_order_event = Mock()
        rule._on_catalogue_new = Mock()
        rule._on_catalogue_processed = Mock()
        rule._on_catalogue_rejected = Mock()

        rule.check_rules()

        rule._on_manifest_create.assert_called_once()
        rule._on_manifest_received.assert_not_called()
        rule._on_work_order_event.assert_not_called()
        rule._on_catalogue_new.assert_not_called()
        rule._on_catalogue_processed.assert_not_called()
        rule._on_catalogue_rejected.assert_not_called()

    def test_manifest_received_triggered(self):
        message = self.create_fake_generic_message(EVENT_MAN_RECEIVED)
        rule = Rule(env='test', config='test', message=message)

        rule._on_manifest_create = Mock()
        rule._on_manifest_received = Mock()
        rule._on_work_order_event = Mock()
        rule._on_catalogue_new = Mock()
        rule._on_catalogue_processed = Mock()
        rule._on_catalogue_rejected = Mock()

        rule.check_rules()

        rule._on_manifest_create.assert_not_called()
        rule._on_manifest_received.assert_called_once()
        rule._on_work_order_event.assert_not_called()
        rule._on_catalogue_new.assert_not_called()
        rule._on_catalogue_processed.assert_not_called()
        rule._on_catalogue_rejected.assert_not_called()

    def test_work_order_dispatched_event_triggered(self):
        message = self.create_fake_generic_message(EVENT_WO_DISPATCHED)
        rule = Rule(env='test', config='test', message=message)

        rule._on_manifest_create = Mock()
        rule._on_manifest_received = Mock()
        rule._on_work_order_event = Mock()
        rule._on_catalogue_new = Mock()
        rule._on_catalogue_processed = Mock()
        rule._on_catalogue_rejected = Mock()

        rule.check_rules()

        rule._on_manifest_create.assert_not_called()
        rule._on_manifest_received.assert_not_called()
        rule._on_work_order_event.assert_called_once()
        rule._on_catalogue_new.assert_not_called()
        rule._on_catalogue_processed.assert_not_called()
        rule._on_catalogue_rejected.assert_not_called()

    def test_work_order_concluded_event_triggered(self):
        message = self.create_fake_generic_message(EVENT_WO_CONCLUDED)
        rule = Rule(env='test', config='test', message=message)

        rule._on_manifest_create = Mock()
        rule._on_manifest_received = Mock()
        rule._on_work_order_event = Mock()
        rule._on_catalogue_new = Mock()
        rule._on_catalogue_processed = Mock()
        rule._on_catalogue_rejected = Mock()

        rule.check_rules()

        rule._on_manifest_create.assert_not_called()
        rule._on_manifest_received.assert_not_called()
        rule._on_work_order_event.assert_called_once()
        rule._on_catalogue_new.assert_not_called()
        rule._on_catalogue_processed.assert_not_called()
        rule._on_catalogue_rejected.assert_not_called()

    def test_catalogue_new_event_triggered(self):
        message = self.create_fake_generic_message(EVENT_CAT_NEW)
        rule = Rule(env='test', config='test', message=message)

        rule._on_manifest_create = Mock()
        rule._on_manifest_received = Mock()
        rule._on_work_order_event = Mock()
        rule._on_catalogue_new = Mock()
        rule._on_catalogue_processed = Mock()
        rule._on_catalogue_rejected = Mock()

        rule.check_rules()

        rule._on_manifest_create.assert_not_called()
        rule._on_manifest_received.assert_not_called()
        rule._on_work_order_event.assert_not_called()
        rule._on_catalogue_new.assert_called_once()
        rule._on_catalogue_processed.assert_not_called()
        rule._on_catalogue_rejected.assert_not_called()

    def test_catalogue_processed_event_triggered(self):
        message = self.create_fake_generic_message(EVENT_CAT_PROCESSED)
        rule = Rule(env='test', config='test', message=message)

        rule._on_manifest_create = Mock()
        rule._on_manifest_received = Mock()
        rule._on_work_order_event = Mock()
        rule._on_catalogue_new = Mock()
        rule._on_catalogue_processed = Mock()
        rule._on_catalogue_rejected = Mock()

        rule.check_rules()

        rule._on_manifest_create.assert_not_called()
        rule._on_manifest_received.assert_not_called()
        rule._on_work_order_event.assert_not_called()
        rule._on_catalogue_new.assert_not_called()
        rule._on_catalogue_processed.assert_called_once()
        rule._on_catalogue_rejected.assert_not_called()

    def test_catalogue_rejected_event_triggered(self):
        message = self.create_fake_generic_message(EVENT_CAT_REJECTED)
        rule = Rule(env='test', config='test', message=message)

        rule._on_manifest_create = Mock()
        rule._on_manifest_received = Mock()
        rule._on_work_order_event = Mock()
        rule._on_catalogue_new = Mock()
        rule._on_catalogue_processed = Mock()
        rule._on_catalogue_rejected = Mock()

        rule.check_rules()

        rule._on_manifest_create.assert_not_called()
        rule._on_manifest_received.assert_not_called()
        rule._on_work_order_event.assert_not_called()
        rule._on_catalogue_new.assert_not_called()
        rule._on_catalogue_processed.assert_not_called()
        rule._on_catalogue_rejected.assert_called_once()

    @mock.patch('notifier.rule.Notify', autospec=True)
    def test_manifest_create_email(self, mocked_notify):
        message = self.create_fake_generic_message(EVENT_MAN_CREATED)
        rule = Rule(env='test', config=config, message=message)
        rule.check_rules()
        self.assertIsInstance(mocked_notify, Notify)
        mocked_notify.return_value.send_email.assert_called_once_with(
            subject=SBJ_MAN_CREATED,
            from_address=config.email.from_address,
            template='manifest_created',
            to=['test@sanger.ac.uk', 'sc@sanger.ac.uk'],
            data={'user_identifier': 'test@sanger.ac.uk'})

    def test_common_work_order_with_id(self):
        message = self.FakeMessage(
            event_type=EVENT_WO_DISPATCHED,
            timestamp=datetime.now().isoformat(),
            user_identifier='test@sanger.ac.uk',
            metadata={'sample_custodian': 'sc@sanger.ac.uk', 'work_order_id': 1234},
            notifier_info={'work_plan_id': 1, 'drs_study_code': 1234})
        rule = Rule(env='test', config=config, message=message)
        rule._generate_wo_link = Mock()
        rule._generate_wo_link.return_value = ''

        to, data = rule._common_work_order()

        self.assertEqual(to, [message.user_identifier])
        self.assertEqual(data, {'work_order_id': message.metadata['work_order_id'], 'link': ''})

    def test_common_work_order_without_id(self):
        message = self.FakeMessage(
            event_type=EVENT_WO_DISPATCHED,
            timestamp=datetime.now().isoformat(),
            user_identifier='test@sanger.ac.uk',
            metadata={'sample_custodian': 'sc@sanger.ac.uk'},
            notifier_info={'work_plan_id': 1, 'drs_study_code': 1234})
        rule = Rule(env='test', config=config, message=message)

        with self.assertRaises(ValueError) as cm:
            rule._common_work_order()

    def test_common_manifest_with_id(self):
        message = self.FakeMessage(
            event_type=EVENT_MAN_RECEIVED,
            timestamp=datetime.now().isoformat(),
            user_identifier='test@sanger.ac.uk',
            metadata={'sample_custodian': 'sc@sanger.ac.uk',
                      'manifest_id': 1234,
                      'deputies': ['dep1@sanger.ac.uk', 'dep2@sanger.ac.uk']},
            notifier_info={'work_plan_id': 1, 'drs_study_code': 1234})
        rule = Rule(env='test', config=config, message=message)
        rule._generate_link = Mock()
        rule._generate_link.return_value = ''

        to, data = rule._common_manifest()

        self.assertEqual(to, [message.user_identifier,
                              message.metadata['sample_custodian'],
                              'dep1@sanger.ac.uk', 'dep2@sanger.ac.uk']),
        self.assertEqual(data, {'manifest_id': message.metadata['manifest_id'], 'link': ''})

    @mock.patch('notifier.rule.Notify', autospec=True)
    def test_on_catalogue_new(self, mocked_notify):
        message = self.FakeMessage(
            event_type=EVENT_CAT_NEW,
            timestamp=datetime.now().isoformat(),
            user_identifier='test@sanger.ac.uk',
            metadata={},
            notifier_info={})
        rule = Rule(env='test', config=config, message=message)

        rule._on_catalogue_new()

        mocked_notify.return_value.send_email.assert_called_once_with(
            subject=SBJ_CAT_NEW,
            from_address=config.email.from_address,
            to=[config.contact.email_dev_team],
            template='catalogue_new',
            data={}
        )

    @mock.patch('notifier.rule.Notify', autospec=True)
    def test_on_catalogue_processed(self, mocked_notify):
        message = self.FakeMessage(
            event_type=EVENT_CAT_PROCESSED,
            timestamp=datetime.now().isoformat(),
            user_identifier='test@sanger.ac.uk',
            metadata={},
            notifier_info={})
        rule = Rule(env='test', config=config, message=message)

        rule._on_catalogue_processed()

        mocked_notify.return_value.send_email.assert_called_once_with(
            subject=SBJ_CAT_PROCESSED,
            from_address=config.email.from_address,
            to=[config.contact.email_dev_team],
            template='catalogue_processed',
            data={}
        )

    @mock.patch('notifier.rule.Notify', autospec=True)
    def test_on_catalogue_rejected(self, mocked_notify):
        message = self.FakeMessage(
            event_type=EVENT_CAT_REJECTED,
            timestamp=datetime.now().isoformat(),
            user_identifier='test@sanger.ac.uk',
            metadata={'error': 'error message'},
            notifier_info={})
        rule = Rule(env='test', config=config, message=message)

        rule._on_catalogue_rejected()

        mocked_notify.return_value.send_email.assert_called_once_with(
            subject=SBJ_CAT_REJECTED,
            from_address=config.email.from_address,
            to=[config.contact.email_dev_team],
            template='catalogue_rejected',
            data={'error': message.metadata['error'], 'timestamp': message.timestamp}
        )

    @mock.patch('notifier.rule.Notify')
    def test_common_work_order_called(self, mocked_notify):
        message = self.create_fake_generic_message(EVENT_WO_DISPATCHED)
        rule = Rule(env='test', config=config, message=message)
        rule._common_work_order = Mock()
        rule._common_work_order.return_value = [], {}
        rule.check_rules()

        rule._common_work_order.assert_called_once()

    @mock.patch('notifier.rule.Notify')
    def test_common_manifest_called(self, mocked_notify):
        message = self.create_fake_generic_message(EVENT_MAN_RECEIVED)
        rule = Rule(env='test', config=config, message=message)
        rule._common_manifest = Mock()
        rule._common_manifest.return_value = [], {}
        rule.check_rules()

        rule._common_manifest.assert_called_once()

    def test_common_catalogue(self):
        rule = Rule(env='test', config=config, message='')
        self.assertEqual(rule._common_catalogue(), [config.contact.email_dev_team])

    def test_generate_link(self):
        rule = Rule(env='test', config=config, message='')
        path = 'path'
        id = 'id'
        link = rule._generate_link(path, id)
        self.assertEqual(link, '{}://{}:{}/{}/{}'.format(
            config.link.protocol,
            config.link.root,
            config.link.port,
            path,
            id))

    def test_generate_wo_link(self):
        rule = Rule(env='test', config=config, message='')
        work_plan_id = '1234'
        link = rule._generate_wo_link(work_plan_id)
        self.assertEqual(link, '{}://{}:{}/{}/{}/{}'.format(
            config.link.protocol,
            config.link.root,
            config.link.port,
            PATH_WORK_ORDER_BEGIN,
            work_plan_id,
            PATH_WORK_ORDER_END))
